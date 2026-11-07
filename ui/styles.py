"""Visual theme for the desktop application."""

APP_STYLE = """
QWidget { background: #111827; color: #e5e7eb; font-size: 14px; }
QMainWindow { background: #0b1220; }
QFrame#card, QFrame#panel { background: #172033; border: 1px solid #26344d; border-radius: 12px; }
QLabel#title { color: #f8fafc; font-size: 27px; font-weight: 700; }
QLabel#subtitle, QLabel#muted { color: #94a3b8; }
QLabel#section { color: #cbd5e1; font-size: 16px; font-weight: 650; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
  background: #0f172a; border: 1px solid #334155; border-radius: 7px;
  padding: 8px; color: #f8fafc; selection-background-color: #2563eb;
}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus { border: 1px solid #60a5fa; }
QPushButton { background: #24324a; border: 1px solid #3b4b67; border-radius: 7px; padding: 9px 14px; }
QPushButton:hover { background: #304360; }
QPushButton#primary { background: #2563eb; border-color: #3b82f6; font-weight: 700; }
QPushButton#primary:hover { background: #1d4ed8; }
QPushButton#mode { padding: 8px 20px; }
QPushButton#mode:checked { background: #0ea5e9; border-color: #38bdf8; color: white; }
QListWidget { background: #0f172a; border: 1px solid #26344d; border-radius: 8px; padding: 4px; }
QListWidget::item { padding: 8px; border-bottom: 1px solid #1e293b; }
QProgressBar { background: #0f172a; border: none; border-radius: 7px; text-align: center; height: 18px; }
QProgressBar::chunk { background: #22c55e; border-radius: 7px; }
QMessageBox { background: #172033; }
"""
