import streamlit as st
import cv2
import winsound  

# --- UI Configuration ---
st.set_page_config(page_title="AI Focus Tracker", page_icon="🎯", layout="wide")

st.sidebar.title("⚙️ AI Settings")
st.sidebar.markdown("Adjust the tracking parameters:")
max_grace_frames = st.sidebar.slider("Forgiveness Timer", min_value=5, max_value=50, value=20)

# The Sound Switch
sound_enabled = st.sidebar.toggle("Enable Audio Alert", value=True)

st.title("🎯 AI Focus Dashboard")
st.markdown("Real-time presence and engagement tracking powered by Computer Vision.")
st.divider()

col1, col2 = st.columns(2)
with col1:
    status_ui = st.empty()
with col2:
    score_ui = st.empty()

st.markdown("**Focus Level**")
progress_bar = st.empty()

st.markdown("### 📷 Live Camera Feed")
video_feed = st.empty()

# --- Backend Initialization ---
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# THIS IS THE LINE THAT WAS MISSING: Defining 'cap'
# We use CAP_DSHOW for better Windows compatibility
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

frames_absent = 0
current_status = "Focused"
current_score = 100
alarm_played = False 

# This 'while' loop uses 'cap' defined above
while cap.isOpened():
    ret, frame = cap.read()
    if not ret: 
        st.error("Camera feed lost. Please restart the app.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        frames_absent = 0 
        current_status = "Focused"
        current_score = 100
        alarm_played = False 
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Tracking...", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    else:
        frames_absent += 1 
        
        if frames_absent < max_grace_frames:
            current_status = "Looking away? 🤔"
            current_score = int(100 - ((frames_absent / max_grace_frames) * 100))
        else:
            current_status = "Distracted / Absent ❌"
            current_score = 0
            
            if not alarm_played and sound_enabled:
                try:
                    winsound.PlaySound("faaah.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                except Exception:
                    winsound.Beep(800, 600)
                alarm_played = True

    status_ui.success(f"**Status:** {current_status} ✅") if current_score == 100 else status_ui.warning(f"**Status:** {current_status}") if current_score > 0 else status_ui.error(f"**Status:** {current_status}")
    score_ui.metric("Engagement Score", f"{current_score}%")
    progress_bar.progress(max(0, current_score) / 100.0)
    video_feed.image(frame, channels="BGR", use_container_width=True)

cap.release()