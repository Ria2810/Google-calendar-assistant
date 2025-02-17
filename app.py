import streamlit as st
from datetime import datetime, timedelta
import dateparser
import os

# Import your existing modules
from google_calendar import schedule_event
from openai_assistant import process_command

# Import voice functions from utils.py
from utils import speech_to_text
from audio_recorder_streamlit import audio_recorder

# ---------------- Helper Functions ----------------
def convert_relative_date(date_str, reference_date=None):
    """Convert a relative date string to absolute ISO 8601 format."""
    if not date_str:
        return date_str
    if reference_date is None:
        reference_date = datetime.now()
    parsed_date = dateparser.parse(date_str, settings={'RELATIVE_BASE': reference_date})
    if parsed_date:
        return parsed_date.strftime("%Y-%m-%dT%H:%M:%S")
    return date_str

def set_default_end_time(meeting_details):
    """If 'end_time' is not provided, set it one hour after 'start_time'."""
    if (not meeting_details.get("end_time") or meeting_details.get("end_time").strip() == "") and meeting_details.get("start_time"):
        try:
            start_dt = datetime.strptime(meeting_details["start_time"], "%Y-%m-%dT%H:%M:%S")
            end_dt = start_dt + timedelta(hours=1)
            meeting_details["end_time"] = end_dt.strftime("%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            st.error("Error setting default end time: " + str(e))
    return meeting_details

# Initialize session state for auto-scheduling
if "final_command" not in st.session_state:
    st.session_state.final_command = ""

st.markdown("<h1 style='text-align: center;'>OpenAI Assistant for Google Calendar Meeting Scheduling📆</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>This app uses OpenAI's natural language processing to schedule meetings on Google Calendar.</h4>", unsafe_allow_html=True)

st.markdown(
    "<br><br><div style='color: #fff; padding: 2px; font-size:1.5rem; font-weight: bold; text-transform: uppercase; text-align:center;'>"
    "ENTER YOUR MEETING COMMAND (e.g., 'Schedule a meeting with Bob tomorrow at 2pm'):"
    "</div>",
    unsafe_allow_html=True
)

# ---------------- Input Section (Text & Voice) ----------------
with st.container():
    col1, col2 = st.columns([9, 1])  # Adjust width for better alignment

    # Text input field - Automatically triggers scheduling on Enter
    with col1:
        user_input_text = st.text_input(
            "Type your meeting command:",
            placeholder="Enter meeting command here...",
            key="text_input"
        )
    
    # Audio input button using audio_recorder
    with col2:
        audio_bytes = audio_recorder()

# If user enters text and presses Enter, store in session state
if user_input_text:
    st.session_state.final_command = user_input_text

# Process audio input (if provided)
if audio_bytes:
    with st.spinner("Transcribing..."):
        audio_file_path = "temp_audio.mp3"
        with open(audio_file_path, "wb") as f:
            f.write(audio_bytes)
        transcript = speech_to_text(audio_file_path)
        os.remove(audio_file_path)

        if transcript:
            st.session_state.final_command = transcript
            st.write(f"Transcribed Text: {transcript}")

# ---------------- Auto-Scheduling Process ----------------
if st.session_state.final_command.strip():
    final_command = st.session_state.final_command
    with st.spinner("Processing your command..."):
        meeting_details = process_command(final_command)
    
    meeting_details["start_time"] = convert_relative_date(meeting_details.get("start_time", ""))
    meeting_details["end_time"] = convert_relative_date(meeting_details.get("end_time", ""))
    meeting_details = set_default_end_time(meeting_details)
    
    st.subheader("Meeting Details:")
    st.json(meeting_details)
    
    if meeting_details.get("summary") and meeting_details.get("start_time") and meeting_details.get("end_time"):
        with st.spinner("Scheduling meeting..."):
            try:
                event_link = schedule_event(
                    summary=meeting_details["summary"],
                    start_time=meeting_details["start_time"],
                    end_time=meeting_details["end_time"],
                    description=meeting_details.get("description", ""),
                    attendees=meeting_details.get("attendees", [])
                )
                st.success(f"Meeting scheduled successfully! [View Event]({event_link})")
                # Clear the session state after successful scheduling
                st.session_state.final_command = ""
            except Exception as e:
                st.error(f"Error scheduling meeting: {e}")
    else:
        st.error("Insufficient meeting details extracted.")

