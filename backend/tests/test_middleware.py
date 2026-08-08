import logging


async def test_request_logging_middleware_logs_method_path_status(client, caplog):
    """
    Test that endpoint calls are logged by checking that the name and message
    of the log are correct. `caplog` is used to capture log messages during this
    test.

    A valid request is sent to api/health. We check that the log message
    shows the correct logger name and that the log message contains the expected
    HTTP method, path, and 200 status code.
    """
    # Only capture logs for an api call to /api/health for core.middleware logger at INFO level
    with caplog.at_level(logging.INFO, logger="core.middleware"):
        response = await client.get("/api/health")

    assert response.status_code == 200
    assert any(
        record.name == "core.middleware" and "GET /api/health 200" in record.message
        for record in caplog.records
    )
