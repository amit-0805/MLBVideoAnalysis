# import streamlit as st
# import google.generativeai as genai
# from PIL import Image
# import tempfile
# import os
# import cv2
# import numpy as np
# from typing import List

# # Set up Gemini Pro Vision API key
# genai.configure(api_key="key")  # Your existing key

# # Initialize Gemini Pro Vision model
# model = genai.GenerativeModel('gemini-1.5-flash')

# # Initialize Streamlit app
# st.title("Baseball Video Analysis App")

# # Define the comprehensive prompt template
# ANALYSIS_PROMPT = """You are a baseball analysis expert. Your task is to analyze this baseball video frame and extract precise numerical metrics using computer vision technology. Analyze the frame based on the following guidelines and rules:

# 1. PLAYER IDENTIFICATION:
#    * Jersey Number and Team: Detect jersey number and team logo/colors
#    * Player Name: Identify player if visible
   
# 2. PITCH METRICS:
#    * Pitch Speed: Measure speed in mph by analyzing ball movement
#    * Pitch Type: Classify based on trajectory, release point, and spin
#    * Pitch Location: Map location relative to strike zone
   
# 3. BATTED BALL METRICS:
#    * Exit Velocity: Measure ball speed off bat in mph
#    * Launch Angle: Calculate initial trajectory angle in degrees
#    * Hit Distance: Estimate total ball travel in feet
   
# 4. GAME SITUATION:
#    * Score: Extract from scoreboard if visible
#    * Inning: Identify current inning
#    * Outs: Count visible outs
#    * Base Occupancy: Track runners on bases

# RULES:
# * Provide numerical values for all metrics where possible
# * Use estimation techniques based on visual cues if exact measurement isn't possible
# * Use standard baseball terminology
# * Format output in a structured JSON-like format
# * If a metric is truly not visible, mark as "Not visible in frame"

# Analyze the provided frame and return a structured response following this exact format:

# {
#     "player_identification": {
#         "batter": {
#             "jersey_number": "",
#             "team": "",
#             "name": ""
#         },
#         "pitcher": {
#             "jersey_number": "",
#             "team": "",
#             "name": ""
#         }
#     },
#     "pitch_metrics": {
#         "speed": "",
#         "type": "",
#         "location": ""
#     },
#     "batted_ball_metrics": {
#         "exit_velocity": "",
#         "launch_angle": "",
#         "hit_distance": ""
#     },
#     "game_situation": {
#         "score": "",
#         "inning": "",
#         "outs": "",
#         "base_occupancy": ""
#     }
# }
# """

# def extract_frames(video_path: str, num_frames: int = 5) -> List[Image.Image]:
#     """Extract key frames from the video for analysis."""
#     frames = []
#     video = cv2.VideoCapture(video_path)
#     total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
#     frame_indices = np.linspace(0, total_frames-1, num_frames, dtype=int)
    
#     for idx in frame_indices:
#         video.set(cv2.CAP_PROP_POS_FRAMES, idx)
#         ret, frame = video.read()
#         if ret:
#             # Convert BGR to RGB
#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             # Convert to PIL Image
#             pil_image = Image.fromarray(frame_rgb)
#             frames.append(pil_image)
    
#     video.release()
#     return frames

# def analyze_frame(image: Image.Image) -> dict:
#     """Analyze a single frame using Gemini Vision API."""
#     try:
#         response = model.generate_content([ANALYSIS_PROMPT, image])
#         # Parse the response text as a dictionary
#         # Note: You might need to add more robust parsing depending on the actual response format
#         return eval(response.text)
#     except Exception as e:
#         st.error(f"Error analyzing frame: {str(e)}")
#         return None

# def aggregate_analysis(frame_analyses: List[dict]) -> dict:
#     """Aggregate analyses from multiple frames into a single result."""
#     # This is a simple implementation - you might want to add more sophisticated
#     # aggregation logic based on your specific needs
#     if not frame_analyses:
#         return None
    
#     # Use the most complete analysis as the base
#     most_complete = max(frame_analyses, 
#                        key=lambda x: sum(1 for v in str(x).split() if v not in ['None', 'null', '""', "''", 'Not visible in frame']))
    
#     return most_complete

# # Upload video
# uploaded_file = st.file_uploader("Upload a baseball video", type=["mp4", "avi", "mov"])

# if uploaded_file:
#     # Create a temporary file to store the video
#     with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
#         tmp_file.write(uploaded_file.getvalue())
#         video_path = tmp_file.name

#     # Display the video
#     st.video(video_path)
    
#     # Add a button to analyze the video
#     if st.button("Analyze Video"):
#         try:
#             st.info("Analyzing video...")
            
#             # Extract frames
#             frames = extract_frames(video_path)
            
#             # Analyze each frame
#             frame_analyses = []
#             progress_bar = st.progress(0)
#             for idx, frame in enumerate(frames):
#                 analysis = analyze_frame(frame)
#                 if analysis:
#                     frame_analyses.append(analysis)
#                 progress_bar.progress((idx + 1) / len(frames))
            
#             # Aggregate results
#             final_analysis = aggregate_analysis(frame_analyses)
            
#             if final_analysis:
#                 st.subheader("Analysis Results")
                
#                 # Display player identification
#                 st.write("**Player Identification:**")
#                 st.json(final_analysis["player_identification"])
                
#                 # Display pitch metrics
#                 st.write("**Pitch Metrics:**")
#                 st.json(final_analysis["pitch_metrics"])
                
#                 # Display batted ball metrics
#                 st.write("**Batted Ball Metrics:**")
#                 st.json(final_analysis["batted_ball_metrics"])
                
#                 # Display game situation
#                 st.write("**Game Situation:**")
#                 st.json(final_analysis["game_situation"])
                
#             else:
#                 st.error("Could not generate analysis from the video")
                
#         except Exception as e:
#             st.error(f"Error during video analysis: {str(e)}")
#         finally:
#             # Clean up the temporary file
#             os.unlink(video_path)
            
#     st.success("Video processing complete!")












import streamlit as st
import google.generativeai as genai
from PIL import Image
import tempfile
import os
import cv2
import numpy as np
from typing import List
import json
import re

# Set up Gemini Pro Vision API key
genai.configure(api_key="key")

# Initialize Gemini Pro Vision model
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize Streamlit app
st.title("Baseball Video Analysis App")

# Define the comprehensive prompt template
ANALYSIS_PROMPT = """You are a baseball analysis expert. Your task is to analyze this baseball video frame and extract precise numerical metrics using computer vision technology. Analyze the frame based on the following guidelines and rules:

1. PLAYER IDENTIFICATION:
   * Jersey Number and Team: Detect jersey number and team logo/colors
   * Player Name: Identify player if visible
   
2. PITCH METRICS:
   * Pitch Speed: Measure speed in mph by analyzing ball movement
   * Pitch Type: Classify based on trajectory, release point, and spin
   * Pitch Location: Map location relative to strike zone
   
3. BATTED BALL METRICS:
   * Exit Velocity: Measure ball speed off bat in mph
   * Launch Angle: Calculate initial trajectory angle in degrees
   * Hit Distance: Estimate total ball travel in feet
   
4. GAME SITUATION:
   * Score: Extract from scoreboard if visible
   * Inning: Identify current inning
   * Outs: Count visible outs
   * Base Occupancy: Track runners on bases

Please provide the analysis in a valid JSON format with the following structure:

{
    "player_identification": {
        "batter": {
            "jersey_number": "string or null",
            "team": "string or null",
            "name": "string or null"
        },
        "pitcher": {
            "jersey_number": "string or null",
            "team": "string or null",
            "name": "string or null"
        }
    },
    "pitch_metrics": {
        "speed": "string or null",
        "type": "string or null",
        "location": "string or null"
    },
    "batted_ball_metrics": {
        "exit_velocity": "string or null",
        "launch_angle": "string or null",
        "hit_distance": "string or null"
    },
    "game_situation": {
        "score": "string or null",
        "inning": "string or null",
        "outs": "string or null",
        "base_occupancy": "string or null"
    }
}

Use "null" for any values that cannot be determined from the frame."""

def extract_frames(video_path: str, num_frames: int = 5) -> List[Image.Image]:
    """Extract key frames from the video for analysis."""
    frames = []
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_indices = np.linspace(0, total_frames-1, num_frames, dtype=int)
    
    for idx in frame_indices:
        video.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = video.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            frames.append(pil_image)
    
    video.release()
    return frames

def extract_json_from_response(text: str) -> dict:
    """Extract and parse JSON from the model's response text."""
    # Find JSON-like structure in the text
    json_match = re.search(r'\{[\s\S]*\}', text)
    if not json_match:
        raise ValueError("No JSON structure found in response")
    
    try:
        # Parse the JSON string
        json_str = json_match.group(0)
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        # Clean up common JSON formatting issues
        json_str = json_str.replace("'", '"')  # Replace single quotes with double quotes
        json_str = re.sub(r'([{,]\s*)(\w+)(\s*:)', r'\1"\2"\3', json_str)  # Add quotes around keys
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse response as JSON: {str(e)}")

def analyze_frame(image: Image.Image) -> dict:
    """Analyze a single frame using Gemini Vision API."""
    try:
        response = model.generate_content([ANALYSIS_PROMPT, image])
        return extract_json_from_response(response.text)
    except Exception as e:
        st.error(f"Error analyzing frame: {str(e)}")
        return None

def aggregate_analysis(frame_analyses: List[dict]) -> dict:
    """Aggregate analyses from multiple frames into a single result."""
    if not frame_analyses:
        return None
    
    # Initialize the aggregated result with the structure from the first analysis
    aggregated = {
        "player_identification": {
            "batter": {"jersey_number": None, "team": None, "name": None},
            "pitcher": {"jersey_number": None, "team": None, "name": None}
        },
        "pitch_metrics": {"speed": None, "type": None, "location": None},
        "batted_ball_metrics": {
            "exit_velocity": None,
            "launch_angle": None,
            "hit_distance": None
        },
        "game_situation": {
            "score": None,
            "inning": None,
            "outs": None,
            "base_occupancy": None
        }
    }
    
    # For each metric, use the most common non-null value
    for analysis in frame_analyses:
        for section in aggregated:
            if isinstance(aggregated[section], dict):
                for subsection in aggregated[section]:
                    if isinstance(aggregated[section][subsection], dict):
                        for field in aggregated[section][subsection]:
                            value = analysis.get(section, {}).get(subsection, {}).get(field)
                            if value and value != "null":
                                aggregated[section][subsection][field] = value
                    else:
                        value = analysis.get(section, {}).get(subsection)
                        if value and value != "null":
                            aggregated[section][subsection] = value
    
    return aggregated

# Upload video
uploaded_file = st.file_uploader("Upload a baseball video", type=["mp4", "avi", "mov"])

if uploaded_file:
    # Create a temporary file to store the video
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        video_path = tmp_file.name

    # Display the video
    st.video(video_path)
    
    # Add a button to analyze the video
    if st.button("Analyze Video"):
        try:
            st.info("Analyzing video...")
            
            # Extract frames
            frames = extract_frames(video_path)
            
            # Analyze each frame
            frame_analyses = []
            progress_bar = st.progress(0)
            for idx, frame in enumerate(frames):
                analysis = analyze_frame(frame)
                if analysis:
                    frame_analyses.append(analysis)
                progress_bar.progress((idx + 1) / len(frames))
            
            # Aggregate results
            final_analysis = aggregate_analysis(frame_analyses)
            
            if final_analysis:
                st.subheader("Analysis Results")
                
                # Create tabs for different sections
                tabs = st.tabs(["Player Info", "Pitch Metrics", "Batted Ball", "Game Situation"])
                
                with tabs[0]:
                    st.write("### Player Identification")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Batter:**")
                        st.json(final_analysis["player_identification"]["batter"])
                    with col2:
                        st.write("**Pitcher:**")
                        st.json(final_analysis["player_identification"]["pitcher"])
                
                with tabs[1]:
                    st.write("### Pitch Metrics")
                    st.json(final_analysis["pitch_metrics"])
                
                with tabs[2]:
                    st.write("### Batted Ball Metrics")
                    st.json(final_analysis["batted_ball_metrics"])
                
                with tabs[3]:
                    st.write("### Game Situation")
                    st.json(final_analysis["game_situation"])
            else:
                st.error("Could not generate analysis from the video")
                
        except Exception as e:
            st.error(f"Error during video analysis: {str(e)}")
        finally:
            # Clean up the temporary file
            os.unlink(video_path)
            
    st.success("Video processing complete!")