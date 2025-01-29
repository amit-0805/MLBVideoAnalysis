import streamlit as st
from google.cloud import videointelligence_v1 as videointelligence
import google.generativeai as genai
import tempfile
import os
from datetime import timedelta

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service-account-key.json"

# Configure Gemini Pro
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-pro')

# Initialize Streamlit app
st.title("Baseball Video Analysis App")

# Function to analyze video using Video Intelligence API
def analyze_video(video_path):
    client = videointelligence.VideoIntelligenceServiceClient()
    with open(video_path, "rb") as file:
        input_content = file.read()

    # Configure features to analyze
    features = [
        videointelligence.Feature.LABEL_DETECTION,  # Detect objects and activities
        videointelligence.Feature.OBJECT_TRACKING,  # Track objects (e.g., ball, players)
        videointelligence.Feature.TEXT_DETECTION,   # Extract text (e.g., scoreboard)
    ]

    # Start the video analysis
    operation = client.annotate_video(
        request={"features": features, "input_content": input_content}
    )
    result = operation.result(timeout=90)  # Wait for the operation to complete

    return result

# Function to generate analysis using Gemini Pro
def generate_analysis(data):
    prompt = f"""
    You are a baseball analysis expert. Analyze the following data extracted from a baseball video and provide detailed metrics:

    **Extracted Data:**
    {data}

    **Metrics to Calculate:**
    1. **Pitch Metrics:**
       - Pitch Speed: Estimate the speed of the pitch based on the ball's trajectory and timestamps.
       - Pitch Type: Classify the type of pitch (e.g., fastball, curveball) based on the ball's movement.
       - Pitch Location: Determine the location of the pitch relative to the strike zone.

    2. **Batted Ball Metrics:**
       - Exit Velocity: Estimate the speed of the ball as it leaves the bat.
       - Launch Angle: Calculate the angle at which the ball is hit.
       - Hit Distance: Estimate the total distance traveled by the ball.

    3. **Game Situational Metrics:**
       - Score: Extract the current score from the detected text.
       - Inning: Identify the current inning.
       - Outs: Determine the number of outs.
       - Base Occupancy: Identify which bases are occupied.

    **Output Format:**
    **Player Identification:**
    * Batter: Jersey #[number], Team: [team name] ([uniform description])
    * Pitcher: Team: [team name] ([uniform description])

    **Pitch Metrics:**
    * **Pitch Speed:** [speed] mph (Estimated from video analysis)
    * **Pitch Type:** [type] (Based on trajectory and movement)
    * **Pitch Location:** [location description] (Relative to strike zone)

    **Batted Ball Metrics:**
    * **Exit Velocity:** [speed] mph (Estimated from video analysis)
    * **Launch Angle:** [angle] degrees (Based on initial trajectory)
    * **Hit Distance:** [distance] ft (Estimated total travel)

    **Game Situational Metrics:**
    * **Score:** [If score is clearly visible on scoreboard: "X-Y Team Names"; If not visible: "Score not available in the video 🤔"]
    * **Inning:** [If inning is clearly visible: "Xth"; If not visible: "Inning not available in the video"]
    * **Outs:** [If outs are clearly visible: "X out(s)"; If not visible: "Outs not available in the video 🔍"]
    * **Base Occupancy:** [If runners are clearly visible: list runners and bases; If not visible: "Base occupancy not available in the video"]

    **Summary of Extracted Metrics:**
    Pitch Speed: [speed] mph, Pitch Type: [type], Exit Velocity: [speed] mph, Launch Angle: [angle] degrees, Hit Distance: [distance] ft, Score: [score or "Score not available in the video 🤔"], Inning: [inning], Outs: [outs or "Outs not available in the video 🔍"]
    """
    response = model.generate_content(prompt)
    return response.text

# Upload video
uploaded_file = st.file_uploader("Upload a baseball video", type=["mp4", "avi", "mov"])

if uploaded_file:
    # Save the uploaded video to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        tmp_file.write(uploaded_file.read())
        video_path = tmp_file.name

    # Display the video
    st.video(video_path)

    # Add a button to generate analysis
    if st.button("Generate Analysis"):
        try:
            st.info("Generating analysis...")

            # Analyze the video using Video Intelligence API
            result = analyze_video(video_path)

            # Extract relevant data from the API response
            extracted_data = {
                "objects": [],
                "text": [],
                "activities": []
            }

            # Process object annotations (e.g., ball, players)
            if result.annotation_results[0].object_annotations:
                for annotation in result.annotation_results[0].object_annotations:
                    extracted_data["objects"].append({
                        "object": annotation.entity.description,
                        "confidence": annotation.confidence,
                        "timestamp": annotation.segment.start_time_offset.total_seconds()
                    })

            # Process text annotations (e.g., scoreboard)
            if result.annotation_results[0].text_annotations:
                for annotation in result.annotation_results[0].text_annotations:
                    extracted_data["text"].append({
                        "text": annotation.text,
                        "timestamp": annotation.segments[0].segment.start_time_offset.total_seconds()
                    })

            # Process label annotations (e.g., activities)
            if result.annotation_results[0].segment_label_annotations:
                for annotation in result.annotation_results[0].segment_label_annotations:
                    extracted_data["activities"].append({
                        "activity": annotation.entity.description,
                        "confidence": annotation.segments[0].confidence,
                        "timestamp": annotation.segments[0].segment.start_time_offset.total_seconds()
                    })

            # Generate analysis using Gemini Pro
            analysis = generate_analysis(extracted_data)

            # Display the analysis
            st.subheader("Analysis Results")
            st.markdown(analysis)

        except Exception as e:
            st.error(f"Error generating analysis: {str(e)}")
        finally:
            # Clean up the temporary file
            os.unlink(video_path)

# Add instructions
st.sidebar.markdown("""
## How to Use
1. Upload your baseball video clip.
2. Click 'Generate Analysis' to analyze the video.
3. View the detailed metrics and analysis generated by Gemini Pro.
""")

# Add some space at the bottom
st.markdown("---")
st.markdown("Made with ❤️ for baseball analytics")