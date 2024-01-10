from fastapi import Request, Security
from app.logger import logger
import time
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.utils import jwt_utils

security = HTTPBearer()

async def log_middleware(request: Request, call_next):
  start_time = time.time()
  response = await call_next(request)
  process_time = time.time() - start_time
  response.headers["X-Process-Time"] = str(process_time)
  log_dict = {
      'url': request.url.path,
      'method': request.method,
      'process_time': process_time
  }
  logger.info(log_dict, extra=log_dict)
  
  return response


def auth_dependency_middleware():
    def _dependency(request: Request, credentials: HTTPAuthorizationCredentials = Security(security)):
        token = credentials.credentials
        user = jwt_utils.verify_token_access(token)
        request.state.user = user
        return user

    return _dependency