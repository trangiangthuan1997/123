# Piper TTS - Chèn Âm thanh Siêu tốc

Add-on cho Anki để chèn âm thanh hàng loạt với hiệu suất cao, sử dụng thư viện Piper TTS.

## 📋 Tính năng

- ⚡ **Hiệu suất cao**: Xử lý hàng nghìn thẻ một cách nhanh chóng
- 🎙️ **Chất lượng cao**: Sử dụng Piper TTS để tạo giọng nói tự nhiên
- 🎯 **Dễ sử dụng**: Giao diện trực quan, dễ cấu hình
- 📊 **Theo dõi tiến trình**: Progress bar hiển thị tiến độ xử lý
- 🔄 **Tùy chọn ghi đè**: Chọn ghi đè hoặc bỏ qua các thẻ đã có âm thanh
- 💾 **Lưu cấu hình**: Ghi nhớ các thiết lập cho lần sử dụng sau

## 📦 Yêu cầu hệ thống

- **Anki**: Phiên bản 23.10 trở lên (đã test với 25.09.2)
- **Python**: 3.9 trở lên (Anki đã tích hợp)
- **Piper TTS**: Binary hoặc thư viện Python
- **Model giọng nói**: File .onnx và .onnx.json

## 🚀 Cài đặt

### Bước 1: Cài đặt Add-on

#### Cách 1: Cài đặt từ AnkiWeb (Khuyên dùng)
1. Mở Anki
2. Vào **Tools** → **Add-ons** → **Get Add-ons...**
3. Nhập mã add-on: `[Mã sẽ có sau khi publish]`
4. Nhấn **OK**

#### Cách 2: Cài đặt thủ công
1. Tải về folder `anki_piper_tts`
2. Mở Anki → **Tools** → **Add-ons** → **View Files**
3. Sao chép folder `anki_piper_tts` vào thư mục add-ons
4. Khởi động lại Anki

### Bước 2: Cài đặt Piper TTS

Xem hướng dẫn chi tiết trong file [INSTALLATION.md](INSTALLATION.md)

**Tóm tắt:**

#### Windows
```bash
# Tải binary từ: https://github.com/rhasspy/piper/releases
# Giải nén và thêm vào PATH
```

#### macOS
```bash
brew install piper-tts
```

#### Linux
```bash
# Tải binary hoặc build từ source
wget https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz
tar -xvf piper_linux_x86_64.tar.gz
sudo mv piper /usr/local/bin/
```

### Bước 3: Tải Model Giọng nói

1. Truy cập: https://github.com/rhasspy/piper/releases
2. Tải model giọng Anh-Mỹ chất lượng cao:
   - **Khuyên dùng**: `en_US-lessac-medium.onnx`
   - File config: `en_US-lessac-medium.onnx.json`
3. Lưu cả hai file vào một thư mục trên máy tính

**⚠️ Lưu ý**: Cả file `.onnx` và `.onnx.json` đều cần thiết!

## 📖 Hướng dẫn sử dụng

### 1. Mở Browser và chọn thẻ

1. Mở Anki Browser: **Browse** (Ctrl/Cmd + B)
2. Chọn các thẻ bạn muốn thêm âm thanh (có thể chọn nhiều thẻ)

### 2. Chạy Add-on

1. Trong Browser, vào menu **Edit** → **Tạo âm thanh (Piper)**
2. Hoặc sử dụng shortcut (nếu đã cấu hình)

### 3. Cấu hình

Một hộp thoại sẽ hiện ra với các tùy chọn:

#### **1. Chọn Note Type**
- Chọn loại thẻ (Note Type) bạn muốn xử lý
- Ví dụ: "Basic", "Cloze", hoặc custom note type của bạn

#### **2. Chọn Trường (Fields)**
- **Trường nguồn**: Trường chứa văn bản cần đọc (mặc định: "English")
- **Trường đích**: Trường sẽ chứa âm thanh (mặc định: "Audio")

#### **3. Chọn Model Giọng nói**
- Nhấn **Browse** và chọn file model `.onnx` đã tải
- Add-on sẽ ghi nhớ đường dẫn cho lần sau

#### **4. Tùy chọn**
- ☑️ **Ghi đè lên âm thanh đã có**: Nếu chọn, sẽ thay thế âm thanh cũ
- ☐ **Mặc định**: Bỏ qua các thẻ đã có âm thanh

### 4. Bắt đầu xử lý

1. Nhấn **Bắt đầu**
2. Một thanh tiến trình sẽ hiển thị quá trình xử lý
3. Bạn có thể nhấn **Hủy** bất cứ lúc nào
4. Sau khi hoàn tất, một thông báo sẽ hiển thị kết quả:
   - Số thẻ đã xử lý
   - Số thẻ đã bỏ qua
   - Số thẻ lỗi (nếu có)

## 🎯 Ví dụ sử dụng

### Ví dụ 1: Thêm âm thanh cho từ vựng tiếng Anh

1. Tạo Note Type với 2 trường:
   - `English`: Chứa từ tiếng Anh
   - `Audio`: Chứa âm thanh

2. Thêm các thẻ với từ vựng trong trường `English`

3. Chọn tất cả thẻ trong Browser

4. Chạy Add-on:
   - Note Type: Chọn note type của bạn
   - Source: English
   - Target: Audio
   - Model: Chọn file en_US-lessac-medium.onnx

5. Nhấn **Bắt đầu** và đợi quá trình hoàn tất

### Ví dụ 2: Cập nhật lại âm thanh cho các thẻ cũ

1. Chọn các thẻ cần cập nhật âm thanh

2. Chạy Add-on

3. **Bật** tùy chọn "Ghi đè lên âm thanh đã có"

4. Nhấn **Bắt đầu**

## ⚙️ Cấu hình nâng cao

Cấu hình được lưu trong file `config.json` và có thể chỉnh sửa qua Anki:

**Tools** → **Add-ons** → Chọn **Piper TTS** → **Config**

```json
{
    "model_path": "/path/to/en_US-lessac-medium.onnx",
    "source_field": "English",
    "target_field": "Audio",
    "overwrite_existing": false,
    "last_note_type": "Basic"
}
```

## 🔧 Xử lý sự cố

### Lỗi: "Không tìm thấy Piper TTS"

**Nguyên nhân**: Piper chưa được cài đặt hoặc không có trong PATH

**Giải pháp**:
1. Kiểm tra Piper đã được cài đặt: `piper --version`
2. Nếu chưa có, cài đặt theo hướng dẫn trong [INSTALLATION.md](INSTALLATION.md)

### Lỗi: "Không tìm thấy file config model"

**Nguyên nhân**: Thiếu file `.onnx.json`

**Giải pháp**:
1. Đảm bảo bạn đã tải cả 2 file:
   - `en_US-lessac-medium.onnx`
   - `en_US-lessac-medium.onnx.json`
2. Cả 2 file phải ở cùng thư mục và có cùng tên

### Lỗi: "Timeout khi tạo âm thanh"

**Nguyên nhân**: Văn bản quá dài hoặc hệ thống chậm

**Giải pháp**:
1. Chia nhỏ văn bản trong trường nguồn
2. Xử lý từng lô thẻ nhỏ hơn

### Add-on không hiển thị trong menu

**Nguyên nhân**: Add-on chưa được cài đặt đúng hoặc Anki chưa khởi động lại

**Giải pháp**:
1. Khởi động lại Anki
2. Kiểm tra **Tools** → **Add-ons** xem add-on có trong danh sách không
3. Nếu có lỗi, nhấn **View** để xem log

## 🎨 Các Model Giọng nói đề xuất

### Tiếng Anh Mỹ
- **en_US-lessac-medium.onnx**: Giọng nam, chất lượng cao (Khuyên dùng)
- **en_US-amy-medium.onnx**: Giọng nữ, tự nhiên
- **en_US-libritts_r-medium.onnx**: Giọng đa dạng

### Tiếng Anh Anh
- **en_GB-alan-medium.onnx**: Giọng nam British
- **en_GB-alba-medium.onnx**: Giọng nữ British

### Model chất lượng cao khác
- **Tải tại**: https://github.com/rhasspy/piper/blob/master/VOICES.md

**💡 Mẹo**: Model "medium" cân bằng tốt giữa chất lượng và tốc độ. Model "low" nhanh hơn nhưng chất lượng thấp hơn.

## 📊 Hiệu suất

- **Tốc độ**: ~2-5 thẻ/giây (phụ thuộc vào độ dài văn bản và CPU)
- **Model size**:
  - Low: ~5-10 MB
  - Medium: ~20-50 MB
  - High: ~50-100 MB
- **RAM usage**: ~100-500 MB (phụ thuộc vào model)

## 🤝 Đóng góp

Nếu bạn muốn đóng góp cho dự án:

1. Fork repository
2. Tạo branch mới: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add some feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Tạo Pull Request

## 📝 Changelog

### Version 1.0.0 (2024-01-XX)
- ✨ Release đầu tiên
- ⚡ Xử lý hàng loạt thẻ với hiệu suất cao
- 🎙️ Tích hợp Piper TTS
- 📊 Progress bar hiển thị tiến độ
- 💾 Lưu cấu hình tự động

## 📄 License

MIT License - Xem file LICENSE để biết chi tiết

## 🙏 Credits

- **Piper TTS**: https://github.com/rhasspy/piper
- **Anki**: https://apps.ankiweb.net/

## 📧 Liên hệ & Hỗ trợ

- **Issues**: Báo lỗi tại GitHub Issues
- **Discussions**: Thảo luận tại GitHub Discussions
- **Email**: [Thêm email của bạn]

---

**Chúc bạn học tập hiệu quả với Anki! 🎓**
