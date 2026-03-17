import azure.functions as func
from fastapi import FastAPI
from fastapi.responses import JSONResponse

fastapi_app = FastAPI()


@fastapi_app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# Azure Functions entry point — wraps the FastAPI app
app = func.AsgiFunctionApp(app=fastapi_app, http_auth_level=func.AuthLevel.ANONYMOUS)
