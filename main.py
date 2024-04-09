from typing import Annotated

import fastapi
import psycopg2
from fastapi import Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = fastapi.FastAPI()
templates = Jinja2Templates(directory="templates")
connection = psycopg2.connect("postgres://postgres:123456@localhost:5432/shop")


@app.get("/")
async def root(request: Request, query: str = None):
    cursor = connection.cursor()
    if query is None:
        cursor.execute("SELECT * FROM products")
    else:
        cursor.execute("SELECT * FROM products WHERE name like %s", (f"%{query}%"))

    result = {}
    for i in cursor.fetchall():
        result[i[1]] = i[2]

    cursor.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"products": result.items()}
    )


@app.get("/add")
async def add_get(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="add.html"
    )


@app.post("/add")
async def add_post(name: Annotated[str, Form()], count: Annotated[int, Form()]):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO products (name, count) VALUES (%s, %s)", (name, count))
    connection.commit()
    cursor.close()
    return HTMLResponse(status_code=301, headers={"Location": "/"})


@app.get("/buy")
async def buy_get(request: Request):
    cursor = connection.cursor()
    cursor.execute("SELECT name, count FROM products")
    products = cursor.fetchall()
    cursor.close()

    return templates.TemplateResponse(
        request=request,
        name="buy.html",
        context={"products": products}
    )


@app.post("/buy")
async def buy_post(name: Annotated[str, Form()], count: Annotated[int, Form()]):
    cursor = connection.cursor()
    cursor.execute("UPDATE products SET count = count - %s WHERE name = %s", (count, name))
    connection.commit()
    cursor.close()
    return HTMLResponse(status_code=301, headers={"Location": "/"})
