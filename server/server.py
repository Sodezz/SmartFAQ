from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from typing import Union

app = FastAPI()

@app.get("/")
def test():
    html_content = "<h2>Я сосал меня ебали</h2>"
    return HTMLResponse(content=html_content)

@app.get("/petuh")
def petuh():
    return {"message": "Python для петухов"}

