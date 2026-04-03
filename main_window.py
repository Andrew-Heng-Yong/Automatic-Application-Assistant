from __future__ import annotations

import threading
from pathlib import Path
from typing import Any

from PySide6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PySide6.QtCore import QTimer

from ui_main_window import Ui_MainWindow
from config_manager import load_json, save_json
import backend.core.automation as automation

BASE_DIR = Path(__file__).resolve().parent


class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Internal state
        self._app_config_path = BASE_DIR / "app_config.json"
        self._gemini_config_path = BASE_DIR / "gemini_config.json"
        self._original_resume_catalog: list[dict[str, Any]] | None = None
        self._automation_thread: threading.Thread | None = None

        # Connect buttons (existing)
        self.ui.button_load_app_config.clicked.connect(self.load_app_config)
        self.ui.button_save_app_config.clicked.connect(self.save_app_config)
        self.ui.button_load_gemini_config.clicked.connect(self.load_gemini_config)
        self.ui.button_save_gemini_config.clicked.connect(self.save_gemini_config)
        self.ui.button_run.clicked.connect(self.run_automation)
        self.ui.button_stop.clicked.connect(self.stop_automation)

        # Connect new widgets safely (may not exist in older UI)
        try:
            self.ui.button_add_resume_row.clicked.connect(self.add_resume_row)
        except Exception:
            pass
        try:
            self.ui.button_remove_resume_row.clicked.connect(self.remove_resume_row)
        except Exception:
            pass
        try:
            self.ui.button_clear_logs.clicked.connect(self.ui.text_logs.clear)
        except Exception:
            pass

        # Initialize UI with current configs if present
        self.load_app_config()
        self.load_gemini_config()

        # Startup log
        try:
            self.log_message("UI initialized.")
        except Exception:
            # If logs widget missing, ignore
            pass

    # --------------------------
    # App config helpers
    # --------------------------
    def load_app_config(self) -> None:
        cfg = load_json(str(self._app_config_path))
        # set widget values with safe defaults
        self.ui.spin_confidence.setValue(float(cfg.get("confidence", self.ui.spin_confidence.value())))
        self.ui.spin_check_interval.setValue(float(cfg.get("check_interval", self.ui.spin_check_interval.value())))
        self.ui.spin_default_timeout.setValue(int(cfg.get("default_timeout", self.ui.spin_default_timeout.value())))
        self.ui.spin_scroll_step.setValue(int(cfg.get("scroll_step", self.ui.spin_scroll_step.value())))
        self.ui.spin_page_ready_timeout.setValue(int(cfg.get("page_ready_timeout", self.ui.spin_page_ready_timeout.value())))
        self.ui.spin_post_apply_timeout.setValue(int(cfg.get("post_apply_timeout", self.ui.spin_post_apply_timeout.value())))
        self.ui.spin_apply_retry_count.setValue(int(cfg.get("apply_retry_count", self.ui.spin_apply_retry_count.value())))
        self.ui.spin_max_scroll_pages.setValue(int(cfg.get("max_scroll_pages", self.ui.spin_max_scroll_pages.value())))
        self.ui.spin_row_half_height.setValue(int(cfg.get("row_half_height", self.ui.spin_row_half_height.value())))
        self.ui.spin_left_scan_width_ratio.setValue(float(cfg.get("left_scan_width_ratio", self.ui.spin_left_scan_width_ratio.value())))
        self.ui.edit_start_anchor.setText(str(cfg.get("start_anchor", self.ui.edit_start_anchor.text())))
        self.ui.edit_end_anchor.setText(str(cfg.get("end_anchor", self.ui.edit_end_anchor.text())))

    def save_app_config(self) -> None:
        cfg = {
            "confidence": float(self.ui.spin_confidence.value()),
            "check_interval": float(self.ui.spin_check_interval.value()),
            "default_timeout": int(self.ui.spin_default_timeout.value()),
            "scroll_step": int(self.ui.spin_scroll_step.value()),
            "page_ready_timeout": int(self.ui.spin_page_ready_timeout.value()),
            "post_apply_timeout": int(self.ui.spin_post_apply_timeout.value()),
            "apply_retry_count": int(self.ui.spin_apply_retry_count.value()),
            "max_scroll_pages": int(self.ui.spin_max_scroll_pages.value()),
            "row_half_height": int(self.ui.spin_row_half_height.value()),
            "left_scan_width_ratio": float(self.ui.spin_left_scan_width_ratio.value()),
            "start_anchor": str(self.ui.edit_start_anchor.text()),
            "end_anchor": str(self.ui.edit_end_anchor.text()),
        }
        save_json(str(self._app_config_path), cfg)

    # --------------------------
    # Gemini config helpers
    # --------------------------
    def load_gemini_config(self) -> None:
        cfg = load_json(str(self._gemini_config_path))
        # preserve original resume catalog for later
        self._original_resume_catalog = cfg.get("RESUME_CATALOG")

        self.ui.edit_api_key.setText(str(cfg.get("API_KEY", self.ui.edit_api_key.text())))
        self.ui.edit_model_name.setText(str(cfg.get("MODEL_NAME", self.ui.edit_model_name.text())))
        # OUTPUT_DIR widget may not exist in some UI versions
        if hasattr(self.ui, "edit_output_dir"):
            self.ui.edit_output_dir.setText(str(cfg.get("OUTPUT_DIR", self.ui.edit_output_dir.text())))
        self.ui.spin_cover_letter_word_limit.setValue(int(cfg.get("COVER_LETTER_WORD_LIMIT", self.ui.spin_cover_letter_word_limit.value())))

        self.ui.text_resume_selection_system_prompt.setPlainText(str(cfg.get("RESUME_SELECTION_SYSTEM_PROMPT", self.ui.text_resume_selection_system_prompt.toPlainText())))
        self.ui.text_resume_selection_user_prompt_template.setPlainText(str(cfg.get("RESUME_SELECTION_USER_PROMPT_TEMPLATE", self.ui.text_resume_selection_user_prompt_template.toPlainText())))

        self.ui.text_cover_letter_system_prompt.setPlainText(str(cfg.get("COVER_LETTER_SYSTEM_PROMPT", self.ui.text_cover_letter_system_prompt.toPlainText())))
        self.ui.text_cover_letter_user_prompt_template.setPlainText(str(cfg.get("COVER_LETTER_USER_PROMPT_TEMPLATE", self.ui.text_cover_letter_user_prompt_template.toPlainText())))

        self.ui.text_minor_change_system_prompt.setPlainText(str(cfg.get("MINOR_CHANGE_SYSTEM_PROMPT", self.ui.text_minor_change_system_prompt.toPlainText())))
        self.ui.text_minor_change_user_prompt_template.setPlainText(str(cfg.get("MINOR_CHANGE_USER_PROMPT_TEMPLATE", self.ui.text_minor_change_user_prompt_template.toPlainText())))

        self.ui.text_additional_personal_information.setPlainText(str(cfg.get("ADDITIONAL_PERSONAL_INFORMATION", self.ui.text_additional_personal_information.toPlainText())))

        # Note: resume catalog table editing not implemented. Preserve original on save.

    def save_gemini_config(self) -> None:
        # Load existing file to preserve keys not present in UI (e.g., RESUME_CATALOG)
        existing = load_json(str(self._gemini_config_path))
        cfg: dict[str, Any] = existing.copy()

        cfg.update(
            {
                "API_KEY": str(self.ui.edit_api_key.text()),
                "MODEL_NAME": str(self.ui.edit_model_name.text()),
                # "OUTPUT_DIR": str(self.ui.edit_output_dir.text()),
            }
        )

        # OUTPUT_DIR may not be present in UI; only include it if widget exists
        if hasattr(self.ui, "edit_output_dir"):
            cfg["OUTPUT_DIR"] = str(self.ui.edit_output_dir.text())

        cfg.update(
            {
                "COVER_LETTER_WORD_LIMIT": int(self.ui.spin_cover_letter_word_limit.value()),

                "RESUME_SELECTION_SYSTEM_PROMPT": str(self.ui.text_resume_selection_system_prompt.toPlainText()),
                "RESUME_SELECTION_USER_PROMPT_TEMPLATE": str(self.ui.text_resume_selection_user_prompt_template.toPlainText()),

                "COVER_LETTER_SYSTEM_PROMPT": str(self.ui.text_cover_letter_system_prompt.toPlainText()),
                "COVER_LETTER_USER_PROMPT_TEMPLATE": str(self.ui.text_cover_letter_user_prompt_template.toPlainText()),

                "MINOR_CHANGE_SYSTEM_PROMPT": str(self.ui.text_minor_change_system_prompt.toPlainText()),
                "MINOR_CHANGE_USER_PROMPT_TEMPLATE": str(self.ui.text_minor_change_user_prompt_template.toPlainText()),

                "ADDITIONAL_PERSONAL_INFORMATION": str(self.ui.text_additional_personal_information.toPlainText()),
            }
        )

        # Ensure RESUME_CATALOG preserved if it existed
        if "RESUME_CATALOG" not in cfg and self._original_resume_catalog is not None:
            cfg["RESUME_CATALOG"] = self._original_resume_catalog

        save_json(str(self._gemini_config_path), cfg)

    # --------------------------
    # Automation control
    # --------------------------
    def _automation_target(self) -> None:
        try:
            automation.main()
        except Exception as exc:
            # show a user-friendly message on failure on the main thread
            QTimer.singleShot(0, lambda: QMessageBox.critical(self, "Automation Error", f"Automation raised an exception: {exc}"))
        finally:
            # Re-enable Run button when finished on the main thread
            QTimer.singleShot(0, lambda: self.ui.button_run.setEnabled(True))

    def run_automation(self) -> None:
        if self._automation_thread and self._automation_thread.is_alive():
            return

        # Clear any previous stop requests and start automation
        try:
            automation.clear_stop()
        except Exception:
            pass
        self.log_message("Starting automation...")
        self.ui.button_run.setEnabled(False)
        self._automation_thread = threading.Thread(target=self._automation_target, daemon=True)
        self._automation_thread.start()

    def stop_automation(self) -> None:
        # Signal the automation to stop cooperatively
        try:
            automation.request_stop()
            self.log_message("Stop requested.")
            QMessageBox.information(self, "Stop", "Stop requested — automation will stop shortly.")
        except Exception as exc:
            QMessageBox.warning(self, "Stop", f"Failed to request stop: {exc}")

    # --------------------------
    # Resume catalog helpers
    # --------------------------
    def add_resume_row(self) -> None:
        # Insert an empty row at the bottom of the resume catalog table
        table = self.ui.table_resume_catalog
        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 0, QTableWidgetItem(""))
        table.setItem(row, 1, QTableWidgetItem(""))

    def remove_resume_row(self) -> None:
        # Remove the currently selected row if any
        table = self.ui.table_resume_catalog
        current = table.currentRow()
        if current >= 0:
            table.removeRow(current)

    # --------------------------
    # Logging helpers
    # --------------------------
    def log_message(self, message: str) -> None:
        try:
            now = message
            self.ui.text_logs.appendPlainText(now)
        except Exception:
            pass


# If this module is run directly, create and show the window (useful for testing)
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
