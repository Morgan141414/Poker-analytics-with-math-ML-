"""Application entry point with a friendly PySide6 fallback."""

from __future__ import annotations

import sys


def main() -> int:
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError:
        print("PokerAnalytics требует PySide6. Установите зависимость командой: pip install PySide6", file=sys.stderr)
        return 1
    from ui.main_window import MainWindow
    from ui.styles import APP_STYLE
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    window = MainWindow(); window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
