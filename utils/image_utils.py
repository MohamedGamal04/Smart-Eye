import os
from datetime import datetime

import cv2


def draw_box(frame, x1, y1, x2, y2, label="", color=(0, 255, 0), thickness=2, font_scale=0.6):
    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
    if label:
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 1)[0]
        cv2.rectangle(
            frame,
            (int(x1), int(y1) - text_size[1] - 10),
            (int(x1) + text_size[0] + 4, int(y1)),
            color,
            -1,
        )
        cv2.putText(
            frame,
            label,
            (int(x1) + 2, int(y1) - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            (0, 0, 0),
            1,
            cv2.LINE_AA,
        )
    return frame


def save_snapshot(frame, directory, prefix="snap"):
    os.makedirs(directory, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    path = os.path.join(directory, f"{prefix}_{ts}.jpg")
    cv2.imwrite(path, frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return path


def frame_to_rgb(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
