# 🔍 Phase 1 — SCAN (Cá nhân, 20 min)

Hãy sử dụng **4 Lenses** dưới đây để quét qua hoạt động vận hành của các công ty thành viên Vingroup. Ghi lại **ít nhất 5 bài toán/bottleneck** thực tế.

### 4 Lenses tìm bài toán AI cho Vingroup:
1. **Lặp lại (Repetitive):** Tác vụ lặp đi lặp lại nhiều lần hằng ngày. (Ví dụ: So khớp hóa đơn sạc điện tại VinFast, route lại chuyến taxi tại Xanh SM).
2. **Tốn thời gian (Time-consuming):** Tác vụ ngốn thời gian xử lý thủ công của nhân viên. (Ví dụ: Soạn thảo phản hồi đánh giá 1-star của cư dân Vinhomes).
3. **AI có thể tốt hơn (AI-upgrade):** Dịch vụ khách hàng hiện tại còn chậm hoặc phản hồi rập khuôn. (Ví dụ: Chatbot CSKH Vinpearl hỗ trợ đặt vé vui chơi).
4. **Pain từ người khác (Stakeholder Pain):** Bottleneck khiến khách hàng hoặc nhân viên thực địa phàn nàn. (Ví dụ: Tài xế Xanh SM phàn nàn về việc hệ thống gợi ý điểm đón khách không chính xác).

> [!TIP]
> **🤖 AI Prompts — Partner brainstorm:**
> Hãy sử dụng prompt sau để brainstorm các bài toán thực tế nếu bạn chưa có ý tưởng:
> *"Tôi là AI Engineer tại Vin Smart Future (Vingroup). Tôi đang tìm kiếm các pain point vận hành cụ thể có thể tối ưu bằng AI cho mảng [Chọn một: VinFast / Xanh SM / Vinhomes / Vinmec]. Hãy gợi ý cho tôi 5 quy trình nghiệp vụ thủ công, tốn nhiều thời gian và gây rò rỉ hiệu suất kèm con số thống kê ước tính về tổn thất."*

### 📝 List bài toán của tôi:
| # | Subsidiary (VinFast/Xanh SM...) | Lens | Mô tả ngắn bài toán |
|---|----------------------------------|------|---------------------|
| 1 | Xanh SM         | Repetitive / Stakeholder Pain  | Tự động phân loại, kiểm tra định vị GPS và điều phối xe sạc cứu hộ lưu động khi xe EV của tài xế báo pin khẩn cấp (< 5%).|
| 2 | VinFast| Time-consuming |Bóc tách log lỗi viễn thông (CAN bus log / Telematics) từ xe gửi về trạm bảo dưỡng để gợi ý sẵn danh mục linh kiện thay thế cho kỹ thuật viên. |
| 3 |Vinhomes | Repetitive / Stakeholder Pain| Tiếp nhận, phân loại và draft câu trả lời xử lý khiếu nại của cư dân (tiếng ồn, rò rỉ nước, hỏng điều hòa hành lang) trên app Vinhomes Resident.|
| 4 | Vinpearl| AI-upgrade|Hỗ trợ lập lịch trình cá nhân hóa và giải đáp tự động đa ngôn ngữ về combo vé, khu vui chơi VinWonders và Safari. |
| 5 |Vinmec | Time-consuming|Tóm tắt hồ sơ tiền sử bệnh án và kết quả xét nghiệm cận lâm sàng của bệnh nhân trước khi bác sĩ bắt đầu ca khám chuyên khoa. |

---

# 🃏 Phase 2 — QUICK-ASSESS (Cá nhân, 30 min)

Chọn **top 3 bài toán** từ danh sách trên và hoàn thiện **3 Quick Problem Cards** dưới đây (10 phút/card).


┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #01                                      │
│                                                             │
│ Bài toán (1 câu): Tự động điều phối xe sạc pin cứu hộ       │
│ lưu động khi xe Xanh SM rơi vào tình trạng pin cạn kiệt.    │
│ Công ty thành viên: [ ] VinFast  [x] Xanh SM  [ ] Vinhomes  │
│                     [ ] Vinmec   [ ] Khác                   │
│                                                             │
│ Ai đang đau (Actor)? Tài xế Xanh SM (nguy cơ nằm đường)     │
│ và Điều phối viên tổng đài (quá tải xác minh vị trí).       │
│                                                             │
│ Workflow thủ công hiện tại (3-5 bước):                      │
│   1. Xe báo pin < 5% ──> 2. Tài xế gọi hotline ──>          │
│   3. ĐTV tra cứu trạm sạc gần nhất/xe cứu hộ trên bản đồ ──>│
│   4. Gọi điện điều xe sạc lưu động xuất phát                │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 3 (⏱ 8-12 phút/lượt)  │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2 & 3 (Tự động   │
│ phân tích telemetry pin, tọa độ và draft lệnh điều phối).   │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│   Thời gian phản hồi và điều xe cứu hộ từ 15 min ──> under   │
│   3 min; tỷ lệ xe cạn pin phải cẩu kéo giảm 60%.            │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [ ] LLM  [x] Agent │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #02                                      │
│                                                             │
│ Bài toán (1 câu): Bóc tách DTC error log của xe điện        │
│ để chuẩn bị linh kiện trước khi xe vào xưởng dịch vụ.        │
│ Công ty thành viên: [x] VinFast  [ ] Xanh SM  [ ] Vinhomes  │
│                     [ ] Vinmec   [ ] Khác                   │
│                                                             │
│ Ai đang đau (Actor)? Cố vấn dịch vụ và Kỹ thuật viên sửa    │
│ chữa tại VinFast Service Workshop.                          │
│                                                             │
│ Workflow thủ công hiện tại (3-5 bước):                      │
│   1. Xe gửi mã lỗi DTC về hệ thống ──> 2. Cố vấn đọc log    │
│   thủ công ──> 3. Tra sổ tay kỹ thuật tra cứu linh kiện ──> │
│   4. Kiểm tra tồn kho và đặt phụ tùng thay thế              │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2 & 3 (⏱ 25 phút/xe)   │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2 & 3 (Phân tích │
│ log lỗi, đối chiếu sổ tay kỹ thuật và draft danh mục part). │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│   Giảm thời gian chẩn đoán ban đầu từ 25 min ──> under 3 min│
│   tăng tỷ lệ phụ tùng có sẵn đúng hẹn từ 70% lên 92%.       │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #03                                      │
│                                                             │
│ Bài toán (1 câu): Phân loại và tự động draft phản hồi các   │
│ ticket khiếu nại, phản ánh cơ sở hạ tầng của cư dân.        │
│ Công ty thành viên: [ ] VinFast  [ ] Xanh SM  [x] Vinhomes  │
│                     [ ] Vinmec   [ ] Khác                   │
│                                                             │
│ Ai đang đau (Actor)? Đội ngũ Chăm sóc khách hàng & Ban Quản │
│ lý tòa nhà Vinhomes.                                        │
│                                                             │
│ Workflow thủ công hiện tại (3-5 bước):                      │
│   1. Cư dân gửi phản ánh lên app ──> 2. CSKH đọc và phân    │
│   loại thủ công ──> 3. Chuyển tiếp kỹ thuật/vệ sinh ──>     │
│   4. Soạn tin nhắn phản hồi tiến độ cho cư dân              │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2 & 4 (⏱ 10 phút/lượt)│
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2 & 4 (Phân tích │
│ mức độ khẩn cấp, gán tag phòng ban và draft tin phản hồi).  │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│   Thời gian phản hồi lần đầu (First Response Time) giảm     │
│   từ 45 min ──> under 5 min; độ hài lòng cư dân (CSAT) > 90%│
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
> [!TIP]
> **🤖 AI Prompts — Stress-Test thẻ bài toán:**
> Hãy dán nội dung thẻ bài toán của bạn vào LLM để nhận phản biện:
> *"Đây là một thẻ bài toán vận hành tôi đề xuất cho Vin Smart Future: [Dán nội dung]. Hãy đóng vai trò là một CFO và Trưởng phòng Vận hành cực kỳ khắt khe, chỉ ra cho tôi 3 điểm yếu về logic, metric, và giải thích vì sao rule-based code thông thường có thể giải quyết bài toán này tốt hơn là dùng AI."*

---