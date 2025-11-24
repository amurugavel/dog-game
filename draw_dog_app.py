import streamlit as st
from streamlit_drawable_canvas import st_canvas
import time
import cv2
import numpy as np
import base64
import requests
from openai import AzureOpenAI

# --- CONFIG ---
AZURE_OPENAI_ENDPOINT = "https://aiengineering-dev-westus-openai.openai.azure.com/"
AZURE_OPENAI_API_KEY = "782c22cae3ff4af784cd5649a53a6bf3"
AZURE_OPENAI_DEPLOYMENT = "gpt-4o-model"
API_VERSION = "2024-08-01-preview"

st.title("Draw a Dog Game (Azure OpenAI)")
st.write("Draw a dog in the canvas below. You have 2.5 minutes! When you're ready, click 'Guess Breed'.")

if "draw_start_time" not in st.session_state:
    st.session_state["draw_start_time"] = None
if "draw_time_limit" not in st.session_state:
    st.session_state["draw_time_limit"] = 150  # 2.5 minutes in seconds



# Always show the canvas (no reset button)
canvas_result = st_canvas(
    fill_color="rgba(255, 105, 180, 0.4)",  # Hot pink fill
    stroke_width=8,
    stroke_color="#FF6347",  # Tomato red
    background_color="#F0F8FF",  # Alice blue background
    height=400,
    width=500,
    drawing_mode="freedraw",
    key="dog_canvas",
    display_toolbar=True
)

if canvas_result.image_data is not None and st.session_state["draw_start_time"] is None:
    st.session_state["draw_start_time"] = time.time()

if st.session_state["draw_start_time"]:
    elapsed = int(time.time() - st.session_state["draw_start_time"])
    remaining = st.session_state["draw_time_limit"] - elapsed
    st.write(f"Time left: {max(0, remaining)} seconds")
    if remaining <= 0:
        st.warning("Time's up! Click 'Guess Breed' to see what Azure OpenAI thinks.")

if st.button("Guess Breed"):
    # Get and display public IP address
    try:
        public_ip = requests.get("https://api.ipify.org", timeout=5).text
        st.info(f"Server Public IP: {public_ip}")
    except Exception as ip_error:
        st.warning(f"Could not fetch public IP: {ip_error}")
    
    if canvas_result.image_data is not None:
        # Show thinking indicator
        with st.spinner("🤔 Analyzing your drawing and talking to Azure OpenAI..."):
            img = cv2.cvtColor(canvas_result.image_data.astype(np.uint8), cv2.COLOR_RGBA2RGB)
            _, buf = cv2.imencode('.png', img)
            img_bytes = buf.tobytes()
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")
            data_url = f"data:image/png;base64,{img_base64}"
            
            client = AzureOpenAI(
                api_key=AZURE_OPENAI_API_KEY,
                api_version=API_VERSION,
                azure_endpoint=AZURE_OPENAI_ENDPOINT,
            )
            try:
                response = client.chat.completions.create(
                    model=AZURE_OPENAI_DEPLOYMENT,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert dog breed classifier. You will be provided with a hand-drawn image of a dog. Your task is to analyze the drawing and identify the most likely dog breed based on the visual characteristics shown in the drawing. Consider features like size, body shape, ear shape, coat type, and any distinctive breed-specific traits visible in the drawing. Provide your best guess for the dog breed."
                        },
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "What dog breed is in this drawing?"},
                                {"type": "image_url", "image_url": {"url": data_url}}
                            ]
                        }
                    ],
                    max_tokens=100
                )
                breed = response.choices[0].message.content
                st.success(f"Azure OpenAI guesses: {breed}")
                if st.session_state["draw_start_time"] and (time.time() - st.session_state["draw_start_time"] <= st.session_state["draw_time_limit"]):
                    st.info("You guessed within the time limit!")
                else:
                    st.warning("You ran out of time!")
            except Exception as e:
                st.error(f"Error: {e}")
                st.write("Check your endpoint, deployment name, API key, and model configuration.")
    else:
        st.warning("Please draw a dog before guessing!")
