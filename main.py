from fastapi import FastAPI, File, UploadFile, Response
from rembg import remove
import uvicorn
import os

app = FastAPI()

# ✅ Preload the model during startup so the first request isn't delayed
@app.on_event("startup")
async def preload_model():
    print("🔥 Preloading model...")
    dummy = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100  # fake PNG file
    try:
        remove(dummy)
    except:
        pass
    print("✅ Model preloaded.")

@app.post("/remove")
async def remove_bg(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        output_data = remove(image_data)
        return Response(content=output_data, media_type="image/png")
    except Exception as e:
        print("❌ Background removal failed:", str(e))
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)

@app.get("/")
@app.head("/")
def root():
    return {"message": "rembg is running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
