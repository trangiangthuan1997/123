"""
TGT97SOUND - Chèn Âm thanh Tự động
Add-on cho Anki để chèn âm thanh hàng loạt sử dụng Piper TTS

Phiên bản: 2.0.0
Author: TGT97
"""

import os
from typing import List, Optional
from aqt import mw, gui_hooks
from aqt.browser import Browser
from aqt.qt import QAction, QProgressDialog, QMessageBox, QDialog, Qt
from aqt.utils import showInfo, showWarning, tooltip
from anki.notes import Note

# Import modules của add-on
from .config_dialog import PiperTTSConfigDialog
from .piper_tts_engine import PiperTTSEngine
from .edge_tts_engine import EdgeTTSEngine
from .install_edge_tts import install_edge_tts, check_edge_tts_installed


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
        # Khởi tạo TTS Engine dựa trên config
        engine_type = config.get('engine', 'edge')  # Mặc định Edge TTS
        print(f"[TGT97SOUND Debug] Engine type: {engine_type}")
        print(f"[TGT97SOUND Debug] Full config: {config}")

        try:
            if engine_type == 'piper':
                # Piper TTS Engine
                length_scale_value = config.get('length_scale', 1.0)
                print(f"[TGT97SOUND Debug] Piper length_scale: {length_scale_value}")
                engine = PiperTTSEngine(
                    config['model_path'],
                    length_scale=length_scale_value
                )
            else:
                # Edge TTS Engine
                voice = config.get('voice', 'en-US-AriaNeural')
                print(f"[TGT97SOUND Debug] Edge TTS voice: {voice}")
                # Convert length_scale to rate for Edge TTS
                # length_scale: 2.0 = 50% speed = -50% rate
                # length_scale: 1.0 = 100% speed = +0% rate
                # length_scale: 0.5 = 200% speed = +100% rate
                length_scale = config.get('length_scale', 1.0)
                rate_percent = int((1.0 - length_scale) * 100)
                rate = f"{rate_percent:+d}%"
                print(f"[TGT97SOUND Debug] Edge TTS rate: {rate}")
                engine = EdgeTTSEngine(voice=voice, rate=rate)
        except Exception as e:
            showWarning(f"Không thể khởi tạo TTS Engine:\n{str(e)}")
            return

        # Tạo progress dialog
        self.progress_dialog = QProgressDialog(
            "Đang khởi động...",
            "Hủy",
            0,
            len(notes),
            self.browser
        )
        self.progress_dialog.setWindowTitle("TGT97SOUND - Đang chèn âm thanh")
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setValue(0)
        self.progress_dialog.setWindowModality(Qt.WindowModality.NonModal)  # Non-modal để user có thể làm việc khác
        self.progress_dialog.setAutoClose(False)  # Không tự động đóng
        self.progress_dialog.setAutoReset(False)  # Không tự động reset
        self.progress_dialog.canceled.connect(self._on_cancel)
        self.cancelled = False

        # Thống kê
        processed_count = 0
        skipped_count = 0
        error_count = 0
        errors = []
        import time
        start_time = time.time()

        # Lấy media folder
        media_folder = mw.col.media.dir()

        # Xử lý từng note
        for i, note in enumerate(notes):
            # Kiểm tra nếu bị hủy
            if self.cancelled:
                break

            # Cập nhật progress với stats
            current_card = i + 1  # Hiển thị 1-based index
            self.progress_dialog.setValue(i)

            # Tính toán stats
            elapsed_time = time.time() - start_time
            if elapsed_time > 0.1:  # Tránh chia cho 0 ở lần đầu
                cards_per_sec = current_card / elapsed_time
                remaining_cards = len(notes) - current_card
                eta_seconds = (remaining_cards / cards_per_sec) if cards_per_sec > 0 else 0
            else:
                cards_per_sec = 0
                eta_seconds = 0

            eta_minutes = int(eta_seconds / 60)
            eta_seconds_remainder = int(eta_seconds % 60)

            # Hiển thị stats
            stats_text = (
                f"Đang xử lý: {current_card}/{len(notes)} thẻ\n"
                f"Tốc độ: {cards_per_sec:.1f} thẻ/giây\n"
                f"Thời gian còn lại: ~{eta_minutes}:{eta_seconds_remainder:02d}\n\n"
                f"💡 Bạn có thể tiếp tục làm các công việc khác trong khi chờ đợi!"
            )
            self.progress_dialog.setLabelText(stats_text)

            # Force update UI
            from aqt.qt import QApplication
            QApplication.processEvents()

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

        # Kiểm tra xem có thực sự bị cancel không
        # Nếu đã xử lý hết tất cả thẻ thì không phải cancel
        total_processed = processed_count + skipped_count + error_count
        if total_processed == len(notes):
            self.cancelled = False  # Hoàn thành hết, không phải cancel

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

        # Kiểm tra xem note có các field cần thiết không
        if source_field not in note:
            return ('skipped', '')
        if target_field not in note:
            return ('skipped', '')

        # Kiểm tra xem target field đã có nội dung chưa
        old_audio_content = note[target_field].strip()
        if not overwrite and old_audio_content:
            return ('skipped', '')

        # Lấy văn bản từ source field
        text = note[source_field].strip()
        if not text:
            return ('skipped', '')

        # Loại bỏ HTML tags nếu có
        text = self._strip_html(text)
        if not text:
            return ('skipped', '')

        # Tạo âm thanh
        filename, error = engine.generate_audio_for_anki(text, media_folder)

        if not filename:
            # Lỗi khi tạo âm thanh - trả về error message chi tiết
            return ('error', error or 'Lỗi không xác định')

        # Xóa file âm thanh cũ nếu đang ghi đè và file khác file mới
        if overwrite and old_audio_content:
            old_filename = self._extract_audio_filename(old_audio_content)
            if old_filename and old_filename != filename:
                try:
                    # Xóa file cũ sử dụng Anki media manager
                    old_file_path = os.path.join(media_folder, old_filename)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                        print(f"[TGT97SOUND Debug] Đã xóa file cũ: {old_filename}")
                except Exception as e:
                    print(f"[TGT97SOUND Debug] Không thể xóa file cũ {old_filename}: {str(e)}")

        # Cập nhật target field
        audio_tag = f"[sound:{filename}]"
        note[target_field] = audio_tag
        mw.col.update_note(note)

        return ('processed', '')

    def _extract_audio_filename(self, audio_content: str) -> Optional[str]:
        """
        Trích xuất tên file từ audio tag

        Args:
            audio_content: Nội dung field audio (ví dụ: "[sound:file.wav]")

        Returns:
            Optional[str]: Tên file nếu tìm thấy, None nếu không
        """
        import re
        # Pattern để match [sound:filename.wav]
        pattern = r'\[sound:([^\]]+)\]'
        match = re.search(pattern, audio_content)
        if match:
            return match.group(1)
        return None

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
    action = QAction("TGT97SOUND - Chèn âm thanh", browser)
    action.triggered.connect(lambda: on_generate_audio(browser))
    browser.form.menuEdit.addAction(action)

    # Thêm menu cài đặt Edge TTS
    install_action = QAction("TGT97SOUND - Cài đặt Edge TTS", browser)
    install_action.triggered.connect(lambda: install_edge_tts())
    browser.form.menuEdit.addAction(install_action)


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
