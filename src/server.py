
import asyncio
import sys
import subprocess
import os
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    process = None
    try:
        while True:
            data = await websocket.receive_text()
            task_description = data
            await websocket.send_text(f"System: Received task - {task_description}")

            # Spawn CLI process
            # We use the same python interpreter
            cmd = [sys.executable, "-m", "src.main", "--task", task_description, "--yes"]
            
            # Use unbuffered output to get logs in real-time
            env = os.environ.copy()
            env["PYTHONUNBUFFERED"] = "1"
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONUTF8"] = "1"
            
            await websocket.send_text("System: Starting Agent Process...")
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )

            async def read_stream(stream, prefix):
                while True:
                    line = await stream.readline()
                    if not line:
                        break
                    decoded = line.decode('utf-8', errors='replace').strip()
                    if decoded:
                        await websocket.send_text(f"{prefix}: {decoded}")

            # Wait for process and stream output
            await asyncio.gather(
                read_stream(process.stdout, "Log"),
                read_stream(process.stderr, "Error")
            )

            await process.wait()
            await websocket.send_text(f"System: Task Finished (Exit Code: {process.returncode})")
            
    except WebSocketDisconnect:
        print("Client disconnected")
        if process and process.returncode is None:
             try:
                 process.terminate()
             except:
                 pass
    except Exception as e:
        await websocket.send_text(f"System: Server Error - {e}")
        if process and process.returncode is None:
            try:
                process.terminate()
            except:
                pass

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    uvicorn.run("src.server:app", host="127.0.0.1", port=8000, reload=False)