# 01 — Problem Scan (Vin Smart Future)

## Phase 1 — SCAN

Dùng 4 lenses quét vận hành các công ty thành viên Vingroup.

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|------------|------|---------------------|
| 1 | VinFast | AI có thể tốt hơn | Chủ xe VF5/VF8/VF9 tự tìm trạm trên app, dễ chọn nhầm cổng CCS2/GBT và chọn trạm ngoài tầm pin. |
| 2 | Xanh SM | Tốn thời gian | Dispatcher xử lý thủ công sự cố hết pin thực địa (tra trụ + soạn tin ~15 phút/lượt). |
| 3 | Vinhomes | Lặp lại | CSKH đọc tay phản ánh cư dân rồi forward sai BQL tòa, SLA phản hồi ~12 giờ. |
| 4 | Vinpearl | Pain từ người khác | Manager miss review khẩn (phòng bẩn, thái độ, mất đồ) trên OTA. |
| 5 | VinFast | Lặp lại | Đối chiếu hóa đơn sạc đối tác với log trụ sạc hằng tuần. |

---

## Phase 2 — 3 Quick Problem Cards

### Card #1 — Trợ lý hướng dẫn trạm sạc VinFast (đề xuất chốt)

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán: Tự động đề xuất lịch sạc và trạm trống đúng cổng  │
│ (CCS2/GBT) theo từng dòng VF5 / VF8 / VF9.                  │
│ Công ty thành viên: [x] VinFast                             │
│                                                             │
│ Ai đang đau? Chủ xe (và CSKH khi khách gọi hỏi đường sạc)   │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Khách hỏi “sạc ở đâu?” (app / chat / gọi)              │
│   → 2. Cung cấp dòng xe, % pin, vị trí, giờ cần xong        │
│   → 3. Tự lọc bản đồ trạm                                   │
│   → 4. Đoán cổng sạc + xem trụ trống                        │
│   → 5. Tự tính còn kịp lịch không                           │
│                                                             │
│ Bước nào tốn nhất? Bước 3–5 (⏱ 8–12 phút/lượt)              │
│ AI có thể nhảy vào? Sau khi rule lọc trạm hợp lệ — LLM nháp │
│ 1 lịch sạc + chỉ đường.                                     │
│                                                             │
│ Metric: 95% đúng cổng; ra lịch khả thi < 1 phút;            │
│         0 đề xuất ngoài tầm pin; 0 tự đặt trụ.              │
│                                                             │
│ Quick Architecture: [x] Rule  [x] LLM                       │
└─────────────────────────────────────────────────────────────┘
```

### Card #2 — Xanh SM sự cố pin thực địa

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán: Dispatcher tra trụ + soạn tin cứu hộ khi tài xế   │
│ hết pin giữa đường.                                         │
│ Công ty thành viên: [x] Xanh SM                             │
│                                                             │
│ Ai đang đau? Dispatcher (quá tải) + tài xế (chờ trên đường) │
│                                                             │
│ Workflow: gọi báo pin → tra GPS → tra trụ trống → soạn tin  │
│ → gọi cứu hộ nếu cần.                                       │
│                                                             │
│ Bottleneck: tra trụ + soạn tin (⏱ 10–15 phút/lượt)          │
│ AI vào: bước soạn tin / đề xuất cứu hộ (HITL duyệt)         │
│ Metric: 15 phút → dưới 3 phút                               │
│ Architecture: [x] LLM                                       │
└─────────────────────────────────────────────────────────────┘
```

### Card #3 — Vinhomes phân loại phản ánh cư dân

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán: Ticket app bị đọc tay, forward sai bộ phận.       │
│ Công ty thành viên: [x] Vinhomes                            │
│                                                             │
│ Ai đang đau? CSKH / BQL tòa + cư dân chờ lòng vòng          │
│                                                             │
│ Workflow: gửi app → CSKH đọc → đoán loại → forward BQL      │
│ → soạn phản hồi.                                            │
│                                                             │
│ Bottleneck: phân loại + soạn phản hồi (⏱ 15–30 phút/ticket) │
│ AI vào: phân loại sự cố, gán tòa, nháp phản hồi             │
│ Metric: 80% gán đúng bộ phận lần đầu; 12h → dưới 2h         │
│ Architecture: [x] LLM                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Quyết định lựa chọn

Chốt **Card #1 — Trợ lý hướng dẫn trạm sạc VinFast**.

- Card #2 gần bài mẫu lab (cứu hộ real-time), không phải “lên lịch sạc chủ động”.
- Card #3 rủi ro tranh chấp phí / căn hộ, cần HITL pháp lý nặng hơn.
- Card #1 đủ AI-upgrade, metric đo được, ranh giới an toàn rõ (đúng cổng, tầm pin, `[DRAFT_ONLY]`).
