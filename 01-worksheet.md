# Lab 02 — Worksheet: AI Product Scoping (Vin Smart Future)

---

## 🏛️ 1. Bối cảnh thực tế: Vin Smart Future (Vingroup)

**Vingroup** — Tập đoàn tư nhân lớn nhất Việt Nam — vừa sáp nhập toàn bộ các phòng ban công nghệ thuộc các công ty thành viên thành một đơn vị công nghệ thống nhất mang tên **Vin Smart Future**. 

Nhiệm vụ của **Vin Smart Future** là xây dựng các giải pháp AI, số hóa, và tự động hóa cốt lõi để nâng cao hiệu suất vận hành và trải nghiệm khách hàng xuyên suốt các công ty thành viên:
* 🚗 **VinFast:** Hệ thống xe điện thông minh (EV), trợ lý AI ảo trong xe, dự đoán bảo trì pin, và quản lý chuỗi cung ứng sản xuất.
* 🚕 **Xanh SM (GSM):** Vận hành đội xe taxi/xe máy điện thông minh, điều vận thông minh (Smart Dispatching), tối ưu hóa lộ trình di chuyển.
* 🏢 **Vinhomes:** Quản lý đô thị thông minh (Smart Cities), trợ lý cư dân thông minh, tối ưu hóa mức tiêu thụ năng lượng.
* 🏥 **Vinmec:** Y tế thông minh, chẩn đoán hình ảnh bằng AI, tối ưu hóa quản lý hồ sơ bệnh án.
* 🎢 **Vinpearl / VinWonders:** Trải nghiệm du lịch số hóa, quản lý phòng và luồng khách thông minh tại các khu vui chơi.

Trong buổi Lab hôm nay, nhóm của bạn sẽ đóng vai trò là **AI Product Engineer** tại **Vin Smart Future**, tiến hành tìm kiếm, scoping, phân tích độ khả thi, thiết lập ranh giới vận hành, và xây dựng một **bản mẫu kỹ thuật (prompt prototype)** cho một bài toán cụ thể thuộc một trong những mảng kinh doanh trên.

---

## 📊 2. Cơ cấu tính điểm bài lab

### 👥 Điểm nhóm (60 điểm)

| Gate | Điểm | Deliverable | Tiêu chí chấm |
|---|---:|---|---|
| **G1. Workflow Mapping** | 20 | Problem Deep-Dive | Vẽ chi tiết quy trình hiện tại: các bước, handoff, thời gian, bottleneck |
| **G2. Problem Statement** | 20 | Problem Deep-Dive | Problem Statement 6-field bám sát thực tế, metric có số và ranh giới rõ ràng |
| **G3. AI Fit & Future Flow** | 10 | Problem Deep-Dive | So sánh Rule vs LLM vs Agent, future flow có bước AI, ranh giới và Fallback |
| **G4. Decision Quality** | 10 | Problem Deep-Dive | Quyết định Go/Not Yet/No-Go trung thực và có chứng cứ rõ ràng |

### 👤 Điểm cá nhân (40 điểm)

| Gate | Điểm | Deliverable | Tiêu chí chấm |
|---|---:|---|---|
| **I1. Scan & Cards** | 15 | Quick Cards | Liệt kê 5 problems sử dụng 3 lenses, hoàn thiện 3 quick cards chất lượng |
| **I2. Prototyping** | 10 | 02-lab/ | Chạy thử nghiệm programmatic prompt prototype thành công |
| **I3. AI Log & Reflection** | 15 | 03-ai-log.md | Phản ánh trung thực về việc dùng AI làm thought-partner (giúp gì, sai gì, sửa gì) |

---

# 🚀 Phase 0 — worked Example: Xanh SM Intelligent Dispatcher (15 min)

*Giảng viên walk-through ví dụ thực tế từ Vin Smart Future để bạn hiểu rõ cách scoping một bài toán AI.*
Đọc chi tiết worked example tại file [02-deliverable-example.md](02-deliverable-example.md).

---

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
| 1 | **Xanh SM (GSM)** | Tốn thời gian | Điều phối viên xử lý thủ công các phản hồi khẩn cấp từ tài xế về sự cố cạn pin hoặc cứu hộ thực địa (mất 12-15 phút/lượt). |
| 2 | **VinFast** | Lặp lại | So khớp tự động hóa đơn dịch vụ sạc điện và đối chiếu dữ liệu giao dịch giữa các trạm sạc đối tác hằng tuần. |
| 3 | **Vinhomes** | AI-upgrade | Phân loại tự động và gợi ý phản hồi phản ánh/khiếu nại của cư dân trên App Vinhomes Resident (rút ngắn thời gian xử lý từ 12 tiếng xuống 15 phút). |
| 4 | **Vinmec** | Pain từ người khác | Bác sĩ mất quá nhiều thời gian đọc lịch sử bệnh án và gõ tóm tắt hồ sơ xuất viện (mất 20-30 phút/bệnh nhân, gây quá tải cho y bác sĩ). |
| 5 | **Vinpearl** | Tốn thời gian | Trợ lý CSKH tự động tư vấn lịch trình du lịch cá nhân hóa và đề xuất combo dịch vụ lưu trú / vé vui chơi VinWonders. |

---

# 🃏 Phase 2 — QUICK-ASSESS (Cá nhân, 30 min)

Chọn **top 3 bài toán** từ danh sách trên và hoàn thiện **3 Quick Problem Cards** dưới đây (10 phút/card).

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

> [!TIP]
> **🤖 AI Prompts — Stress-Test thẻ bài toán:**
> Hãy dán nội dung thẻ bài toán của bạn vào LLM để nhận phản biện:
> *"Đây là một thẻ bài toán vận hành tôi đề xuất cho Vin Smart Future: [Dán nội dung]. Hãy đóng vai trò là một CFO và Trưởng phòng Vận hành cực kỳ khắt khe, chỉ ra cho tôi 3 điểm yếu về logic, metric, và giải thích vì sao rule-based code thông thường có thể giải quyết bài toán này tốt hơn là dùng AI."*

---

# 🏗️ Phase 3 — DEEP-DIVE (Nhóm, 85 min)

## 3.1. Current-State Workflow Mapping (25 min)
**Mô tả chi tiết quy trình xử lý sự cố hết pin thủ công của Xanh SM:**

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

## 3.2. Problem Statement (6-field) & Metrics (15 min)

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | Điều phối viên trung tâm (Dispatcher) thuộc Khối Vận hành Xanh SM (GSM). |
| **2. Current Workflow** | Đọc cuộc gọi/log sự cố $\rightarrow$ Tra GPS xe $\rightarrow$ Tra cứu trạm sạc VinFast còn trống thủ công $\rightarrow$ Soạn SMS/Chat hướng dẫn hoặc gọi xe cứu hộ. |
| **3. Bottleneck** | Bước tra cứu thủ công tình trạng trụ sạc khả dụng và gõ tin nhắn chỉ đường mất 10-12 phút/lượt, gây quá tải nặng nề giờ cao điểm. |
| **4. Business Impact** | Tăng 300% thời gian xe nằm chờ cạn pin trên đường, rủi ro gây tắc nghẽn giao thông, làm trễ chuyến đón khách tiếp theo, giảm doanh thu xe. |
| **5. Success Metric** | 90% các yêu cầu xử lý sự cố sạc pin được AI tự động tra cứu và dự thảo tin nhắn chỉ đường/lệnh cứu hộ trong **dưới 15 giây** (thay vì 16 phút). |
| **6. Operational Boundary** | AI chỉ được phép đóng vai trò Co-pilot **soạn thảo nháp (`[DRAFT_ONLY]`)** cho Dispatcher duyệt trước khi gửi. Khi pin < 5%, AI **tuyệt đối không được chỉ đường trạm > 5km** mà phải kích hoạt lệnh xe sạc di động (`dispatch_mobile_charger`). |

---

## 3.3. Future-State Flow & AI Fit (25 min)
* **Xác định mức AI Fit (AI-Fit Matrix):** `[x] LLM Feature (Co-pilot hỗ trợ điều phối)`

**Future-State Workflow (Quy trình tương lai có AI):**
* 🔵 **AI Step 1:** AI tự động đọc GPS + dung lượng pin % $\rightarrow$ Truy vấn API trạm sạc VinFast khả dụng gần nhất.
* 🔵 **AI Step 2:** AI áp dụng Ranh giới an toàn (Pin < 5% $\rightarrow$ Phát lệnh `dispatch_mobile_charger`; Pin $\ge$ 5% $\rightarrow$ Soạn sẵn tin nhắn chỉ đường trạm sạc).
* 🔵 **AI Step 3:** AI xuất ra câu trả lời kèm thẻ `[DRAFT_ONLY]` gửi tới màn hình Dispatcher dưới 3 giây.
* 🟢 **Human Step (HITL):** Dispatcher kiểm tra nhanh tin nháp trên màn hình và ấn nút **Approve (Phê duyệt)** hoặc chỉnh sửa nhẹ.
* ↩️ **Fallback Step:** Nếu LLM API gặp sự cố ngắt kết nối (Timeout/Offline), hệ thống tự động chuyền ticket về quy trình Dispatcher xử lý thủ công truyền thống.

---

# 💻 Phase 4 — TECHNICAL PROMPT PROTOTYPE (Nhóm, 30 min)

*Đã hoàn tất kiểm thử thành công tại file [`starter-code/prompt_prototype.py`](starter-code/prompt_prototype.py) với 100% Assertion Passed (Rule 1 & Rule 2).*

---

# 🏁 Phase 5 — EVALUATE (Nhóm, 20 min)

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

---

# 📝 Phase 6 — REFLECTION (Cá nhân)
*Ghi nhận phản ánh của cá nhân bạn về việc phối hợp với AI trong buổi học hôm nay vào file `03-ai-log.md`.*
