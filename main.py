import uvicorn
from app import app

if __name__ == '__main__':
    # start local server
    # reload True artinya server akan restart otomatis ketika ada perubahan code
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
