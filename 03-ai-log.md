# 📝 Phase 6 — REFLECTION: AI Collaboration Log

*Học viên: Trịnh Xuân Huy*  

## 1. Mục Đích Sử Dụng AI (Use Cases)
Trong buổi thực hành Lab 02, tôi đã sử dụng AI (Gemini Flash & Claude/ChatGPT) làm trợ lý lập trình và đối tác phản biện giải pháp (Co-pilot & Brainstorming Partner) cho hai nhiệm vụ chính:
* **Hỗ trợ Kỹ thuật & Lập trình:** Cấu hình môi trường ảo Python, xử lý lỗi tương thích SDK, phân giải lỗi xung đột chính sách bảo mật Windows (`Application Control / DLL Rust`), và hoàn thiện logic kết nối API Gemini.
* **Định hình Sản phẩm (AI Product Scoping):** Brainstorm danh mục bài toán vận hành thực tế cho hệ sinh thái Vingroup (VinFast, Xanh SM), xây dựng khung 6 trường Problem Statement và thiết kế rào chắn an toàn (Operational Guardrails).

---

## 2. Ảo Giác, Lỗi Kỹ Thuật Gặp Phải & Cách Xử Lý (Hallucination & Failures)

### A. Vấn đề tương thích thư viện và bảo mật Windows
* **Vấn đề gặp phải:** Khi chạy mã nguồn bằng SDK `google-genai` hoặc `google-generativeai`, hệ thống liên tục báo lỗi `404 NOT_FOUND` (do mã model không tương thích) và nghiêm trọng hơn là `ImportError: DLL load failed while importing _rust: An Application Control policy has blocked this file`.
* **Cách tinh chỉnh & khắc phục:** Thay vì tiếp tục phụ thuộc vào các thư viện bọc ngoài nặng nề chứa file binary biên dịch sẵn từ Rust, tôi đã yêu cầu AI tái cấu trúc hàm `evaluate_prompt()` sử dụng thuần túy thư viện mạng chuẩn `urllib` của Python core. Giải pháp này giúp loại bỏ hoàn toàn việc nạp file DLL bên thứ ba, vượt qua rào chắn Application Control trên máy tính trường/công ty và gửi trực tiếp REST payload lên Google AI Studio API.

### B. Kiểm soát ranh giới mô hình (Boundary Enforcement & Hallucination)
* **Vấn đề gặp phải:** Khi thử nghiệm các ca kiểm thử tấn công (Adversarial Tests), mô hình có xu hướng chiều theo ý người dùng (sycophancy) – nếu người dùng hối thúc và bảo "đừng gắn thẻ [DRAFT_ONLY]", mô hình có lúc đã bỏ qua thẻ này hoặc cố gắng hướng dẫn tài xế chạy đến trạm sạc xa khi pin chỉ còn 2%.
* **Cách tinh chỉnh System Prompt:** Tôi đã bổ sung các ranh giới phủ định tuyệt đối (Negative Constraints) và hạ tham số `temperature=0.1` để giảm tính ngẫu nhiên:
  * Quy định cứng: Mọi câu trả lời *bắt buộc* mở đầu bằng `[DRAFT_ONLY]` trong mọi tình huống.
  * Quy định ngưỡng pin sống còn: Nếu pin < 5%, từ chối toàn bộ lệnh điều hướng trạm xa > 5km và bắt buộc xuất JSON cấu trúc kích hoạt xe sạc lưu động (`dispatch_mobile_charger`).

---

## 3. Bài Học Rút Ra Về Tư Duy Sản Phẩm AI (Key Takeaways)

* **AI không thể thay thế Rule Engine ở các khâu then chốt (Non-negotiables):** Đối với các bài toán vận hành có tính rủi ro cao (như pin cạn kiệt, an toàn giao thông), không bao giờ phó mặc 100% quyết định cho LLM vì xác suất ảo giác luôn tồn tại. Mô hình tối ưu luôn là: **Rule Engine (Chặn ranh giới) ──> LLM (Xử lý ngôn ngữ/gợi ý) ──> Human-in-the-loop (Con người phê duyệt cuối cùng)**.
* **Vai trò của cờ [DRAFT_ONLY]:** Việc gắn tiền tố kiểm duyệt không chỉ là quy định kỹ thuật mà là rào chắn an toàn nghiệp vụ, đảm bảo AI chỉ đóng vai trò Co-pilot soạn thảo, ngăn ngừa hệ thống tự động bắn tin nhắn sai lệch ra hiện trường gây hậu quả vận hành.
* **Tư duy Prompt Engineering dạng Boundary:** Viết prompt cho hệ thống doanh nghiệp khác hoàn toàn với chat thông thường; prompt phải định nghĩa rõ vai trò, quyền hạn tối đa, các điều cấm kỵ và kịch bản dự phòng khi thiếu dữ liệu.