by_time_range()`, `get_statistics_by_date()`, `get_hourly_statistics()`, `export_history_to_json()`, `clear_old_records()`.
- `predict_simple.py`: Tích hợp `TimeExtractor` và báo cáo `duration` (thời gian xử lý) trong kết quả dự đoán.
- `app_simple.py`: Flask app với endpoint `/predict` và các endpoint truy vấn lịch sử `/api/history/*` (date, time-range, statistics, hourly, all, export, cleanup).
- Documentations (Tiếng Việt): 11 file hướng dẫn + README cho GitHub.
- Test scripts: `check_basic.py`, `quick_test.py`, `example_time_extractor.py`.

---

## 4. Mô tả kỹ thuật (Technical details)

### 4.1 TimeExtractor - thành phần thời gian
- Chức năng: trích xuất thành phần thời gian từ `datetime` và lưu metadata phân tích.
- Các thành phần trích xuất: `year`, `month`, `day`, `hour`, `minute`, `second`, `timestamp`, `formatted`, `date`, `time`, `week_day`, `month_name`, `iso_week`, `quarter`, `day_of_year`, `unix_timestamp`.

Ví dụ trả về (rút gọn):
```json
{
  "year": 2025,
  "month": 11,
  "day": 16,
  "hour": 14,
  "minute": 30,
  "second": 45,
  "timestamp": "2025-11-16T14:30:45.123456",
  "formatted": "2025-11-16 14:30:45"
}
```

### 4.2 Database schema (SQLite - `analysis_history`)
```sql
CREATE TABLE analysis_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  year INTEGER,
  month INTEGER,
  day INTEGER,
  hour INTEGER,
  minute INTEGER,
  second INTEGER,
  image_name TEXT,
  prediction TEXT,
  confidence REAL,
  duration REAL,
  notes TEXT
);
```

---

## 5. Hướng dẫn demo cho giảng viên / trợ giảng (Demo instructions)

Trước khi demo, đảm bảo đã cài dependencies:

```powershell
# trong Powershell (Windows)
cd d:\project\weather_classification
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### A. Kiểm tra nhanh toàn bộ (health check)

```powershell
python check_basic.py
```
- Kết quả mong đợi: `10/10 kiểm tra thành công`.

### B. Chạy demo web app

```powershell
python app_simple.py
```
- Mở: `http://localhost:5000`
- Upload ảnh (jpg/png) và click `Phân Loại`.
- Kết quả trả về gồm:
  - `class` (ví dụ: Sunny)
  - `confidence` (ví dụ: 0.95)
  - `duration` (thời gian xử lý, giây)
  - `timestamp` & `time_components` (year/month/day/hour/minute/second...)

### C. Gọi API predict (curl / HTTP)

```bash
curl -X POST -F "file=@photo.jpg" http://localhost:5000/predict
```
- Kiểm tra response JSON có trường `time_components`.

### D. Truy vấn lịch sử theo thời gian

- Theo ngày:
  - `GET /api/history/date?year=2025&month=11&day=16`
- Theo khoảng giờ:
  - `GET /api/history/time-range?start_hour=8&end_hour=17&year=2025&month=11&day=16`
- Xuất JSON:
  - `GET /api/history/export?year=2025&month=11`

### E. Export & Kiểm tra dữ liệu
- File JSON xuất ra sẽ chứa các trường thời gian chi tiết để phân tích.

---

## 6. Checklist kiểm tra cho các em (dành cho sinh viên kiểm tra tính năng demo)

Yêu cầu sinh viên tick từng mục sau khi kiểm tra:

- [ ] Chạy `python check_basic.py` và nhận thông báo `10/10`.
- [ ] Chạy `python app_simple.py` và truy cập web UI.
- [ ] Upload ảnh, nhận kết quả dự đoán.
- [ ] Trong response có `time_components` và `duration`.
- [ ] Gọi `GET /api/history/date` trả về bản ghi vừa tạo.
- [ ] Gọi `GET /api/history/time-range` trả về bản ghi trong khoảng giờ tương ứng.
- [ ] Thử `export` và mở file JSON, kiểm tra trường `year/month/day/hour/minute/second`.
- [ ] Chạy `example_time_extractor.py` và xem outputs ví dụ.

Ghi chú: Nếu có lỗi encoding (ký tự tiếng Việt) trên terminal Windows, chạy với `PYTHONIOENCODING=utf-8` hoặc PowerShell: `$env:PYTHONIOENCODING="utf-8"; python check_basic.py`.

---

## 7. Kết quả hiện có & minh chứng (Progress so far)

- Module `TimeExtractor` đã cài đặt và tích hợp.
- API và web app đã hoạt động cục bộ (đã test bằng `check_basic.py`).
- Tài liệu hướng dẫn tiếng Việt đầy đủ (11 file + README).
- Model checkpoint có sẵn trong `checkpoints/simple_model_best.h5`.

Các logs kiểm tra (ví dụ): `check_basic.py` trả về `10/10` kiểm tra thành công trên môi trường dev.

---

## 8. Lịch trình & Kế hoạch theo lịch học (School schedule)

> Lưu ý: phần này là mẫu — vui lòng thay các mốc thời gian theo lịch chính xác của trường.

- Tuần 1-4: Tiền nghiên cứu, thu thập dữ liệu, cài đặt môi trường.
- Tuần 5-7: Thiết kế model, viết `time_extractor.py` và tích hợp.
- Tuần 8: Nộp báo cáo giữa kỳ (bản này) và chuẩn bị demo giữa kỳ.
- Ngày trình bày giữa kỳ: [Điền ngày của trường]
  - Nội dung demo: run app, show predictions, explain TimeExtractor và các truy vấn.
- Tuần 9-12: Cải tiến model, thêm metric, thu thập feedback.
- Cuối kỳ: Hoàn thiện báo cáo cuối kỳ và nộp.

---

## 9. Rủi ro & Biện pháp giảm thiểu

- Rủi ro: Thiếu dữ liệu, model không generalize tốt.
  - Giảm thiểu: Augmentation, tăng dữ liệu, kiểm tra cross-validation.
- Rủi ro: Lỗi môi trường (TensorFlow version mismatch).
  - Giảm thiểu: Cố định `requirements.txt`, hướng dẫn cài đặt rõ ràng.
- Rủi ro: Vấn đề encoding tiếng Việt trên terminal.
  - Giảm thiểu: Hướng dẫn bật `PYTHONIOENCODING` hoặc dùng PowerShell với UTF-8.

---

## 10. Kế hoạch tiếp theo (Next steps)

- Thu thập thêm dữ liệu test và cải thiện accuracy.
- Thêm UI hiển thị thống kê theo giờ/ngày/tháng.
- Tạo script đánh giá (evaluation) và báo cáo metric (precision/recall/F1).
- Chuẩn bị slide và demo ngắn (5-7 phút) cho buổi giữa kỳ.

---

## 11. Phụ lục (Appendix)

### 11.1 Các lệnh hữu ích

```powershell
# Kích hoạt virtualenv
.\.venv\Scripts\Activate.ps1

# Cài dependencies
pip install -r requirements.txt

# Health check
python check_basic.py

# Chạy app
python app_simple.py

# Test scripts
python quick_test.py
python example_time_extractor.py
```

### 11.2 Các endpoint REST chính

- `POST /predict` - upload file ảnh, trả kết quả dự đoán + `time_components`
- `GET /api/history/date?year=&month=&day=` - truy vấn theo ngày
- `GET /api/history/time-range?start_hour=&end_hour=&year=&month=&day=` - truy vấn theo giờ
- `GET /api/history/export?year=&month=` - xuất JSON
- `POST /api/history/cleanup` - dọn dẹp bản ghi cũ

---

## 12. Yêu cầu từ GV (cần xác nhận)

- Vui lòng cung cấp ngày trình bày giữa kỳ chính xác để nhóm điều chỉnh timeline.
- Có cần nộp bản in (PDF) không? Nếu có, tôi có thể xuất Markdown sang PDF giúp (cần công cụ `pandoc` hoặc trình soạn thảo).

---

**Người thực hiện:** [Tên sinh viên]  
**Email liên hệ:** [email@example.com]

