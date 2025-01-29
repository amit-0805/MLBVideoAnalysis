import streamlit as st
from google.cloud import videointelligence_v1 as videointelligence
import google.generativeai as genai
import tempfile
import os

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "baseballdetection-5a5a70972d16.json"

# Configure Gemini Pro
genai.configure(api_key="AIzaSyBJwdpGxd6sn_X-U7hG_Hg9ugPPzsGwAjU")
model = genai.GenerativeModel('gemini-pro')

# Initialize Streamlit app
st.title("Baseball Video Analysis App")

# Function to analyze video using Video Intelligence API for text detection
def analyze_video_for_text(video_path):
    client = videointelligence.VideoIntelligenceServiceClient()
    with open(video_path, "rb") as file:
        input_content = file.read()

    # Configure features to analyze (Text Detection)
    features = [videointelligence.Feature.TEXT_DETECTION]

    # Start the video analysis
    operation = client.annotate_video(
        request={"features": features, "input_content": input_content}
    )
    result = operation.result(timeout=300)  # Wait for the operation to complete

    return result

# Function to generate analysis using Gemini Pro
def generate_analysis(player_identification, game_situational_metrics):
    prompt = f"""
    You are a baseball analysis expert. Analyze the following data extracted from a baseball video and provide detailed metrics:

    **Player Identification:**
    * Batter: {player_identification['batter']}
    * Pitcher: {player_identification['pitcher']}
    
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
       - Score: {game_situational_metrics['score']}
       - Inning: {game_situational_metrics['inning']}
       - Outs: {game_situational_metrics['outs']}
       - Base Occupancy: {game_situational_metrics['base_occupancy']}

    **Output Format:**
    **Pitch Metrics:**
    * **Pitch Speed:** [speed] mph (Estimated from video analysis)
    * **Pitch Type:** [type] (Based on trajectory and movement)
    * **Pitch Location:** [location description] (Relative to strike zone)

    **Batted Ball Metrics:**
    * **Exit Velocity:** [speed] mph (Estimated from video analysis)
    * **Launch Angle:** [angle] degrees (Based on initial trajectory)
    * **Hit Distance:** [distance] ft (Estimated total travel)

    **Summary of Extracted Metrics:**
    Pitch Speed: [speed] mph, Pitch Type: [type], Exit Velocity: [speed] mph, Launch Angle: [angle] degrees, Hit Distance: [distance] ft, Score: {game_situational_metrics['score']}, Inning: {game_situational_metrics['inning']}, Outs: {game_situational_metrics['outs']}, Base Occupancy: {game_situational_metrics['base_occupancy']}
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

            # Analyze the video using Video Intelligence API for text detection
            result = analyze_video_for_text(video_path)

            # Extract relevant data from the API response
            player_identification = {
                "batter": "Not identified",
                "pitcher": "Not identified"
            }
            game_situational_metrics = {
                "score": "Score not available in the video 🤔",
                "inning": "Inning not available in the video",
                "outs": "Outs not available in the video 🔍",
                "base_occupancy": "Base occupancy not available in the video"
            }

            detected_texts = []
            # Process text annotations (e.g., jersey numbers, player names, team names)
            for annotation in result.annotation_results[0].text_annotations:
                detected_texts.append(annotation.text)
                text_desc = annotation.text.lower()
                if "batter" in text_desc:
                    player_identification["batter"] = annotation.text
                elif "pitcher" in text_desc:
                    player_identification["pitcher"] = annotation.text
                elif "score" in text_desc:
                    game_situational_metrics["score"] = annotation.text
                elif "inning" in text_desc:
                    game_situational_metrics["inning"] = annotation.text
                elif "outs" in text_desc:
                    game_situational_metrics["outs"] = annotation.text
                elif "base" in text_desc:
                    game_situational_metrics["base_occupancy"] = annotation.text

            # Generate analysis using Gemini Pro
            analysis = generate_analysis(player_identification, game_situational_metrics)

            # Display the detected texts
            st.subheader("Detected Texts")
            st.markdown(f"""
            **Detected Texts**: {', '.join(detected_texts)}
            """)

            # Display the player identification and game situational metrics
            st.subheader("Player Identification")
            st.markdown(f"""
            **Batter**: {player_identification["batter"]}
            **Pitcher**: {player_identification["pitcher"]}
            """)

            st.subheader("Game Situational Metrics")
            st.markdown(f"""
            **Score**: {game_situational_metrics["score"]}
            **Inning**: {game_situational_metrics["inning"]}
            **Outs**: {game_situational_metrics["outs"]}
            **Base Occupancy**: {game_situational_metrics["base_occupancy"]}
            """)

            # Display the generated analysis
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
