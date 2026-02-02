from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from rembg import remove
from PIL import Image
import io
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
        "http://localhost:5500",
        "https://manticike.github.io",
        ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    output = remove(image)

    buffer = io.BytesIO()
    output.save(buffer, format="PNG")
    buffer.seek(0)

    return Response(
        content=buffer.getvalue(),
        media_type="image/png"
    )

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8080))  # Cloud Run sets PORT
    uvicorn.run(app, host="0.0.0.0", port=port)
