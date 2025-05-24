from fastapi import FastAPI, File, UploadFile, Response
from rembg import remove, new_session
import uvicorn
import os

app = FastAPI()

# ✅ Use the lightweight model to stay under RAM limits
session = new_session("u2netp")

@app.post("/remove")
async def remove_bg(file: UploadFile = File(...)):
    print("📥 Received request")
    try:
        image_data = await file.read()
        output_data = remove(image_data, session=session)
        print("✅ Successfully processed image")
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
