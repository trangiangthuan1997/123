# Hướng dẫn cài đặt Add-on Anki Image Inserter

## Yêu cầu hệ thống

- **Anki**: Version 25.09.2 trở lên
- **Python**: 3.13.5 (đi kèm với Anki)
- **Hệ điều hành**: Windows 11 / macOS / Linux

## Các bước cài đặt

### Bước 1: Cài đặt Anki

1. Download Anki từ: https://apps.ankiweb.net/
2. Cài đặt phiên bản mới nhất (25.09.2+)

### Bước 2: Cài đặt Python Dependencies

Add-on cần các thư viện Python sau:
- `requests` - Download ảnh từ internet
- `Pillow` - Xử lý ảnh (resize, compress)
- `beautifulsoup4` - Parse HTML từ Google Images

**Cách cài:**

#### Windows:
```bash
# Mở Command Prompt (cmd) hoặc PowerShell
cd "C:\Program Files\Anki"
python -m pip install requests Pillow beautifulsoup4
```

#### macOS/Linux:
```bash
# Mở Terminal
python3 -m pip install requests Pillow beautifulsoup4
```

**Lưu ý:** Nếu Anki đã cài sẵn các thư viện này, bạn có thể bỏ qua bước này.

### Bước 3: Cài đặt Add-on

#### Cách 1: Từ Git Repository (Recommended)

1. Download code từ repository:
   ```
   https://github.com/trangiangthuan1997/123
   Branch: claude/anki-addon-image-insertion-011CUow3ML6VWL2iyfANN48k
   ```

2. Copy folder `anki_image_inserter` vào thư mục add-ons của Anki:

   **Windows:**
   ```
   C:\Users\<TÊN_USER>\AppData\Roaming\Anki2\addons21\
   ```

   **macOS:**
   ```
   ~/Library/Application Support/Anki2/addons21/
   ```

   **Linux:**
   ```
   ~/.local/share/Anki2/addons21/
   ```

3. Cấu trúc thư mục sau khi copy:
   ```
   addons21/
   └── anki_image_inserter/
       ├── __init__.py
       ├── card_processor.py
       ├── image_api.py
       ├── image_processor.py
       ├── ui_dialog.py
       ├── config.json
       └── manifest.json
   ```

#### Cách 2: Từ backup file

Nếu bạn đã backup folder `anki_image_inserter`, chỉ cần copy vào thư mục `addons21`.

### Bước 4: Cấu hình Add-on (Tùy chọn)

1. Mở Anki
2. **Tools → Add-ons → anki_image_inserter → Config**
3. Cấu hình các tùy chọn:

```json
{
    "source_field": "English",      // Tên field chứa từ vựng
    "target_field": "Image",        // Tên field sẽ chèn ảnh vào
    "images_per_card": 6,           // Số ảnh mỗi thẻ (MẶC ĐỊNH: 6)

    "api_keys": {
        "bing": "",                 // API key Bing (tùy chọn)
        "unsplash": "",             // API key Unsplash (tùy chọn)
        "pexels": "",               // API key Pexels (tùy chọn)
        "pixabay": ""               // API key Pixabay (tùy chọn)
    }
}
```

**Lưu ý:**
- **Google Images** (web scraper) luôn hoạt động, KHÔNG CẦN API key
- Các API khác là TÙY CHỌN, giúp tăng nguồn ảnh
- **Unsplash** sẽ được dùng làm backup nếu Google không đủ ảnh

### Bước 5: Đăng ký API Keys (Tùy chọn)

Nếu muốn sử dụng nhiều nguồn ảnh hơn:

#### Unsplash (Recommended - backup source)
1. Đăng ký tại: https://unsplash.com/developers
2. Tạo app mới
3. Copy **Access Key** vào config

#### Bing Image Search
1. Đăng ký Azure: https://azure.microsoft.com/
2. Tạo **Bing Search v7 API**
3. Copy **Key** vào config

#### Pexels
1. Đăng ký tại: https://www.pexels.com/api/
2. Copy **API Key** vào config

#### Pixabay
1. Đăng ký tại: https://pixabay.com/api/docs/
2. Copy **API Key** vào config

### Bước 6: Khởi động lại Anki

1. Đóng Anki hoàn toàn
2. Mở lại Anki
3. Kiểm tra add-on: **Tools → Add-ons** → Phải thấy **anki_image_inserter**

## Cách sử dụng

### Thêm ảnh vào thẻ

1. Trong Anki, vào **Browse** (Ctrl+Shift+B)
2. Chọn các thẻ cần thêm ảnh
3. **Right-click → Add Images to Cards**
4. Add-on sẽ tự động:
   - Tìm 6 ảnh cho mỗi từ vựng
   - Download và resize ảnh
   - Chèn vào field "Image" với layout 3 cột

### Lưu ý
- Add-on sẽ **BỎ QUA** các thẻ đã có ảnh (hiện tại tính năng này đang TẮT để test)
- Tốc độ: ~3-5 giây/thẻ với Google Images
- Ảnh sẽ được resize về 800x600px, JPEG 85% quality

## Xử lý lỗi thường gặp

### Lỗi: "cannot access local variable 're'"
- **Nguyên nhân:** Code cũ chưa update
- **Fix:** Xem hướng dẫn ở commit `4fb610c`

### Lỗi: "No images found"
- **Nguyên nhân:** Google bị block hoặc không tìm thấy ảnh
- **Fix:**
  - Kiểm tra kết nối internet
  - Thêm Unsplash API key làm backup

### Lỗi: "Too many images (>6)"
- **Nguyên nhân:** Đã fix ở commit `27e1298`
- **Fix:** Update code mới nhất

### Add-on không xuất hiện trong menu
- **Fix:**
  1. Kiểm tra folder name: phải là `anki_image_inserter`
  2. Kiểm tra có file `__init__.py` không
  3. Restart Anki

## Backup Add-on

Để backup add-on (đề phòng cài lại Windows):

1. Copy toàn bộ folder:
   ```
   C:\Users\<TÊN_USER>\AppData\Roaming\Anki2\addons21\anki_image_inserter\
   ```

2. Lưu vào USB/Cloud (Google Drive, OneDrive, etc.)

3. Khi cài lại Windows:
   - Cài Anki
   - Cài Python dependencies
   - Copy folder backup vào `addons21`
   - Restart Anki

## Cập nhật Add-on

Khi có phiên bản mới:

1. Download code mới từ Git
2. **Backup config cũ** (Tools → Add-ons → Config → Copy)
3. Xóa folder `anki_image_inserter` cũ
4. Copy folder mới vào
5. Paste config cũ vào
6. Restart Anki

## Liên hệ & Hỗ trợ

- **Repository:** https://github.com/trangiangthuan1997/123
- **Branch:** claude/anki-addon-image-insertion-011CUow3ML6VWL2iyfANN48k
- **Latest commit:** 4fb610c (FIX: UnboundLocalError)

## Changelog

### Version 1.0 (Latest)
- ✅ Fix: Chèn ĐÚNG 6 ảnh mỗi thẻ (hard limit tất cả APIs)
- ✅ Fix: UnboundLocalError với biến `re`
- ✅ Feature: Debug logging chi tiết
- ✅ Performance: ~3-5 giây/thẻ (chỉ dùng Google Images)
- ✅ Layout: 3-column responsive grid
- ✅ Deduplication: Tắt perceptual hash (tối ưu tốc độ)

### Known Issues
- Skip logic hiện đang TẮT (để test lại các thẻ)
- Sẽ BẬT lại trong phiên bản production

## License

MIT License - Free to use and modify
