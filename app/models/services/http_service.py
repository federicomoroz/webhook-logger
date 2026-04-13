import httpx
from fastapi import HTTPException

from app.views.schemas.tester import SendRequest, SendResponse


class HttpService:
    @staticmethod
    async def send(request: SendRequest) -> SendResponse:
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.request(
                    method=request.method.upper(),
                    url=request.url,
                    json=request.payload if request.payload else None,
                    headers={"Content-Type": "application/json", **request.headers},
                )
            return SendResponse(
                status_code=resp.status_code,
                body=resp.text[:4000],
                elapsed_ms=round(resp.elapsed.total_seconds() * 1000, 1),
                ok=resp.is_success,
            )
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Request timed out after 15s.")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"Request failed: {exc}")
