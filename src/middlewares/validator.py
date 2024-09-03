from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

class ValidationErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except RequestValidationError as exc:
            errors = exc.errors()
            first_error = errors[0]['msg'] if errors else "Invalid request"
            return JSONResponse(status_code=400, content={"message": first_error})
