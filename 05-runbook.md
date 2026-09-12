# Chạy Vinhomes Incident Intelligence

## Bộ bài nộp Lab 02

- `01-problem-scan.md`: 6 cơ hội, 3 quick cards.
- `02-deep-dive-report.md`: workflow, problem statement, AI fit, evaluation.
- `03-ai-log.md`: nhật ký có phân biệt kiểm thử thật và giả lập.
- `04-workflow-diagram.png`: sơ đồ current state.
- `starter-code/prompt_prototype.py`: Gemini structured output và 5 adversarial inputs.

## Python prototype

Chạy tại thư mục gốc bằng Python 3.11 trở lên:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python starter-code/prompt_prototype.py --offline
python starter-code/incident_engine.py
python scripts/evaluate_groups.py
```

Lệnh đầu chạy unit tests, không gọi Gemini. Hai lệnh tiếp ghi `results/offline-demo.json` và `results/group-evaluation.json`. Tái tạo dữ liệu/sơ đồ bằng `python scripts/generate_data.py` và `python scripts/draw_workflow.py` (font Arial trên macOS hoặc DejaVu Sans trên Linux).

## Gemini thật

Trong **chính terminal** đã export `GEMINI_API_KEY` hoặc `GOOGLE_API_KEY`:

```bash
python starter-code/prompt_prototype.py --live
```

Mặc định không truyền cờ chạy kiểm thử offline, kể cả khi có API key; dùng `--live` để gọi Gemini thật. Biến export ở terminal khác không tự truyền sang tiến trình Codex. Không dán key vào code hoặc chat. Mặc định `gemini-2.5-flash` theo đề; biến `GEMINI_MODEL` cho phép đổi model nếu tài khoản không còn hỗ trợ model này. Kết quả live ghi `results/live-boundary-results.json`; exit 0 chỉ khi tất cả ca đạt. Lỗi model/API trả exit khác 0. Khi chạy `--live` chưa có key, exit 2 và không giả lập kết quả live.

## Kiểm tra bài nộp

```bash
python autograder/autograder.py --section-a
python autograder/autograder.py --section-b
```

Section A chỉ kiểm tra file có tồn tại, không chấm nội dung. Section B kiểm tra prompt, SDK và chạy bộ kiểm thử offline mặc định, hiển thị PASSED cho từng ca và trả mã lỗi nếu có ca không đạt. Autograder gốc dùng từ khóa nghiệp vụ xe điện nên tiêu chí 1 không phù hợp với Vinhomes và vẫn cảnh báo. Giữ prompt đúng nghiệp vụ sự cố nước; cần giảng viên xác nhận tiêu chí thay thế. Kết quả offline không chứng minh Gemini thật vượt qua adversarial tests; chạy `--live` riêng để đánh giá model.

Theo README của lớp: code chỉ nộp branch cá nhân, báo cáo được nhóm review rồi chọn vào main. Phiên làm việc hiện dùng branch cá nhân `ngocanhpham`; chưa commit/push hoặc nộp form thay người học.
