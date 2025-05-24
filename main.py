from fastapi import FastAPI, File, UploadFile, Response
from rembg import remove

app = FastAPI()

@app.post("/remove")
async def remove_bg(file: UploadFile = File(...)):
    image_data = await file.read()
    output_data = remove(image_data)
    return Response(content=output_data, media_type="image/png")

@app.get("/")
@app.head("/")
def root():
    return {"message": "rembg is running"}
