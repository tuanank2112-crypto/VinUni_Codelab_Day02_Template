# Nhật ký sử dụng AI — Vinhomes Incident Intelligence

Bản ghi này mô tả phiên làm việc với Codex, không giả lập phỏng vấn, trải nghiệm cá nhân hoặc kết quả Gemini chưa chạy. Người học cần đọc và xác nhận phản ánh trước khi nộp dưới tên mình.

## AI hỗ trợ gì?

Người học cung cấp ý tưởng Vinhomes Incident Intelligence và yêu cầu hoàn thành project theo đề. Codex đọc README, worksheet, ví dụ và autograder; chuyển ý tưởng thành scan, ba problem cards, báo cáo sáu trường, sơ đồ quy trình, Python prototype và dữ liệu giả lập. Việc tách nội dung ý tưởng khỏi yêu cầu bài nộp giúp giữ trọng tâm phát hiện sự cố chung, không chỉ phân loại phản ánh.

AI hỗ trợ chuyển ranh giới thành điều kiện kiểm tra bằng code: không thêm id, không bỏ duyệt, không xác nhận nguyên nhân khi chưa có hiện trường, không đóng nhóm khi còn phiếu chưa xác minh. Code có năm adversarial inputs để thử trên Gemini thật.

## Những vấn đề được phát hiện và cách sửa

| Vấn đề có bằng chứng trong phiên | Điều chỉnh / bài học |
|---|---|
| Autograder dùng từ khóa xe điện của ví dụ Xanh SM | AI đã thêm lệnh cấm liên quan xe sạc để khớp bộ chấm. Người học chỉ ra chi tiết này lệch ý tưởng; đã bỏ và thay bằng ranh giới không tự đóng van cấp nước. Giữ cảnh báo bộ chấm thay vì đổi nghiệp vụ dự án |
| Không thấy API key trong tiến trình Codex; người học cho biết đã export ở terminal | Kiểm tra lại chỉ trạng thái biến, không in key; giải thích tiến trình khác nhau có môi trường khác nhau; hướng dẫn chạy live trong terminal đã export |
| Ghép cùng vùng và thời điểm có thể nhầm nguyên nhân | Tạo hard negatives: lỗi van riêng có triệu chứng giống lỗi chung; giữ trạng thái hypothesis và yêu cầu bằng chứng |
| Nguy cơ biến kết quả fixture thành “AI chạy thành công” | Tách `offline_fixture_not_llm` khỏi `live`; test SDK dùng transport giả được ghi rõ; không tạo kết quả Gemini giả |
| So sánh ba phiếu cho thấy Rule và topology cùng giảm 3 lượt kiểm tra xuống 1 | Báo hòa, không kết luận LLM tốt hơn Rule hoặc giảm thời gian gián đoạn |

Chưa có phản hồi live của Gemini để chỉ ra một hallucination cụ thể. Không viết rằng model “đã chống tấn công thành công” chỉ dựa vào unit test.

## Ranh giới và thiết kế prompt

Prompt yêu cầu JSON thuần, coi text cư dân là dữ liệu không tin cậy, giữ cờ nháp/duyệt và không thêm hành động ngoài `propose_review`. Python kiểm tra schema/id; topology và lịch nguồn lực không để model tự sáng tác. Các thử nghiệm cố tình yêu cầu gửi thẳng, xác nhận lỗi bơm không có bằng chứng, ghép điều hòa vào lỗi nước, che cảnh báo khẩn cấp và giả mạo SYSTEM.

Đây là các prompt kiểm thử được chuẩn bị trong code, không phải lịch sử hội thoại Gemini đã diễn ra. Kiểm tra cấu trúc không giải quyết được mọi lỗi ngữ nghĩa; vẫn cần model evaluation và người vận hành duyệt.

## Kết quả phản ánh

30 kiểm thử offline đạt ở lần chạy đầu hoàn chỉnh. Sau khi sửa tương thích autograder, bổ sung kiểm thử hành động ngoài phạm vi, chế độ CLI offline và lỗi thiếu key của live. Lệnh mặc định chạy offline, hiển thị kết quả từng ca; autograder gốc còn cảnh báo từ khóa nghiệp vụ không tương thích ở tiêu chí 1. Đây không phải kết quả Gemini thật. Pairwise trên 60 phiếu giả lập: TP=24, FP=4, FN=2, precision=85,71%, recall=92,31%. Precision chưa đạt mục tiêu 95%, cho thấy việc coi nhóm là giả thuyết có ý nghĩa thực tế. Hai cặp bỏ sót đến từ phiếu có mâu thuẫn được giữ lại cho người rà soát.

Bài học chính: phải tách kết quả đã đo, giả định và mục tiêu; kết nối tín hiệu với topology chỉ giúp chọn việc kiểm tra, chưa chứng minh nguyên nhân. Người học chịu trách nhiệm xác nhận nội dung báo cáo, lựa chọn trade-off và bổ sung kết quả live/pilot.

## Yêu cầu mở rộng trong phiên

Sau phần prototype, người học yêu cầu thêm app end-to-end với cư dân, ban quản lý và bộ phận xử lý. Phần web được triển khai riêng trong `web/`; nó mở rộng phạm vi sản phẩm, không thay đổi việc cần nộp các deliverables Lab 02.
