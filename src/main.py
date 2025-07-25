import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.adapters.api.routes import router

app = FastAPI()

app.include_router(router=router)


@app.get('/ping')
def ping():
    return JSONResponse(content={'status': 'ok'}, status_code=200)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
