import streamlit as st
from PIL import Image
import io
import os
import random

# --- CONFIG ---
AZURE_OPENAI_ENDPOINT = "https://aiengineering-dev-westus-openai.openai.azure.com/"  # Full endpoint for chat completions
AZURE_OPENAI_API_KEY = "782c22cae3ff4af784cd5649a53a6bf3"
MODEL_NAME = "gpt-4o-model"  # Change if using a different model
API_VERSION = "2024-08-01-preview"  # Update if needed


st.title("Dog Breed Classifier (Azure OpenAI)")
st.write("Upload a dog image to classify its breed using Azure OpenAI.")

# --- RANDOM 20 DOG IMAGES ---
st.header("Random Dog Images (Direct URLs)")
dog_image_urls = [
    "https://images.dog.ceo/breeds/shiba/shiba-13.jpg",
    "https://images.dog.ceo/breeds/husky/n02110185_1469.jpg",
    "https://cdn.pixabay.com/photo/2016/12/13/05/15/puppy-1903313_640.jpg",
    "https://images.pexels.com/photos/1490908/pexels-photo-1490908.jpeg?cs=srgb&dl=pexels-svetozar-milashevich-99573-1490908.jpg&fm=jpg"
]
if st.button("Random 4") or "selected_images" not in st.session_state:
    selected_images = random.sample(dog_image_urls, 4)
    st.session_state["selected_images"] = selected_images
    st.session_state["current_image_idx"] = 0

if "selected_images" in st.session_state:
    selected_images = st.session_state["selected_images"]
    idx = st.session_state.get("current_image_idx", 0)
    img_url = selected_images[idx]
    st.image(img_url, caption=f"Image {idx+1} of 20", use_column_width=True)
    if st.button("Classify this image"):
        import requests
        img_response = requests.get(img_url)
        img_bytes = img_response.content
        import base64
        mime_type = "image/jpeg" if ".jpg" in img_url or ".jpeg" in img_url else "image/png"
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
        data_url = f"data:{mime_type};base64,{img_base64}"
        from openai import AzureOpenAI
        AZURE_OPENAI_ENDPOINT = "https://aiengineering-dev-westus-openai.openai.azure.com/"
        AZURE_OPENAI_API_KEY = "782c22cae3ff4af784cd5649a53a6bf3"
        AZURE_OPENAI_DEPLOYMENT = "gpt-4o-model"
        API_VERSION = "2024-08-01-preview"
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
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What dog breed is in this image?"},
                            {"type": "image_url", "image_url": {"url": data_url}}
                        ]
                    }
                ],
                max_tokens=100
            )
            breed = response.choices[0].message.content
            st.success(f"Predicted Breed: {breed}")
        except Exception as e:
            st.error(f"Error: {e}")
            st.write("Check your endpoint, deployment name, API key, and model configuration.")
    if st.button("Next image"):
        st.session_state["current_image_idx"] = (idx + 1) % len(selected_images)

uploaded_file = st.file_uploader("Choose a dog image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("Classifying...")

    # Convert image to bytes
    # Always re-save the image with PIL to ensure valid bytes
    import base64
    ext = uploaded_file.name.split('.')[-1].lower()
    if ext in ["jpg", "jpeg"]:
        mime_type = "image/jpeg"
        format = "JPEG"
    elif ext == "png":
        mime_type = "image/png"
        format = "PNG"
    else:
        st.error("Unsupported image format. Please upload a JPEG or PNG file.")
        st.stop()
    buf = io.BytesIO()
    image.save(buf, format=format)
    img_bytes = buf.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    data_url = f"data:{mime_type};base64,{img_base64}"

    from openai import AzureOpenAI
    AZURE_OPENAI_ENDPOINT = "https://aiengineering-dev-westus-openai.openai.azure.com/"
    AZURE_OPENAI_API_KEY = "782c22cae3ff4af784cd5649a53a6bf3"
    AZURE_OPENAI_DEPLOYMENT = "gpt-4o-model"
    API_VERSION = "2024-08-01-preview"

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
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What dog breed is in this image?"},
                        {"type": "image_url", "image_url": {"url": data_url}}
                    ]
                }
            ],
            max_tokens=100
        )
        breed = response.choices[0].message.content
        st.success(f"Predicted Breed: {breed}")
    except Exception as e:
        st.error(f"Error: {e}")
        st.write("Check your endpoint, deployment name, API key, and model configuration.")
    # ...existing code...
else:
    st.info("Please upload an image to classify.")
