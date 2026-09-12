# 📄 02-deep-dive-report.md — Problem Deep-Dive & Evaluation Report
**Dự án:** Vin Smart Future — AI Co-pilot Điều Phối Cứu Hộ Sạc Pin Xanh SM (GSM)  
**Đơn vị phát triển:** Vin Smart Future (Vingroup)  

---

# 🏗️ Phase 3 — DEEP-DIVE: Báo Cáo Phân Tích Sâu

## 3.1. Current-State Workflow Mapping
**Mô tả chi tiết quy trình xử lý sự cố hết pin thủ công của Xanh SM:**

![Sơ đồ quy trình hiện tại](04-workflow-diagram.png)

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Bước 1       │     │ Bước 2       │     │ Bước 3       │     │ Bước 4       │
│ Nhận cuộc    │ ──> │ Tra định vị  │ ──> │ Tra trạm sạc │ ──> │ Soạn tin nhắn│
│ gọi sự cố    │     │ GPS xe       │     │ VinFast còn  │     │ hướng dẫn /  │
│              │     │              │     │ trụ trống 🔴 │     │ cứu hộ 🔴    │
│ Ai: Dispatch │     │ Ai: Dispatch │     │ Ai: Dispatch │     │ Ai: Dispatch │
│ ⏱ 2 phút     │     │ ⏱ 2 phút     │     │ ⏱ 5 phút     │     │ ⏱ 5 phút     │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                      │
                                                                      ▼
                                                               ┌──────────────┐
                                                               │ Bước 5       │
                                                               │ Gọi xe cứu   │
                                                               │ hộ nếu cần   │
                                                               │ Ai: Dispatch │
                                                               │ ⏱ 2 phút     │
                                                               └──────────────┘
```
* 🔴 **Bottleneck 1:** Bước 3 — Tra cứu thủ công trụ sạc VinFast còn trống trong bán kính phù hợp (mất 5 phút).
* 🔴 **Bottleneck 2:** Bước 4 — Gõ tin nhắn hướng dẫn/chỉ đường thủ công gửi qua App tài xế (mất 5 phút).
* 🔄 **Handoff:** Chuyển thông tin từ Tài xế $\rightarrow$ Dispatcher $\rightarrow$ Hệ thống tra cứu trạm sạc $\rightarrow$ Tài xế/Đội cứu hộ.
* **Tổng thời gian vận hành trung bình:** **16 phút / lượt xử lý sự cố**.

---

## 3.2. Problem Statement (6-field) & Metrics

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | Điều phối viên trung tâm (Dispatcher) thuộc Khối Vận hành Xanh SM (GSM). |
| **2. Current Workflow** | Đọc cuộc gọi/log sự cố $\rightarrow$ Tra GPS xe $\rightarrow$ Tra cứu trạm sạc VinFast còn trống thủ công $\rightarrow$ Soạn SMS/Chat hướng dẫn hoặc gọi xe cứu hộ. |
| **3. Bottleneck** | Bước tra cứu thủ công tình trạng trụ sạc khả dụng và gõ tin nhắn chỉ đường mất 10-12 phút/lượt, gây quá tải nặng nề giờ cao điểm. |
| **4. Business Impact** | Tăng 300% thời gian xe nằm chờ cạn pin trên đường, rủi ro gây tắc nghẽn giao thông, làm trễ chuyến đón khách tiếp theo, giảm doanh thu xe. |
| **5. Success Metric** | 90% các yêu cầu xử lý sự cố sạc pin được AI tự động tra cứu và dự thảo tin nhắn chỉ đường/lệnh cứu hộ trong **dưới 15 giây** (thay vì 16 phút). |
| **6. Operational Boundary** | AI chỉ được phép đóng vai trò Co-pilot **soạn thảo nháp (`[DRAFT_ONLY]`)** cho Dispatcher duyệt trước khi gửi. Khi pin < 5%, AI **tuyệt đối không được chỉ đường trạm > 5km** mà phải kích hoạt lệnh xe sạc di động (`dispatch_mobile_charger`). |

---

## 3.3. Future-State Flow & AI Fit
* **Xác định mức AI Fit (AI-Fit Matrix):** `[x] LLM Feature (Co-pilot hỗ trợ điều phối)`

**Future-State Workflow (Quy trình tương lai có AI):**
* 🔵 **AI Step 1:** AI tự động đọc GPS + dung lượng pin % $\rightarrow$ Truy vấn API trạm sạc VinFast khả dụng gần nhất.
* 🔵 **AI Step 2:** AI áp dụng Ranh giới an toàn (Pin < 5% $\rightarrow$ Phát lệnh `dispatch_mobile_charger`; Pin $\ge$ 5% $\rightarrow$ Soạn sẵn tin nhắn chỉ đường trạm sạc).
* 🔵 **AI Step 3:** AI xuất ra câu trả lời kèm thẻ `[DRAFT_ONLY]` gửi tới màn hình Dispatcher dưới 3 giây.
* 🟢 **Human Step (HITL):** Dispatcher kiểm tra nhanh tin nháp trên màn hình và ấn nút **Approve (Phê duyệt)** hoặc chỉnh sửa nhẹ.
* ↩️ **Fallback Step:** Nếu LLM API gặp sự cố ngắt kết nối (Timeout/Offline), hệ thống tự động chuyền ticket về quy trình Dispatcher xử lý thủ công truyền thống.

---

# 💻 Phase 4 — TECHNICAL PROMPT PROTOTYPE

*Đã hoàn tất kiểm thử thành công tại file [`starter-code/prompt_prototype.py`](starter-code/prompt_prototype.py) với 100% Assertion Passed (Rule 1 & Rule 2).*

---

# 🏁 Phase 5 — EVALUATE: Đánh Giá & Quyết Định

### AI Readiness Checklist:
1. [x] Chúng tôi có sẵn dữ liệu mẫu/logs sạch để test? (Có log GPS và vị trí trạm sạc VinFast).
2. [x] Rủi ro khi AI sai có nằm trong tầm kiểm soát (qua HITL hoặc Fallback)? (Có thẻ `[DRAFT_ONLY]` bắt buộc Dispatcher duyệt).
3. [x] Stakeholders sẵn sàng thay đổi quy trình làm việc cũ? (Khối Vận hành GSM ủng hộ giảm tải cho Dispatcher).

### Quyết định cuối cùng của Ban Giám Đốc Vin Smart Future:
[x] **GO (Bắt đầu xây dựng Prototype):** Bắt đầu phát triển với scope hẹp.
[ ] **NOT YET (Cần tích lũy thêm dữ liệu/xác lập baseline)**
[ ] **NO-GO (Không khả thi / Rule-based tốt hơn)**

**Justification (Lý giải quyết định dựa trên bằng chứng kỹ thuật và chi phí):**
> Dự án đạt tiêu chí GO vì:
> 1. Giải quyết đúng điểm nghẽn thực địa (giảm thời gian từ 16 phút xuống 15 giây).
> 2. Rủi ro vận hành được cô lập hoàn toàn nhờ cơ chế Human-in-the-loop (`[DRAFT_ONLY]`) và quy tắc an toàn khi pin < 5%.
> 3. Bản mẫu kỹ thuật (`prompt_prototype.py`) đã chạy kiểm thử thực tế trên Gemini API đạt kết quả 100% chính xác.
