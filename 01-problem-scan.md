# 📄 01-problem-scan.md — Problem Scanning & Quick Cards
**Khóa học:** Lab 02 — AI Product Scoping (Vin Smart Future)  
**Tác giả (Cá nhân):** AI Product Engineer  

---

# 🔍 Phase 1 — SCAN: Danh Sách 5 Bài Toán Vận Hành (Vingroup)

| # | Subsidiary (Công ty thành viên) | Lens | Mô tả ngắn bài toán |
|---|----------------------------------|------|---------------------|
| 1 | **Xanh SM (GSM)** | **Tốn thời gian** | Điều phối viên xử lý thủ công các phản hồi khẩn cấp từ tài xế về sự cố cạn pin hoặc cứu hộ thực địa (mất 12-15 phút/lượt). |
| 2 | **VinFast** | **Lặp lại** | So khớp tự động hóa đơn dịch vụ sạc điện và đối chiếu dữ liệu giao dịch giữa các trạm sạc đối tác hằng tuần. |
| 3 | **Vinhomes** | **AI-upgrade** | Phân loại tự động và gợi ý phản hồi phản ánh/khiếu nại của cư dân trên App Vinhomes Resident (rút ngắn thời gian xử lý từ 12 tiếng xuống 15 phút). |
| 4 | **Vinmec** | **Pain từ người khác** | Bác sĩ mất quá nhiều thời gian đọc lịch sử bệnh án và gõ tóm tắt hồ sơ xuất viện (mất 20-30 phút/bệnh nhân, gây quá tải cho y bác sĩ). |
| 5 | **Vinpearl** | **Tốn thời gian** | Trợ lý CSKH tự động tư vấn lịch trình du lịch cá nhân hóa và đề xuất combo dịch vụ lưu trú / vé vui chơi VinWonders. |

---

# 🃏 Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán: Tự động tra cứu trạm sạc & dự thảo chỉ dẫn/lệnh   │
│ cứu hộ cho tài xế Xanh SM báo cạn pin khẩn cấp.             │
│ Công ty thành viên: [ ] VinFast  [x] Xanh SM  [ ] Vinhomes  │
│                     [ ] Vinmec   [ ] Khác (Ghi rõ)________  │
│                                                             │
│ Ai đang đau (Actor)? Tài xế (chờ lâu), Dispatcher (quá tải) │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Nhận cuộc gọi ──> 2. Đọc GPS xe ──> 3. Tra trạm sạc còn trụ │
│   ──> 4. Soạn SMS chỉ đường ──> 5. Điều xe cứu hộ nếu pin < 5%│
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 3 & 4 (⏱ 10 phút/lượt) │
│ AI nhảy vào hỗ trợ ở bước nào? Bước 3 & 4 (Tự động đọc GPS, │
│ kiểm tra ranh giới pin < 5% & draft tin nhắn chỉ dẫn/cứu hộ)│
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│   Giảm thời gian xử lý sự cố từ 15 phút ──> dưới 2 phút/lượt│
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán: Phân loại tự động phản ánh cư dân và dự thảo nội  │
│ dung phản hồi chuẩn mực cho Ban quản lý tòa nhà Vinhomes.   │
│ Công ty thành viên: [ ] VinFast  [ ] Xanh SM  [x] Vinhomes  │
│                     [ ] Vinmec   [ ] Khác (Ghi rõ)________  │
│                                                             │
│ Ai đang đau (Actor)? Cư dân (chờ lâu), BQL tòa nhà (quá tải)│
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Cư dân gửi ticket trên App ──> 2. BQL đọc & phân loại   │
│   ──> 3. Chuyển kỹ thuật/vệ sinh ──> 4. Gõ phản hồi cư dân   │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2 & 4 (⏱ 45 phút/ticket)│
│ AI nhảy vào hỗ trợ ở bước nào? Bước 2 & 4 (Phân loại tự động│
│ đúng phòng ban & soạn nháp câu trả lời cho BQL duyệt)      │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│   Giảm thời gian phản hồi đầu tiên từ 12 tiếng ──> dưới 15 min│
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán: Tự động trích xuất thông tin bệnh án và dự thảo   │
│ văn bản tóm tắt hồ sơ xuất viện cho bác sĩ Vinmec duyệt.    │
│ Công ty thành viên: [ ] VinFast  [ ] Xanh SM  [ ] Vinhomes  │
│                     [x] Vinmec   [ ] Khác (Ghi rõ)________  │
│                                                             │
│ Ai đang đau (Actor)? Bác sĩ điều trị (quá tải gõ văn bản),  │
│                     Bệnh nhân (chờ thủ tục xuất viện lâu)   │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Quyết định xuất viện ──> 2. Đọc lại lịch sử bệnh án,   │
│   xét nghiệm ──> 3. Tự gõ tóm tắt xuất viện ──> 4. Ký duyệt  │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2 & 3 (⏱ 25 phút/bệnh nhân)│
│ AI nhảy vào hỗ trợ ở bước nào? Bước 2 & 3 (Gom dữ liệu EHR  │
│ và draft sẵn bản tóm tắt y khoa để bác sĩ kiểm tra & ký)    │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│   Giảm thời gian chuẩn bị hồ sơ xuất viện từ 25 min ──> 5 min│
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```
