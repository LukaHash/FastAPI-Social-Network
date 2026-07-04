# Simple Social 🚀

> A modern, full-stack media-sharing platform built with FastAPI and Streamlit. Share your moments through images and videos, manage your profile, and connect with a global feed in real-time.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Educational-orange.svg)]()

---

## 📑 Table of Contents

- [About](#-about)
- [✨ Features](#features)
- [🧰 Tech Stack](#-tech-stack)
- [📋 Requirements](#-requirements)
- [🚀 Installation](#-installation)
- [⚙️ Configuration](#%EF%B8%8F-configuration)
- [▶️ Usage](#%EF%B8%8F-usage)
- [🔍 How It Works](#-how-it-works)
- [📁 Project Structure](#-project-structure)
- [❓ FAQ / Troubleshooting](#-faq--troubleshooting)
- [📄 License](#-license)

---

## 🎯 About

**Simple Social** is a lightweight social network clone designed to demonstrate the power of asynchronous Python web frameworks and cloud media integration. 

Unlike traditional apps that store files locally, Simple Social leverages **ImageKit.io** for cloud-based media optimization and delivery, ensuring that your images and videos load lightning-fast regardless of their original size.

The project implements a complete authentication flow, from user registration to JWT-based session management, providing a secure environment for users to share content.

---

## Features

- ✅ **Secure Authentication** — Full user lifecycle (Register $\rightarrow$ Login $\rightarrow$ Verify) using JWT tokens.
- ✅ **Universal Media Upload** — Support for both images (JPG, PNG, etc.) and videos (MP4, AVI, etc.).
- ✅ **Cloud Storage Integration** — Automated uploads to ImageKit.io with unique filename generation.
- ✅ **Dynamic Global Feed** — Real-time feed showing the latest posts from all users, sorted by date.
- ✅ **Ownership Control** — Users can only delete posts they have created (Server-side validation).
- ✅ **Optimized Delivery** — Integrated ImageKit transformations for uniform media display in the frontend.
- ✅ **Asynchronous Architecture** — Non-blocking DB operations using `SQLAlchemy` and `aiosqlite` for high performance.

---

## 🧰 Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) — High-performance async API framework.
- **Frontend**: [Streamlit](https://streamlit.io/) — Rapidly deployed interactive UI.
- **Database**: [SQLite](https://www.sqlite.org/) (via `aiosqlite`) — Lightweight, serverless relational database.
- **Auth System**: [FastAPI Users](https://fastapi-users.github.io/fastapi-users/) — Ready-to-use registration and JWT logic.
- **Media Cloud**: [ImageKit.io](https://imagekit.io/) — Cloud storage and image/video optimization.
- **Server**: [Uvicorn](https://www.uvicorn.org/) — ASGI server for running the FastAPI app.

---

## 📋 Requirements

- **Python 3.9** or newer
- **ImageKit.io Account** (Free tier is sufficient)
- **Private API Key** from your ImageKit dashboard
- Internet connection (for media uploads and frontend delivery)

---

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd simple-social
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuration

The application requires an external API key to handle media uploads. 

1. Create a `.env` file in the root directory:
   ```bash
   touch .env
   ```

2. Add your ImageKit credentials:
   ```env
   IMAGEKIT_PRIVATE_KEY=your_private_key_here
   IMAGEKIT_PUBLIC_KEY=your_public_key_here
   IMAGEKIT_URL=your_imagekit_url_here
   SECRET=your_secret_here
   ```

---

## ▶️ Usage

To get the full experience, you need to run both the backend and the frontend simultaneously.

### 1. Start the Backend
```bash
python Fast_api.py
```
- **API URL**: `http://localhost:8000`
- **Interactive Docs (Swagger)**: `http://localhost:8000/docs`

### 2. Start the Frontend
In a separate terminal:
```bash
streamlit run frontend.py
```
- **Frontend URL**: `http://localhost:8501`

---

## 🔍 How It Works

### 🔄 The Content Flow
1. **Upload**: The user selects a file in Streamlit $\rightarrow$ File is sent to FastAPI $\rightarrow$ FastAPI creates a temporary local copy $\rightarrow$ Uploads to **ImageKit.io** $\rightarrow$ Deletes temporary file $\rightarrow$ Saves the cloud URL to **SQLite**.
2. **Authentication**: `fastapi-users` handles the password hashing and JWT token generation. The frontend stores this token in `st.session_state` to authenticate subsequent requests.
3. **Feed**: The backend queries the database for all posts, joins them with user emails, and returns a JSON list which Streamlit renders as a scrollable feed.

### 🛠️ Media Optimization
The frontend uses **ImageKit Transformation URLs**. Instead of loading the raw file, the app requests a transformed version (e.g., adding overlays or resizing) directly from the CDN, reducing bandwidth and improving speed.

---

## 📁 Project Structure

```text
simple-social/
├── Fast_api.py          # Server entry point (Uvicorn runner)
├── app.py               # API Endpoints & Main Application logic
├── db.py                # SQLAlchemy models & DB connection
├── users.py             # Auth logic & UserManager configuration
├── schemas.py           # Pydantic models for data validation
├── images.py            # ImageKit.io initialization
├── frontend.py          # Streamlit UI implementation
├── requirements.txt     # Project dependencies
└── .env                 # Environment variables (Private)
```

---

## ❓ FAQ / Troubleshooting

**❓ I get a "500 Internal Server Error" during upload**
Check your `.env` file. Ensure your `IMAGEKIT_PRIVATE_KEY` is correct and that you have a stable internet connection.

**❓ The images/videos aren't loading in the feed**
Make sure the backend is running. The frontend fetches the URLs from the API; if the API is down, the feed will be empty.

**❓ How do I change the database?**
Currently, the app uses `sqlite+aiosqlite:///./test.db`. To move to PostgreSQL, change the `DATABASE_URL` in `db.py` and install `asyncpg`.

**❓ I can't delete a post**
The system has a security check: `if post.user_id != user.id: raise HTTPException(403)`. You can only delete posts created by your own account.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---
