"""SQLite persistence for PokerAnalytics."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class HistoryStore:
    """Small, dependency-free store for completed analyses."""

    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path) if path else Path(__file__).resolve().parent / "poker_history.sqlite3"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute(
            """CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                mode TEXT NOT NULL,
                hole_cards TEXT NOT NULL,
                board TEXT NOT NULL,
                opponents INTEGER NOT NULL,
                pot REAL NOT NULL,
                stake REAL NOT NULL,
                equity REAL NOT NULL,
                outs INTEGER NOT NULL,
                result TEXT NOT NULL
            )"""
        )
        self._connection.commit()

    def add(self, *, mode: str, hole_cards: list[str], board: list[str], opponents: int,
            pot: float, stake: float, equity: float, outs: int, result: str) -> int:
        cur = self._connection.execute(
            """INSERT INTO analyses
            (mode, hole_cards, board, opponents, pot, stake, equity, outs, result)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (mode, json.dumps(hole_cards), json.dumps(board), opponents, pot, stake,
             equity, outs, result),
        )
        self._connection.commit()
        return int(cur.lastrowid)

    def recent(self, limit: int = 25) -> list[dict[str, Any]]:
        rows = self._connection.execute(
            "SELECT * FROM analyses ORDER BY id DESC LIMIT ?", (max(1, limit),)
        ).fetchall()
        return [dict(row) for row in rows]

    def close(self) -> None:
        self._connection.close()
