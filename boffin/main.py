from fastapi import FastAPI

from boffin.hero.rest import router as hero_router

app = FastAPI()
app.include_router(hero_router)
