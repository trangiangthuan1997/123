# 📖 Hướng Dẫn Cài Đặt Đầy Đủ - Piper TTS Add-on

Hướng dẫn này bao gồm TẤT CẢ các bước cần thiết để cài đặt và chạy add-on từ đầu.

---

## 📋 Tổng Quan

Add-on này tạo âm thanh tự động cho flashcards Anki bằng Piper TTS.

**Cần cài đặt:**
1. ✅ Anki (25.09.2 hoặc mới hơn)
2. ✅ Piper TTS (binary)
3. ✅ Model giọng nói Piper (.onnx)
4. ✅ Add-on này

**Thời gian cài đặt:** ~10-15 phút

---

## 🚀 BƯỚC 1: Cài Đặt Piper TTS

### Windows (Khuyên dùng - Đơn giản nhất)

#### 1.1. Tải Piper Binary

1. Truy cập: https://github.com/rhasspy/piper/releases/latest
2. Tìm và tải: **`piper_windows_amd64.zip`**
3. Giải nén vào thư mục, ví dụ: `C:\piper\`

Sau khi giải nén, bạn sẽ có:
```
C:\piper\
  ├── piper.exe
  ├── espeak-ng-data\ (folder)
  └── các file .dll
```

#### 1.2. Thêm Piper vào PATH

**Cách A: Copy vào System32 (Dễ nhất - Khuyên dùng)**

1. Mở folder `C:\piper\`
2. **Copy TẤT CẢ** file và folder
3. Paste vào: `C:\Windows\System32\`
4. Xong! ✅

**Cách B: Thêm vào Environment Variable**

1. Nhấn `Win + R`, gõ: `sysdm.cpl`, Enter
2. Tab **Advanced** → **Environment Variables**
3. Trong **System variables**, tìm `Path` → **Edit**
4. **New** → Nhập: `C:\piper`
5. **OK** → **OK** → **OK**
6. **Khởi động lại Command Prompt**

#### 1.3. Kiểm Tra Piper Đã Cài Đặt

1. Mở **Command Prompt** (Win + R → `cmd`)
2. Gõ:
   ```cmd
   piper --version
   ```
3. Nếu thấy version number (ví dụ: `1.2.0`) → ✅ **Thành công!**
4. Nếu lỗi `'piper' is not recognized...` → Quay lại bước 1.2

---

## 📥 BƯỚC 2: Tải Model Giọng Nói

### 2.1. Tải Model

1. Truy cập: https://github.com/rhasspy/piper/releases/latest
2. Scroll xuống **Assets**
3. Tải **2 files** này (Giọng Anh-Mỹ chất lượng cao):

   **File 1:** `voice-en-us-lessac-medium.onnx` (~35 MB)

   **File 2:** `voice-en-us-lessac-medium.onnx.json` (~5 KB)

   ⚠️ **QUAN TRỌNG**: Phải tải CẢ HAI files!

### 2.2. Lưu Model

1. Tạo thư mục: `C:\piper_models\`
2. Copy 2 files vừa tải vào đó
3. Kết quả:
   ```
   C:\piper_models\
     ├── voice-en-us-lessac-medium.onnx
     └── voice-en-us-lessac-medium.onnx.json
   ```

### 2.3. Test Model

Mở Command Prompt và chạy:
```cmd
echo Hello world | piper --model C:\piper_models\voice-en-us-lessac-medium.onnx --output_file C:\test.wav
```

Nếu file `C:\test.wav` được tạo và phát được âm thanh → ✅ **Thành công!**

---

## 📦 BƯỚC 3: Cài Đặt Add-on

### 3.1. Lấy Code Add-on

**Cách 1: Download từ GitHub**

1. Vào: https://github.com/[your-repo]/anki-piper-tts
2. **Code** → **Download ZIP**
3. Giải nén

**Cách 2: Clone Repository**

```cmd
git clone https://github.com/[your-repo]/anki-piper-tts.git
```

### 3.2. Copy Vào Anki

1. Mở Anki
2. **Tools** → **Add-ons** → **View Files**
3. Một folder sẽ mở ra (ví dụ: `C:\Users\...\Anki2\addons21\`)
4. **Copy folder `anki_piper_tts`** vào đây
5. Kết quả:
   ```
   C:\Users\[user]\AppData\Roaming\Anki2\addons21\
     └── anki_piper_tts\
         ├── __init__.py
         ├── config_dialog.py
         ├── piper_tts_engine.py
         ├── config.json
         ├── manifest.json
         └── các file khác...
   ```

### 3.3. Khởi Động Lại Anki

1. **Đóng Anki hoàn toàn** (check Task Manager, không còn anki.exe)
2. **Mở lại Anki**
3. Kiểm tra: **Tools** → **Add-ons** → Tìm "Piper TTS - Chèn Âm thanh Siêu tốc"
4. Nếu thấy → ✅ **Add-on đã cài thành công!**

---

## ⚙️ BƯỚC 4: Cấu Hình & Sử Dụng

### 4.1. Chuẩn Bị Note Type

**Tạo hoặc chỉnh sửa Note Type với 2 trường:**

1. **Tools** → **Manage Note Types**
2. Chọn note type (hoặc **Add** để tạo mới)
3. **Fields** → Đảm bảo có 2 fields:
   - `English` - Chứa từ/câu tiếng Anh
   - `Audio` - Chứa âm thanh

### 4.2. Tạo Âm Thanh Cho Thẻ

#### Bước 1: Chọn Thẻ
1. Mở **Browser** (Ctrl + B hoặc **Browse**)
2. **Chọn các thẻ** bạn muốn thêm âm thanh (có thể chọn nhiều thẻ)

#### Bước 2: Chạy Add-on
1. Menu **Edit** → **Tạo âm thanh (Piper)**
2. Hoặc chuột phải vào thẻ → **Tạo âm thanh (Piper)**

#### Bước 3: Cấu Hình

Dialog cấu hình sẽ hiện ra với 4 phần:

**1. Chọn Note Type**
- Chọn note type của bạn (ví dụ: "Basic", "Cloze", etc.)

**2. Chọn Trường (Fields)**
- **Trường nguồn**: `English` (chứa văn bản)
- **Trường đích**: `Audio` (chứa âm thanh)

**3. Chọn Model Giọng nói**
- Nhấn **Browse**
- Chọn: `C:\piper_models\voice-en-us-lessac-medium.onnx`
- Add-on sẽ ghi nhớ cho lần sau

**4. Tùy chọn**
- ☐ **Ghi đè lên âm thanh đã có**: Bỏ trống nếu chỉ tạo cho thẻ chưa có âm thanh
- ☑ **Ghi đè lên âm thanh đã có**: Chọn nếu muốn tạo lại tất cả
- **Tốc độ đọc**: `2.0x` (chậm 50% - dễ nghe) hoặc tùy chỉnh:
  - `1.0x` = Bình thường
  - `2.0x` = Chậm gấp đôi (50% tốc độ)
  - `0.5x` = Nhanh gấp đôi (200% tốc độ)

#### Bước 4: Bắt Đầu
1. Nhấn **Bắt đầu**
2. Progress bar sẽ hiển thị tiến độ
3. Đợi cho đến khi hoàn thành
4. Thông báo kết quả sẽ hiện:
   ```
   Hoàn thành!

   Đã xử lý: 50 thẻ
   Đã bỏ qua: 0 thẻ
   Lỗi: 0 thẻ
   ```

### 4.3. Kiểm Tra Kết Quả

1. Trong Browser, click vào một thẻ đã xử lý
2. Field **Audio** sẽ có: `[sound:piper_tts_xxxxx.wav]`
3. Click **Preview** hoặc review thẻ để nghe âm thanh

---

## 🔧 Xử Lý Sự Cố

### Lỗi: "Không tìm thấy Piper TTS"

**Nguyên nhân**: Piper chưa cài đặt hoặc không có trong PATH

**Giải pháp**:
1. Mở Command Prompt
2. Gõ: `piper --version`
3. Nếu lỗi → Quay lại **BƯỚC 1** và làm lại

### Lỗi: "Không tìm thấy file config model"

**Nguyên nhân**: Thiếu file `.onnx.json`

**Giải pháp**:
1. Kiểm tra folder `C:\piper_models\`
2. Phải có CẢ HAI files:
   - `voice-en-us-lessac-medium.onnx`
   - `voice-en-us-lessac-medium.onnx.json`
3. Nếu thiếu → Tải lại từ **BƯỚC 2**

### Lỗi: "File âm thanh không được tạo"

**Giải pháp**:
1. Test Piper thủ công (xem 2.3)
2. Nếu test thủ công OK → Update add-on code
3. Nếu test thủ công lỗi → Cài lại Piper

### Màn hình đen (CMD) nhấp nháy liên tục

**Giải pháp**: Đảm bảo bạn dùng **version mới nhất** của add-on (đã fix)

### Tốc độ đọc không thay đổi

**Giải pháp**:
1. Chọn lại thẻ
2. **BẬT** "Ghi đè lên âm thanh đã có"
3. Chạy lại với tốc độ mới
4. File mới sẽ được tạo

---

## 📊 Models Giọng Nói Khác

Nếu muốn thử giọng khác, tải từ: https://github.com/rhasspy/piper/releases

### Tiếng Anh Mỹ
| Model | Giọng | Chất lượng | Kích thước |
|-------|-------|-----------|-----------|
| `voice-en-us-lessac-medium` | Nam | Cao | ~35 MB |
| `voice-en-us-amy-medium` | Nữ | Cao | ~30 MB |
| `voice-en-us-ryan-medium` | Nam | Cao | ~40 MB |
| `voice-en-us-lessac-high` | Nam | Rất cao | ~80 MB |

### Tiếng Anh Anh
| Model | Giọng | Chất lượng |
|-------|-------|-----------|
| `voice-en-gb-alan-medium` | Nam British | Cao |
| `voice-en-gb-alba-medium` | Nữ British | Cao |

⚠️ **Lưu ý**: Luôn tải CẢ HAI files (`.onnx` và `.onnx.json`)!

---

## 💡 Tips & Tricks

### Tip 1: Xử Lý Nhiều Thẻ Cùng Lúc
- Add-on xử lý rất nhanh (~2-5 thẻ/giây)
- Có thể chọn hàng nghìn thẻ một lúc
- Progress bar cho biết tiến độ

### Tip 2: Tùy Chỉnh Tốc Độ
- Học từ mới: Dùng `2.0x` (chậm, dễ nghe)
- Review: Dùng `1.0x` hoặc `0.8x` (bình thường)
- Nghe nhanh: Dùng `0.5x` (nhanh gấp đôi)

### Tip 3: Cache File
- Cùng text + model + tốc độ → Dùng lại file cũ (nhanh)
- Đổi model hoặc tốc độ → Tạo file mới

### Tip 4: Dọn Dẹp
Xóa file âm thanh không dùng:
```
C:\Users\[user]\AppData\Roaming\Anki2\Người dùng 1\collection.media\
```
Tìm và xóa các file: `piper_tts_*.wav` không cần thiết

---

## 📁 Cấu Trúc Thư Mục Hoàn Chỉnh

Sau khi cài đặt xong, bạn sẽ có:

```
C:\piper\                          ← Piper binary
  ├── piper.exe
  └── espeak-ng-data\

C:\piper_models\                   ← Models
  ├── voice-en-us-lessac-medium.onnx
  └── voice-en-us-lessac-medium.onnx.json

C:\Users\[user]\AppData\Roaming\Anki2\
  └── addons21\
      └── anki_piper_tts\         ← Add-on
          ├── __init__.py
          ├── config_dialog.py
          ├── piper_tts_engine.py
          └── ...
```

---

## ✅ Checklist Cài Đặt

In hoặc lưu checklist này:

- [ ] Tải Piper binary (`piper_windows_amd64.zip`)
- [ ] Giải nén vào `C:\piper\`
- [ ] Copy vào `C:\Windows\System32\` hoặc thêm vào PATH
- [ ] Test: `piper --version` → Thành công
- [ ] Tải 2 files model (`.onnx` và `.onnx.json`)
- [ ] Lưu vào `C:\piper_models\`
- [ ] Test model: Tạo được file `test.wav`
- [ ] Copy folder `anki_piper_tts` vào Anki addons
- [ ] Restart Anki
- [ ] Thấy add-on trong Tools → Add-ons
- [ ] Tạo Note Type với fields "English" và "Audio"
- [ ] Test add-on với 1-2 thẻ
- [ ] Thành công! 🎉

---

## 🆘 Liên Hệ & Hỗ Trợ

- **GitHub Issues**: [Link đến repo của bạn]
- **Piper Documentation**: https://github.com/rhasspy/piper
- **Anki Forums**: https://forums.ankiweb.net/

---

## 📝 Version Info

- **Add-on Version**: 1.0.0
- **Anki Version**: 25.09.2+
- **Python**: 3.9+
- **Piper**: 1.2.0+

---

**Chúc bạn học tập hiệu quả với Anki! 🎓**

Lưu file này lại để sau này cài đặt lại dễ dàng!
