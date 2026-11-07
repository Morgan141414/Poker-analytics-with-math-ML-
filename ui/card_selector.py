"""Card input widgets supporting text and individual rank/suit fields."""

from __future__ import annotations

import re

try:
    from PySide6.QtCore import Signal
    from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QLineEdit, QWidget
except ImportError:  # Keep importing the module possible in headless environments.
    Signal = None  # type: ignore[assignment]


RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
SUITS = (("♠", "s"), ("♥", "h"), ("♦", "d"), ("♣", "c"))
CARD_RE = re.compile(r"^(10|[2-9TJQKA])[shdc]$", re.IGNORECASE)


def normalize_card(value: str) -> str:
    value = value.strip().upper().replace("10", "T")
    if len(value) == 2:
        return value[0] + value[1].lower()
    return value


if Signal is not None:
    class CardSelector(QWidget):
        cardsChanged = Signal()

        def __init__(self, title: str, count: int, parent=None, required: bool = True) -> None:
            super().__init__(parent)
            self.count = count
            self.required = required
            layout = QHBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(QLabel(title))
            self.text = QLineEdit()
            self.text.setPlaceholderText("Ah Kd" if count == 2 else "Qh 7c 2s")
            self.text.setToolTip("Введите карты через пробел: Ah Kd")
            self.text.textChanged.connect(self.cardsChanged)
            layout.addWidget(self.text, 1)
            self.rank_fields: list[QComboBox] = []
            self.suit_fields: list[QComboBox] = []
            for _ in range(count):
                rank = QComboBox(); rank.addItems(["—", *RANKS])
                suit = QComboBox(); suit.addItems(["—", *[symbol for symbol, _ in SUITS]])
                rank.currentIndexChanged.connect(self.cardsChanged)
                suit.currentIndexChanged.connect(self.cardsChanged)
                self.rank_fields.append(rank); self.suit_fields.append(suit)
                layout.addWidget(rank); layout.addWidget(suit)

        def cards(self) -> list[str]:
            raw = [normalize_card(x) for x in self.text.text().split() if x.strip()]
            if raw:
                return raw
            cards = []
            for rank, suit in zip(self.rank_fields, self.suit_fields):
                if rank.currentIndex() == 0 or suit.currentIndex() == 0:
                    continue
                cards.append(rank.currentText() + SUITS[suit.currentIndex() - 1][1])
            return cards

        def set_cards(self, cards: list[str]) -> None:
            self.text.setText(" ".join(cards))

        def validate(self) -> tuple[list[str], str | None]:
            cards = self.cards()
            if self.required and len(cards) != self.count:
                return cards, f"Нужно указать {self.count} карт(ы)."
            if len(cards) > self.count:
                return cards, f"Можно указать не больше {self.count} карт."
            if any(not CARD_RE.match(card) for card in cards):
                return cards, "Формат карты: ранг + масть, например Ah или Td."
            if len(set(cards)) != len(cards):
                return cards, "Одна и та же карта указана несколько раз."
            return cards, None
else:
    class CardSelector:  # pragma: no cover - only used to produce a clear error.
        def __init__(self, *args, **kwargs):
            raise RuntimeError("Для графического интерфейса установите PySide6: pip install PySide6")
