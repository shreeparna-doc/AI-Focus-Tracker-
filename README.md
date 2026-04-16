# 🎯 AI Focus Tracker

An AI-powered engagement monitor that uses Computer Vision to track user presence and focus.

## 🚀 How it Works
- **Face Detection:** Uses OpenCV's Haar Cascade to identify the user's face in real-time.
- **Focus Logic:** Tracks the "Engagement Score" based on user presence.
- **Audio Alerts:** If the user stays distracted for too long, a "Faaah!" alarm triggers.
- **Mute Toggle:** Includes a sidebar switch to enable/disable audio alerts.

## 🛠️ Tech Stack
- **Python 3.x**
- **OpenCV** (Computer Vision)
- **Streamlit** (Web Interface)
- **Winsound** (Windows Audio API)

## 💻 Setup & Installation
1. Install the requirements:
   ```bash
   pip install opencv-python streamlit