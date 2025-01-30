# import streamlit as st
# from google.cloud import videointelligence_v1 as videointelligence
# import google.generativeai as genai
# import tempfile
# import os

# # Set up Google Cloud credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "baseballdetection-7523dff198bc.json"

# # Configure Gemini Pro
# genai.configure(api_key="AIzaSyBJwdpGxd6sn_X-U7hG_Hg9ugPPzsGwAjU")
# model = genai.GenerativeModel('gemini-pro')

# # Initialize Streamlit app
# st.title("Baseball Video Analysis App")

# # Function to analyze video using Video Intelligence API for text detection
# def analyze_video_for_text(video_path):
#     client = videointelligence.VideoIntelligenceServiceClient()
#     with open(video_path, "rb") as file:
#         input_content = file.read()

#     # Configure features to analyze (Text Detection)
#     features = [videointelligence.Feature.TEXT_DETECTION]

#     # Start the video analysis
#     operation = client.annotate_video(
#         request={"features": features, "input_content": input_content}
#     )
#     result = operation.result(timeout=300)  # Wait for the operation to complete

#     return result

# # Function to generate analysis using Gemini Pro
# def generate_analysis(player_identification, game_situational_metrics):
#     prompt = f"""
#     You are a baseball analysis expert. Analyze the following data extracted from a baseball video and provide detailed metrics:

#     **Player Identification:**
#     * Batter: {player_identification['batter']}
#     * Pitcher: {player_identification['pitcher']}
    
#     **Metrics to Calculate:**
#     1. **Pitch Metrics:**
#        - Pitch Speed: Estimate the speed of the pitch based on the ball's trajectory and timestamps.
#        - Pitch Type: Classify the type of pitch (e.g., fastball, curveball) based on the ball's movement.
#        - Pitch Location: Determine the location of the pitch relative to the strike zone.

#     2. **Batted Ball Metrics:**
#        - Exit Velocity: Estimate the speed of the ball as it leaves the bat.
#        - Launch Angle: Calculate the angle at which the ball is hit.
#        - Hit Distance: Estimate the total distance traveled by the ball.

#     3. **Game Situational Metrics:**
#        - Score: {game_situational_metrics['score']}
#        - Inning: {game_situational_metrics['inning']}
#        - Outs: {game_situational_metrics['outs']}
#        - Base Occupancy: {game_situational_metrics['base_occupancy']}

#     **Output Format:**
#     **Pitch Metrics:**
#     * **Pitch Speed:** [speed] mph (Estimated from video analysis)
#     * **Pitch Type:** [type] (Based on trajectory and movement)
#     * **Pitch Location:** [location description] (Relative to strike zone)

#     **Batted Ball Metrics:**
#     * **Exit Velocity:** [speed] mph (Estimated from video analysis)
#     * **Launch Angle:** [angle] degrees (Based on initial trajectory)
#     * **Hit Distance:** [distance] ft (Estimated total travel)

#     **Summary of Extracted Metrics:**
#     Pitch Speed: [speed] mph, Pitch Type: [type], Exit Velocity: [speed] mph, Launch Angle: [angle] degrees, Hit Distance: [distance] ft, Score: {game_situational_metrics['score']}, Inning: {game_situational_metrics['inning']}, Outs: {game_situational_metrics['outs']}, Base Occupancy: {game_situational_metrics['base_occupancy']}
#     """
#     response = model.generate_content(prompt)
#     return response.text

# # Upload video
# uploaded_file = st.file_uploader("Upload a baseball video", type=["mp4", "avi", "mov"])

# if uploaded_file:
#     # Save the uploaded video to a temporary file
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
#         tmp_file.write(uploaded_file.read())
#         video_path = tmp_file.name

#     # Display the video
#     st.video(video_path)

#     # Add a button to generate analysis
#     if st.button("Generate Analysis"):
#         try:
#             st.info("Generating analysis...")

#             # Analyze the video using Video Intelligence API for text detection
#             result = analyze_video_for_text(video_path)

#             # Extract relevant data from the API response
#             player_identification = {
#                 "batter": "Not identified",
#                 "pitcher": "Not identified"
#             }
#             game_situational_metrics = {
#                 "score": "Score not available in the video 🤔",
#                 "inning": "Inning not available in the video",
#                 "outs": "Outs not available in the video 🔍",
#                 "base_occupancy": "Base occupancy not available in the video"
#             }

#             detected_texts = []
#             # Process text annotations (e.g., jersey numbers, player names, team names)
#             for annotation in result.annotation_results[0].text_annotations:
#                 detected_texts.append(annotation.text)
#                 text_desc = annotation.text.lower()
#                 if "batter" in text_desc:
#                     player_identification["batter"] = annotation.text
#                 elif "pitcher" in text_desc:
#                     player_identification["pitcher"] = annotation.text
#                 elif "score" in text_desc:
#                     game_situational_metrics["score"] = annotation.text
#                 elif "inning" in text_desc:
#                     game_situational_metrics["inning"] = annotation.text
#                 elif "outs" in text_desc:
#                     game_situational_metrics["outs"] = annotation.text
#                 elif "base" in text_desc:
#                     game_situational_metrics["base_occupancy"] = annotation.text

#             # Generate analysis using Gemini Pro
#             analysis = generate_analysis(player_identification, game_situational_metrics)

#             # Display the detected texts
#             st.subheader("Detected Texts")
#             st.markdown(f"""
#             **Detected Texts**: {', '.join(detected_texts)}
#             """)

#             # Display the player identification and game situational metrics
#             st.subheader("Player Identification")
#             st.markdown(f"""
#             **Batter**: {player_identification["batter"]}
#             **Pitcher**: {player_identification["pitcher"]}
#             """)

#             st.subheader("Game Situational Metrics")
#             st.markdown(f"""
#             **Score**: {game_situational_metrics["score"]}
#             **Inning**: {game_situational_metrics["inning"]}
#             **Outs**: {game_situational_metrics["outs"]}
#             **Base Occupancy**: {game_situational_metrics["base_occupancy"]}
#             """)

#             # Display the generated analysis
#             st.subheader("Analysis Results")
#             st.markdown(analysis)

#         except Exception as e:
#             st.error(f"Error generating analysis: {str(e)}")
#         finally:
#             # Clean up the temporary file
#             os.unlink(video_path)

# # Add instructions
# st.sidebar.markdown("""
# ## How to Use
# 1. Upload your baseball video clip.
# 2. Click 'Generate Analysis' to analyze the video.
# 3. View the detailed metrics and analysis generated by Gemini Pro.
# """)

# # Add some space at the bottom
# st.markdown("---")
# st.markdown("Made with ❤️ for baseball analytics")




























# import streamlit as st
# from google.cloud import videointelligence_v1 as videointelligence
# import google.generativeai as genai
# import tempfile
# import os
# import re

# # Set up Google Cloud credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "baseballdetection-7523dff198bc.json"

# # Configure Gemini Pro
# genai.configure(api_key="AIzaSyBJwdpGxd6sn_X-U7hG_Hg9ugPPzsGwAjU")
# model = genai.GenerativeModel('gemini-pro')

# # Initialize Streamlit app
# st.title("Baseball Video Analysis App")

# # Function to analyze video using Video Intelligence API for text detection
# def analyze_video_for_text(video_path):
#     client = videointelligence.VideoIntelligenceServiceClient()
#     with open(video_path, "rb") as file:
#         input_content = file.read()

#     # Configure features to analyze (Text Detection)
#     features = [videointelligence.Feature.TEXT_DETECTION]

#     # Start the video analysis
#     operation = client.annotate_video(
#         request={"features": features, "input_content": input_content}
#     )
#     result = operation.result(timeout=300)  # Wait for the operation to complete

#     return result

# # Function to group text annotations by proximity
# def group_text_annotations(annotations):
#     grouped_texts = []
#     for annotation in annotations:
#         text = annotation.text
#         vertices = annotation.segments[0].frames[0].rotated_bounding_box.vertices
#         # Calculate the center of the bounding box
#         center_x = sum(vertex.x for vertex in vertices) / 4
#         center_y = sum(vertex.y for vertex in vertices) / 4

#         # Check if this text is near any existing group
#         added_to_group = False
#         for group in grouped_texts:
#             group_center_x = group["center_x"]
#             group_center_y = group["center_y"]
#             # If the text is within a certain distance, add it to the group
#             if abs(center_x - group_center_x) < 50 and abs(center_y - group_center_y) < 50:
#                 group["texts"].append(text)
#                 added_to_group = True
#                 break

#         # If not added to any group, create a new group
#         if not added_to_group:
#             grouped_texts.append({
#                 "texts": [text],
#                 "center_x": center_x,
#                 "center_y": center_y
#             })

#     return grouped_texts

# # Function to identify players from grouped texts
# def identify_players(grouped_texts):
#     players = []
#     for group in grouped_texts:
#         texts = group["texts"]
#         player_info = {
#             "name": None,
#             "jersey_number": None,
#             "team": None
#         }

#         # Look for player name, jersey number, and team name
#         for text in texts:
#             # Check for jersey number (1-99)
#             if re.match(r"^\d{1,2}$", text):
#                 player_info["jersey_number"] = text
#             # Check for team name (e.g., DODGERS)
#             elif text.isupper() and len(text) > 2 and not re.search(r"[^A-Z]", text):
#                 player_info["team"] = text
#             # Check for player name (capitalized, no special characters, and not a team name)
#             elif text.istitle() and not re.search(r"[^A-Za-z]", text) and len(text) > 2:
#                 player_info["name"] = text

#         # Add player info if valid
#         if player_info["name"] or player_info["jersey_number"] or player_info["team"]:
#             players.append(player_info)

#     return players

# # Function to generate analysis using Gemini Pro
# def generate_analysis(player_identification, game_situational_metrics):
#     prompt = f"""
#     You are a baseball analysis expert. Analyze the following data extracted from a baseball video and provide detailed metrics:

#     **Player Identification:**
#     * Batter: {player_identification['batter']}
#     * Pitcher: {player_identification['pitcher']}
    
#     **Metrics to Calculate:**
#     1. **Pitch Metrics:**
#        - Pitch Speed: Estimate the speed of the pitch based on the ball's trajectory and timestamps.
#        - Pitch Type: Classify the type of pitch (e.g., fastball, curveball) based on the ball's movement.
#        - Pitch Location: Determine the location of the pitch relative to the strike zone.

#     2. **Batted Ball Metrics:**
#        - Exit Velocity: Estimate the speed of the ball as it leaves the bat.
#        - Launch Angle: Calculate the angle at which the ball is hit.
#        - Hit Distance: Estimate the total distance traveled by the ball.

#     3. **Game Situational Metrics:**
#        - Score: {game_situational_metrics['score']}
#        - Inning: {game_situational_metrics['inning']}
#        - Outs: {game_situational_metrics['outs']}
#        - Base Occupancy: {game_situational_metrics['base_occupancy']}

#     **Output Format:**
#     **Pitch Metrics:**
#     * **Pitch Speed:** [speed] mph (Estimated from video analysis)
#     * **Pitch Type:** [type] (Based on trajectory and movement)
#     * **Pitch Location:** [location description] (Relative to strike zone)

#     **Batted Ball Metrics:**
#     * **Exit Velocity:** [speed] mph (Estimated from video analysis)
#     * **Launch Angle:** [angle] degrees (Based on initial trajectory)
#     * **Hit Distance:** [distance] ft (Estimated total travel)

#     **Summary of Extracted Metrics:**
#     Pitch Speed: [speed] mph, Pitch Type: [type], Exit Velocity: [speed] mph, Launch Angle: [angle] degrees, Hit Distance: [distance] ft, Score: {game_situational_metrics['score']}, Inning: {game_situational_metrics['inning']}, Outs: {game_situational_metrics['outs']}, Base Occupancy: {game_situational_metrics['base_occupancy']}
#     """
#     response = model.generate_content(prompt)
#     return response.text

# # Upload video
# uploaded_file = st.file_uploader("Upload a baseball video", type=["mp4", "avi", "mov"])

# if uploaded_file:
#     # Save the uploaded video to a temporary file
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
#         tmp_file.write(uploaded_file.read())
#         video_path = tmp_file.name

#     # Display the video
#     st.video(video_path)

#     # Add a button to generate analysis
#     if st.button("Generate Analysis"):
#         try:
#             st.info("Generating analysis...")

#             # Analyze the video using Video Intelligence API for text detection
#             result = analyze_video_for_text(video_path)

#             # Group text annotations by proximity
#             grouped_texts = group_text_annotations(result.annotation_results[0].text_annotations)

#             # Identify players from grouped texts
#             players = identify_players(grouped_texts)

#             # Extract relevant data from the API response
#             player_identification = {
#                 "batter": "Not identified",
#                 "pitcher": "Not identified"
#             }
#             game_situational_metrics = {
#                 "score": "Score not available in the video 🤔",
#                 "inning": "Inning not available in the video",
#                 "outs": "Outs not available in the video 🔍",
#                 "base_occupancy": "Base occupancy not available in the video"
#             }

#             # Assign players to batter and pitcher if identified
#             if players:
#                 player_identification["batter"] = f"{players[0].get('name', 'Unknown')} ({players[0].get('jersey_number', 'No number')}, {players[0].get('team', 'No team')})"
#                 if len(players) > 1:
#                     player_identification["pitcher"] = f"{players[1].get('name', 'Unknown')} ({players[1].get('jersey_number', 'No number')}, {players[1].get('team', 'No team')})"

#             # Generate analysis using Gemini Pro
#             analysis = generate_analysis(player_identification, game_situational_metrics)

#             # Display the grouped texts
#             st.subheader("Grouped Texts")
#             for group in grouped_texts:
#                 st.markdown(f"""
#                 **Grouped Texts**: {', '.join(group["texts"])}
#                 """)

#             # Display the player identification
#             st.subheader("Player Identification")
#             st.markdown(f"""
#             **Batter**: {player_identification["batter"]}
#             **Pitcher**: {player_identification["pitcher"]}
#             """)

#             # Display the game situational metrics
#             st.subheader("Game Situational Metrics")
#             st.markdown(f"""
#             **Score**: {game_situational_metrics["score"]}
#             **Inning**: {game_situational_metrics["inning"]}
#             **Outs**: {game_situational_metrics["outs"]}
#             **Base Occupancy**: {game_situational_metrics["base_occupancy"]}
#             """)

#             # Display the generated analysis
#             st.subheader("Analysis Results")
#             st.markdown(analysis)

#         except Exception as e:
#             st.error(f"Error generating analysis: {str(e)}")
#         finally:
#             # Clean up the temporary file
#             os.unlink(video_path)

# # Add instructions
# st.sidebar.markdown("""
# ## How to Use
# 1. Upload your baseball video clip.
# 2. Click 'Generate Analysis' to analyze the video.
# 3. View the detailed metrics and analysis generated by Gemini Pro.
# """)

# # Add some space at the bottom
# st.markdown("---")
# st.markdown("Made with ❤️ for baseball analytics")





































## Almost right but batter pitcher doubt
# import streamlit as st
# from google.cloud import videointelligence_v1 as videointelligence
# import google.generativeai as genai
# import tempfile
# import os
# import re

# # Set up Google Cloud credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "baseballdetection-7523dff198bc.json"

# # Configure Gemini Pro
# genai.configure(api_key="AIzaSyBJwdpGxd6sn_X-U7hG_Hg9ugPPzsGwAjU")
# model = genai.GenerativeModel('gemini-pro')

# # Initialize Streamlit app
# st.title("Baseball Video Analysis App")

# # Function to analyze video using Video Intelligence API for text detection
# def analyze_video_for_text(video_path):
#     client = videointelligence.VideoIntelligenceServiceClient()
#     with open(video_path, "rb") as file:
#         input_content = file.read()

#     # Configure features to analyze (Text Detection)
#     features = [videointelligence.Feature.TEXT_DETECTION]

#     # Start the video analysis
#     operation = client.annotate_video(
#         request={"features": features, "input_content": input_content}
#     )
#     result = operation.result(timeout=300)  # Wait for the operation to complete

#     return result

# # Function to group text annotations by proximity
# def group_text_annotations(annotations):
#     grouped_texts = []
#     for annotation in annotations:
#         text = annotation.text
#         vertices = annotation.segments[0].frames[0].rotated_bounding_box.vertices
#         # Calculate the center of the bounding box
#         center_x = sum(vertex.x for vertex in vertices) / 4
#         center_y = sum(vertex.y for vertex in vertices) / 4

#         # Check if this text is near any existing group
#         added_to_group = False
#         for group in grouped_texts:
#             group_center_x = group["center_x"]
#             group_center_y = group["center_y"]
#             # If the text is within a certain distance, add it to the group
#             if abs(center_x - group_center_x) < 50 and abs(center_y - group_center_y) < 50:
#                 group["texts"].append(text)
#                 added_to_group = True
#                 break

#         # If not added to any group, create a new group
#         if not added_to_group:
#             grouped_texts.append({
#                 "texts": [text],
#                 "center_x": center_x,
#                 "center_y": center_y
#             })

#     return grouped_texts

# # Function to identify players from grouped texts
# def identify_players(grouped_texts):
#     players = []
#     for group in grouped_texts:
#         texts = group["texts"]
#         player_info = {
#             "name": None,
#             "jersey_number": None
#         }

#         # Look for player name and jersey number
#         for text in texts:
#             # Check for jersey number (1-99)
#             if re.match(r"^\d{1,2}$", text):
#                 player_info["jersey_number"] = text
#             # Check for player name (all caps, no special characters, and not a team name)
#             elif text.isupper() and not re.search(r"[^A-Z]", text) and len(text) > 2:
#                 player_info["name"] = text

#         # Add player info if valid
#         if player_info["name"] or player_info["jersey_number"]:
#             players.append(player_info)

#     return players

# # Function to generate analysis using Gemini Pro
# def generate_analysis(player_identification, game_situational_metrics):
#     prompt = f"""
#     You are a baseball analysis expert. Analyze the following data extracted from a baseball video and provide detailed metrics:

#     **Player Identification:**
#     * Batter: {player_identification['batter']}
#     * Pitcher: {player_identification['pitcher']}
    
#     **Metrics to Calculate:**
#     1. **Pitch Metrics:**
#        - Pitch Speed: Estimate the speed of the pitch based on the ball's trajectory and timestamps.
#        - Pitch Type: Classify the type of pitch (e.g., fastball, curveball) based on the ball's movement.
#        - Pitch Location: Determine the location of the pitch relative to the strike zone.

#     2. **Batted Ball Metrics:**
#        - Exit Velocity: Estimate the speed of the ball as it leaves the bat.
#        - Launch Angle: Calculate the angle at which the ball is hit.
#        - Hit Distance: Estimate the total distance traveled by the ball.

#     3. **Game Situational Metrics:**
#        - Score: {game_situational_metrics['score']}
#        - Inning: {game_situational_metrics['inning']}
#        - Outs: {game_situational_metrics['outs']}
#        - Base Occupancy: {game_situational_metrics['base_occupancy']}

#     **Output Format:**
#     **Pitch Metrics:**
#     * **Pitch Speed:** [speed] mph (Estimated from video analysis)
#     * **Pitch Type:** [type] (Based on trajectory and movement)
#     * **Pitch Location:** [location description] (Relative to strike zone)

#     **Batted Ball Metrics:**
#     * **Exit Velocity:** [speed] mph (Estimated from video analysis)
#     * **Launch Angle:** [angle] degrees (Based on initial trajectory)
#     * **Hit Distance:** [distance] ft (Estimated total travel)

#     **Summary of Extracted Metrics:**
#     Pitch Speed: [speed] mph, Pitch Type: [type], Exit Velocity: [speed] mph, Launch Angle: [angle] degrees, Hit Distance: [distance] ft, Score: {game_situational_metrics['score']}, Inning: {game_situational_metrics['inning']}, Outs: {game_situational_metrics['outs']}, Base Occupancy: {game_situational_metrics['base_occupancy']}
#     """
#     response = model.generate_content(prompt)
#     return response.text

# # Upload video
# uploaded_file = st.file_uploader("Upload a baseball video", type=["mp4", "avi", "mov"])

# if uploaded_file:
#     # Save the uploaded video to a temporary file
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
#         tmp_file.write(uploaded_file.read())
#         video_path = tmp_file.name

#     # Display the video
#     st.video(video_path)

#     # Add a button to generate analysis
#     if st.button("Generate Analysis"):
#         try:
#             st.info("Generating analysis...")

#             # Analyze the video using Video Intelligence API for text detection
#             result = analyze_video_for_text(video_path)

#             # Group text annotations by proximity
#             grouped_texts = group_text_annotations(result.annotation_results[0].text_annotations)

#             # Identify players from grouped texts
#             players = identify_players(grouped_texts)

#             # Extract relevant data from the API response
#             player_identification = {
#                 "batter": "Not identified",
#                 "pitcher": "Not identified"
#             }
#             game_situational_metrics = {
#                 "score": "Score not available in the video 🤔",
#                 "inning": "Inning not available in the video",
#                 "outs": "Outs not available in the video 🔍",
#                 "base_occupancy": "Base occupancy not available in the video"
#             }

#             # Assign players to batter and pitcher if identified
#             if players:
#                 player_identification["batter"] = f"{players[0].get('name', 'Unknown')} ({players[0].get('jersey_number', 'No number')})"
#                 if len(players) > 1:
#                     player_identification["pitcher"] = f"{players[1].get('name', 'Unknown')} ({players[1].get('jersey_number', 'No number')})"

#             # Generate analysis using Gemini Pro
#             analysis = generate_analysis(player_identification, game_situational_metrics)

#             # Display the grouped texts
#             st.subheader("Grouped Texts")
#             for group in grouped_texts:
#                 st.markdown(f"""
#                 **Grouped Texts**: {', '.join(group["texts"])}
#                 """)

#             # Display the player identification
#             st.subheader("Player Identification")
#             st.markdown(f"""
#             **Batter**: {player_identification["batter"]}
#             **Pitcher**: {player_identification["pitcher"]}
#             """)

#             # Display the game situational metrics
#             st.subheader("Game Situational Metrics")
#             st.markdown(f"""
#             **Score**: {game_situational_metrics["score"]}
#             **Inning**: {game_situational_metrics["inning"]}
#             **Outs**: {game_situational_metrics["outs"]}
#             **Base Occupancy**: {game_situational_metrics["base_occupancy"]}
#             """)

#             # Display the generated analysis
#             st.subheader("Analysis Results")
#             st.markdown(analysis)

#         except Exception as e:
#             st.error(f"Error generating analysis: {str(e)}")
#         finally:
#             # Clean up the temporary file
#             os.unlink(video_path)

# # Add instructions
# st.sidebar.markdown("""
# ## How to Use
# 1. Upload your baseball video clip.
# 2. Click 'Generate Analysis' to analyze the video.
# 3. View the detailed metrics and analysis generated by Gemini Pro.
# """)

# # Add some space at the bottom
# st.markdown("---")
# st.markdown("Made with ❤️ for baseball analytics")














































##only numbers
# import streamlit as st
# from google.cloud import videointelligence_v1 as videointelligence
# import google.generativeai as genai
# import tempfile
# import os
# import re

# # Set up Google Cloud credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "baseballdetection-7523dff198bc.json"

# # Configure Gemini Pro
# genai.configure(api_key="AIzaSyBJwdpGxd6sn_X-U7hG_Hg9ugPPzsGwAjU")
# model = genai.GenerativeModel('gemini-pro')

# # Initialize Streamlit app
# st.title("Baseball Video Analysis App")

# # Function to analyze video using Video Intelligence API for text detection
# def analyze_video_for_text(video_path):
#     client = videointelligence.VideoIntelligenceServiceClient()
#     with open(video_path, "rb") as file:
#         input_content = file.read()

#     # Configure features to analyze (Text Detection)
#     features = [videointelligence.Feature.TEXT_DETECTION]

#     # Start the video analysis
#     operation = client.annotate_video(
#         request={"features": features, "input_content": input_content}
#     )
#     result = operation.result(timeout=300)  # Wait for the operation to complete

#     return result

# # Function to group text annotations by proximity
# def group_text_annotations(annotations):
#     grouped_texts = []
#     for annotation in annotations:
#         text = annotation.text
#         vertices = annotation.segments[0].frames[0].rotated_bounding_box.vertices
#         # Calculate the center of the bounding box
#         center_x = sum(vertex.x for vertex in vertices) / 4
#         center_y = sum(vertex.y for vertex in vertices) / 4

#         # Check if this text is near any existing group
#         added_to_group = False
#         for group in grouped_texts:
#             group_center_x = group["center_x"]
#             group_center_y = group["center_y"]
#             # If the text is within a certain distance, add it to the group
#             if abs(center_x - group_center_x) < 50 and abs(center_y - group_center_y) < 50:
#                 group["texts"].append(text)
#                 added_to_group = True
#                 break

#         # If not added to any group, create a new group
#         if not added_to_group:
#             grouped_texts.append({
#                 "texts": [text],
#                 "center_x": center_x,
#                 "center_y": center_y
#             })

#     return grouped_texts

# # Function to identify players from grouped texts (with improved logic)
# def identify_players(grouped_texts):
#     players = []
#     for group in grouped_texts:
#         texts = group["texts"]
#         jersey_number = None
#         player_type = None  # "pitcher" or "batter"

#         # Look for jersey number (1-99) and player type (P or B)
#         for text in texts:
#             if re.match(r"^\d{1,2}$", text):  # Check for jersey number
#                 jersey_number = text
#             elif text.upper() == "P":  # Check for pitcher identifier
#                 player_type = "pitcher"
#             elif text.upper() == "B":  # Check for batter identifier
#                 player_type = "batter"

#         # Add player info if valid
#         if jersey_number:
#             players.append({
#                 "jersey_number": jersey_number,
#                 "type": player_type  # "pitcher", "batter", or None
#             })

#     return players

# # Function to generate analysis using Gemini Pro
# def generate_analysis(player_identification, game_situational_metrics):
#     prompt = f"""
#     You are a baseball analysis expert. Analyze the following data extracted from a baseball video and provide detailed metrics:

#     **Player Identification:**
#     * Batter: {player_identification['batter']}
#     * Pitcher: {player_identification['pitcher']}
    
#     **Metrics to Calculate:**
#     1. **Pitch Metrics:**
#        - Pitch Speed: Estimate the speed of the pitch based on the ball's trajectory and timestamps.
#        - Pitch Type: Classify the type of pitch (e.g., fastball, curveball) based on the ball's movement.
#        - Pitch Location: Determine the location of the pitch relative to the strike zone.

#     2. **Batted Ball Metrics:**
#        - Exit Velocity: Estimate the speed of the ball as it leaves the bat.
#        - Launch Angle: Calculate the angle at which the ball is hit.
#        - Hit Distance: Estimate the total distance traveled by the ball.

#     3. **Game Situational Metrics:**
#        - Score: {game_situational_metrics['score']}
#        - Inning: {game_situational_metrics['inning']}
#        - Outs: {game_situational_metrics['outs']}
#        - Base Occupancy: {game_situational_metrics['base_occupancy']}

#     **Output Format:**
#     **Pitch Metrics:**
#     * **Pitch Speed:** [speed] mph (Estimated from video analysis)
#     * **Pitch Type:** [type] (Based on trajectory and movement)
#     * **Pitch Location:** [location description] (Relative to strike zone)

#     **Batted Ball Metrics:**
#     * **Exit Velocity:** [speed] mph (Estimated from video analysis)
#     * **Launch Angle:** [angle] degrees (Based on initial trajectory)
#     * **Hit Distance:** [distance] ft (Estimated total travel)

#     **Summary of Extracted Metrics:**
#     Pitch Speed: [speed] mph, Pitch Type: [type], Exit Velocity: [speed] mph, Launch Angle: [angle] degrees, Hit Distance: [distance] ft, Score: {game_situational_metrics['score']}, Inning: {game_situational_metrics['inning']}, Outs: {game_situational_metrics['outs']}, Base Occupancy: {game_situational_metrics['base_occupancy']}
#     """
#     response = model.generate_content(prompt)
#     return response.text

# # Upload video
# uploaded_file = st.file_uploader("Upload a baseball video", type=["mp4", "avi", "mov"])

# if uploaded_file:
#     # Save the uploaded video to a temporary file
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
#         tmp_file.write(uploaded_file.read())
#         video_path = tmp_file.name

#     # Display the video
#     st.video(video_path)

#     # Add a button to generate analysis
#     if st.button("Generate Analysis"):
#         try:
#             st.info("Generating analysis...")

#             # Analyze the video using Video Intelligence API for text detection
#             result = analyze_video_for_text(video_path)

#             # Group text annotations by proximity
#             grouped_texts = group_text_annotations(result.annotation_results[0].text_annotations)

#             # Identify players from grouped texts (only jersey numbers)
#             players = identify_players(grouped_texts)

#             # Extract relevant data from the API response
#             player_identification = {
#                 "batter": "Not identified",
#                 "pitcher": "Not identified"
#             }
#             game_situational_metrics = {
#                 "score": "Score not available in the video 🤔",
#                 "inning": "Inning not available in the video",
#                 "outs": "Outs not available in the video 🔍",
#                 "base_occupancy": "Base occupancy not available in the video"
#             }

#             # Assign players to batter and pitcher if identified
#             if players:
#                 for player in players:
#                     if player["type"] == "pitcher":
#                         player_identification["pitcher"] = f"Jersey Number: {player['jersey_number']}"
#                     elif player["type"] == "batter":
#                         player_identification["batter"] = f"Jersey Number: {player['jersey_number']}"
#                     else:
#                         # If no type is specified, assume the first number is the pitcher and the second is the batter
#                         if "pitcher" not in player_identification:
#                             player_identification["pitcher"] = f"Jersey Number: {player['jersey_number']}"
#                         else:
#                             player_identification["batter"] = f"Jersey Number: {player['jersey_number']}"

#             # Generate analysis using Gemini Pro
#             analysis = generate_analysis(player_identification, game_situational_metrics)

#             # Display the grouped texts
#             st.subheader("Grouped Texts")
#             for group in grouped_texts:
#                 st.markdown(f"""
#                 **Grouped Texts**: {', '.join(group["texts"])}
#                 """)

#             # Display the player identification
#             st.subheader("Player Identification")
#             st.markdown(f"""
#             **Batter**: {player_identification["batter"]}
#             **Pitcher**: {player_identification["pitcher"]}
#             """)

#             # Display the game situational metrics
#             st.subheader("Game Situational Metrics")
#             st.markdown(f"""
#             **Score**: {game_situational_metrics["score"]}
#             **Inning**: {game_situational_metrics["inning"]}
#             **Outs**: {game_situational_metrics["outs"]}
#             **Base Occupancy**: {game_situational_metrics["base_occupancy"]}
#             """)

#             # Display the generated analysis
#             st.subheader("Analysis Results")
#             st.markdown(analysis)

#         except Exception as e:
#             st.error(f"Error generating analysis: {str(e)}")
#         finally:
#             # Clean up the temporary file
#             os.unlink(video_path)

# # Add instructions
# st.sidebar.markdown("""
# ## How to Use
# 1. Upload your baseball video clip.
# 2. Click 'Generate Analysis' to analyze the video.
# 3. View the detailed metrics and analysis generated by Gemini Pro.
# """)

# # Add some space at the bottom
# st.markdown("---")
# st.markdown("Made with ❤️ for baseball analytics")






























import streamlit as st
from google.cloud import videointelligence_v1 as videointelligence
import google.generativeai as genai
import tempfile
import os
import re

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "baseballdetection-7523dff198bc.json"

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

# Function to group text annotations by proximity
def group_text_annotations(annotations):
    grouped_texts = []
    for annotation in annotations:
        text = annotation.text
        vertices = annotation.segments[0].frames[0].rotated_bounding_box.vertices
        # Calculate the center of the bounding box
        center_x = sum(vertex.x for vertex in vertices) / 4
        center_y = sum(vertex.y for vertex in vertices) / 4

        # Check if this text is near any existing group
        added_to_group = False
        for group in grouped_texts:
            group_center_x = group["center_x"]
            group_center_y = group["center_y"]
            # If the text is within a certain distance, add it to the group
            if abs(center_x - group_center_x) < 50 and abs(center_y - group_center_y) < 50:
                group["texts"].append(text)
                added_to_group = True
                break

        # If not added to any group, create a new group
        if not added_to_group:
            grouped_texts.append({
                "texts": [text],
                "center_x": center_x,
                "center_y": center_y
            })

    return grouped_texts

# Function to identify jersey numbers from grouped texts
def identify_jersey_numbers(grouped_texts):
    jersey_numbers = []
    for group in grouped_texts:
        texts = group["texts"]
        for text in texts:
            if re.match(r"^\d{1,2}$", text):  # Check for jersey number (1-99)
                jersey_numbers.append(text)
    return jersey_numbers

# Function to generate analysis using Gemini Pro
def generate_analysis(jersey_numbers, game_situational_metrics):
    prompt = f"""
    You are a baseball analysis expert. Analyze the following data extracted from a baseball video and provide detailed metrics:

    **Identified Jersey Numbers:**
    {', '.join(jersey_numbers) if jersey_numbers else "No jersey numbers identified"}

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

    **Game Situational Metrics:**
    * **Score:** {game_situational_metrics['score']}
    * **Inning:** {game_situational_metrics['inning']}
    * **Outs:** {game_situational_metrics['outs']}
    * **Base Occupancy:** {game_situational_metrics['base_occupancy']}

    **Summary of Extracted Metrics:**
    Pitch Speed: [speed] mph, Pitch Type: [type], Exit Velocity: [speed] mph, Launch Angle: [angle] degrees, Hit Distance: [distance] ft, Score: {game_situational_metrics['score']}, Inning: {game_situational_metrics['inning']}, Outs: {game_situational_metrics['outs']}, Base Occupancy: {game_situational_metrics['base_occupancy']}

    **Additional Notes:**
    - If the ball speed is below 90 mph, consider it a slower pitch (e.g., changeup or curveball).
    - If the exit velocity is below 90 mph, consider it a weakly hit ball.
    - If the launch angle is below 10 degrees, consider it a ground ball.
    - If the launch angle is above 25 degrees, consider it a fly ball.
    - If the hit distance is below 300 feet, consider it a short hit.
    - If the hit distance is above 400 feet, consider it a home run.
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

            # Group text annotations by proximity
            grouped_texts = group_text_annotations(result.annotation_results[0].text_annotations)

            # Identify jersey numbers from grouped texts
            jersey_numbers = identify_jersey_numbers(grouped_texts)

            # Extract relevant data from the API response
            game_situational_metrics = {
                "score": "Score not available in the video 🤔",
                "inning": "Inning not available in the video",
                "outs": "Outs not available in the video 🔍",
                "base_occupancy": "Base occupancy not available in the video"
            }

            # Generate analysis using Gemini Pro
            analysis = generate_analysis(jersey_numbers, game_situational_metrics)

            # Display the grouped texts
            st.subheader("Grouped Texts")
            for group in grouped_texts:
                st.markdown(f"""
                **Grouped Texts**: {', '.join(group["texts"])}
                """)

            # Display the identified jersey numbers
            st.subheader("Identified Jersey Numbers")
            st.markdown(f"""
            **Jersey Numbers**: {', '.join(jersey_numbers) if jersey_numbers else "No jersey numbers identified"}
            """)

            # Display the game situational metrics
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














