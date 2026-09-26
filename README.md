<div align="center">

# 🪖 Helmet Detection System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF?style=for-the-badge&logo=yolo&logoColor=black)](https://docs.ultralytics.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Real-time computer vision platform for safety compliance and helmet detection using custom-trained YOLO, FastAPI microservices, and Streamlit.**

[Explore Features](#-key-features) • [System Architecture](#-system-architecture) • [Getting Started](#-getting-started) • [API Documentation](#-api-endpoints)

</div>

---

## 📌 Overview

The **Helmet Detection System** provides real-time detection of safety helmets across image uploads, video files, and live video streams. Built with a decoupled microservice architecture, the project leverages **FastAPI** for high-performance AI inference execution and **Streamlit** for an intuitive, interactive dashboard.

Whether deployed for industrial safety monitoring, traffic surveillance, or site compliance, this application provides dynamic visual bounding boxes and confidence score analytics.

---

## ✨ Key Features

- 🎯 **High-Precision YOLO Detection**: Detects helmets and unhelmeted individuals with low latency.
- ⚡ **Asynchronous Microservice API**: Powered by FastAPI and Uvicorn for scalable inference requests.
- 💻 **Interactive Dashboard**: Modern UI built with Streamlit supporting drag-and-drop media uploads.
- 🎥 **Stream & Video Processing**: Real-time bounding box annotations on static images, MP4 uploads, and live webcams.
- 🔌 **Decoupled Architecture**: Modular backend/frontend structure allowing easy replacement of models or interfaces.

---

## 🏗️ System Architecture

```text
┌─────────────────────────┐               ┌──────────────────────────┐
│                         │  HTTP Request │                          │
│   Streamlit Dashboard   ├──────────────►│    FastAPI Backend API   │
│  (Port 8501 / Frontend) │  (Multipart)  │  (Port 8000 / AI Engine) │
│                         │◄──────────────┤                          │
└─────────────────────────┘  JSON / Media └─────────────┬────────────┘
                                                        │
                                                        ▼
                                          ┌──────────────────────────┐
                                          │   YOLO Detection Engine  │
                                          │  (Ultralytics PyTorch)   │
                                          └──────────────────────────┘
