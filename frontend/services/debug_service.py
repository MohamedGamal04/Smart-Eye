from __future__ import annotations

from backend.repository import db


class DebugService:
    def get_db_path(self) -> str:
        return db.get_db_path()

    @staticmethod
    def ensure_cameras(conn) -> list[int]:
        rows = conn.execute("SELECT id FROM cameras LIMIT 10").fetchall()
        if not rows:
            conn.execute(
                "INSERT INTO cameras (name, source, location) VALUES (?, ?, ?)",
                ("Demo Camera 1", "demo://0", "Front Entrance"),
            )
            conn.execute(
                "INSERT INTO cameras (name, source, location) VALUES (?, ?, ?)",
                ("Demo Camera 2", "demo://1", "Back Door"),
            )
            conn.commit()
            rows = conn.execute("SELECT id FROM cameras LIMIT 10").fetchall()
        return [r[0] for r in rows]
