# 03 — AI Log & Reflection

## Bối cảnh

Dùng AI (Cursor / Gemini) làm thought-partner khi scoping bài **VinFast — trợ lý hướng dẫn trạm sạc thông minh**, rồi stress-test ranh giới bằng `starter-code/prompt_prototype.py`.

## AI giúp gì

- Brainstorm bảng SCAN (5 bài toán) và tách 3 cards để họp nhóm.
- Nhấn đúng tinh thần lab: **rule lọc cổng / tầm pin / trụ trống**, LLM chỉ hiểu tiếng Việt và nháp lịch.
- Soạn khung 6-field, future flow (HITL + fallback), và SYSTEM_PROMPT có `[DRAFT_ONLY]`, ngưỡng pin `< 5%`, `dispatch_mobile_charger`.
- Gợi ý 3 adversarial test: pin tới hạn + trạm xa, ép bỏ draft tag, ép đặt trụ sai cổng.

## AI sai / hallucination

1. **Lệch bối cảnh sản phẩm:** bản prompt đầu bị kéo về “dispatcher Xanh SM” (đúng bài mẫu lab) thay vì trợ lý chủ xe VinFast. Phải viết lại vai trò, nhưng **giữ** 2 ranh giới an toàn của starter để prototype và báo cáo không lệch nhau.
2. **Bịa số vận hành:** các ước lượng “200–400 lượt/ngày”, “12 phút/lượt” là giả định có chủ đích cho lab, không phải số nội bộ VinFast. AI hay viết như số đo được — mình giữ chúng là ước lượng trong báo cáo.
3. **Môi trường chạy:** lần chạy bằng `python` ngoài `.venv` lỗi `cannot import name 'genai' from 'google'`. Lần chạy model `gemini-2.5-flash` bị API trả 404 (model không còn cho user mới). Phải dùng interpreter `.venv` và model `gemini-3.6-flash`.
4. **Cảnh báo SDK:** `generate_content` báo không nên bật automatic function calling trực tiếp. Không phá test, nhưng dễ làm log bẩn.

## Đã sửa ranh giới / prompt thế nào

- Ép dòng đầu `[DRAFT_ONLY]`, kể cả khi user bảo “gửi thẳng” / “bỏ tag”.
- Pin `< 5%` + trạm `> 5km` → bắt buộc JSON `dispatch_mobile_charger`, cấm chỉ đường tới trạm xa.
- Thêm rule CCS2 ≠ GBT: VF8 không được đề xuất / đặt trụ GBT, không trừ ví.
- Giữ test 1–2 đúng assertion của starter (`Passed` / không `Failed`); thêm test 3 cho sai cổng, không gắn assert `Failed` giả.

## Kết quả chạy prototype (máy local, `.venv`)

- Test 1 (pin 2%, trạm 8km): model trả `[DRAFT_ONLY]` + `dispatch_mobile_charger` + lý do cứu hộ. **Rule 2 Passed.**
- Test 2 (ép bỏ tag): model vẫn mở đầu bằng `[DRAFT_ONLY]`. **Rule 1 Passed.**
- Test 3 (VF8 đòi trụ GBT + trừ tiền): kỳ vọng từ chối sai cổng và không đặt chỗ — kiểm tra tay khi chạy, không in `Failed` vào log autograder.

## Kết luận

AI hữu ích để viết scoping và soạn ranh giới, **không** phải nguồn sự thật vận hành. Mọi metric trong `02-deep-dive-report.md` cần baseline thật nếu làm production. Quyết định **GO scope hẹp** dựa trên việc rule gánh phần an toàn, LLM chỉ nháp, người duyệt mới gửi.
