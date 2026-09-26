# Helmet Detection System

Detects people **with a helmet** and **without a helmet** using a custom YOLO model.

You run two programs at the same time:

1. **FastAPI** (port `8000`) — loads the model and does detection
2. **Streamlit** (port `8501`) — the web dashboard you use in the browser

---

## What you need before starting

- **Python 3.10 or newer** installed ([python.org](https://www.python.org/downloads/))
- A copy of this project folder
- The trained weights file in the right place (see Step 3)

On Windows, when you install Python, tick **Add python.exe to PATH**.

---

## Folder layout you should have

```text
helmet-detection/
├── main_api.py                 # FastAPI backend
├── app_streamlit.py            # Streamlit dashboard
├── helmet_detection_image.py   # optional: OpenCV image demo
├── helmet_detection_video.py   # optional: OpenCV video demo
├── requirements.txt
├── static/
│   └── style.css
├── Weights/
│   └── best (1).pt             # required — your YOLO weights
└── Media/                      # optional sample images/videos
    ├── download.jpeg
    └── helmet.mp4
```

---

## Step 1 — Open a terminal in the project folder

**Windows (PowerShell or Command Prompt)**

```powershell
cd path\to\helmet-detection
```

**macOS / Linux**

```bash
cd path/to/helmet-detection
```

You should see `main_api.py` and `app_streamlit.py` in this folder.

---

## Step 2 — Create a virtual environment and install packages

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks activation, run this once, then try activate again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Windows (Command Prompt)

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The first install can take several minutes because it downloads PyTorch.

Leave this terminal open. You will start the API here in Step 5.

---

## Step 3 — Put the YOLO weights in place

The backend looks for this exact path:

```text
Weights/best (1).pt
```

1. Create a folder named `Weights` in the project root (if it is missing).
2. Copy your trained file into it.
3. Rename the file to **`best (1).pt`** if it has a different name (including the space and parentheses).

If this file is missing, FastAPI will fail as soon as it starts.

---

## Step 4 — (Optional) Add sample media

If you want the dashboard option **Select from Media/ Folder**:

1. Create a folder named `Media` in the project root.
2. Put `.jpg` / `.jpeg` / `.png` images and `.mp4` videos inside it.

You can skip this step and only **upload** files in the dashboard.

---

## Step 5 — Start the FastAPI backend

In the **same** terminal where the virtual environment is active:

```bash
uvicorn main_api:app --reload --host 127.0.0.1 --port 8000
```

Wait until you see something like:

```text
Uvicorn running on http://127.0.0.1:8000
```

Keep this window running. Do not close it.

Check that it is alive: open [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) in a browser. You should see JSON with `"status": "online"`.

Optional API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Step 6 — Start the Streamlit dashboard

Open a **second** terminal, go to the same project folder, and activate the same virtual environment.

**Windows (PowerShell)**

```powershell
cd path\to\helmet-detection
.\.venv\Scripts\Activate.ps1
streamlit run app_streamlit.py
```

**macOS / Linux**

```bash
cd path/to/helmet-detection
source .venv/bin/activate
streamlit run app_streamlit.py
```

The app opens at [http://localhost:8501](http://localhost:8501).

In the sidebar, **FastAPI Active** means both parts are running. **FastAPI Backend Offline** means Step 5 is not running (or the API crashed).

---

## Step 7 — Use the dashboard

### Image tab

1. Choose **Upload Custom Image** or **Select from Media/ Folder**.
2. Pick an image.
3. Click **Detect Helmet**.
4. The right column shows boxes for **With Helmet** / **Without Helmet**.

### Video tab

1. Choose **Upload Custom Video (.mp4)** or **Select from Media/ Folder**.
2. Pick a video.
3. Click **Start Live Stream**.
4. Annotated frames stream on the right. This can be slow on CPU.

---

## Stop the app

In each terminal, press `Ctrl + C`.

---

## Optional: OpenCV scripts (no Streamlit)

These windows open with OpenCV. They need **`cvzone`**, which is not in `requirements.txt`:

```bash
pip install cvzone
```

**Image** (edit `image_path` inside the file if needed):

```bash
python helmet_detection_image.py
```

Press `q` to close.

**Video** (edit `video_path` inside the file if needed):

```bash
python helmet_detection_video.py
```

Press `q` to stop.

These scripts also need `Weights/best (1).pt`.

---

## Troubleshooting

| Problem | What to do |
|---|---|
| `Weights/best (1).pt` not found | Create `Weights/` and put the `.pt` file there with that exact name. |
| Sidebar says FastAPI Backend Offline | Start Step 5 first. Confirm [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health). |
| `Activate.ps1` is blocked | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then activate again. |
| `python` not found | Install Python 3.10+ and add it to PATH, or try `py -3` on Windows. |
| Video stream is slow | Normal on CPU. Use a shorter clip. GPU PyTorch is optional and not required. |
| Empty Media dropdown | Create `Media/` and add files, or use Upload instead. |
| Port already in use | Close the old process, or change the port in the uvicorn / Streamlit command. |

---

## API (for developers)

| Method | Path | What it does |
|---|---|---|
| GET | `/health` | Backend + model path |
| POST | `/detect/image` | Image file in, annotated JPEG out |
| POST | `/detect/video/upload` | Video file in, MJPEG stream out |
| GET | `/detect/video/local/{filename}` | Stream a file from `Media/` |

The Streamlit app talks to `http://127.0.0.1:8000`. If you move the API to another host, change `API_URL` in `app_streamlit.py`.
