# 🏗️ Phase 3 — DEEP-DIVE (Nhóm, 85 min)

## 3.2. Problem Statement (6-field) & Metrics (15 min)
Điền đầy đủ 6 trường thông tin của bài toán:

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | Chủ xe điện cá nhân (VinFast VF5, VF8, VF9), tài xế dịch vụ Xanh SM và Đội ngũ hỗ trợ vận hành hạ tầng trạm sạc VinFast. |
| **2. Current Workflow** | Xem danh sách trạm trên app ──> Tự lọc cổng sạc và kiểm tra trụ trống thủ công ──> Tự ước lượng lộ trình và mức tiêu hao pin ──> Lái xe đến trạm. |
| **3. Bottleneck** | Thiếu cơ chế đề xuất thông minh theo ngữ cảnh: Không tự động khớp loại cổng/công suất phù hợp với từng dòng xe, không dự đoán được tình trạng quá tải/trụ trống theo thời gian thực khi xe đang trên đường tới. |
| **4. Business Impact** | Gây tâm lý "lo âu về cự ly/pin" (range anxiety) cho người dùng xe điện; gây dồn ứ cục bộ tại một số trạm sạc trọng điểm trong khi các trạm lân cận còn trống; giảm chỉ số hài lòng khách hàng (CSAT) đối với hệ sinh thái xe điện VinFast. |
| **5. Success Metric** | Giảm thời gian tìm kiếm và chọn trạm sạc từ 8 phút xuống dưới 30 giây.Tỷ lệ gợi ý trạm sạc chính xác cổng tương thích và còn chỗ trống đạt > 95%.Tối ưu hóa hiệu suất sử dụng trạm sạc toàn mạng lưới, giảm 35% thời gian chờ đợi tại các trụ sạc cao điểm. |
| **6. Operational Boundary** | Được phép: Đọc mức pin hiện tại, dòng xe, chuẩn cổng sạc, tọa độ điểm đến để gợi ý top 3 trạm sạc tối ưu và lập lộ trình dừng nạp.TUYỆT ĐỐI không: Không tự động can thiệp khóa cổng/đặt trước chỗ khi người dùng chưa đồng ý; không đề xuất trạm sạc vượt quá quãng đường xe có thể di chuyển với dung lượng pin còn lại (kèm hệ số an toàn 15%).Điểm cần duyệt (Gatekeeper): Mọi lộ trình hoặc trạm sạc gợi ý phải gắn cờ [DRAFT_ONLY] và yêu cầu tài xế bấm "Xác nhận dẫn đường" trên màn hình ô tô. |

## 3.3. Future-State Flow & AI Fit (25 min)
Lựa chọn: [x] LLM Feature kết hợp Rule Engine

Lý do: Khâu lọc phần cứng (chuẩn cổng sạc CCS2, công suất trạm, bán kính pin an toàn) bắt buộc phải dùng Rule Engine để đảm bảo chính xác 100%. Khâu lập lịch trình phức tạp (tối ưu dừng nghỉ theo thói quen lái, phân tích ngôn ngữ tự nhiên từ câu lệnh giọng nói của tài xế) do LLM xử lý.
* **Vẽ Future-State Flow:** Đánh dấu rõ:
  [Tài xế yêu cầu dẫn đường / Xe báo Pin < 20%]
                    │
                    ▼
[Rule Engine: Lọc cứng theo Dòng xe & Chuẩn cổng]
(Ví dụ: VF8 ──> Lọc trạm có súng sạc CCS2 >= 150kW)
                    │
                    ▼
🔵 AI Step (LLM Planner)
(Đọc tình trạng trụ trống thời gian thực,
tính toán quãng đường, gắn nhãn [DRAFT_ONLY],
soạn gợi ý lộ trình kèm thời gian sạc ước tính)
                    │
                    ▼
🟢 Human Step (HITL)
(Tài xế bấm nút "Chấp nhận Lộ trình" trên màn hình xe)
                    │
                    ▼
[Hệ thống kích hoạt Navigation & Đặt trước slot sạc]
---