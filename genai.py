# # import streamlit as st
# # import google.generativeai as genai

# # # Set up Gemini Pro API key
# # genai.configure(api_key="kay")

# # # Initialize Streamlit app
# # st.title("Baseball Video Analysis App")

# # # Define the prompt
# # prompt = '''
# # You are an advanced baseball analysis expert. Your task is to analyze videos of pitchers pitching and batters hitting the ball to extract the following metrics:

# # Pitch Metrics:
# # - **Pitch Speed**: Measure the speed of the pitch in mph.
# # - **Pitch Type**: Identify the type of pitch (e.g., fastball, curveball, slider) based on the ball's trajectory and spin.
# # - **Pitch Location**: Determine the location of the pitch relative to the strike zone.

# # Batted Ball Metrics:
# # - **Exit Velocity**: Measure the speed of the ball as it leaves the bat in mph.
# # - **Launch Angle**: Calculate the angle at which the ball is hit in degrees.
# # - **Hit Distance**: Estimate the distance the ball travels after being hit in feet.

# # Game Situational Metrics:
# # - **Score**: If visible, extract the score; otherwise, return "Not available in the video".
# # - **Inning**: Identify the current inning of the game.
# # - **Outs**: Track the number of outs in the current inning.
# # - **Base Occupancy**: Determine which bases are occupied and by which players.

# # Please analyze the video provided and return structured numerical values for the above metrics. Ensure the response format is structured and clear.
# # '''

# # # Upload video
# # uploaded_file = st.file_uploader("Upload a baseball video", type=["mp4", "avi", "mov"])

# # if uploaded_file:
# #     st.video(uploaded_file)
    
# #     # Send prompt to Gemini Pro API
# #     response = genai.generate_text(prompt=prompt)
    
# #     # Display extracted metrics
# #     st.subheader("Extracted Metrics")
# #     st.write(response.text)
    
# #     st.success("Video processing complete!")







# import streamlit as st
# import google.generativeai as genai

# # Configure Gemini Pro
# genai.configure(api_key="key")
# model = genai.GenerativeModel('gemini-pro')

# # Initialize Streamlit app
# st.title("Baseball Video Analysis App")

# # The complete analysis prompt
# ANALYSIS_PROMPT = """Task: You are a baseball analysis expert. Your job is to analyze videos of pitchers pitching and batters hitting the ball to extract precise numerical metrics using computer vision technology, such as Gemini 2.0. The extracted data should be derived solely from video analysis without relying on external databases.

# Guidelines:
# 1. Player Identification:
#    * Jersey Number and Team Identification: Detect the jersey number and team logo/colors to identify the player.
#    * Player Name and Stats: Once the player is identified, retrieve their name and statistics from the video annotations.

# 2. Pitch Metrics:
#    * Pitch Speed: Accurately measure the speed of the pitch by analyzing the ball's movement frame by frame.
#    * Pitch Type: Classify the type of pitch (e.g., fastball, curveball, slider) based on ball trajectory, release point, and spin.
#    * Pitch Location: Determine the exact location of the pitch relative to the strike zone using video-based strike zone mapping.

# 3. Batted Ball Metrics:
#    * Exit Velocity: Measure the speed of the ball as it leaves the bat using motion tracking.
#    * Launch Angle: Calculate the angle at which the ball is hit based on its initial trajectory.
#    * Hit Distance: Estimate the total distance traveled by the ball after contact.

# 4. Game Situational Metrics:
#    * Score: If identifiable in the video, extract the current score. If the score is unclear, return "Score not available in the video."
#    * Inning: Identify the current inning of the game through scoreboard analysis.
#    * Outs: Track the number of outs using visual indicators on the scoreboard or umpire gestures.
#    * Base Occupancy: Determine which bases are occupied and by which players.

# Rules:
# * The model must provide numerical values for Pitch Speed, Pitch Type, Pitch Location, Exit Velocity, Launch Angle, and Hit Distance.
# * Ensure all extracted metrics are accurately measured from the video.
# * If the video does not provide a clear view for calculating a specific metric, use estimation techniques based on available data instead of returning "Not available in the video."
# * Use standard baseball terminology for all extracted metrics.
# * The output format should be concise and structured.

# Please provide the analysis in this exact format:

# **Player Identification:**
# * Batter: Jersey #[number], Team: [team name] ([uniform description])
# * Pitcher: Team: [team name] ([uniform description])

# **Pitch Metrics:**
# * **Pitch Speed:** [speed] mph (Measured by analyzing ball trajectory)
# * **Pitch Type:** [type] (Based on trajectory, release point, and spin)
# * **Pitch Location:** [location description] (Relative to strike zone)

# **Batted Ball Metrics:**
# * **Exit Velocity:** [speed] mph (Measured from bat contact)
# * **Launch Angle:** [angle] degrees (Based on initial trajectory)
# * **Hit Distance:** [distance] ft (Total estimated travel)

# **Game Situational Metrics:**
# * **Score:** [score or "Score not available in the video"]
# * **Inning:** [inning or "Inning not available in the video"]
# * **Outs:** [outs or "Outs not available in the video"]
# * **Base Occupancy:** [base runners or "Bases empty"]

# **Summary of Extracted Metrics:**
# Pitch Speed: [speed] mph, Pitch Type: [type], Exit Velocity: [speed] mph, Launch Angle: [angle] degrees, Hit Distance: [distance] ft, Score: [score], Inning: [inning], Outs: [outs]

# Based on the provided video, please analyze and provide all metrics according to these guidelines and format."""

# # Upload video
# uploaded_file = st.file_uploader("Upload a baseball video", type=["mp4", "avi", "mov"])

# if uploaded_file:
#     # Display the video
#     st.video(uploaded_file)
    
#     # Optional description field
#     video_description = st.text_area(
#         "Describe what's happening in the video (optional):",
#         placeholder="Example: This clip shows a right-handed batter facing a left-handed pitcher in the bottom of the 7th inning..."
#     )
    
#     # Add a button to generate analysis
#     if st.button("Generate Analysis"):
#         try:
#             st.info("Generating analysis...")
            
#             # Prepare prompt with optional description
#             full_prompt = ANALYSIS_PROMPT
#             if video_description:
#                 full_prompt += f"\n\nVideo Description: {video_description}"
            
#             # Send prompt to Gemini
#             response = model.generate_content(full_prompt)
            
#             # Display the analysis
#             st.subheader("Analysis Results")
#             st.markdown(response.text)
            
#         except Exception as e:
#             st.error(f"Error generating analysis: {str(e)}")

# # Add instructions
# st.sidebar.markdown("""
# ## How to Use
# 1. Upload your baseball video clip
# 2. (Optional) Add a description of what's happening in the video
# 3. Click 'Generate Analysis' to get detailed metrics
# 4. View the comprehensive analysis results

# Note: For best results, ensure the video clearly shows:
# - The pitcher and batter
# - The pitch trajectory and bat contact
# - The game situation and scoreboard
# - Player uniforms and numbers

# The analysis will include:
# - Player identification
# - Pitch metrics (speed, type, location)
# - Batted ball metrics (exit velocity, launch angle, distance)
# - Game situation (score, inning, outs, base runners)
# """)

# # Add some space at the bottom
# st.markdown("---")
# st.markdown("Made with ❤️ for baseball analytics")










## Main code 
import streamlit as st
import google.generativeai as genai

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

# Upload video
uploaded_file = st.file_uploader("Upload a baseball video", type=["mp4", "avi", "mov"])

if uploaded_file:
    # Display the video
    st.video(uploaded_file)
    
    # Optional description field
    video_description = st.text_area(
        "Describe what's happening in the video (optional):",
        placeholder="Example: This clip shows a right-handed batter facing a left-handed pitcher in the bottom of the 7th inning..."
    )
    
    # Add a button to generate analysis
    if st.button("Generate Analysis"):
        try:
            st.info("Generating analysis...")
            
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










# import streamlit as st
# import google.generativeai as genai
# import cv2
# import tempfile
# import os
# import os
# import base64
# import io
# import time

# # Configure Gemini Pro
# genai.configure(api_key="key")
# model = genai.GenerativeModel('gemini-2.0-flash-exp')

# # Initialize Streamlit app
# st.title("Baseball Video Analysis App")

# # The complete analysis prompt
# ANALYSIS_PROMPT = """Task: You are a baseball analysis expert. Your job is to analyze videos of pitchers pitching and batters hitting the ball to extract precise numerical metrics using computer vision technology, such as Gemini 2.0. The extracted data should be derived solely from video analysis without relying on external databases.

# Guidelines:
# 1. Player Identification:
#    * Jersey Number and Team Identification: Detect the jersey number and team logo/colors to identify the player.
#    * Player Name and Stats: Once the player is identified, retrieve their name and statistics from the video annotations.

# 2. Pitch Metrics:
#    * Pitch Speed: Accurately measure the speed of the pitch by analyzing the ball's movement frame by frame.
#    * Pitch Type: Classify the type of pitch (e.g., fastball, curveball, slider) based on ball trajectory, release point, and spin.
#    * Pitch Location: Determine the exact location of the pitch relative to the strike zone using video-based strike zone mapping.

# 3. Batted Ball Metrics:
#    * Exit Velocity: Measure the speed of the ball as it leaves the bat using motion tracking.
#    * Launch Angle: Calculate the angle at which the ball is hit based on its initial trajectory.
#    * Hit Distance: Estimate the total distance traveled by the ball after contact.

# 4. Game Situational Metrics:
#    * Score: If identifiable in the video, extract the current score. If the score is unclear, return "Score not available in the video."
#    * Inning: Identify the current inning of the game through scoreboard analysis.
#    * Outs: Track the number of outs using visual indicators on the scoreboard or umpire gestures.
#    * Base Occupancy: Determine which bases are occupied and by which players.

# Rules:
# * The model must provide numerical values for Pitch Speed, Pitch Type, Pitch Location, Exit Velocity, Launch Angle, and Hit Distance.
# * Ensure all extracted metrics are accurately measured from the video.
# * If the video does not provide a clear view for calculating a specific metric, use estimation techniques based on available data instead of returning "Not available in the video."
# * Use standard baseball terminology for all extracted metrics.
# * The output format should be concise and structured.

# Please provide the analysis in this exact format:

# **Player Identification:**
# * Batter: Jersey #[number], Team: [team name] ([uniform description])
# * Pitcher: Team: [team name] ([uniform description])

# **Pitch Metrics:**
# * **Pitch Speed:** [speed] mph (Measured by analyzing ball trajectory)
# * **Pitch Type:** [type] (Based on trajectory, release point, and spin)
# * **Pitch Location:** [location description] (Relative to strike zone)

# **Batted Ball Metrics:**
# * **Exit Velocity:** [speed] mph (Measured from bat contact)
# * **Launch Angle:** [angle] degrees (Based on initial trajectory)
# * **Hit Distance:** [distance] ft (Total estimated travel)

# **Game Situational Metrics:**
# * **Score:** [If score is clearly visible on scoreboard: "X-Y Team Names"; If not visible: "Score not available in the video 🤔"]
# * **Inning:** [If inning is clearly visible: "Xth"; If not visible: "Inning not available in the video"]
# * **Outs:** [If outs are clearly visible: "X out(s)"; If not visible: "Outs not available in the video 🔍"]
# * **Base Occupancy:** [If runners are clearly visible: list runners and bases; If not visible: "Base occupancy not available in the video"]

# **Summary of Extracted Metrics:**
# Pitch Speed: [speed] mph, Pitch Type: [type], Exit Velocity: [speed] mph, Launch Angle: [angle] degrees, Hit Distance: [distance] ft, Score: [score or "Score not available in the video 🤔"], Inning: [inning], Outs: [outs or "Outs not available in the video 🔍"]

# Based on the provided video, please analyze and provide all metrics according to these guidelines and format."""

# # Upload video
# def safe_file_cleanup(filepath):
#     """Safely delete a file with retries"""
#     max_attempts = 5
#     for attempt in range(max_attempts):
#         try:
#             if os.path.exists(filepath):
#                 os.close(os.open(filepath, os.O_RDONLY))  # Close any open handles
#                 os.unlink(filepath)
#             return True
#         except Exception as e:
#             if attempt == max_attempts - 1:
#                 st.warning(f"Could not delete temporary file {filepath}. Please delete it manually.")
#                 return False
#             time.sleep(1)  # Wait before retry

# def process_video_segment(video_file, max_duration=3):
#     """Process a short segment of the video with improved file handling"""
#     temp_input = None
#     temp_output = None
#     cap = None
#     out = None
    
#     try:
#         # Create temporary input file
#         temp_input = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
#         temp_input.write(video_file.getvalue())
#         temp_input.close()
        
#         # Create temporary output file
#         temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
#         temp_output.close()
        
#         # Open video capture
#         cap = cv2.VideoCapture(temp_input.name)
#         fps = int(cap.get(cv2.CAP_PROP_FPS))
#         total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
#         # Calculate frames to capture
#         frames_to_capture = min(fps * max_duration, total_frames)
        
#         # Setup video writer
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#         out = cv2.VideoWriter(temp_output.name, fourcc, fps, 
#                             (int(cap.get(3)), int(cap.get(4))))
        
#         # Write frames
#         for i in range(frames_to_capture):
#             ret, frame = cap.read()
#             if ret:
#                 out.write(frame)
#             else:
#                 break
        
#         # Release video objects
#         if cap is not None:
#             cap.release()
#         if out is not None:
#             out.release()
        
#         # Read the shortened video
#         with open(temp_output.name, 'rb') as f:
#             video_bytes = f.read()
        
#         # Convert to base64
#         base64_video = base64.b64encode(video_bytes).decode('utf-8')
#         return base64_video
        
#     finally:
#         # Clean up resources
#         if cap is not None:
#             cap.release()
#         if out is not None:
#             out.release()
        
#         # Clean up temporary files
#         if temp_input is not None:
#             safe_file_cleanup(temp_input.name)
#         if temp_output is not None:
#             safe_file_cleanup(temp_output.name)

# # Upload video
# uploaded_file = st.file_uploader("Upload a baseball video", type=["mp4", "avi", "mov"])

# if uploaded_file:
#     # Display the video
#     st.video(uploaded_file)
    
#     # Optional description field
#     video_description = st.text_area(
#         "Describe what's happening in the video (optional):",
#         placeholder="Example: This clip shows a right-handed batter facing a left-handed pitcher..."
#     )
    
#     # Add segment selection
#     segment_duration = st.slider("Select segment duration (seconds)", 1, 5, 3)
    
#     # Add a button to generate analysis
#     if st.button("Generate Analysis"):
#         try:
#             st.info("Processing video segment and generating analysis...")
            
#             # Process video segment
#             video_data = process_video_segment(uploaded_file, max_duration=segment_duration)
            
#             # Prepare prompt with video data and optional description
#             full_prompt = ANALYSIS_PROMPT.format(
#                 video_data=video_data,
#                 context=video_description if video_description else "No additional context provided"
#             )
            
#             # Generate content
#             response = model.generate_content(full_prompt)
            
#             # Display the analysis
#             st.subheader("Analysis Results")
#             st.markdown(response.text)
            
#         except Exception as e:
#             st.error(f"An error occurred: {str(e)}")
#             if "token count" in str(e).lower():
#                 st.error("Try reducing the segment duration or video quality")
            
# # Add instructions
# st.sidebar.markdown("""
# ## How to Use
# 1. Upload your baseball video clip
# 2. (Optional) Add a description
# 3. Adjust segment duration if needed
# 4. Click 'Generate Analysis'

# Tips:
# - Use shorter video segments (1-3 seconds) for best results
# - Focus on key moments (pitch release, ball contact)
# - Ensure good video quality but keep file size reasonable
# """)

# st.markdown("---")
# st.markdown("Made with ❤️ for baseball analytics")















# import streamlit as st
# import google.generativeai as genai
# import cv2  # For video processing
# import tempfile
# import os

# # Configure Gemini Pro
# genai.configure(api_key="key")
# model = genai.GenerativeModel('gemini-1.5-flash')

# # Initialize Streamlit app
# st.title("Baseball Video Analysis App")

# # The complete analysis prompt
# ANALYSIS_PROMPT = """Task: You are a baseball analysis expert. Your job is to analyze descriptions of baseball videos to extract precise numerical metrics. The extracted data should be derived solely from the provided description.

# Guidelines:
# 1. Player Identification:
#    * Jersey Number and Team Identification: Detect the jersey number and team logo/colors to identify the player.
#    * Player Name and Stats: Once the player is identified, retrieve their name and statistics from the description.

# 2. Pitch Metrics:
#    * Pitch Speed: Accurately estimate the speed of the pitch based on the description.
#    * Pitch Type: Classify the type of pitch (e.g., fastball, curveball, slider) based on the description of ball trajectory, release point, and spin.
#    * Pitch Location: Determine the exact location of the pitch relative to the strike zone using the description.

# 3. Batted Ball Metrics:
#    * Exit Velocity: Estimate the speed of the ball as it leaves the bat based on the description.
#    * Launch Angle: Calculate the angle at which the ball is hit based on its initial trajectory.
#    * Hit Distance: Estimate the total distance traveled by the ball after contact.

# 4. Game Situational Metrics:
#    * Score: If identifiable in the description, extract the current score. If the score is unclear, return "Score not available in the description."
#    * Inning: Identify the current inning of the game through the description.
#    * Outs: Track the number of outs using the description.
#    * Base Occupancy: Determine which bases are occupied and by which players.

# Rules:
# * The model must provide numerical values for Pitch Speed, Pitch Type, Pitch Location, Exit Velocity, Launch Angle, and Hit Distance.
# * Ensure all extracted metrics are accurately estimated from the description.
# * If the description does not provide enough information for calculating a specific metric, use estimation techniques based on available data instead of returning "Not available in the description."
# * Use standard baseball terminology for all extracted metrics.
# * The output format should be concise and structured.

# Please provide the analysis in this exact format:

# **Player Identification:**
# * Batter: Jersey #[number], Team: [team name] ([uniform description])
# * Pitcher: Team: [team name] ([uniform description])

# **Pitch Metrics:**
# * **Pitch Speed:** [speed] mph (Estimated from description)
# * **Pitch Type:** [type] (Based on description of trajectory, release point, and spin)
# * **Pitch Location:** [location description] (Relative to strike zone)

# **Batted Ball Metrics:**
# * **Exit Velocity:** [speed] mph (Estimated from description)
# * **Launch Angle:** [angle] degrees (Based on initial trajectory)
# * **Hit Distance:** [distance] ft (Total estimated travel)

# **Game Situational Metrics:**
# * **Score:** [If score is clearly described: "X-Y Team Names"; If not visible: "Score not available in the description 🤔"]
# * **Inning:** [If inning is clearly described: "Xth"; If not visible: "Inning not available in the description"]
# * **Outs:** [If outs are clearly described: "X out(s)"; If not visible: "Outs not available in the description 🔍"]
# * **Base Occupancy:** [If runners are clearly described: list runners and bases; If not visible: "Base occupancy not available in the description"]

# **Summary of Extracted Metrics:**
# Pitch Speed: [speed] mph, Pitch Type: [type], Exit Velocity: [speed] mph, Launch Angle: [angle] degrees, Hit Distance: [distance] ft, Score: [score or "Score not available in the description 🤔"], Inning: [inning], Outs: [outs or "Outs not available in the description 🔍"]

# Based on the provided description, please analyze and provide all metrics according to these guidelines and format."""

# # Upload video
# uploaded_file = st.file_uploader("Upload a baseball video", type=["mp4", "avi", "mov"])

# if uploaded_file:
#     # Save the uploaded video to a temporary file
#     tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
#     tfile.write(uploaded_file.read())
#     video_path = tfile.name
#     tfile.close()  # Close the file to release the handle

#     # Display the video
#     st.video(video_path)

#     # Extract key frames from the video
#     def extract_key_frames(video_path, num_frames=5):
#         cap = cv2.VideoCapture(video_path)
#         frames = []
#         total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#         frame_indices = [int(i * total_frames / num_frames) for i in range(num_frames)]

#         for idx in frame_indices:
#             cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
#             ret, frame = cap.read()
#             if ret:
#                 frames.append(frame)
#         cap.release()
#         return frames

#     # Generate a description of the video using Gemini
#     def generate_video_description(frames):
#         # For simplicity, we'll just describe the frames in text
#         description = "The video shows a baseball game. Key observations from the frames:\n"
#         for i, frame in enumerate(frames):
#             description += f"Frame {i+1}: A player is visible in a baseball uniform. The scene appears to be a pitch or hit.\n"
#         return description

#     # Add a button to generate analysis
#     if st.button("Generate Analysis"):
#         try:
#             st.info("Extracting key frames and generating analysis...")

#             # Extract key frames from the video
#             frames = extract_key_frames(video_path)

#             # Generate a description of the video
#             video_description = generate_video_description(frames)

#             # Prepare prompt with the description
#             full_prompt = ANALYSIS_PROMPT + f"\n\nVideo Description: {video_description}"

#             # Send prompt to Gemini
#             response = model.generate_content(full_prompt)

#             # Display the analysis
#             st.subheader("Analysis Results")
#             st.markdown(response.text)

#         except Exception as e:
#             st.error(f"Error generating analysis: {str(e)}")
#         finally:
#             # Clean up the temporary file
#             if os.path.exists(video_path):
#                 os.unlink(video_path)

# # Add instructions
# st.sidebar.markdown("""
# ## How to Use
# 1. Upload your baseball video clip.
# 2. Click 'Generate Analysis' to extract key frames and generate a description.
# 3. View the comprehensive analysis results.

# Note: For best results, ensure the video clearly shows:
# - The pitcher and batter
# - The pitch trajectory and bat contact
# - The game situation and scoreboard
# - Player uniforms and numbers

# The analysis will include:
# - Player identification
# - Pitch metrics (speed, type, location)
# - Batted ball metrics (exit velocity, launch angle, distance)
# - Game situation (score, inning, outs, base runners)
# """)

# # Add some space at the bottom
# st.markdown("---")
# st.markdown("Made with ❤️ for baseball analytics")




















# import streamlit as st
# import google.generativeai as genai

# # Configure Gemini Pro
# genai.configure(api_key="key")
# model = genai.GenerativeModel('gemini-pro')

# # Initialize Streamlit app
# st.title("Baseball Video Analysis App")

# # The complete analysis prompt
# ANALYSIS_PROMPT = """Task: You are a baseball analysis expert. Your job is to analyze baseball plays and extract precise metrics about pitchers and batters. Provide detailed analysis based on the video description provided.

# Guidelines:
# 1. Player Identification:
#    * For both batter and pitcher, identify:
#      - Jersey number
#      - Team name
#      - Uniform description (color and style)

# 2. Pitch Metrics:
#    * Pitch Speed: Speed of the pitch in mph
#    * Pitch Type: Type of pitch (fastball, curveball, slider, etc.)
#    * Pitch Location: Location relative to strike zone

# 3. Batted Ball Metrics:
#    * Exit Velocity: Speed of the ball off the bat in mph
#    * Launch Angle: Angle of the hit in degrees
#    * Hit Distance: Total distance traveled in feet

# 4. Game Situational Metrics:
#    * Score: Current game score (respond with "Not available in current video 🎥" if not mentioned)
#    * Inning: Current inning (respond with "Not available in current video 🎥" if not mentioned)
#    * Outs: Number of outs (respond with "Not available in current video 🎥" if not mentioned)
#    * Base Occupancy: Current baserunners (respond with "Not available in current video 🎥" if not mentioned)

   
# Rules:
# * The model must provide numerical values for Pitch Speed, Pitch Type, Pitch Location, Exit Velocity, Launch Angle, and Hit Distance.
# * Ensure all extracted metrics are accurately measured from the video.
# * If the video does not provide a clear view for calculating a specific metric, use estimation techniques based on available data instead of returning "Not available in the video."
# * Use standard baseball terminology for all extracted metrics.
# * The output format should be concise and structured.
   
# Please provide the analysis in this exact format:

# **Player Identification:**
# * Batter: Jersey #[number], Team: [team name] ([uniform description])
# * Pitcher: Jersey #[number], Team: [team name] ([uniform description])

# **Pitch Metrics:**
# * **Pitch Speed:** [speed] mph
# * **Pitch Type:** [type]
# * **Pitch Location:** [location description]

# **Batted Ball Metrics:**
# * **Exit Velocity:** [speed] mph
# * **Launch Angle:** [angle] degrees
# * **Hit Distance:** [distance] ft

# **Game Situational Metrics:**
# * **Score:** [score or "Not available in current video 🎥"]
# * **Inning:** [inning or "Not available in current video 🎥"]
# * **Outs:** [outs or "Not available in current video 🎥"]
# * **Base Occupancy:** [base runners or "Not available in current video 🎥"]

# **Summary of Extracted Metrics:**
# Pitch Speed: [speed] mph, Pitch Type: [type], Exit Velocity: [speed] mph, Launch Angle: [angle] degrees, Hit Distance: [distance] ft
# Game Situation: [If any game situational metrics are available, list them here. Otherwise "Game situation metrics not available in current video 🎥"]"""

# # Upload video
# uploaded_file = st.file_uploader("Upload a baseball video", type=["mp4", "avi", "mov"])

# if uploaded_file:
#     # Display the video
#     st.video(uploaded_file)
    
#     # Required description field
#     video_description = st.text_area(
#         "Describe what's happening in the video (required):",
#         placeholder="Example: The video shows batter #5 from the Dodgers in a white uniform with blue accents facing a Yankees pitcher in a grey uniform. The pitcher throws...",
#         help="Please provide details about the players, their numbers, teams, and uniforms visible in the video."
#     )
    
#     # Add a button to generate analysis with a unique key
#     if st.button("Generate Analysis", key="generate_analysis_button") and video_description:
#         try:
#             st.info("Generating analysis...")
            
#             # Prepare prompt with video description
#             full_prompt = f"{ANALYSIS_PROMPT}\n\nVideo Description: {video_description}"
            
#             # Send prompt to Gemini
#             response = model.generate_content(full_prompt)
            
#             # Display the analysis
#             st.subheader("Analysis Results")
#             st.markdown(response.text)
            
#         except Exception as e:
#             st.error(f"Error generating analysis: {str(e)}")
#     elif not video_description:
#         st.warning("Please provide a description of the video first!")

# # Add instructions
# st.sidebar.markdown("""
# ## How to Use
# 1. Upload your baseball video clip
# 2. Provide a detailed description of the video, including:
#    - Player jersey numbers
#    - Team names
#    - Uniform descriptions
#    - Any visible game situations
# 3. Click 'Generate Analysis' to get detailed metrics
# 4. View the comprehensive analysis results

# The analysis will provide:
# - Player identification details
# - Pitch metrics
# - Batted ball metrics
# - Game situation details (if provided)
# """)

# # Add some space at the bottom
# st.markdown("---")
# st.markdown("Made with ❤️ for baseball analytics")
































































# import streamlit as st
# import google.generativeai as genai

# # Configure Gemini Pro
# genai.configure(api_key="key")
# model = genai.GenerativeModel('gemini-pro')

# # Initialize Streamlit app
# st.title("Baseball Video Analysis App")

# # The complete analysis prompt
# ANALYSIS_PROMPT = """You are a baseball analysis expert. Based on the provided video description, extract and analyze the following metrics with exact precision:

# **Required Player Details (Must Extract These Exactly):**
# - Batter's jersey number (if visible)
# - Batter's team name (based on uniform)
# - Batter's uniform description
# - Pitcher's jersey number (if visible)
# - Pitcher's team name (based on uniform)
# - Pitcher's uniform description

# Analyze and provide:

# 1. Pitch Metrics:
#    * Pitch Speed: Speed of the pitch in mph
#    * Pitch Type: Type of pitch (fastball, curveball, slider, etc.)
#    * Pitch Location: Location relative to strike zone

# 2. Batted Ball Metrics:
#    * Exit Velocity: Speed of the ball off the bat in mph
#    * Launch Angle: Angle of the hit in degrees
#    * Hit Distance: Total distance traveled in feet

# 3. Game Situational Metrics:
#    * Score: Current game score (respond with "Not available in current video 🎥" if not mentioned)
#    * Inning: Current inning (respond with "Not available in current video 🎥" if not mentioned)
#    * Outs: Number of outs (respond with "Not available in current video 🎥" if not mentioned)
#    * Base Occupancy: Current baserunners (respond with "Not available in current video 🎥" if not mentioned)


# Format your response exactly like this:

# **Player Identification:**
# * Batter: Jersey #[exact number], Team: [team name] ([uniform details])
# * Pitcher: Jersey #[exact number if visible], Team: [team name] ([uniform details])

# **Pitch Metrics:**
# * **Pitch Speed:** [speed] mph
# * **Pitch Type:** [type]
# * **Pitch Location:** [location]

# **Batted Ball Metrics:**
# * **Exit Velocity:** [speed] mph
# * **Launch Angle:** [angle] degrees
# * **Hit Distance:** [distance] ft

# **Game Situational Metrics:**
# * **Score:** [score or "Not available in current video 🎥"]
# * **Inning:** [inning or "Not available in current video 🎥"]
# * **Outs:** [outs or "Not available in current video 🎥"]
# * **Base Occupancy:** [runners or "Not available in current video 🎥"]

# **Summary:**
# [Brief summary of the play including key metrics]"""

# # Upload video
# uploaded_file = st.file_uploader("Upload a baseball video", type=["mp4", "avi", "mov"])

# # if uploaded_file:
# #     # Display the video
# #     st.video(uploaded_file)
    
# #     # Required description field
# #     video_description = st.text_area(
# #         "Describe what's happening in the video (required):",
# #         placeholder="Example: The video shows batter #5 from the Dodgers wearing a white uniform with blue accents. They're facing a Yankees pitcher in a grey road uniform.",
# #         help="Please include jersey numbers, team names, and uniform details that are visible in the video."
# #     )
    
# #     # Single button with analysis logic
# #     if st.button("Generate Analysis", key="generate_analysis"):
# #         if not video_description:
# #             st.warning("Please provide a description of the video first!")
# #         else:
# #             try:
# #                 st.info("Analyzing video description...")
                
# #                 # Combine prompt with description
# #                 full_prompt = f"{ANALYSIS_PROMPT}\n\nVideo Description: {video_description}"
                
# #                 # Get analysis from Gemini Pro
# #                 response = model.generate_content(full_prompt)
                
# #                 # Display results
# #                 st.subheader("Analysis Results")
# #                 st.markdown(response.text)
                
# #             except Exception as e:
# #                 st.error(f"Error generating analysis: {str(e)}")

# # # Sidebar instructions
# # st.sidebar.markdown("""
# # ## How to Use

# # 1. Upload your baseball video clip
# # 2. Provide a detailed description including:
# #    - Player jersey numbers
# #    - Team names
# #    - Uniform colors and styles
# #    - Any visible game details
# # 3. Click 'Generate Analysis'

# # Tips for Best Results:
# # - Be specific about jersey numbers you can see
# # - Describe uniform colors and designs
# # - Mention any visible scoreboard information
# # """)

# # # Footer
# # st.markdown("---")
# # st.markdown("Made with ❤️ for baseball analytics")



# if uploaded_file:
#     # Display the video
#     st.video(uploaded_file)
    
#     # Optional description field
#     video_description = st.text_area(
#         "Describe what's happening in the video (optional):",
#         placeholder="Add any additional details about the play (optional)",
#         help="You can add extra details, but the system will analyze the video automatically"
#     )
    
#     # Generate analysis button
#     if st.button("Generate Analysis", key="generate_analysis"):
#         try:
#             st.info("Analyzing...")
            
#             # Use description if provided, otherwise use default prompt
#             full_prompt = ANALYSIS_PROMPT
#             if video_description:
#                 full_prompt += f"\n\nAdditional Details: {video_description}"
            
#             # Get analysis from Gemini Pro
#             response = model.generate_content(full_prompt)
            
#             # Display results
#             st.subheader("Analysis Results")
#             st.markdown(response.text)
            
#         except Exception as e:
#             st.error(f"Error generating analysis: {str(e)}")

# # Sidebar instructions
# st.sidebar.markdown("""
# ## How to Use

# 1. Upload your baseball video clip
# 2. (Optional) Add any additional details about the play
# 3. Click 'Generate Analysis'

# The system will automatically extract:
# - Player jersey numbers
# - Team identification
# - Game metrics and statistics
# """)

# # Footer
# st.markdown("---")
# st.markdown("Made with ❤️ for baseball analytics")