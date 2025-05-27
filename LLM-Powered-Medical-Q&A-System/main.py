# main.py — Entry point for running the FastAPI app

from core.registrar import register_app
import uvicorn

app = register_app()

if __name__ == "__main__":
    #  Launch the app in development mode
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
