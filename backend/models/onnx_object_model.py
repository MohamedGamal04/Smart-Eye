import ast
import json
import logging
import os

import numpy as np

_logger = logging.getLogger(__name__)


class MissingModelFile(Exception):
    pass


class ONNXObjectModel:
    def __init__(self, weight_path: str, confidence: float = 0.6, classes=None, preferred_provider: str = "auto"):
        self._weight_path = weight_path
        self._confidence = confidence
        self._classes = classes
        self._preferred_provider = (preferred_provider or "auto").lower()
        self._session = None
        self._loaded = False
        self._input_name = None
        self._input_shape = None
        self._class_names = {}
        self._using_cpu_fallback = False
        self._last_provider: str | None = None
        self._last_error: str | None = None

    def load(self):
        try:
            import onnxruntime as ort

            names_map = {}
            self._last_error = None
            self._using_cpu_fallback = False

            if not os.path.isfile(self._weight_path):
                raise MissingModelFile(f"Model file not found: {self._weight_path}")

            try:
                avail = ort.get_available_providers() or []
            except Exception:
                avail = []

            gpu_provider = None
            if self._preferred_provider and self._preferred_provider not in ("auto", "cpu"):
                pref_map = {
                    "cuda": "CUDAExecutionProvider",
                    "dml": "DmlExecutionProvider",
                    "rocm": "ROCMExecutionProvider",
                    "coreml": "CoreMLExecutionProvider",
                    "openvino": "OpenVINOExecutionProvider",
                }
                mapped = pref_map.get(self._preferred_provider, self._preferred_provider)
                if mapped in avail and mapped != "CPUExecutionProvider":
                    gpu_provider = mapped
            if gpu_provider is None:
                for p in (
                    "CUDAExecutionProvider",
                    "DmlExecutionProvider",
                    "ROCMExecutionProvider",
                    "CoreMLExecutionProvider",
                    "OpenVINOExecutionProvider",
                ):
                    if p in avail:
                        gpu_provider = p
                        break
            providers: list[str] = [gpu_provider] if gpu_provider else ["CPUExecutionProvider"]

            _logger.info("Available ORT providers: %s | selected: %s", avail, providers)

            so = ort.SessionOptions()
            so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            so.intra_op_num_threads = 2
            so.inter_op_num_threads = 1
            so.log_severity_level = 3

            try:
                self._session = ort.InferenceSession(self._weight_path, sess_options=so, providers=providers)
                self._last_provider = (self._session.get_providers() or providers)[0]
            except Exception as e:
                _logger.warning("Failed to create ONNX InferenceSession with providers %s, trying CPU only (%s)", providers, e)
                try:
                    self._session = ort.InferenceSession(self._weight_path, sess_options=so, providers=["CPUExecutionProvider"])
                    self._using_cpu_fallback = True
                    self._last_provider = "CPUExecutionProvider"
                except Exception:
                    self._session = ort.InferenceSession(self._weight_path, sess_options=so)
                    self._last_provider = (self._session.get_providers() or ["unknown"])[0]

            inputs = self._session.get_inputs()
            if not inputs:
                raise RuntimeError("ONNX model has no inputs")
            inp = inputs[0]
            self._input_name = inp.name
            shape = inp.shape
            if len(shape) >= 4 and shape[-2] is not None and shape[-1] is not None:
                self._input_shape = (int(shape[-1]), int(shape[-2]))
            else:
                self._input_shape = (640, 640)

            try:
                w = self._input_shape[0]
                h = self._input_shape[1]
                dummy = np.zeros((1, 3, int(h), int(w)), dtype=np.float32)
                try:
                    self._session.run(None, {inp.name: dummy})
                except Exception as _e:
                    _logger.warning("ONNX warmup failed on provider %s, falling back to CPU: %s", self._last_provider, _e)
                    self._session = ort.InferenceSession(self._weight_path, sess_options=so, providers=["CPUExecutionProvider"])
                    self._using_cpu_fallback = True
                    self._last_provider = "CPUExecutionProvider"
                    self._session.run(None, {inp.name: dummy})
            except Exception as _e:
                _logger.warning("Warmup failed: %s", _e)
                self._last_error = f"warmup: {_e}"

                try:
                    import onnxruntime as ort

                    self._session = ort.InferenceSession(self._weight_path, sess_options=so, providers=["CPUExecutionProvider"])
                    self._using_cpu_fallback = True
                    self._last_provider = "CPUExecutionProvider"
                    self._session.run(None, {inp.name: dummy})
                except Exception:
                    pass

            try:
                meta = self._session.get_modelmeta()
                if meta and hasattr(meta, "custom_metadata_map"):
                    for k, v in meta.custom_metadata_map.items():
                        if "name" in k.lower():
                            try:
                                names_map = ast.literal_eval(v)
                                break
                            except Exception:
                                try:
                                    names_map = json.loads(v)
                                    break
                                except Exception:
                                    pass
            except Exception:
                pass

            if not names_map:
                try:
                    import onnx

                    model = onnx.load(self._weight_path)
                    for prop in model.metadata_props:
                        if "name" in prop.key.lower():
                            try:
                                names_map = ast.literal_eval(prop.value)
                                break
                            except Exception:
                                try:
                                    names_map = json.loads(prop.value)
                                    break
                                except Exception:
                                    pass
                except Exception:
                    pass

            if names_map:
                self._class_names = {int(k): str(v) for k, v in names_map.items()}
            else:
                dummy = np.zeros((1, 3, self._input_shape[1], self._input_shape[0]), dtype=np.float32)
                outs = self._session.run(None, {self._input_name: dummy})
                if outs:
                    arr = np.array(outs[0])
                    d = arr.shape[1] if arr.ndim >= 2 else 0
                    num_classes = max(0, d - 4)
                    self._class_names = {i: str(i) for i in range(num_classes)}

            self._loaded = True
            _logger.info("ONNX model loaded: %d classes, CPU_fallback=%s", len(self._class_names), self._using_cpu_fallback)
        except Exception as e:
            self._loaded = False
            self._last_error = str(e)
            _logger.exception("Failed to load ONNX model: %s", e)
            raise

    @property
    def is_loaded(self):
        return self._loaded

    @property
    def class_names(self):
        return self._class_names

    @property
    def confidence(self):
        return self._confidence

    @confidence.setter
    def confidence(self, val):
        self._confidence = val

    @property
    def using_cpu_fallback(self):
        return self._using_cpu_fallback

    @property
    def last_provider(self):
        return self._last_provider

    @property
    def provider(self):
        return self._last_provider or ("CPU" if self._using_cpu_fallback else "DML")

    @property
    def last_error(self):
        return self._last_error

    def detect(self, frame):
        if not self._loaded:
            return []

        import cv2

        h, w = frame.shape[:2]
        inp_w, inp_h = self._input_shape

        img = cv2.dnn.blobFromImage(
            frame,
            scalefactor=1.0 / 255.0,
            size=(inp_w, inp_h),
            mean=(0, 0, 0),
            swapRB=True,
            crop=False,
        )

        try:
            outs = self._session.run(None, {self._input_name: img})
        except Exception as e:
            self._last_error = f"inference error on {self._last_provider or 'unknown'}: {e}"
            if not self._using_cpu_fallback:
                _logger.warning("Inference failed with DML, switching to CPU permanently: %s", e)
                try:
                    import onnxruntime as ort

                    self._session = ort.InferenceSession(self._weight_path, providers=["CPUExecutionProvider"])
                    self._using_cpu_fallback = True
                    self._last_provider = "CPUExecutionProvider"
                    outs = self._session.run(None, {self._input_name: img})
                except Exception:
                    _logger.exception("CPU fallback also failed")
                    return []
            else:
                _logger.exception("CPU inference failed")
                return []

        if not outs:
            return []

        out = np.array(outs[0])
        if out.ndim == 3:
            out = out[0].T
        elif out.ndim == 2:
            out = out.T

        detections = []

        boxes_xyxy = []
        boxes_xywh = []
        scores = []
        classes = []

        if out.ndim == 2 and out.shape[1] >= 5:
            for row in out:
                x, y, w_box, h_box = float(row[0]), float(row[1]), float(row[2]), float(row[3])
                class_probs = row[4:]

                if class_probs.size == 0:
                    continue

                cls_id = int(np.argmax(class_probs))
                cls_conf = float(class_probs[cls_id])

                if cls_conf < self._confidence:
                    continue

                scale_x = float(w) / float(inp_w)
                scale_y = float(h) / float(inp_h)

                cx = x * scale_x
                cy = y * scale_y
                bw = w_box * scale_x
                bh = h_box * scale_y

                x1 = int(max(0, cx - bw / 2))
                y1 = int(max(0, cy - bh / 2))
                x2 = int(min(w - 1, cx + bw / 2))
                y2 = int(min(h - 1, cy + bh / 2))

                boxes_xyxy.append([x1, y1, x2, y2])
                boxes_xywh.append([x1, y1, x2 - x1, y2 - y1])
                scores.append(cls_conf)
                classes.append(cls_id)

        if boxes_xywh:
            try:
                idxs = cv2.dnn.NMSBoxes(boxes_xywh, scores, self._confidence, 0.45)
                idxs = np.array(idxs).flatten().tolist() if len(idxs) > 0 else []
            except Exception:
                idxs = list(range(len(boxes_xyxy)))
        else:
            idxs = []

        for i in idxs:
            bbox = boxes_xyxy[i]
            detections.append(
                {
                    "bbox": bbox,
                    "confidence": float(scores[i]),
                    "class": int(classes[i]),
                    "class_name": self._class_names.get(int(classes[i]), str(classes[i])),
                }
            )

        return detections

    @staticmethod
    def inspect_model(weight_path):
        try:
            import onnxruntime as ort

            sess = ort.InferenceSession(weight_path)
            names = {}

            try:
                meta = sess.get_modelmeta()
                if meta and hasattr(meta, "custom_metadata_map"):
                    for k, v in meta.custom_metadata_map.items():
                        if "name" in k.lower():
                            try:
                                names = ast.literal_eval(v)
                                break
                            except Exception:
                                try:
                                    names = json.loads(v)
                                    break
                                except Exception:
                                    pass
            except Exception:
                pass

            if not names:
                try:
                    import onnx

                    model = onnx.load(weight_path)
                    for prop in model.metadata_props:
                        if "name" in prop.key.lower():
                            try:
                                names = ast.literal_eval(prop.value)
                                break
                            except Exception:
                                try:
                                    names = json.loads(prop.value)
                                    break
                                except Exception:
                                    pass
                except Exception:
                    pass

            if names:
                names = {int(k): str(v) for k, v in names.items()}

            return {
                "class_names": names,
                "classes": names,
                "num_classes": len(names),
                "task": "detect",
            }
        except Exception:
            return None
