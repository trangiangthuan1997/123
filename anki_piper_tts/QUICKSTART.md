# 🚀 Quick Start - Piper TTS Add-on

Hướng dẫn bắt đầu nhanh trong 5 phút!

## ⚡ Cài đặt Nhanh

### 1. Cài đặt Piper TTS

**Windows:**
```bash
# Tải từ: https://github.com/rhasspy/piper/releases
# Giải nén và thêm vào PATH
```

**macOS:**
```bash
brew install piper-tts
```

**Linux:**
```bash
wget https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz
tar -xzf piper_linux_x86_64.tar.gz
sudo mv piper /usr/local/bin/
```

### 2. Tải Model

```bash
# Tạo thư mục
mkdir ~/piper_models
cd ~/piper_models

# Tải model (thay VERSION với version mới nhất, ví dụ: v1.2.0)
wget https://github.com/rhasspy/piper/releases/download/VERSION/en_US-lessac-medium.onnx
wget https://github.com/rhasspy/piper/releases/download/VERSION/en_US-lessac-medium.onnx.json
```

**Hoặc tải thủ công:**
- Truy cập: https://github.com/rhasspy/piper/releases
- Tải 2 file: `en_US-lessac-medium.onnx` và `en_US-lessac-medium.onnx.json`

### 3. Cài đặt Add-on

1. Sao chép folder `anki_piper_tts` vào thư mục add-ons của Anki:
   - **Windows**: `%APPDATA%\Anki2\addons21\`
   - **macOS**: `~/Library/Application Support/Anki2/addons21/`
   - **Linux**: `~/.local/share/Anki2/addons21/`

2. Khởi động lại Anki

## 🎯 Sử dụng

### Chuẩn bị Note Type

1. Tạo hoặc chỉnh sửa Note Type với 2 trường:
   - `English` - Chứa văn bản
   - `Audio` - Chứa âm thanh

### Thêm Âm thanh

1. **Mở Browser** (Ctrl/Cmd + B)

2. **Chọn thẻ** cần thêm âm thanh

3. **Chạy Add-on**: Menu **Edit** → **Tạo âm thanh (Piper)**

4. **Cấu hình**:
   - Note Type: Chọn note type của bạn
   - Trường nguồn: English
   - Trường đích: Audio
   - Model: Chọn file `.onnx` đã tải

5. **Nhấn Bắt đầu** và đợi!

## ✅ Kiểm tra

```bash
# Test Piper
piper --version

# Test tạo âm thanh
echo "Hello world" | piper \
  --model ~/piper_models/en_US-lessac-medium.onnx \
  --output_file test.wav
```

## 📚 Tài liệu đầy đủ

- [README.md](README.md) - Hướng dẫn chi tiết
- [INSTALLATION.md](INSTALLATION.md) - Cài đặt chi tiết

## 🆘 Gặp vấn đề?

### Lỗi "piper not found"
→ Piper chưa có trong PATH. Xem [INSTALLATION.md](INSTALLATION.md)

### Lỗi "config file not found"
→ Thiếu file `.onnx.json`. Phải tải cả 2 file!

### Lỗi khác
→ Xem phần [Xử lý sự cố](README.md#🔧-xử-lý-sự-cố) trong README

---

**Xong! Bắt đầu thêm âm thanh cho thẻ của bạn! 🎉**
