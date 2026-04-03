from __future__ import annotations

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

from ui_overlay_window import Ui_OverlayWindow


class OverlayWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_OverlayWindow()
        self.ui.setupUi(self)

        # Keep on top but don't steal focus
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.Tool)

        # Small default texts
        try:
            self.ui.Status.setText("Status: Idle")
        except Exception:
            pass
        try:
            self.ui.StatusStream.setText("")
        except Exception:
            pass

    def set_status_text(self, text: str) -> None:
        try:
            self.ui.Status.setText(text)
        except Exception:
            pass

    def set_status_stream(self, text: str) -> None:
        # Replace the label text with the latest log line
        try:
            self.ui.StatusStream.setText(text)
        except Exception:
            pass

    def set_running_state(self, running: bool, paused: bool) -> None:
        # Update main status and enable/disable overlay buttons accordingly
        try:
            if running:
                if paused:
                    self.set_status_text("Status: Paused")
                else:
                    self.set_status_text("Status: Running")
            else:
                self.set_status_text("Status: Idle")
        except Exception:
            pass

        # Buttons
        try:
            self.ui.OverlayRun.setEnabled(not running)
        except Exception:
            pass
        try:
            self.ui.OverlayPause.setEnabled(running and not paused)
        except Exception:
            pass
        try:
            self.ui.OverlayResume.setEnabled(running and paused)
        except Exception:
            pass
        try:
            self.ui.OverlayStop.setEnabled(running)
        except Exception:
            pass

    def bring_to_front(self) -> None:
        try:
            self.show()
            self.raise_()
            self.activateWindow()
        except Exception:
            pass
