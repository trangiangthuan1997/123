# Anki Image Inserter Add-on

Tự động chèn 6 ảnh minh họa vào thẻ từ vựng Anki, giúp ghi nhớ từ vựng hiệu quả hơn thông qua hình ảnh.

## Tính năng

✅ **Tự động tìm và chèn 6 ảnh** cho mỗi từ vựng
✅ **Google Images** làm nguồn chính (không cần API key)
✅ **Unsplash backup** nếu Google không đủ ảnh
✅ **Layout 3 cột responsive** tự động điều chỉnh trên mobile
✅ **Tối ưu tốc độ**: ~3-5 giây/thẻ
✅ **Tự động resize & compress**: 800x600px, JPEG 85%
✅ **Lọc ảnh thông minh**: Chặn quảng cáo, sản phẩm, text images

## Quick Start

### 1. Cài đặt dependencies

```bash
# Windows
cd "C:\Program Files\Anki"
python -m pip install requests Pillow beautifulsoup4

# macOS/Linux
python3 -m pip install requests Pillow beautifulsoup4
```

### 2. Cài đặt add-on

Copy folder `anki_image_inserter` vào:

- **Windows**: `C:\Users\<USER>\AppData\Roaming\Anki2\addons21\`
- **macOS**: `~/Library/Application Support/Anki2/addons21/`
- **Linux**: `~/.local/share/Anki2/addons21/`

### 3. Restart Anki

### 4. Sử dụng

1. Mở **Browse** (Ctrl+Shift+B)
2. Chọn thẻ cần thêm ảnh
3. **Right-click → Add Images to Cards**
4. Đợi add-on xử lý (progress bar hiển thị tiến trình)

## Cấu hình

**Tools → Add-ons → anki_image_inserter → Config**

```json
{
    "source_field": "English",      // Field chứa từ vựng
    "target_field": "Image",        // Field sẽ chèn ảnh
    "images_per_card": 6,           // Số ảnh mỗi thẻ

    "api_keys": {
        "unsplash": "",             // Unsplash API (khuyến nghị)
        "bing": "",                 // Bing API (tùy chọn)
        "pexels": "",               // Pexels API (tùy chọn)
        "pixabay": ""               // Pixabay API (tùy chọn)
    }
}
```

**Lưu ý:**
- Google Images **KHÔNG CẦN** API key (luôn hoạt động)
- Chỉ cần Unsplash API key để làm backup source
- Các API khác hoàn toàn tùy chọn

## Yêu cầu hệ thống

- Anki 25.09.2+
- Python 3.13.5+ (đi kèm Anki)
- Internet connection
- Windows 11 / macOS / Linux

## Hướng dẫn chi tiết

Xem file [INSTALLATION.md](./INSTALLATION.md) để biết:
- Hướng dẫn cài đặt từng bước
- Cách đăng ký API keys
- Xử lý lỗi thường gặp
- Backup và restore add-on

## Ví dụ

**Input:** Card với field "English" = "apple"

**Output:** 6 ảnh về "apple" được chèn vào field "Image" với layout:

```
┌─────────┬─────────┬─────────┐
│  Ảnh 1  │  Ảnh 2  │  Ảnh 3  │
├─────────┼─────────┼─────────┤
│  Ảnh 4  │  Ảnh 5  │  Ảnh 6  │
└─────────┴─────────┴─────────┘
```

## Changelog

### v1.0 (Latest) - 2025-01-18

✅ Fix: Chèn ĐÚNG 6 ảnh (hard limit tất cả APIs)
✅ Fix: UnboundLocalError với biến `re`
✅ Performance: Tối ưu tốc độ xuống 3-5s/thẻ
✅ Debug: Logging chi tiết ở mọi bước
✅ Layout: Responsive 3-column grid

**Breaking changes:**
- Tắt perceptual hash deduplication (tối ưu tốc độ)
- Skip logic tạm thời TẮT (để testing)

## Troubleshooting

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| `UnboundLocalError: 're'` | Code cũ | Update từ commit `4fb610c` |
| Chèn >6 ảnh | APIs trả về quá nhiều | Đã fix ở commit `27e1298` |
| Không tìm thấy ảnh | Google bị block | Thêm Unsplash API key |
| Quá chậm (>10s/thẻ) | Fetch quá nhiều nguồn | Chỉ dùng Google + Unsplash |

## API Sources

| Source | Status | API Key | Rate Limit |
|--------|--------|---------|------------|
| **Google Images** | ✅ Active | Không cần | Unlimited (scraper) |
| **Unsplash** | ✅ Backup | Cần | 50 requests/hour (free) |
| Bing | Tùy chọn | Cần | 1000/month (free) |
| Pexels | Tùy chọn | Cần | 200/hour (free) |
| Pixabay | Tùy chọn | Cần | 5000/hour (free) |

**Khuyến nghị:** Chỉ cần **Google + Unsplash** là đủ!

## Kỹ thuật

- **Threading**: QTimer (main thread) - tránh crash Anki
- **Image processing**: Pillow - resize 800x600, JPEG 85%
- **Deduplication**: URL-based (perceptual hash bị TẮT)
- **Filtering**: Multi-layer (size, aspect ratio, URL patterns)
- **Layout**: CSS Grid responsive
- **Error handling**: Try-catch với fallback

## Roadmap

- [ ] Re-enable skip logic (production)
- [ ] Add progress percentage
- [ ] Batch download optimization
- [ ] Custom image count per card
- [ ] Manual image selection UI
- [ ] Export/import settings

## License

MIT License

## Credits

Developed with Claude Code by Anthropic

## Support

- Issues: https://github.com/trangiangthuan1997/123/issues
- Branch: `claude/anki-addon-image-insertion-011CUow3ML6VWL2iyfANN48k`
