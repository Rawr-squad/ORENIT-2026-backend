import logging
import time
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

app_logger = logging.getLogger("app")
request_logger = logging.getLogger("requests")


async def log_requests(request: Request, call_next):
    start_time = time.time()

    request_logger.info(f"{request.method} {request.url.path}")

    try:
        response = await call_next(request)
        process_time = time.time() - start_time

        # Логируем успешные ответы
        if 400 <= response.status_code < 600:
            # Это ошибка, но не исключение
            app_logger.warning(
                f"HTTP {response.status_code} | {request.method} {request.url.path} | "
                f"{process_time:.3f}s"
            )
        else:
            request_logger.info(f"{response.status_code} | {process_time:.3f}s")

        response.headers["X-Process-Time"] = str(process_time)
        return response

    except HTTPException as e:
        # Ловим кастомные HTTPException
        process_time = time.time() - start_time

        app_logger.error(
            f"HTTP {e.status_code} | {request.method} {request.url.path} | "
            f"{process_time:.3f}s | Detail: {e.detail}"
        )

        request_logger.error(
            f"HTTP {e.status_code} | {request.method} {request.url.path} | "
            f"{process_time:.3f}s | Detail: {e.detail}"
        )

        # Возвращаем ответ с тем же статусом
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )

    except Exception as e:
        # Ловим все остальные исключения
        process_time = time.time() - start_time

        app_logger.error(
            f"ERROR | {request.method} {request.url.path} | "
            f"{process_time:.3f}s | {type(e).__name__}: {str(e)}",
            exc_info=True
        )

        request_logger.error(
            f"ERROR | {request.method} {request.url.path} | "
            f"{process_time:.3f}s | {type(e).__name__}: {str(e)}"
        )

        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )