"""Main application window for Study Mode and Live Input Mode."""

from __future__ import annotations

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (
        QDoubleSpinBox, QFrame, QGridLayout, QHBoxLayout, QLabel, QListWidget,
        QMainWindow, QMessageBox, QPushButton, QSpinBox, QVBoxLayout, QWidget,
    )
except ImportError:  # Allow importing non-UI helpers on machines without Qt.
    QMainWindow = object  # type: ignore[misc,assignment]

from data.storage import HistoryStore
from ui.card_selector import CardSelector
from ui.calculator import calculate_equity


class MainWindow(QMainWindow):
    def __init__(self, store: HistoryStore | None = None) -> None:
        if QMainWindow is object:
            raise RuntimeError("Для графического интерфейса установите PySide6: pip install PySide6")
        super().__init__()
        self.store = store or HistoryStore()
        self.mode = "Study"
        self.setWindowTitle("PokerAnalytics — Hand Equity Lab")
        self.resize(1100, 720)
        self._build_ui()
        self._load_history()

    def _build_ui(self) -> None:
        root = QWidget(); self.setCentralWidget(root)
        outer = QVBoxLayout(root); outer.setContentsMargins(28, 24, 28, 24); outer.setSpacing(16)
        title = QLabel("PokerAnalytics"); title.setObjectName("title")
        outer.addWidget(title)
        subtitle = QLabel("Оценка equity против случайных соперников и история раздач"); subtitle.setObjectName("subtitle")
        outer.addWidget(subtitle)
        modes = QHBoxLayout(); self.study_button = QPushButton("Study Mode"); self.live_button = QPushButton("Live Input Mode")
        for button in (self.study_button, self.live_button): button.setObjectName("mode"); button.setCheckable(True); modes.addWidget(button)
        self.study_button.setChecked(True); self.study_button.clicked.connect(lambda: self._set_mode("Study")); self.live_button.clicked.connect(lambda: self._set_mode("Live")); modes.addStretch()
        outer.addLayout(modes)
        body = QHBoxLayout(); body.setSpacing(16); outer.addLayout(body, 1)
        left = QFrame(); left.setObjectName("panel"); form = QVBoxLayout(left); form.setContentsMargins(18, 18, 18, 18); form.setSpacing(13)
        label = QLabel("Ввод раздачи"); label.setObjectName("section"); form.addWidget(label)
        self.hole = CardSelector("Ваша рука", 2); self.board = CardSelector("Board", 5, required=False)
        form.addWidget(self.hole); form.addWidget(self.board)
        hint = QLabel("Для флопа/тёрна оставьте лишние поля пустыми и используйте строку сверху."); hint.setObjectName("muted"); hint.setWordWrap(True); form.addWidget(hint)
        grid = QGridLayout(); grid.addWidget(QLabel("Случайных соперников"), 0, 0); self.opponents = QSpinBox(); self.opponents.setRange(1, 8); self.opponents.setValue(1); grid.addWidget(self.opponents, 0, 1)
        grid.addWidget(QLabel("Pot"), 1, 0); self.pot = QDoubleSpinBox(); self.pot.setRange(0, 1_000_000); self.pot.setDecimals(2); grid.addWidget(self.pot, 1, 1)
        grid.addWidget(QLabel("Ваша ставка"), 2, 0); self.stake = QDoubleSpinBox(); self.stake.setRange(0, 1_000_000); self.stake.setDecimals(2); grid.addWidget(self.stake, 2, 1); form.addLayout(grid)
        self.calculate_button = QPushButton("Рассчитать equity"); self.calculate_button.setObjectName("primary"); self.calculate_button.clicked.connect(self.calculate); form.addWidget(self.calculate_button); form.addStretch()
        body.addWidget(left, 3)
        right = QFrame(); right.setObjectName("panel"); result = QVBoxLayout(right); result.setContentsMargins(18, 18, 18, 18); result.setSpacing(12)
        result_title = QLabel("Результат"); result_title.setObjectName("section"); result.addWidget(result_title)
        self.equity_label = QLabel("—"); self.equity_label.setAlignment(Qt.AlignCenter); self.equity_label.setStyleSheet("font-size: 46px; font-weight: 700; color: #22c55e;"); result.addWidget(self.equity_label)
        self.result_text = QLabel("Введите карты и нажмите «Рассчитать equity»."); self.result_text.setWordWrap(True); result.addWidget(self.result_text)
        self.history_label = QLabel("Последние расчёты"); self.history_label.setObjectName("section"); result.addWidget(self.history_label)
        self.history = QListWidget(); result.addWidget(self.history, 1); body.addWidget(right, 2)

    def _set_mode(self, mode: str) -> None:
        self.mode = mode
        self.study_button.setChecked(mode == "Study"); self.live_button.setChecked(mode == "Live")
        self.calculate_button.setText("Рассчитать и сохранить" if mode == "Study" else "Рассчитать live equity")

    def calculate(self) -> None:
        hole, error = self.hole.validate()
        if error: QMessageBox.warning(self, "Проверьте карты", error); return
        board, error = self.board.validate()
        if error: QMessageBox.warning(self, "Проверьте board", error); return
        if len(board) > 5: QMessageBox.warning(self, "Проверьте board", "На board может быть не больше 5 карт."); return
        if len(set(hole + board)) != len(hole + board): QMessageBox.warning(self, "Проверьте карты", "Одна и та же карта указана несколько раз."); return
        try: stats = calculate_equity(hole, board, self.opponents.value())
        except ValueError as exc: QMessageBox.warning(self, "Не удалось рассчитать", str(exc)); return
        equity = stats["equity"] * 100
        self.equity_label.setText(f"{equity:.1f}%")
        call_value = self.pot.value() + self.stake.value()
        verdict = "сильная позиция" if equity >= 55 else "пограничное решение" if equity >= 35 else "осторожно"
        self.result_text.setText(f"{verdict.capitalize()} против {self.opponents.value()} случайных соперников. "
                                 f"Примерная ценность pot после колла: {call_value * stats['equity']:.2f}. "
                                 f"Outs на улучшение: {stats['outs']}.")
        self.store.add(mode=self.mode, hole_cards=hole, board=board, opponents=self.opponents.value(), pot=self.pot.value(), stake=self.stake.value(), equity=equity, outs=stats["outs"], result=verdict)
        self._load_history()

    def _load_history(self) -> None:
        self.history.clear()
        for row in self.store.recent():
            cards = " ".join(__import__("json").loads(row["hole_cards"]))
            self.history.addItem(f"{row['created_at'][:16]}  {row['mode']}  {cards}  → {row['equity']:.1f}%")

    def closeEvent(self, event) -> None:
        self.store.close(); event.accept()
