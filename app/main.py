from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import books
 
app = FastAPI(title="Library API – Khoa CNTT", version="1.0.0",
              description="API quản lý sách của Thư viện số Khoa CNTT")

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    # Nếu là lỗi 404 hoặc 409 thì trả về đúng format
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "HTTP Error", "message": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # IN RA TERMINAL ĐỂ XEM LỖI THẬT LÀ GÌ (Rất quan trọng)
    print("LỖI VALIDATION THẬT SỰ ĐÂY:", exc.errors()) 
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Validation Error", "message": "Dữ liệu không hợp lệ"},
    )

app.include_router(books.router)
 
@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}