from fastapi import FastAPI, File, UploadFile, Response
from rembg import remove, new_session
import uvicorn
import os

app = FastAPI()

# ✅ Use the lightweight model to stay under RAM limits
session = new_session("u2netp")

@app.post("/remove")
async def remove_bg(file: UploadFile = File(...)):
    print("📥 Received /remove request")
    try:
        image_data = await file.read()
        print(f"📦 Received file: {file.filename}, {len(image_data)} bytes")

        output_data = remove(image_data, session=session)
        print("✅ Background removal successful")

        return Response(content=output_data, media_type="image/png")

    except Exception as e:
        print("❌ Background removal failed:", str(e))
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)


@app.get("/")
@app.head("/")
def root():
    return {"message": "rembg is running"}

import threading
import requests
import time

def warmup():
    time.sleep(3)  # wait a few seconds for server to boot
    try:
        print("🔥 Warming up with self-ping...")
        requests.get("http://0.0.0.0:10000/")
    except Exception as e:
        print("Warmup failed:", e)

threading.Thread(target=warmup).start()



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
