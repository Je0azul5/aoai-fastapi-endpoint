import logging
import traceback

import azure.functions as func
from azure.functions import AsgiMiddleware

logger = logging.getLogger("function_app")

try:
    from .main import app
except Exception:
    app = None
    import_error = traceback.format_exc()
    logger.exception("Failed to import ASGI application")

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    try:
        if app is None:
            return func.HttpResponse(f"Import error: {import_error}", status_code=500)
        return AsgiMiddleware(app).handle(req, context)
    except Exception:
        logger.exception("Unhandled runtime error in Azure Functions entrypoint")
        return func.HttpResponse(
            f"Runtime error: {traceback.format_exc()}",
            status_code=500,
        )
