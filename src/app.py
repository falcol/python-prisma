from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import RedirectResponse

from src.prisma import prisma
from src.routers import apis

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.include_router(apis, prefix="/apis")

@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


@app.get("/", tags=["root"])
async def root():
    return RedirectResponse("/docs")
