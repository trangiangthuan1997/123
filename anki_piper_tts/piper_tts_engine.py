"""
Piper TTS Engine Module
Xử lý việc tạo âm thanh từ văn bản sử dụng Piper TTS
"""

import os
import subprocess
import hashlib
import wave
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Tuple


class PiperTTSEngine:
    """Engine để tạo âm thanh bằng Piper TTS"""

    def __init__(self, model_path: str, length_scale: float = 1.0):
        """
        Khởi tạo Piper TTS Engine

        Args:
            model_path: Đường dẫn đến file model .onnx
            length_scale: Tốc độ đọc (1.0 = bình thường, 2.0 = chậm 50%, 0.5 = nhanh 200%)
        """
        self.model_path = model_path
        self.length_scale = length_scale
        self.model_config_path = self._get_model_config_path(model_path)
        self._validate_model()

        # Check Piper installation một lần duy nhất khi khởi tạo
        is_installed, error_msg = self._check_piper_installation()
        if not is_installed:
            raise RuntimeError(error_msg)

    def _get_model_config_path(self, model_path: str) -> str:
        """Lấy đường dẫn đến file config .json của model"""
        return model_path.replace('.onnx', '.onnx.json')

    def _validate_model(self) -> None:
        """Kiểm tra xem model có tồn tại không"""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Không tìm thấy file model: {self.model_path}")

        if not os.path.exists(self.model_config_path):
            raise FileNotFoundError(
                f"Không tìm thấy file config model: {self.model_config_path}\n"
                f"File config phải có cùng tên với model và thêm .json"
            )

    def _check_piper_installation(self) -> Tuple[bool, str]:
        """
        Kiểm tra xem Piper có được cài đặt không

        Returns:
            Tuple[bool, str]: (có cài đặt, thông báo lỗi nếu có)
        """
        try:
            # Thử gọi piper với --help (nhanh hơn --version và không bị timeout)
            result = subprocess.run(
                ['piper', '--help'],
                capture_output=True,
                text=True,
                timeout=10,
                stdin=subprocess.DEVNULL  # Đảm bảo không chờ stdin
            )
            return True, ""
        except FileNotFoundError:
            return False, "Không tìm thấy Piper TTS. Vui lòng cài đặt Piper TTS trước."
        except subprocess.TimeoutExpired:
            # Nếu timeout nhưng process đã chạy, coi như Piper có sẵn
            return True, ""
        except Exception as e:
            return False, f"Lỗi khi kiểm tra Piper TTS: {str(e)}"

    def generate_audio(self, text: str, output_path: str) -> Tuple[bool, str]:
        """
        Tạo file âm thanh từ văn bản

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

        # Tạo thư mục output nếu chưa có
        output_dir = os.path.dirname(output_path)
        if output_dir:  # Chỉ tạo nếu có dirname
            os.makedirs(output_dir, exist_ok=True)

        # Tạo file tạm trong temp folder (tránh vấn đề Unicode path trên Windows)
        temp_fd, temp_path = tempfile.mkstemp(suffix='.wav', prefix='piper_')
        os.close(temp_fd)  # Đóng file descriptor

        try:
            # Chuyển đổi paths thành absolute paths
            abs_model_path = os.path.abspath(self.model_path)
            abs_temp_path = os.path.abspath(temp_path)

            # Build command với length_scale
            command = [
                'piper',
                '--model', abs_model_path,
                '--output_file', abs_temp_path,
                '--length_scale', str(self.length_scale)
            ]

            # Debug: In ra command để kiểm tra
            print(f"[Piper TTS Debug] Running command: {' '.join(command)}")
            print(f"[Piper TTS Debug] Length scale: {self.length_scale}")

            # Gọi Piper để tạo âm thanh vào temp file
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )

            # Truyền text vào stdin và đợi process hoàn thành
            stdout, stderr = process.communicate(input=text, timeout=60)

            if process.returncode != 0:
                return False, f"Piper trả về lỗi (code {process.returncode}): {stderr}"

            # Kiểm tra temp file đã được tạo
            if not os.path.exists(abs_temp_path):
                return False, f"File tạm không được tạo. stderr: {stderr}"

            # Kiểm tra file có nội dung không
            if os.path.getsize(abs_temp_path) == 0:
                return False, "File âm thanh trống"

            # Copy từ temp sang output path (handle Unicode correctly)
            shutil.copy2(abs_temp_path, output_path)

            # Xóa temp file
            os.unlink(abs_temp_path)

            return True, ""

        except subprocess.TimeoutExpired:
            # Cleanup temp file nếu có
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            return False, "Timeout khi tạo âm thanh"
        except Exception as e:
            # Cleanup temp file nếu có
            if os.path.exists(temp_path):
                os.unlink(temp_path)
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
        # - Hash của model path (model khác → file khác)
        # - Length scale (tốc độ khác → file khác)
        unique_string = f"{text}|{self.model_path}|{self.length_scale}"
        text_hash = hashlib.md5(unique_string.encode('utf-8')).hexdigest()[:12]
        filename = f"piper_tts_{text_hash}.wav"
        output_path = os.path.join(media_folder, filename)

        # Nếu file đã tồn tại, trả về luôn
        if os.path.exists(output_path):
            print(f"[Piper TTS Debug] File đã tồn tại, sử dụng lại: {filename}")
            return filename, ""

        print(f"[Piper TTS Debug] Tạo file mới: {filename}")

        # Tạo âm thanh
        success, error = self.generate_audio(text, output_path)

        if success:
            return filename, ""
        else:
            return None, error


class PiperTTSEngineAlternative:
    """
    Engine thay thế sử dụng thư viện piper-tts Python
    (Chỉ sử dụng nếu không có binary piper)
    """

    def __init__(self, model_path: str):
        """Khởi tạo engine với model path"""
        self.model_path = model_path
        self.voice = None
        self._load_model()

    def _load_model(self) -> None:
        """Tải model vào bộ nhớ"""
        try:
            from piper import PiperVoice
            self.voice = PiperVoice.load(self.model_path)
        except ImportError:
            raise ImportError(
                "Không tìm thấy thư viện piper-tts. "
                "Vui lòng cài đặt: pip install piper-tts"
            )
        except Exception as e:
            raise Exception(f"Không thể tải model: {str(e)}")

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
        if not self.voice:
            return None, "Model chưa được tải"

        text = text.strip()
        if not text:
            return None, "Văn bản trống"

        try:
            # Tạo tên file
            text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()[:12]
            filename = f"piper_tts_{text_hash}.wav"
            output_path = os.path.join(media_folder, filename)

            # Nếu file đã tồn tại, trả về luôn
            if os.path.exists(output_path):
                return filename, ""

            # Tạo âm thanh
            with wave.open(output_path, 'wb') as wav_file:
                self.voice.synthesize(text, wav_file)

            return filename, ""

        except Exception as e:
            return None, f"Lỗi khi tạo âm thanh: {str(e)}"
