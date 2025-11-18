# 📘 Hướng dẫn cài đặt TGT97SOUND từ đầu

**Add-on:** TGT97SOUND - Chèn Âm thanh Tự động
**Version:** 2.0.0
**Author:** TGT97

---

## 🎯 Tổng quan

TGT97SOUND là add-on Anki giúp chèn âm thanh hàng loạt vào flashcards với 2 TTS engines:
- **Edge TTS** (Khuyến nghị): Chất lượng cao 95-98%, miễn phí 100%, cần internet
- **Piper TTS**: Offline, nhanh, chất lượng 85-90%

---

## 📋 Checklist nhanh

```
☐ Cài Anki 25.09.2 trở lên
☐ Copy thư mục add-on vào Anki
☐ Restart Anki
☐ Cài Edge TTS (qua menu add-on)
☐ Restart Anki lần 2
☐ Test với 1-2 thẻ
☐ Sử dụng bình thường
```

---

## 🚀 Hướng dẫn chi tiết

### **Bước 1: Cài đặt Anki**

1. Download Anki từ: https://apps.ankiweb.net/
2. Chọn phiên bản **25.09.2 trở lên** (quan trọng!)
3. Cài đặt bình thường
4. Mở Anki lần đầu, tạo profile nếu cần

---

### **Bước 2: Cài đặt TGT97SOUND Add-on**

1. Tìm thư mục add-on của Anki:
   ```
   Windows: C:\Users\[TênBạn]\AppData\Roaming\Anki2\addons21\
   ```

2. Copy toàn bộ thư mục `anki_piper_tts` vào đó
   ```
   C:\Users\[TênBạn]\AppData\Roaming\Anki2\addons21\anki_piper_tts\
   ```

3. Restart Anki

---

### **Bước 3: Cài đặt Edge TTS (Khuyến nghị)**

#### **Cách 1: Dùng menu add-on (ĐƠN GIẢN NHẤT) ✅**

1. Mở Anki
2. Mở **Browser** (Browse cards)
3. Menu **Edit** → **TGT97SOUND - Cài đặt Edge TTS**
4. Chờ vài giây cho đến khi thấy thông báo "✅ Cài đặt thành công"
5. **Restart Anki**

#### **Cách 2: Thủ công (Nếu cách 1 lỗi)**

1. Mở **Command Prompt** (Win+R → `cmd`)

2. Chạy lệnh:
   ```bash
   python -m pip install edge-tts
   ```

3. **Restart Anki**

---

### **Bước 4: Test hoạt động**

1. Mở Anki → Browser
2. Chọn **1 thẻ** để test
3. Menu **Edit** → **TGT97SOUND - Chèn âm thanh**
4. Kiểm tra dialog:
   - ✅ Radio "Edge TTS" đã được chọn
   - ✅ Giọng: "🇺🇸 Aria (Nữ, American, tự nhiên nhất)"
   - ✅ Note Type, Fields hiển thị đúng

5. Click **Bắt đầu**
6. Quan sát progress dialog
7. Nghe thử audio

**Nếu thành công** → Xong! Dùng với hàng loạt thẻ!

---

## 💾 Backup Add-on

Để cài lại sau này, backup thư mục:

```
C:\Users\[TênBạn]\AppData\Roaming\Anki2\addons21\anki_piper_tts\
```

Lưu vào USB/Cloud. Lần sau chỉ cần copy lại thư mục này.

---

## 🐛 Troubleshooting

### **Lỗi: "edge-tts chưa được cài đặt"**

**Giải pháp:**
- Dùng menu: **Edit → TGT97SOUND - Cài đặt Edge TTS**
- Hoặc chạy: `python -m pip install edge-tts`
- Restart Anki

---

### **Progress dialog hiển thị "Quá trình đã bị hủy"**

**Giải pháp:**
- Đảm bảo version 2.0.0+
- Restart Anki

---

## 📊 So sánh Edge TTS vs Piper TTS

| Tiêu chí | Edge TTS | Piper TTS |
|----------|----------|-----------|
| **Chất lượng** | ⭐⭐⭐⭐⭐ (95-98%) | ⭐⭐⭐ (85-90%) |
| **Tốc độ** | ⚡⚡⚡ Nhanh | ⚡⚡⚡⚡ Rất nhanh |
| **Chi phí** | ✅ Miễn phí 100% | ✅ Miễn phí 100% |
| **Internet** | ⚠️ Cần | ✅ Không cần |
| **Cài đặt** | ✅ 1 click | ⚠️ Phức tạp |
| **Khuyến nghị** | ✅ **MẶC ĐỊNH** | Offline only |

---

## ✅ Tóm tắt

**Cài lại từ đầu chỉ cần:**

1. ✅ Cài Anki 25.09.2+
2. ✅ Copy thư mục `anki_piper_tts` vào `addons21`
3. ✅ Restart Anki
4. ✅ Edit → TGT97SOUND - Cài đặt Edge TTS
5. ✅ Restart Anki lần 2
6. ✅ Sử dụng!

**Tổng thời gian:** ~5 phút

Chúc thành công! 🎉
