import azure.functions as func
from azure.functions import AsgiMiddleware

try:
    from .main import app
except Exception as e:
    app = None
    import_error = str(e)

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    try:
        if app is None:
            return func.HttpResponse(f"Import error: {import_error}", status_code=500)
        return AsgiMiddleware(app).handle(req, context)
    except Exception as e:
        return func.HttpResponse(f"Runtime error: {e}", status_code=500)