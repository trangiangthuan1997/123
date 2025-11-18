# Hướng Dẫn Cài Đặt Add-on Chèn Ảnh Tự Động

## Cài lần đầu

### Bước 1: Cài Anki
- Download tại: https://apps.ankiweb.net/
- Cài version 25.09.2 trở lên

### Bước 2: Cài thư viện Python (chỉ 2 thư viện)
Mở **Command Prompt** (cmd) và chạy:

```cmd
"C:\Users\admin\AppData\Local\AnkiProgramFiles\.venv\Scripts\pip.exe" install requests Pillow
```

**Lưu ý:** Nếu báo lỗi, thêm `--break-system-packages` vào cuối lệnh.

### Bước 3: Copy folder add-on vào Anki
Copy folder **`anki_image_inserter`** vào đây:
```
C:\Users\admin\AppData\Roaming\Anki2\addons21\
```

Kết quả:
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

### Bước 4: Khởi động lại Anki
Đóng Anki hoàn toàn, mở lại là xong!

---

## Cài lại sau khi format Windows

### Cách 1: Từ backup (NHANH NHẤT)

**Trước khi format, backup 2 folder này:**
1. Add-on: `C:\Users\admin\AppData\Roaming\Anki2\addons21\anki_image_inserter\`
2. Data Anki: `C:\Users\admin\AppData\Roaming\Anki2\` (nếu muốn giữ thẻ cũ)

**Sau khi format:**
1. Cài Anki
2. Chạy lệnh cài thư viện (bước 2 ở trên)
3. Copy 2 folder backup vào đúng vị trí
4. Restart Anki → Xong!

### Cách 2: Từ Git

1. Cài Anki
2. Chạy lệnh cài thư viện (bước 2 ở trên)
3. Vào: https://github.com/trangiangthuan1997/123
4. Chọn branch: `claude/anki-addon-image-insertion-011CUow3ML6VWL2iyfANN48k`
5. Click **Code → Download ZIP**
6. Giải nén, copy folder `anki_image_inserter` vào `addons21`
7. Restart Anki → Xong!

---

## Cách dùng

1. Mở Anki → **Browse** (Ctrl+Shift+B)
2. Chọn các thẻ cần thêm ảnh
3. **Chuột phải → Add Images to Cards**
4. Chờ add-on chạy xong

**Kết quả:** Mỗi thẻ sẽ có 6 ảnh, layout 3 cột đẹp mắt.

---

## Cấu hình (nếu cần)

**Tools → Add-ons → anki_image_inserter → Config**

```json
{
    "source_field": "English",      // Field chứa từ vựng
    "target_field": "Image",        // Field sẽ chèn ảnh vào
    "images_per_card": 6            // Số ảnh mỗi thẻ (mặc định: 6)
}
```

Đổi `"English"` và `"Image"` thành tên field của bạn nếu khác.

---

## Xử lý lỗi

### Lỗi: "pip is not recognized..."
Dùng lệnh này thay thế:
```cmd
python -m pip install requests Pillow
```

Hoặc:
```cmd
py -m pip install requests Pillow
```

### Add-on không chạy / báo lỗi thiếu thư viện
Chạy lại lệnh cài thư viện:
```cmd
"C:\Users\admin\AppData\Local\AnkiProgramFiles\.venv\Scripts\pip.exe" install requests Pillow --break-system-packages
```

### Add-on không xuất hiện trong menu
1. Kiểm tra folder name phải đúng là `anki_image_inserter`
2. Kiểm tra có file `__init__.py` bên trong không
3. Restart Anki

### Chèn sai số lượng ảnh / báo lỗi "UnboundLocalError"
Code cũ chưa update. Download code mới nhất từ Git (commit `4fb610c`)

---

## Thông tin version

**Version hiện tại:** 1.0 (2025-01-18)
- ✅ Chèn đúng 6 ảnh mỗi thẻ
- ✅ Tốc độ nhanh: 3-5 giây/thẻ
- ✅ Không cần API key (dùng Google Images miễn phí)
- ✅ Layout responsive 3 cột

**Repository:** https://github.com/trangiangthuan1997/123
**Branch:** `claude/anki-addon-image-insertion-011CUow3ML6VWL2iyfANN48k`

---

## Tóm tắt nhanh

**3 bước cài đặt:**
1. Cài Anki
2. Chạy: `pip install requests Pillow`
3. Copy folder `anki_image_inserter` vào `addons21`

**Khi format Windows:**
- Backup folder `anki_image_inserter` ra USB/Cloud
- Sau khi cài lại, copy vào lại là xong!

Hết! Đơn giản vậy thôi! 🎉
