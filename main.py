from typing import Annotated

import fastapi
from fastapi import Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = fastapi.FastAPI()
templates = Jinja2Templates(directory="templates")
product = {}


@app.get("/")
async def root(request: Request, query: str = None):
    if query is None:
        result = product.items()
    else:
        result = []
        for p in product.items():
            if query.lower() in p[0].lower():
                result.append(p)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"products": result}
    )


@app.get("/add")
async def add_get(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="add.html"
    )


@app.post("/add")
async def add_post(name: Annotated[str, Form()], count: Annotated[int, Form()]):
    product[name] = count
    return HTMLResponse(status_code=301, headers={"Location": "/"})


@app.get("/buy")
async def buy_get(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="buy.html",
        context={"products": product.items()}
    )


@app.post("/buy")
async def buy_post(name: Annotated[str, Form()], count: Annotated[int, Form()]):
    product[name] -= count
    return HTMLResponse(status_code=301, headers={"Location": "/"})
