# Vinhomes Incident Intelligence — Problem Scan

**Lab 02 · AI Product Scoping · Vin Smart Future**

Bối cảnh doanh nghiệp được sử dụng theo đề bài. Những quy trình, thời lượng và tác động dưới đây là **giả thuyết thiết kế**, không phải số liệu khảo sát hoặc tuyên bố về vận hành thực tế của doanh nghiệp. Ý tưởng gốc do người học cung cấp: kết nối phản ánh → xác minh sự cố chung → điều phối → kiểm chứng khắc phục.

## Phase 1 — SCAN bằng 4 lenses

| # | Subsidiary | Lens | Bài toán / bottleneck cần kiểm chứng |
|---|---|---|---|
| 1 | Vinhomes | Tốn thời gian; Stakeholder Pain | Nước yếu ở nhiều căn cùng nhánh nhưng phản ánh được xử lý riêng, làm chậm nhận diện sự cố chung và có thể gây kiểm tra trùng. |
| 2 | Vinhomes | Lặp lại | Điều phối viên liên tục đối chiếu ca trực, tay nghề, vật tư và lịch vào căn hộ khi phân việc hoặc khi kỹ thuật viên bận đột xuất. |
| 3 | Vinhomes | AI-upgrade; Stakeholder Pain | Cư dân nhận cập nhật khác nhau về cùng sự cố; ghi chú “kiểm tra lại ngày mai” có thể không trở thành nhiệm vụ theo dõi. |
| 4 | VinFast | Lặp lại | Nhân viên đối soát phiên sạc và hóa đơn có mã tham chiếu thiếu hoặc mô tả khác nhau; phải rà soát ngoại lệ thủ công. |
| 5 | Xanh SM | AI-upgrade | Mô tả điểm đón tự do khó đối chiếu với địa chỉ; điều phối phải hỏi lại tài xế và khách. |
| 6 | Vinpearl | Tốn thời gian | Nhân viên đọc email đặt phòng đoàn để trích ngày, số phòng, loại phòng và các điều kiện chưa rõ trước khi kiểm tra quỹ phòng. |

## Phase 2 — Ba Quick Problem Cards

### Card 1 — Phát hiện giả thuyết sự cố nước chung

| Trường | Nội dung |
|---|---|
| Bài toán, công ty | Vinhomes: phát hiện các phản ánh nước yếu/mất nước có thể cùng sự cố để kiểm tra đúng phạm vi. |
| Actor | Điều phối viên ban quản lý; kỹ thuật viên chịu kiểm tra trùng; cư dân chịu thời gian gián đoạn. |
| Workflow hiện tại (giả định) | 1. Tiếp nhận → 2. Chuẩn hóa phiếu → 3. Tìm phiếu/hạ tầng liên quan → 4. Phân công kiểm tra → 5. Xác minh và cập nhật. |
| Bottleneck | Bước 3: 8 phút/phiếu để đối chiếu triệu chứng, thời điểm, vùng cấp nước; khác cách diễn đạt dễ bỏ sót. |
| AI hỗ trợ | LLM trích xuất triệu chứng; Python đối chiếu topology và cửa sổ 15 phút; điều phối viên duyệt giả thuyết. |
| Metric có số | Mục tiêu pilot: thời gian rà soát trung vị 8 → ≤3 phút/phiếu; pairwise precision ≥95%, recall ≥85% trên tập kiểm thử chưa dùng điều chỉnh quy tắc. Chưa đạt/đo thực tế. |
| Quick Architecture | **LLM Feature + Rule**, không agent tự trị. |
| Dữ liệu / ranh giới | Phiếu ẩn danh, timestamp, topology có phiên bản; không kết luận cùng nguyên nhân chỉ vì cùng triệu chứng. |

### Card 2 — Đề xuất lịch kiểm tra khả thi

| Trường | Nội dung |
|---|---|
| Bài toán, công ty | Vinhomes: lập lại lịch kiểm tra khi nhân sự, vật tư hoặc lịch tiếp cận thay đổi. |
| Actor | Điều phối viên kỹ thuật; kỹ thuật viên nhận lịch; cư dân chờ tiếp cận căn hộ. |
| Workflow hiện tại (giả định) | 1. Nhận việc → 2. Tra kỹ năng/ca trực → 3. Gọi xác nhận vật tư và lịch cư dân → 4. Phân việc → 5. Điều chỉnh khi có thay đổi. |
| Bottleneck | Bước 2–4: giả định 10 phút/lần lập hoặc đổi lịch cho 3–5 công việc. |
| AI hỗ trợ | Python kiểm tra ràng buộc và đề xuất lịch; LLM chỉ chuẩn hóa ghi chú công việc, không tính toán thay bộ lập lịch. |
| Metric có số | Mục tiêu: 10 → ≤4 phút/lần lập lịch; 0 vi phạm chuyên môn/ca trực/tiếp cận; giảm ≥10% phút di chuyển so với FIFO trên cùng workload. |
| Quick Architecture | **Rule / thuật toán lập lịch** trước; LLM tùy chọn. |
| Dữ liệu / ranh giới | Ca trực, thời lượng, travel matrix, kho vật tư; lịch không khả thi phải báo điều phối thay vì ép phân công. |

### Card 3 — Soạn cập nhật và theo dõi sau sửa chữa

| Trường | Nội dung |
|---|---|
| Bài toán, công ty | Vinhomes: biến trạng thái đã duyệt và ghi chú kỹ thuật thành nháp thông báo cùng nhiệm vụ theo dõi. |
| Actor | CSKH ban quản lý; kỹ thuật viên; cư dân cần thông tin nhất quán. |
| Workflow hiện tại (giả định) | 1. Đọc ghi chú → 2. Hỏi lại kỹ thuật → 3. Soạn tin → 4. Duyệt/gửi → 5. Nhắc tái kiểm tra. |
| Bottleneck | Bước 1–3: giả định 6 phút/cập nhật; lời hẹn dễ không có người chịu trách nhiệm. |
| AI hỗ trợ | Trích nhiệm vụ còn mở; soạn nháp từ trạng thái được duyệt, phân biệt “đang kiểm tra” với “đã xác nhận”. |
| Metric có số | Mục tiêu: 6 → ≤2 phút/nháp; 100% hẹn theo dõi có chủ việc và hạn; 0 tin tự gửi hoặc tiết lộ dữ liệu hộ khác. |
| Quick Architecture | **LLM Feature + state machine + human review**. |
| Dữ liệu / ranh giới | Không tự hứa ETA, không dùng thông tin riêng của từng hộ trong thông báo chung, không tự đóng phiếu. |

## Lựa chọn và phản biện

Chọn **Card 1** làm trọng tâm; lấy một phần Card 2 để trình diễn kế hoạch kiểm tra và xác minh. Card 3 là hướng mở rộng, chưa xây chức năng gửi thông báo. Đây là một chuỗi quyết định có thể kiểm chứng trong scope hai tòa, thay vì ba sản phẩm độc lập.

- Nếu mô tả đã có mã lỗi chuẩn và topology đủ sạch, Rule có thể đạt chất lượng tương đương với chi phí thấp hơn. Vì vậy phải giữ baseline Rule, không mặc định LLM tốt hơn.
- Tiết kiệm lượt kiểm tra không đồng nghĩa giảm gián đoạn: kiểm tra chung sai có thể làm chậm xử lý lỗi trong từng căn. Đo cả ghép nhầm và thời gian chờ của phiếu bị giữ riêng.
- Chưa phỏng vấn ban quản lý và chưa đo 8 phút/phiếu. Đây là giả thuyết baseline cần quan sát tối thiểu 30 phiên xử lý; chưa dùng để tính ROI hoặc cam kết lợi ích.

Phân tích chi tiết: [02-deep-dive-report.md](02-deep-dive-report.md).
