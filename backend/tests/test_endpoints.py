import pytest

PROTECTED_ROUTES = [
    ("GET", "/api/hello"),
    ("GET", "/api/ping-database"),
]

UNPROTECTED_ROUTES = [
    ("GET", "/api/health"),
    ("GET", "/api/ping"),
    ("POST", "/api/auth/register"),
    ("POST", "/api/auth/login"),
]


@pytest.mark.parametrize("method,path", PROTECTED_ROUTES)
async def test_requires_auth(client, method, path):
    """
    Test that protected endpoints reject requests without a session cookie.
    """
    response = await client.request(method, path)
    assert response.status_code == 401


@pytest.mark.parametrize("method,path", UNPROTECTED_ROUTES)
async def test_does_not_require_auth(client, method, path):
    """
    Test that explicitly unprotected endpoints do not reject requests for lack
    of a session cookie (i.e. they don't return 401).
    """
    response = await client.request(method, path)
    assert response.status_code != 401
