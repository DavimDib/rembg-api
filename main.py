from fastapi import FastAPI, File, UploadFile, Response, Request
from fastapi.responses import JSONResponse
from rembg import remove
import uvicorn
import os

app = FastAPI()

@app.post("/remove")
async def remove_bg(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        output_data = remove(image_data)
        return Response(content=output_data, media_type="image/png")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/")
@app.head("/")
def root():
    return {"message": "rembg is running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
