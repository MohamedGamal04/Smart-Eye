import os
import threading

import cv2
import numpy as np


class HeatmapGenerator:
    def __init__(self, width=640, height=480):
        self._width = width
        self._height = height
        self._accumulator = np.zeros((height, width), dtype=np.float32)
        self._count = 0

    def add_detection(self, bbox, frame_w, frame_h):
        x1, y1, x2, y2 = bbox
        sx1 = int(x1 / frame_w * self._width)
        sy1 = int(y1 / frame_h * self._height)
        sx2 = int(x2 / frame_w * self._width)
        sy2 = int(y2 / frame_h * self._height)
        sx1 = max(0, min(sx1, self._width - 1))
        sy1 = max(0, min(sy1, self._height - 1))
        sx2 = max(0, min(sx2, self._width))
        sy2 = max(0, min(sy2, self._height))
        self._accumulator[sy1:sy2, sx1:sx2] += 1
        self._count += 1

    def generate(self, background=None, alpha=0.6):
        if self._count == 0:
            if background is not None:
                return background.copy()
            return np.zeros((self._height, self._width, 3), dtype=np.uint8)
        normalized = self._accumulator / self._accumulator.max()
        heatmap = (normalized * 255).astype(np.uint8)
        colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        if background is not None:
            bg = cv2.resize(background, (self._width, self._height))
            result = cv2.addWeighted(bg, 1 - alpha, colored, alpha, 0)
        else:
            result = colored
        return result

    def save(self, filepath, background=None):
        img = self.generate(background)
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        cv2.imwrite(filepath, img)
        return filepath

    def reset(self):
        self._accumulator[:] = 0
        self._count = 0


_generators = {}
_generators_lock = threading.Lock()


def get_generator(camera_id, width=640, height=480):
    with _generators_lock:
        if camera_id not in _generators:
            _generators[camera_id] = HeatmapGenerator(width, height)
        return _generators[camera_id]
