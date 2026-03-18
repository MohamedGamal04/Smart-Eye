from backend.repository import db


def filter_detections_by_zone(detection_results, camera_id, frame_w, frame_h):
    try:
        zones = db.get_zones(camera_id=camera_id, enabled_only=True)
    except Exception:
        return [{"zone": None, "results": detection_results}]
    if not zones:
        return [{"zone": None, "results": detection_results}]

    def _center_in_zone(bbox, zone):
        bx1, by1, bx2, by2 = bbox
        cx = (bx1 + bx2) / 2
        cy = (by1 + by2) / 2
        zx1 = zone["x1"] * frame_w
        zy1 = zone["y1"] * frame_h
        zx2 = zone["x2"] * frame_w
        zy2 = zone["y2"] * frame_h
        return zx1 <= cx <= zx2 and zy1 <= cy <= zy2

    def _filter_by_zone(entries, zone):
        out = []
        for ent in entries:
            bbox = ent.get("bbox")
            if not bbox:
                continue
            if _center_in_zone(bbox, zone):
                out.append(ent)
        return out

    zone_results = []
    for zone in zones:
        filtered_objects = _filter_by_zone(detection_results.get("objects", []), zone)
        filtered_faces = _filter_by_zone(detection_results.get("faces", []), zone)
        zone_result = {
            "zone": zone,
            "results": {
                "faces": filtered_faces,
                "objects": filtered_objects,
                "face_time_ms": detection_results.get("face_time_ms", 0),
                "object_time_ms": detection_results.get("object_time_ms", 0),
            },
        }
        zone_results.append(zone_result)

    def _not_in_any(entries):
        out = []
        for ent in entries:
            bbox = ent.get("bbox")
            if not bbox:
                continue
            if any(_center_in_zone(bbox, z) for z in zones):
                continue
            out.append(ent)
        return out

    unzoned_faces = _not_in_any(detection_results.get("faces", []))
    unzoned_objects = _not_in_any(detection_results.get("objects", []))
    if unzoned_faces or unzoned_objects:
        zone_results.append(
            {
                "zone": None,
                "results": {
                    "faces": unzoned_faces,
                    "objects": unzoned_objects,
                    "face_time_ms": 0,
                    "object_time_ms": 0,
                },
            }
        )
    return zone_results
