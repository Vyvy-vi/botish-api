import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .dependencies import get_meta
from .routes import coinflip, diceroll, jokes, quotes

# from pydantic import BaseModel

META = get_meta()

app = FastAPI(
    title=META["name"],
    description=META["description"],
    contact=META["author"],
    license_info=META["license"],
    version=META["version"],
)

app.mount("/static", StaticFiles(directory="website/static"), name="static")

app.include_router(coinflip.router)
app.include_router(jokes.router)
app.include_router(diceroll.router)
app.include_router(quotes.router)

templates = Jinja2Templates(directory="website/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("src.main:app")
