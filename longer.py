import streamlit as st
import google.generativeai as genai
import cv2
import tempfile
import os
from datetime import timedelta

# Configure Gemini Pro
genai.configure(api_key="key")
model = genai.GenerativeModel('gemini-pro')

# Initialize Streamlit app
st.title("Baseball Video Analysis App")

# The complete analysis prompt
ANALYSIS_PROMPT = """Task: You are a baseball analysis expert. Your job is to analyze videos of pitchers pitching and batters hitting the ball to extract precise numerical metrics using computer vision technology, such as Gemini 2.0. The extracted data should be derived solely from video analysis without relying on external databases.

Guidelines:
1. Player Identification:
   * Jersey Number and Team Identification: Detect the jersey number and team logo/colors to identify the player.
   * Player Name and Stats: Once the player is identified, retrieve their name and statistics from the video annotations.

2. Pitch Metrics:
   * Pitch Speed: Accurately measure the speed of the pitch by analyzing the ball's movement frame by frame.
   * Pitch Type: Classify the type of pitch (e.g., fastball, curveball, slider) based on ball trajectory, release point, and spin.
   * Pitch Location: Determine the exact location of the pitch relative to the strike zone using video-based strike zone mapping.

3. Batted Ball Metrics:
   * Exit Velocity: Measure the speed of the ball as it leaves the bat using motion tracking.
   * Launch Angle: Calculate the angle at which the ball is hit based on its initial trajectory.
   * Hit Distance: Estimate the total distance traveled by the ball after contact.

4. Game Situational Metrics:
   * Score: If identifiable in the video, extract the current score. If the score is unclear, return "Score not available in the video."
   * Inning: Identify the current inning of the game through scoreboard analysis.
   * Outs: Track the number of outs using visual indicators on the scoreboard or umpire gestures.
   * Base Occupancy: Determine which bases are occupied and by which players.

Rules:
* The model must provide numerical values for Pitch Speed, Pitch Type, Pitch Location, Exit Velocity, Launch Angle, and Hit Distance.
* Ensure all extracted metrics are accurately measured from the video.
* If the video does not provide a clear view for calculating a specific metric, use estimation techniques based on available data instead of returning "Not available in the video."
* Use standard baseball terminology for all extracted metrics.
* The output format should be concise and structured.

Please provide the analysis in this exact format:

**Player Identification:**
* Batter: Jersey #[number], Team: [team name] ([uniform description])
* Pitcher: Team: [team name] ([uniform description])

**Pitch Metrics:**
* **Pitch Speed:** [speed] mph (Measured by analyzing ball trajectory)
* **Pitch Type:** [type] (Based on trajectory, release point, and spin)
* **Pitch Location:** [location description] (Relative to strike zone)

**Batted Ball Metrics:**
* **Exit Velocity:** [speed] mph (Measured from bat contact)
* **Launch Angle:** [angle] degrees (Based on initial trajectory)
* **Hit Distance:** [distance] ft (Total estimated travel)

**Game Situational Metrics:**
* **Score:** [If score is clearly visible on scoreboard: "X-Y Team Names"; If not visible: "Score not available in the video 🤔"]
* **Inning:** [If inning is clearly visible: "Xth"; If not visible: "Inning not available in the video"]
* **Outs:** [If outs are clearly visible: "X out(s)"; If not visible: "Outs not available in the video 🔍"]
* **Base Occupancy:** [If runners are clearly visible: list runners and bases; If not visible: "Base occupancy not available in the video"]

**Summary of Extracted Metrics:**
Pitch Speed: [speed] mph, Pitch Type: [type], Exit Velocity: [speed] mph, Launch Angle: [angle] degrees, Hit Distance: [distance] ft, Score: [score or "Score not available in the video 🤔"], Inning: [inning], Outs: [outs or "Outs not available in the video 🔍"]

Based on the provided video, please analyze and provide all metrics according to these guidelines and format."""

# Function to process video and detect events
def process_video(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    # Placeholder for detected events (pitches/batted balls)
    events = []

    # Process the video in chunks (e.g., 10-second segments)
    for i in range(0, int(duration), 10):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * fps)
        ret, frame = cap.read()
        if not ret:
            break

        # Placeholder: Add logic to detect pitches/batted balls using computer vision
        # For now, we'll assume an event is detected every 10 seconds
        events.append({
            "timestamp": str(timedelta(seconds=i)),
            "description": "Pitch detected"
        })

    cap.release()
    return events

# Upload video
uploaded_file = st.file_uploader("Upload a baseball video", type=["mp4", "avi", "mov"])

if uploaded_file:
    # Save the uploaded video to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        tmp_file.write(uploaded_file.read())
        video_path = tmp_file.name

    # Display the video
    st.video(video_path)

    # Optional description field
    video_description = st.text_area(
        "Describe what's happening in the video (optional):",
        placeholder="Example: This clip shows a right-handed batter facing a left-handed pitcher in the bottom of the 7th inning..."
    )

    # Add a button to generate analysis
    if st.button("Generate Analysis"):
        try:
            st.info("Generating analysis...")

            # Process the video to detect events
            events = process_video(video_path)

            # Display timestamps and events
            st.subheader("Detected Events")
            for event in events:
                st.write(f"**Timestamp:** {event['timestamp']} - {event['description']}")

            # Prepare prompt with optional description
            full_prompt = ANALYSIS_PROMPT
            if video_description:
                full_prompt += f"\n\nVideo Description: {video_description}"

            # Send prompt to Gemini
            response = model.generate_content(full_prompt)

            # Display the analysis
            st.subheader("Analysis Results")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"Error generating analysis: {str(e)}")
        finally:
            # Clean up the temporary file
            os.unlink(video_path)

# Add instructions
st.sidebar.markdown("""
## How to Use
1. Upload your baseball video clip
2. (Optional) Add a description of what's happening in the video
3. Click 'Generate Analysis' to get detailed metrics
4. View the comprehensive analysis results

Note: For best results, ensure the video clearly shows:
- The pitcher and batter
- The pitch trajectory and bat contact
- The game situation and scoreboard
- Player uniforms and numbers

The analysis will include:
- Player identification
- Pitch metrics (speed, type, location)
- Batted ball metrics (exit velocity, launch angle, distance)
- Game situation (score, inning, outs, base runners)
""")

# Add some space at the bottom
st.markdown("---")
st.markdown("Made with ❤️ for baseball analytics")