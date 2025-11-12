# Hướng dẫn Cài đặt Chi tiết - Piper TTS Add-on

Tài liệu này hướng dẫn chi tiết cách cài đặt Piper TTS và các model giọng nói cần thiết.

## Mục lục

- [Cài đặt Piper TTS](#cài-đặt-piper-tts)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [Tải Model Giọng nói](#tải-model-giọng-nói)
- [Kiểm tra Cài đặt](#kiểm-tra-cài-đặt)
- [Xử lý Sự cố](#xử-lý-sự-cố)

---

## Cài đặt Piper TTS

### Windows

#### Cách 1: Tải Binary (Khuyên dùng)

1. **Tải Piper TTS**
   - Truy cập: https://github.com/rhasspy/piper/releases/latest
   - Tải file: `piper_windows_amd64.zip`

2. **Giải nén**
   - Giải nén file zip vào một thư mục, ví dụ: `C:\Program Files\Piper`
   - Bạn sẽ có các file:
     - `piper.exe`
     - Các file DLL cần thiết

3. **Thêm vào PATH**

   **Cách A: Thêm vào System PATH (Khuyên dùng)**
   - Nhấn `Win + R`, gõ `sysdm.cpl` và Enter
   - Chọn tab **Advanced** → **Environment Variables**
   - Trong **System variables**, tìm biến `Path` và nhấn **Edit**
   - Nhấn **New** và thêm đường dẫn: `C:\Program Files\Piper`
   - Nhấn **OK** để lưu
   - **Khởi động lại Command Prompt** để PATH có hiệu lực

   **Cách B: Copy vào thư mục Windows**
   - Copy `piper.exe` và các file DLL vào `C:\Windows\System32`

4. **Kiểm tra**
   ```cmd
   piper --version
   ```

#### Cách 2: Build từ Source (Nâng cao)

```powershell
# Cài đặt dependencies
# Yêu cầu: Visual Studio 2019+, CMake, Git

git clone https://github.com/rhasspy/piper.git
cd piper
mkdir build
cd build
cmake ..
cmake --build . --config Release
```

---

### macOS

#### Cách 1: Sử dụng Homebrew (Khuyên dùng)

```bash
# Cài đặt Homebrew nếu chưa có
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Cài đặt Piper TTS
brew install piper-tts

# Kiểm tra
piper --version
```

#### Cách 2: Tải Binary

1. **Tải file**
   - Truy cập: https://github.com/rhasspy/piper/releases/latest
   - Tải file: `piper_macos_x86_64.tar.gz` (Intel) hoặc `piper_macos_aarch64.tar.gz` (Apple Silicon)

2. **Giải nén và cài đặt**
   ```bash
   # Giải nén
   tar -xzf piper_macos_*.tar.gz

   # Di chuyển vào /usr/local/bin
   sudo mv piper /usr/local/bin/
   sudo chmod +x /usr/local/bin/piper

   # Kiểm tra
   piper --version
   ```

#### Cách 3: Build từ Source

```bash
# Cài đặt dependencies
brew install cmake git

# Clone và build
git clone https://github.com/rhasspy/piper.git
cd piper
mkdir build && cd build
cmake ..
make
sudo make install
```

---

### Linux

#### Cách 1: Tải Binary (Khuyên dùng)

**Ubuntu/Debian:**

```bash
# Tải binary
wget https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz

# Giải nén
tar -xzf piper_linux_x86_64.tar.gz

# Di chuyển vào /usr/local/bin
sudo mv piper /usr/local/bin/
sudo chmod +x /usr/local/bin/piper

# Kiểm tra
piper --version
```

**Arch Linux:**

```bash
# Cài đặt từ AUR
yay -S piper-tts-bin

# Hoặc
paru -S piper-tts-bin
```

**Fedora/RHEL/CentOS:**

```bash
# Tải binary
wget https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz

# Giải nén và cài đặt
tar -xzf piper_linux_x86_64.tar.gz
sudo mv piper /usr/local/bin/
sudo chmod +x /usr/local/bin/piper
```

#### Cách 2: Build từ Source

**Cài đặt dependencies:**

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y git cmake build-essential

# Fedora/RHEL
sudo dnf install -y git cmake gcc-c++ make

# Arch Linux
sudo pacman -S git cmake base-devel
```

**Build Piper:**

```bash
# Clone repository
git clone https://github.com/rhasspy/piper.git
cd piper

# Build
mkdir build && cd build
cmake ..
make -j$(nproc)

# Cài đặt
sudo make install

# Kiểm tra
piper --version
```

---

## Tải Model Giọng nói

### Bước 1: Chọn Model

Truy cập: https://github.com/rhasspy/piper/blob/master/VOICES.md

**Model đề xuất cho tiếng Anh Mỹ:**

| Model | Giọng | Chất lượng | Kích thước | Tốc độ |
|-------|-------|-----------|-----------|---------|
| en_US-lessac-medium | Nam | Cao | ~35 MB | Nhanh |
| en_US-amy-medium | Nữ | Cao | ~30 MB | Nhanh |
| en_US-libritts_r-medium | Đa dạng | Rất cao | ~45 MB | Trung bình |

### Bước 2: Tải Model

#### Cách 1: Tải trực tiếp (Dễ nhất)

1. **Truy cập trang releases**
   - https://github.com/rhasspy/piper/releases/latest

2. **Tìm và tải model**
   - Tìm trong Assets: `en_US-lessac-medium.onnx`
   - Tải cả 2 file:
     - ✅ `en_US-lessac-medium.onnx` (model file)
     - ✅ `en_US-lessac-medium.onnx.json` (config file)

3. **Lưu vào thư mục**
   - Tạo thư mục: `~/piper_models/` (hoặc bất kỳ đâu)
   - Lưu cả 2 file vào đó

#### Cách 2: Sử dụng wget/curl

```bash
# Tạo thư mục
mkdir -p ~/piper_models
cd ~/piper_models

# Tải model (thay thế URL với model bạn muốn)
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx.json

# Kiểm tra
ls -lh
```

#### Cách 3: Script tự động

```bash
#!/bin/bash
# download_piper_model.sh

MODEL_NAME="en_US-lessac-medium"
MODEL_DIR="$HOME/piper_models"
VERSION="v1.2.0"  # Kiểm tra version mới nhất tại GitHub

mkdir -p "$MODEL_DIR"
cd "$MODEL_DIR"

echo "Đang tải model: $MODEL_NAME"

# Tải model
curl -L -o "$MODEL_NAME.onnx" \
  "https://github.com/rhasspy/piper/releases/download/$VERSION/$MODEL_NAME.onnx"

# Tải config
curl -L -o "$MODEL_NAME.onnx.json" \
  "https://github.com/rhasspy/piper/releases/download/$VERSION/$MODEL_NAME.onnx.json"

echo "✅ Hoàn tất! Model đã được lưu tại: $MODEL_DIR"
ls -lh
```

### Bước 3: Xác nhận File

Đảm bảo bạn có cả 2 file:

```
📁 ~/piper_models/
  ├── 📄 en_US-lessac-medium.onnx          (30-40 MB)
  └── 📄 en_US-lessac-medium.onnx.json     (1-5 KB)
```

**⚠️ Quan trọng**: File `.onnx.json` phải có cùng tên với file `.onnx`!

---

## Kiểm tra Cài đặt

### 1. Kiểm tra Piper đã cài đặt

```bash
# Kiểm tra version
piper --version

# Output mong đợi:
# piper version 1.2.0 (hoặc tương tự)
```

### 2. Kiểm tra Model

```bash
# Di chuyển đến thư mục model
cd ~/piper_models

# Kiểm tra cả 2 file tồn tại
ls -lh en_US-lessac-medium.onnx*
```

### 3. Test tạo âm thanh

```bash
# Tạo file test
echo "Hello, this is a test." | piper \
  --model ~/piper_models/en_US-lessac-medium.onnx \
  --output_file test_output.wav

# Phát âm thanh
# Linux: aplay test_output.wav
# macOS: afplay test_output.wav
# Windows: start test_output.wav
```

Nếu file âm thanh được tạo và phát thành công, bạn đã cài đặt đúng! ✅

---

## Xử lý Sự cố

### Lỗi: "piper: command not found"

**Nguyên nhân**: Piper chưa có trong PATH

**Giải pháp**:

1. **Kiểm tra Piper đã được cài đặt**
   ```bash
   # Linux/macOS
   which piper
   ls -l /usr/local/bin/piper

   # Windows
   where piper
   ```

2. **Thêm vào PATH thủ công**

   **Linux/macOS** (thêm vào `~/.bashrc` hoặc `~/.zshrc`):
   ```bash
   export PATH="$PATH:/usr/local/bin"
   ```

   **Windows**: Xem hướng dẫn ở phần Windows trên

### Lỗi: "Could not load model"

**Nguyên nhân**: File model không đúng hoặc thiếu file config

**Giải pháp**:

1. **Kiểm tra file tồn tại**
   ```bash
   ls -lh ~/piper_models/en_US-lessac-medium.onnx*
   ```

2. **Kiểm tra quyền truy cập**
   ```bash
   chmod 644 ~/piper_models/en_US-lessac-medium.onnx*
   ```

3. **Tải lại model**
   - Đảm bảo tải cả 2 file (.onnx và .onnx.json)

### Lỗi: "File config not found"

**Nguyên nhân**: Thiếu file `.onnx.json`

**Giải pháp**:

1. Tải file config từ GitHub (xem Bước 2 ở trên)
2. Đảm bảo file có tên chính xác:
   - Model: `en_US-lessac-medium.onnx`
   - Config: `en_US-lessac-medium.onnx.json` (không phải `en_US-lessac-medium.json`)

### Lỗi Permission Denied (Linux/macOS)

**Giải pháp**:

```bash
# Cấp quyền thực thi
sudo chmod +x /usr/local/bin/piper

# Hoặc chạy với sudo
sudo piper --version
```

### Lỗi Library/DLL not found (Windows)

**Nguyên nhân**: Thiếu Visual C++ Runtime

**Giải pháp**:

Tải và cài đặt:
- Microsoft Visual C++ Redistributable (latest)
- Link: https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist

---

## Model khác

### Tiếng Anh Anh

```bash
# en_GB-alan-medium (Nam, British)
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_GB-alan-medium.onnx
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_GB-alan-medium.onnx.json

# en_GB-alba-medium (Nữ, British)
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_GB-alba-medium.onnx
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_GB-alba-medium.onnx.json
```

### Ngôn ngữ khác

Xem danh sách đầy đủ: https://github.com/rhasspy/piper/blob/master/VOICES.md

---

## Tài nguyên thêm

- **Piper GitHub**: https://github.com/rhasspy/piper
- **Model Repository**: https://huggingface.co/rhasspy/piper-voices
- **Documentation**: https://rhasspy.github.io/piper/
- **Community**: https://github.com/rhasspy/piper/discussions

---

**🎉 Chúc mừng! Bạn đã hoàn tất cài đặt Piper TTS!**

Quay lại [README.md](README.md) để tiếp tục hướng dẫn sử dụng add-on.
