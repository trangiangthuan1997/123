"""
Edge TTS Engine - Sử dụng Microsoft Edge Read Aloud API
Miễn phí, chất lượng cao, không giới hạn
"""

import os
import hashlib
import asyncio
from typing import Optional, Tuple
import subprocess
import sys


class EdgeTTSEngine:
    """
    TTS Engine sử dụng Microsoft Edge TTS (miễn phí, chất lượng cao)
    """

    def __init__(self, voice: str = "en-US-AriaNeural", rate: str = "+0%"):
        """
        Khởi tạo Edge TTS Engine

        Args:
            voice: Tên giọng đọc (ví dụ: en-US-AriaNeural)
            rate: Tốc độ đọc (ví dụ: "+0%", "+50%", "-50%")
        """
        self.voice = voice
        self.rate = rate
        self._check_edge_tts()

    def _check_edge_tts(self) -> Tuple[bool, str]:
        """
        Kiểm tra xem edge-tts đã được cài đặt chưa

        Returns:
            Tuple[bool, str]: (có cài đặt, thông báo)
        """
        try:
            result = subprocess.run(
                [sys.executable, "-m", "edge_tts", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return True, ""
            else:
                return False, "edge-tts không hoạt động đúng"
        except subprocess.TimeoutExpired:
            return False, "Timeout khi kiểm tra edge-tts"
        except FileNotFoundError:
            return False, "edge-tts chưa được cài đặt. Vui lòng cài: pip install edge-tts"
        except Exception as e:
            return False, f"Lỗi khi kiểm tra edge-tts: {str(e)}"

    async def _generate_audio_async(self, text: str, output_path: str) -> Tuple[bool, str]:
        """
        Tạo file âm thanh từ văn bản (async)

        Args:
            text: Văn bản cần chuyển thành giọng nói
            output_path: Đường dẫn file output (.mp3 hoặc .wav)

        Returns:
            Tuple[bool, str]: (thành công, thông báo lỗi nếu có)
        """
        try:
            import edge_tts

            # Tạo thư mục output nếu chưa có
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            # Tạo file tạm .mp3
            temp_mp3 = output_path.replace('.wav', '.mp3')

            # Tạo communicate object
            communicate = edge_tts.Communicate(text, self.voice, rate=self.rate)

            # Lưu thành file mp3
            await communicate.save(temp_mp3)

            # Convert mp3 to wav using ffmpeg nếu cần
            if output_path.endswith('.wav'):
                # Sử dụng subprocess để convert
                result = subprocess.run(
                    ['ffmpeg', '-i', temp_mp3, '-acodec', 'pcm_s16le', '-ar', '22050', output_path, '-y'],
                    capture_output=True,
                    text=True
                )

                # Xóa file mp3 tạm
                if os.path.exists(temp_mp3):
                    os.remove(temp_mp3)

                if result.returncode != 0:
                    # Nếu ffmpeg không có, giữ lại file mp3
                    os.rename(temp_mp3, output_path.replace('.wav', '.mp3'))
                    print(f"[TGT97SOUND Debug] ffmpeg không có, sử dụng .mp3 thay vì .wav")

            return True, ""

        except ImportError:
            return False, "Thư viện edge-tts chưa được cài đặt. Vui lòng chạy: pip install edge-tts"
        except Exception as e:
            return False, f"Lỗi khi tạo âm thanh: {str(e)}"

    def generate_audio(self, text: str, output_path: str) -> Tuple[bool, str]:
        """
        Tạo file âm thanh từ văn bản (sync wrapper)

        Args:
            text: Văn bản cần chuyển thành giọng nói
            output_path: Đường dẫn file output (.wav)

        Returns:
            Tuple[bool, str]: (thành công, thông báo lỗi nếu có)
        """
        # Làm sạch văn bản
        text = text.strip()
        if not text:
            return False, "Văn bản trống"

        # Chạy async function trong event loop
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._generate_audio_async(text, output_path))
            loop.close()
            return result
        except Exception as e:
            return False, f"Lỗi khi tạo âm thanh: {str(e)}"

    def generate_audio_for_anki(
        self,
        text: str,
        media_folder: str
    ) -> Tuple[Optional[str], str]:
        """
        Tạo file âm thanh và lưu vào thư mục media của Anki

        Args:
            text: Văn bản cần chuyển thành giọng nói
            media_folder: Đường dẫn đến thư mục collection.media

        Returns:
            Tuple[Optional[str], str]: (tên file nếu thành công, thông báo lỗi)
        """
        # Tạo tên file duy nhất dựa trên:
        # - Hash của văn bản
        # - Voice
        # - Rate (tốc độ)
        unique_string = f"{text}|{self.voice}|{self.rate}"
        text_hash = hashlib.md5(unique_string.encode('utf-8')).hexdigest()[:12]
        filename = f"tgt97sound_{text_hash}.mp3"  # Sử dụng mp3 cho Edge TTS
        output_path = os.path.join(media_folder, filename)

        # Nếu file đã tồn tại, trả về luôn
        if os.path.exists(output_path):
            print(f"[TGT97SOUND Debug] File đã tồn tại, sử dụng lại: {filename}")
            return filename, ""

        print(f"[TGT97SOUND Debug] Tạo file mới với Edge TTS: {filename}")
        print(f"[TGT97SOUND Debug] Voice: {self.voice}, Rate: {self.rate}")

        # Tạo âm thanh
        success, error = self.generate_audio(text, output_path)

        if success:
            return filename, ""
        else:
            return None, error


# Danh sách giọng hay nhất
BEST_VOICES = {
    "en-US-AriaNeural": "🇺🇸 Aria (Nữ, American, tự nhiên nhất)",
    "en-US-GuyNeural": "🇺🇸 Guy (Nam, American, rõ ràng)",
    "en-US-JennyNeural": "🇺🇸 Jenny (Nữ, American, friendly)",
    "en-US-RyanNeural": "🇺🇸 Ryan (Nam, American, energetic)",
    "en-GB-SoniaNeural": "🇬🇧 Sonia (Nữ, British, elegant)",
    "en-GB-RyanNeural": "🇬🇧 Ryan (Nam, British, professional)",
    "en-AU-NatashaNeural": "🇦🇺 Natasha (Nữ, Australian)",
    "en-AU-WilliamNeural": "🇦🇺 William (Nam, Australian)",
}
