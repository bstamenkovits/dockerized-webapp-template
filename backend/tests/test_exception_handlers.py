import json

from starlette.requests import Request

from app import app
from core.exception_handlers import unhandled_exception_handler


def test_unhandled_exception_handler_is_registered():
    """
    Test that the unhandled exception handler is registered in the app's
    exception handlers (i.e. is the exception handler actually used).
    """
    assert app.exception_handlers[Exception] is unhandled_exception_handler


async def test_unhandled_exception_handler_returns_consistent_json():
    """
    Test that the unhandled exception handler returns a consistent JSON response
    with a 500 status code when an unhandled exception occurs.
    """
    scope = {"type": "http", "method": "GET", "path": "/api/boom", "headers": []}
    request = Request(scope)

    response = await unhandled_exception_handler(request, RuntimeError("boom"))

    assert response.status_code == 500
    assert json.loads(response.body) == {"detail": "Internal server error"}
