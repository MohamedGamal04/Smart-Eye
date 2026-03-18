import contextlib
import logging
import os

try:
    import cv2
except Exception:
    cv2 = None
try:
    import psutil
except Exception:
    psutil = None

logger = logging.getLogger(__name__)


def apply_limits(limit_resources: bool, max_threads: int = 1):
    try:
        if limit_resources:
            os.environ["OMP_NUM_THREADS"] = "1"
            os.environ["OPENBLAS_NUM_THREADS"] = "1"
            os.environ["MKL_NUM_THREADS"] = "1"
            os.environ["NUMEXPR_MAX_THREADS"] = "1"
            os.environ["OMP_THREAD_LIMIT"] = "1"
            th = 1
        else:
            os.environ["OMP_NUM_THREADS"] = str(max_threads)
            os.environ["OPENBLAS_NUM_THREADS"] = str(max_threads)
            os.environ["MKL_NUM_THREADS"] = str(max_threads)
            os.environ["NUMEXPR_MAX_THREADS"] = str(max_threads)
            os.environ["OMP_THREAD_LIMIT"] = str(max_threads)
            th = max(1, int(max_threads))
    except Exception:
        logger.exception("Failed to set thread environment variables")

    try:
        if cv2 is not None:
            cv2.setNumThreads(th)
    except Exception:
        logger.debug("Failed to set OpenCV threads", exc_info=True)

    try:
        if limit_resources:
            if psutil is not None:
                p = psutil.Process()
                with contextlib.suppress(Exception):
                    p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
                with contextlib.suppress(Exception):
                    p.nice(10)
            else:
                try:
                    import ctypes

                    handle = ctypes.windll.kernel32.GetCurrentProcess()
                    ctypes.windll.kernel32.SetPriorityClass(handle, 0x4000)
                except Exception:
                    pass
    except Exception:
        logger.debug("Failed to lower process priority", exc_info=True)
