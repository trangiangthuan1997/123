"""
Script tự động cài edge-tts vào Anki Python environment
"""

import subprocess
import sys
from aqt.utils import showInfo, showWarning
from aqt.qt import QMessageBox, QProgressDialog, QApplication


def install_edge_tts():
    """Cài đặt edge-tts vào Anki Python environment"""
    try:
        # Tạo progress dialog
        progress = QProgressDialog(
            "Đang cài đặt edge-tts...\nVui lòng chờ...",
            None,
            0,
            0
        )
        progress.setWindowTitle("TGT97SOUND - Đang cài đặt")
        progress.setMinimumDuration(0)
        progress.setValue(0)
        progress.show()
        QApplication.processEvents()

        # Chạy pip install với Python của Anki
        print("[TGT97SOUND] Đang cài đặt edge-tts...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "edge-tts"],
            capture_output=True,
            text=True,
            timeout=120
        )

        progress.close()

        if result.returncode == 0:
            showInfo(
                "✅ Cài đặt edge-tts thành công!\n\n"
                "Vui lòng RESTART ANKI để áp dụng thay đổi.\n\n"
                "Sau đó bạn có thể sử dụng TGT97SOUND với Edge TTS bình thường."
            )
            print("[TGT97SOUND] Cài đặt thành công!")
            print(result.stdout)
            return True
        else:
            showWarning(
                "❌ Lỗi khi cài đặt edge-tts:\n\n"
                f"{result.stderr}\n\n"
                "Vui lòng thử cách thủ công:\n"
                "1. Tìm thư mục Anki install (ví dụ: C:\\Program Files\\Anki)\n"
                "2. Mở CMD tại đó\n"
                "3. Chạy: python.exe -m pip install edge-tts"
            )
            print(f"[TGT97SOUND] Lỗi: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        showWarning("Timeout khi cài đặt edge-tts. Vui lòng thử lại.")
        return False
    except Exception as e:
        showWarning(f"Lỗi khi cài đặt edge-tts:\n{str(e)}")
        print(f"[TGT97SOUND] Exception: {str(e)}")
        return False


def check_edge_tts_installed():
    """Kiểm tra xem edge-tts đã được cài đặt chưa"""
    try:
        import edge_tts
        return True
    except ImportError:
        return False
