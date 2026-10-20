# 📚 Library API – Thư viện số Khoa CNTT

## 📖 Mô tả Case Study

Thư viện Khoa CNTT hiện quản lý sách bằng tệp Excel, gây khó khăn khi sinh viên 
tra cứu và khi thủ thư cập nhật. Case study xây dựng **Library API** — một RESTful API 
cho phép cả website thư viện lẫn ứng dụng di động của sinh viên cùng truy vấn dữ liệu sách.

**Yêu cầu nghiệp vụ:**
- Xem danh sách sách, tìm theo tên/tác giả, phân trang
- Xem chi tiết sách theo id
- Thêm sách mới (ISBN duy nhất)
- Cập nhật toàn bộ hoặc một phần thông tin sách
- Xóa sách khỏi hệ thống

**Yêu cầu:** Python 3.10+, FastAPI, Pydantic v2, Uvicorn, Postman/Newman.

## ⚙️ Cài đặt và chạy

```bash
# 1. Clone repo
git clone https://github.com/kthuy9102/library-api.git
cd library-api

# 2. Tạo & kích hoạt môi trường ảo
python3 -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate

# 3. Cài dependencies
pip install -r requirements.txt

# 4. Chạy server
uvicorn app.main:app --reload