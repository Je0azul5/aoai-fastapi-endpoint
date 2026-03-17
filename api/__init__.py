import logging

import azure.functions as func
from azure.functions import AsgiMiddleware

logger = logging.getLogger("function_app")
app = None

try:
    from .main import app
except Exception:
    logger.exception("Failed to import ASGI application")

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    if app is None:
        return func.HttpResponse("Application failed to start", status_code=500)

    try:
        return AsgiMiddleware(app).handle(req, context)
    except Exception:
        logger.exception("Unhandled runtime error in Azure Functions entrypoint")
        return func.HttpResponse("Internal server error", status_code=500)
