# 🪖 Helmet Detection System

An AI-powered computer vision application that detects helmets on images and live video streams using a custom-trained **YOLO** model. Built with a decoupled architecture using **FastAPI** as the backend engine and **Streamlit** for the frontend dashboard.

---

## 🏗️ Architecture & Project Structure

```text
Helmet_Detection_Project/
├── Media/                   # Sample images & videos
├── Weights/
│   └── best (1).pt          # Trained YOLO PyTorch weights
├── static/
│   └── style.css            # Custom glassmorphism UI styles
├── main_api.py              # FastAPI server (Inference Engine)
├── app_streamlit.py         # Streamlit UI Dashboard
├── requirements.txt         # Project dependencies
├── .gitignore
└── README.md