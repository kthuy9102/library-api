# 📘 README.md – Library API (Bài thực hành số 4)

---

## 📖 Mô tả Case Study

Thư viện Khoa CNTT hiện quản lý sách bằng tệp Excel, gây khó khăn khi sinh viên tra cứu và thủ thư nhập liệu. Dự án **Library API** được xây dựng nhằm:

- Cung cấp RESTful API cho phép website thư viện và ứng dụng di động cùng gọi dữ liệu.
- Thay thế quy trình tra cứu thủ công bằng truy vấn JSON nhanh chóng.

**Luồng hoạt động tiêu biểu:**

- Sinh viên mở app → `GET /books?q=python` → API trả danh sách JSON → App hiển thị.
- Thủ thư nhập sách mới → `POST /books` → API kiểm tra dữ liệu, lưu lại và trả `201 Created`.

---

## 🛠 Công nghệ sử dụng

| Thành phần | Phiên bản / Ghi chú |
|---|---|
| Python | ≥ 3.10 |
| FastAPI | `fastapi[standard]` |
| Pydantic | v2 (ràng buộc dữ liệu) |
| Uvicorn | ASGI server |
| Postman | Kiểm thử API + Collection Runner |
| Newman | Chạy test bằng CLI (tùy chọn) |
| Git / GitHub | Quản lý mã nguồn, PR theo nhánh tính năng |

---

## 📂 Cấu trúc dự án

```
library-api/
├── app/
│   ├── __init__.py
│   ├── main.py            # Khởi tạo FastAPI, include router, /health
│   ├── models.py          # Pydantic: BookBase, BookCreate, BookUpdate, BookOut
│   ├── data.py            # Dữ liệu mẫu trong bộ nhớ (BOOKS)
│   └── routers/
│       ├── __init__.py
│       └── books.py       # 6 endpoint CRUD
├── postman/               # Collection + Environment (export v2.1)
├── docs/                  # Ảnh minh chứng (swagger.png, postman_runner.png)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Cài đặt và chạy

### 1. Clone dự án

```bash
git clone <URL_REPO>
cd library-api
```

### 2. Tạo môi trường ảo và cài dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate          # Linux/macOS
# .venv\Scripts\activate           # Windows

pip install "fastapi[standard]"
pip freeze > requirements.txt      # nếu chưa có
```

### 3. Chạy server

> ⚠️ **Lưu ý:** Phải chạy ở **thư mục gốc dự án** `library-api/`, không chạy trong `app/`.

```bash
uvicorn app.main:app --reload
```

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health

---

## 📐 Đặc tả dữ liệu tài nguyên Book

| Trường | Kiểu | Ràng buộc | Ví dụ |
|---|---|---|---|
| `id` | int | Hệ thống tự sinh, tăng dần | 1 |
| `isbn` | str | Đúng 13 chữ số, **duy nhất** | `9786040000011` |
| `title` | str | 1–200 ký tự, bắt buộc | Lập trình Python cơ bản |
| `author` | str | 1–100 ký tự, bắt buộc | Nguyễn Văn Hùng |
| `year` | int | 1900 – 2100 | 2022 |
| `quantity` | int | ≥ 0, mặc định 1 | 5 |

---

## 🔌 Danh sách Endpoint

| Phương thức | Endpoint | Chức năng | Thành công | Lỗi |
|---|---|---|---|---|
| `GET` | `/books` | Danh sách; lọc `?q=`, `?author=`, phân trang `?skip=`, `?limit=` | 200 | 422 |
| `GET` | `/books/{id}` | Chi tiết một cuốn sách | 200 | 404 |
| `POST` | `/books` | Thêm sách mới | 201 | 409, 422 |
| `PUT` | `/books/{id}` | Cập nhật **toàn bộ** | 200 | 404, 409, 422 |
| `PATCH` | `/books/{id}` | Cập nhật **một phần** | 200 | 404, 422 |
| `DELETE` | `/books/{id}` | Xóa sách | 204 | 404 |
| `GET` | `/health` | Kiểm tra trạng thái server | 200 | – |

### Xử lý lỗi chuẩn HTTP

| Mã | Ý nghĩa | Tình huống |
|---|---|---|
| **404** | Not Found | `id` không tồn tại |
| **409** | Conflict | ISBN bị trùng khi tạo/cập nhật |
| **422** | Unprocessable Entity | Dữ liệu sai ràng buộc Pydantic |
| **204** | No Content | Xóa thành công, không có body |

---

## 🧪 Kiểm thử với Postman

### 1. Chuẩn bị

- Mở Postman Desktop (hoặc Web).
- Import 2 file trong thư mục `postman/`:
  - `Library-API.postman_collection.json`
  - `Library-Local.postman_environment.json`
- Chọn environment **Library-Local** ở góc trên phải.

### 2. Kịch bản kiểm thử (12 test case)

| Mã | Request | Dữ liệu / Ý nghĩa | Mong đợi |
|---|---|---|---|
| TC01 | `GET /health` | Server đang chạy | 200 |
| TC02 | `GET /books` | Danh sách mặc định | 200 |
| TC03 | `GET /books?author=hùng&limit=1` | Lọc tác giả, phân trang | 200, 1 bản ghi |
| TC04 | `GET /books/1` | Sách tồn tại | 200 |
| TC05 | `GET /books/999` | Sách không tồn tại | 404 |
| TC06 | `POST /books` | Dữ liệu hợp lệ; lưu `id` vào `bookId` | 201 |
| TC07 | `POST /books` | Gửi lại ISBN của TC06 | 409 |
| TC08 | `POST /books` | `isbn="123"`, `year=1800` | 422 |
| TC09 | `PUT /books/{{bookId}}` | Gửi đủ trường, đổi `title` | 200 |
| TC10 | `PATCH /books/{{bookId}}` | `{"quantity": 10}` | 200 |
| TC11 | `DELETE /books/{{bookId}}` | Xóa sách vừa tạo | 204 |
| TC12 | `GET /books/{{bookId}}` | Kiểm tra sau khi xóa | 404 |

### 3. Body mẫu cho TC06

```json
{
  "isbn": "9786040000042",
  "title": "Phát triển Web API với FastAPI",
  "author": "Lê Minh Tuấn",
  "year": 2024,
  "quantity": 4
}
```

### 4. Script kiểm thử tự động (TC06)

Mở tab **Scripts → Post-response** (Postman cũ: **Tests**), dán đoạn script:

```javascript
pm.test("Trả về 201 Created", () => {
    pm.response.to.have.status(201);
});
const book = pm.response.json();
pm.test("Có id và đúng ISBN", () => {
    pm.expect(book).to.have.property("id");
    pm.expect(book.isbn).to.eql("9786040000042");
});
pm.collectionVariables.set("bookId", book.id);   // dùng cho TC09–TC12
```

Các request khác tối thiểu kiểm tra mã trạng thái, ví dụ TC05:

```javascript
pm.test("Trả về 404", () => pm.response.to.have.status(404));
```

### 5. Chạy toàn bộ bằng Collection Runner

- Chuột phải vào collection **Library API** → **Run collection**.
- **Giữ đúng thứ tự TC01 → TC12**.
- Nhấn **Run** → kỳ vọng: **12/12 Passed**.
- Chụp màn hình lưu thành `docs/postman_runner.png`.

> 💡 **Lưu ý:** Dữ liệu lưu trong bộ nhớ, vì vậy trước mỗi lần chạy Runner nên **khởi động lại server** để TC07 (ISBN trùng) cho kết quả ổn định.

### 6. Chạy bằng CLI với Newman (tùy chọn)

```bash
npx newman run postman/Library-API.postman_collection.json \
    -e postman/Library-Local.postman_environment.json
```

---

## 🖼 Ảnh minh chứng

| Ảnh | Mô tả |
|---|---|
| `docs/swagger.png` | Swagger UI hiển thị đầy đủ 7 endpoint (2 nhóm: **System**, **Books**) |
| `docs/postman_runner.png` | Kết quả Collection Runner 12/12 test case Passed |

---

## 🌿 Quy trình Git & Pull Request

### Commit theo Conventional Commits

```bash
git switch -c feature/books-api

git add .
git commit -m "feat: implement books CRUD API"
git commit -m "feat: add PATCH endpoint"
git commit -m "test: add postman collection and environment"
git commit -m "docs: update README with test cases"

git push -u origin feature/books-api
```

### Tạo Pull Request

1. Vào GitHub → tạo **Pull Request** từ `feature/books-api` → `main`.
2. Mô tả thay đổi + cách kiểm thử.
3. Gửi link PR lên LMS để nộp bài.

---

## Phần mở rộng

### 1. Nghiệp vụ mượn/trả sách

- `POST /books/{id}/borrow` → giảm `quantity` đi 1; nếu `quantity == 0` trả **409** với thông báo `"Sách đã hết"`.
- `POST /books/{id}/return` → tăng `quantity` lên 1.
- Bổ sung TC13–TC15 vào Postman Collection (ví dụ: mượn sách `id=3` đang hết phải nhận **409**).

### 2. Định dạng lỗi thống nhất

Viết exception handler trả mọi lỗi về dạng:

```json
{
  "error": "CONFLICT",
  "message": "ISBN 9786040000042 đã tồn tại"
}
```

---

## 🐛 Lỗi thường gặp và cách khắc phục

| Hiện tượng | Nguyên nhân / Cách khắc phục |
|---|---|
| `ModuleNotFoundError: No module named 'app'` | Chạy uvicorn ở thư mục gốc `library-api/`, không chạy trong `app/`; kiểm tra có `app/__init__.py` |
| `command not found: uvicorn` | Chưa kích hoạt venv: `source .venv/bin/activate` |
| Postman báo *Could not send request* | Server chưa chạy hoặc sai `baseUrl`; chưa chọn environment **Library-Local** |
| POST luôn trả **422** | Chưa chọn **Body → raw → JSON**, hoặc JSON sai cú pháp (thiếu dấu phẩy, dùng nháy đơn) |
| TC09–TC12 gọi sai `id` | TC06 chưa lưu biến `bookId`; kiểm tra script `pm.collectionVariables.set` |
| PATCH làm mất dữ liệu | Thiếu `exclude_unset=True` khi gọi `model_dump()` |

---

## 📋 Tiêu chí đánh giá

| TT | Tiêu chí | Điểm |
|---|---|---|
| 1 | Khởi tạo dự án đúng cấu trúc; có venv, `requirements.txt`, `.gitignore` | 1.0 |
| 2 | Pydantic model đúng đặc tả (ràng buộc, tách Create/Update/Out) | 1.5 |
| 3 | GET danh sách (lọc, phân trang) + GET chi tiết (404 đúng) | 2.0 |
| 4 | POST (201, 409), PUT, PATCH (`exclude_unset`), DELETE (204) đúng | 2.5 |
| 5 | Swagger UI đầy đủ tags, summary, mô tả | 0.5 |
| 6 | Postman: đủ 12 test case có script, Runner 100%, đã export | 1.5 |
| 7 | Git: commit chuẩn, PR có mô tả; README đầy đủ kèm ảnh | 1.0 |
| | **Tổng cộng** | **10** |
| ➕ | Bài tập mở rộng | +1.0 (tối đa 10) |

---

## ❓ Câu hỏi

**Câu 1.** `response_model` dùng để kiểm chứng (validate) và định dạng dữ liệu đầu ra theo model `BookOut`, đồng thời sinh schema hiển thị trên Swagger UI. Nó đảm bảo API không trả về các trường dư thừa hoặc sai kiểu.

**Câu 2.** 
- `PUT` là **thay thế toàn bộ** tài nguyên → client phải gửi đầy đủ tất cả các trường.
- `PATCH` là **cập nhật một phần** → client chỉ gửi các trường muốn thay đổi.
- `PATCH` cần `exclude_unset=True` để chỉ lấy những trường thực sự được client gửi lên (không lấy các trường có giá trị mặc định `None`), tránh ghi đè dữ liệu cũ bằng `None`.

**Câu 3.** FastAPI trả về mã **422 Unprocessable Entity**. Không dùng 400 vì 400 thường ám chỉ lỗi cú pháp HTTP (malformed request), còn 422 chỉ ra rằng request đúng cú pháp nhưng dữ liệu không thỏa mãn ràng buộc ngữ nghĩa (validation error). FastAPI mặc định dùng 422 theo chuẩn của nó.

**Câu 4.** Theo chuẩn HTTP, **204 No Content** nghĩa là xử lý thành công nhưng không có nội dung trả về — phù hợp với hành động xóa (client không cần dữ liệu gì sau khi xóa). Nếu cố tình trả về body trong response 204, nhiều client/proxy sẽ gặp lỗi hoặc bỏ qua body vì đây là vi phạm đặc tả HTTP (RFC 7231).

**Câu 5.** `exclude_id` giúp **bỏ qua việc kiểm tra trùng ISBN với chính cuốn sách đang cập nhật**. Nếu bỏ `exclude_id` khi gọi trong `PUT`, khi client cập nhật sách mà vẫn giữ nguyên ISBN cũ, hệ thống sẽ thấy ISBN đó "đã tồn tại" (chính là của cuốn sách đang sửa) và trả về lỗi **409 Conflict** sai.

**Câu 6.** Vì dữ liệu lưu trong **bộ nhớ (list Python)**, sẽ mất khi tắt server. Nếu không khởi động lại:
- Lần chạy Runner thứ 2, TC06 (thêm sách) sẽ bị lỗi **409** vì ISBN đã tồn tại từ lần chạy trước.
- TC07 (test trùng ISBN) sẽ không còn ý nghĩa kiểm thử đúng kịch bản (vì dữ liệu đã bị "bẩn").

**Câu 7.** `BookId` là một kiểu dữ liệu có ràng buộc: `book_id` phải là số nguyên **lớn hơn 0** (`gt=0`). Nếu client gọi `GET /books/-5`, FastAPI sẽ trả về **422 Unprocessable Entity** do vi phạm ràng buộc `gt=0`, kèm mô tả lỗi chỉ ra tham số `book_id` không hợp lệ.

**Câu 8.** 
- `BookCreate`: dùng cho `POST` (thêm mới) và `PUT` (thay thế) — yêu cầu đầy đủ các trường bắt buộc.
- `BookUpdate`: dùng cho `PATCH` — mọi trường đều **tùy chọn** (`Optional`) để cho phép cập nhật một phần.
- `BookOut`: dùng cho output — có thêm trường `id` do hệ thống sinh ra.
- **Phải tách 3 model** vì mỗi thao tác có yêu cầu dữ liệu khác nhau. Dùng chung 1 model sẽ khiến client phải gửi thừa trường khi `PATCH`, hoặc không thể validate đúng khi `POST`/`PUT`. Tách ra giúp code rõ ràng, đúng nghiệp vụ và schema Swagger chính xác hơn.
## 📚 Tài liệu tham khảo

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)
- [Postman Learning Center](https://learning.postman.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)

