"""
Piper TTS - Chèn Âm thanh Siêu tốc
Add-on cho Anki để chèn âm thanh hàng loạt sử dụng Piper TTS

Phiên bản: 1.0.0
"""

import os
from typing import List, Optional
from aqt import mw, gui_hooks
from aqt.browser import Browser
from aqt.qt import QAction, QProgressDialog, QMessageBox, QDialog
from aqt.utils import showInfo, showWarning, tooltip
from anki.notes import Note

# Import modules của add-on
from .config_dialog import PiperTTSConfigDialog
from .piper_tts_engine import PiperTTSEngine


class PiperTTSBulkProcessor:
    """Xử lý hàng loạt thẻ với Piper TTS"""

    def __init__(self, browser: Browser):
        """
        Khởi tạo processor

        Args:
            browser: Browser window của Anki
        """
        self.browser = browser
        self.config = self._load_config()
        self.progress_dialog = None
        self.cancelled = False

    def _load_config(self) -> dict:
        """Tải cấu hình từ Anki"""
        return mw.addonManager.getConfig(__name__) or {}

    def _save_config(self):
        """Lưu cấu hình vào Anki"""
        mw.addonManager.writeConfig(__name__, self.config)

    def run(self):
        """Chạy quá trình xử lý"""
        # Lấy các thẻ đã chọn
        selected_nids = self.browser.selectedNotes()
        if not selected_nids:
            showWarning("Không có thẻ nào được chọn. Vui lòng chọn ít nhất một thẻ.")
            return

        # Hiển thị dialog cấu hình
        dialog = PiperTTSConfigDialog(self.browser, self.config)
        # PyQt6: exec() trả về 1 (Accepted) hoặc 0 (Rejected)
        if not dialog.exec():
            return

        # Lấy cấu hình từ dialog
        config = dialog.get_config()
        self._save_config()

        # Lọc các thẻ theo note type
        notes_to_process = self._filter_notes_by_type(
            selected_nids,
            config['note_type']
        )

        if not notes_to_process:
            showWarning(
                f"Không tìm thấy thẻ nào có Note Type '{config['note_type']}' "
                f"trong các thẻ đã chọn."
            )
            return

        # Xử lý các thẻ
        self._process_notes(notes_to_process, config)

    def _filter_notes_by_type(
        self,
        note_ids: List[int],
        note_type_name: str
    ) -> List[Note]:
        """
        Lọc các note theo note type

        Args:
            note_ids: Danh sách note IDs
            note_type_name: Tên note type

        Returns:
            Danh sách các Note cần xử lý
        """
        filtered_notes = []

        for nid in note_ids:
            note = mw.col.get_note(nid)
            if note.note_type()['name'] == note_type_name:
                filtered_notes.append(note)

        return filtered_notes

    def _process_notes(self, notes: List[Note], config: dict):
        """
        Xử lý danh sách các note

        Args:
            notes: Danh sách các note
            config: Cấu hình xử lý
        """
        # Khởi tạo Piper TTS Engine
        length_scale_value = config.get('length_scale', 1.0)
        print(f"[Piper TTS Debug] Config length_scale: {length_scale_value}")
        print(f"[Piper TTS Debug] Full config: {config}")

        try:
            engine = PiperTTSEngine(
                config['model_path'],
                length_scale=length_scale_value
            )
        except Exception as e:
            showWarning(f"Không thể khởi tạo Piper TTS Engine:\n{str(e)}")
            return

        # Tạo progress dialog
        self.progress_dialog = QProgressDialog(
            "Đang xử lý...",
            "Hủy",
            0,
            len(notes),
            self.browser
        )
        self.progress_dialog.setWindowTitle("Piper TTS - Đang xử lý")
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setValue(0)
        self.progress_dialog.canceled.connect(self._on_cancel)
        self.cancelled = False

        # Thống kê
        processed_count = 0
        skipped_count = 0
        error_count = 0
        errors = []

        # Lấy media folder
        media_folder = mw.col.media.dir()

        # Xử lý từng note
        for i, note in enumerate(notes):
            # Kiểm tra nếu bị hủy
            if self.cancelled:
                break

            # Cập nhật progress
            self.progress_dialog.setValue(i)
            self.progress_dialog.setLabelText(
                f"Đang xử lý thẻ {i+1}/{len(notes)}..."
            )

            # Xử lý note
            result, error_msg = self._process_single_note(
                note,
                config,
                engine,
                media_folder
            )

            if result == 'processed':
                processed_count += 1
            elif result == 'skipped':
                skipped_count += 1
            elif result == 'error':
                error_count += 1
                # Lưu 5 lỗi đầu tiên để hiển thị
                if len(errors) < 5:
                    errors.append(f"Thẻ {note.id}: {error_msg}")

        # Đóng progress dialog
        self.progress_dialog.close()

        # Refresh browser
        self.browser.model.reset()
        mw.reset()

        # Hiển thị kết quả
        if self.cancelled:
            message = (
                f"Quá trình đã bị hủy.\n\n"
                f"Đã xử lý: {processed_count} thẻ\n"
                f"Đã bỏ qua: {skipped_count} thẻ\n"
                f"Lỗi: {error_count} thẻ"
            )
        else:
            message = (
                f"Hoàn thành!\n\n"
                f"Đã xử lý: {processed_count} thẻ\n"
                f"Đã bỏ qua: {skipped_count} thẻ\n"
                f"Lỗi: {error_count} thẻ"
            )

        # Thêm chi tiết lỗi nếu có
        if errors:
            message += "\n\nCác lỗi gặp phải:"
            for error in errors:
                message += f"\n- {error}"
            if error_count > len(errors):
                message += f"\n... và {error_count - len(errors)} lỗi khác"

        showInfo(message)

    def _process_single_note(
        self,
        note: Note,
        config: dict,
        engine: PiperTTSEngine,
        media_folder: str
    ) -> tuple[str, str]:
        """
        Xử lý một note

        Args:
            note: Note cần xử lý
            config: Cấu hình
            engine: Piper TTS Engine
            media_folder: Thư mục media

        Returns:
            tuple[str, str]: (status, error_message)
            status: 'processed', 'skipped', hoặc 'error'
            error_message: Thông báo lỗi nếu có
        """
        source_field = config['source_field']
        target_field = config['target_field']
        overwrite = config['overwrite_existing']
        use_ipa = config.get('use_ipa', False)
        ipa_field = config.get('ipa_field')

        # Kiểm tra xem note có các field cần thiết không
        if source_field not in note:
            return ('skipped', '')
        if target_field not in note:
            return ('skipped', '')

        # Kiểm tra xem target field đã có nội dung chưa
        if not overwrite and note[target_field].strip():
            return ('skipped', '')

        # Quyết định dùng IPA hay text thường
        text = None
        use_phonemes = False

        # Ưu tiên: IPA field (nếu bật và có nội dung)
        if use_ipa and ipa_field and ipa_field in note:
            ipa_text = note[ipa_field].strip()
            # Loại bỏ HTML tags nếu có
            ipa_text = self._strip_html(ipa_text)
            # Làm sạch IPA notation (loại bỏ dấu / và [])
            ipa_text = self._clean_ipa_notation(ipa_text)
            if ipa_text:
                text = ipa_text
                use_phonemes = True
                print(f"[Piper TTS Debug] Sử dụng IPA (đã làm sạch): {text[:50]}...")

        # Fallback: Text thường từ source field
        if not text:
            text = note[source_field].strip()
            if not text:
                return ('skipped', '')
            # Loại bỏ HTML tags nếu có
            text = self._strip_html(text)
            if not text:
                return ('skipped', '')
            print(f"[Piper TTS Debug] Sử dụng text thường: {text[:50]}...")

        # Tạo âm thanh
        filename, error = engine.generate_audio_for_anki(
            text,
            media_folder,
            use_phonemes=use_phonemes
        )

        if not filename:
            # Lỗi khi tạo âm thanh - trả về error message chi tiết
            return ('error', error or 'Lỗi không xác định')

        # Cập nhật target field
        audio_tag = f"[sound:{filename}]"
        note[target_field] = audio_tag
        mw.col.update_note(note)

        return ('processed', '')

    def _clean_ipa_notation(self, ipa_text: str) -> str:
        """
        Làm sạch IPA notation để sử dụng với Piper espeak phonemes

        Args:
            ipa_text: Văn bản IPA có thể chứa dấu / hoặc []

        Returns:
            str: IPA đã làm sạch
        """
        # Loại bỏ dấu / hoặc [] bao quanh IPA
        cleaned = ipa_text.strip()

        # Loại bỏ dấu / từ đầu và cuối (ví dụ: /ˈhɛloʊ/ -> ˈhɛloʊ)
        if cleaned.startswith('/') and cleaned.endswith('/'):
            cleaned = cleaned[1:-1]

        # Loại bỏ dấu [ ] từ đầu và cuối (ví dụ: [ˈhɛloʊ] -> ˈhɛloʊ)
        if cleaned.startswith('[') and cleaned.endswith(']'):
            cleaned = cleaned[1:-1]

        # Trim whitespace
        cleaned = cleaned.strip()

        return cleaned

    def _strip_html(self, text: str) -> str:
        """
        Loại bỏ HTML tags từ văn bản

        Args:
            text: Văn bản có thể chứa HTML

        Returns:
            str: Văn bản đã loại bỏ HTML
        """
        from html.parser import HTMLParser

        class HTMLStripper(HTMLParser):
            def __init__(self):
                super().__init__()
                self.reset()
                self.strict = False
                self.convert_charrefs = True
                self.text = []

            def handle_data(self, data):
                self.text.append(data)

            def get_data(self):
                return ''.join(self.text)

        stripper = HTMLStripper()
        stripper.feed(text)
        return stripper.get_data().strip()

    def _on_cancel(self):
        """Xử lý khi người dùng hủy"""
        self.cancelled = True


def add_browser_action(browser: Browser):
    """
    Thêm action vào Browser menu

    Args:
        browser: Browser window
    """
    action = QAction("Tạo âm thanh (Piper)", browser)
    action.triggered.connect(lambda: on_generate_audio(browser))
    browser.form.menuEdit.addAction(action)


def on_generate_audio(browser: Browser):
    """
    Xử lý khi người dùng nhấn nút tạo âm thanh

    Args:
        browser: Browser window
    """
    processor = PiperTTSBulkProcessor(browser)
    processor.run()


# Đăng ký action với Browser
gui_hooks.browser_menus_did_init.append(add_browser_action)
