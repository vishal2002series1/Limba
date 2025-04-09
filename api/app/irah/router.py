from fastapi import Request, Response, HTTPException, status
from fastapi.routing import APIRoute
from fastapi.exceptions import RequestValidationError
from typing import Callable
import time

class IRAH_APIRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        fastapi_route_handler = super().get_route_handler()

        async def irah_route_handler(request: Request) -> Response:
            try:
                start_time = time.time()
                response = await fastapi_route_handler(request)
                process_time = 1000 * (time.time() - start_time)
                response.headers["X-Process-Time"] = str(process_time)
                return response
            except KeyError as e:
                print("KeyError:", e)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=e.args
                )
            except Exception as e:
                print(e)
                raise e

        return irah_route_handler