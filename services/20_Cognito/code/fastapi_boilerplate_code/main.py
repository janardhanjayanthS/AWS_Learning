import os

import uvicorn
from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

app = FastAPI()
app.add_middleware(
    SessionMiddleware, secret_key='asdfasdfa13fasa032', same_site="lax", https_only=False
)

oauth = OAuth()
oauth.register(
    name="oidc",
    authority="https://cognito-idp.us-east-1.amazonaws.com/us-east-1_6o9GaI28R",
    client_id="28v52oa4u6rlt08cl0mns3e48e",
    client_secret="<client secret>",
    server_metadata_url="https://cognito-idp.us-east-1.amazonaws.com/us-east-1_6o9GaI28R/.well-known/openid-configuration",
    client_kwargs={"scope": "phone openid email"},
)


@app.get("/")
async def index(request: Request):
    user = request.session.get("user")
    if user:
        return {"message": f"Hello, {user['email']}", "logout_url": "/logout"}
    return {"message": "Welcome! Please login.", "login_url": "/login"}


@app.get("/login")
async def login(request: Request):
    redirect_uri = "http://localhost:8001/authorize"
    return await oauth.oidc.authorize_redirect(request, redirect_uri)


@app.get("/authorize")
async def authorize(request: Request):
    token = await oauth.oidc.authorize_access_token(request)
    user = token["userinfo"]
    request.session["user"] = dict(user)
    return RedirectResponse(url="/")


@app.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")


@app.get("/secret")
async def secret(request: Request):
    print(request.session)
    if not request.session.get("user"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    return {"the secret secret ingredient of the secret soup is:": "nothing!"}


if __name__ == "__main__":
    uvicorn.run(app, port=8001)
