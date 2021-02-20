from starlette import status
from starlette.responses import JSONResponse

# buat custom response
def ok(message, datas=None):
    content = {
        "error": False,
        "message": message,
        "datas": datas
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)

def badRequest(message, datas=None):
    content = {
        "error": True,
        "message": message,
        "datas": datas
    }
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)