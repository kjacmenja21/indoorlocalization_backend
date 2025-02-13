from fastapi import HTTPException, status


def credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def unauthorized_basic() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Basic"},
    )


def unauthorized_bearer() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authorization credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def forbidden(
    msg: str = "You don't have permission to access this resource",
) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=msg,
        headers={"WWW-Authenticate": "Bearer"},
    )


def not_found(msg: str = "Resource not found.") -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)


def conflict(msg: str = "Resource already exists.") -> HTTPException:
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)


def unauthorized(msg: str = "Token has expired.") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=msg,
        headers={"WWW-Authenticate": "Bearer"},
    )


def unprocessable_entity(msg: str = "Unprocessable entity.") -> HTTPException:
    return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=msg)


def too_many_requests(msg: str = "Too many requests") -> HTTPException:
    return HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=msg)


def stop_application(msg: str = "Shutting down due to critical startup error.") -> None:
    raise SystemExit(msg)
