from dotenv import load_dotenv

load_dotenv() # will load the environment variables from .env file (api key)

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY")) 

# function to load gemini pro vision


def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type" : uploaded_file.type,
                "data" : bytes_data
            }
        ]
        return image_parts
    else:
        return FileNotFoundError("No File Uploaded")

# streamlit setup code

st.set_page_config(page_title="Multilanguage Invoice Extractor")

st.header("Invoice Information Extractor")
st.write("Powered by Gemini Pro Vision")
input = st.text_input("Input Prompt: ", key = "input")
uploaded_file = st.file_uploader("Choose an image of the invoice", type = ["jpg", "png", "jpeg"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption = "Uploaded Invoice", use_column_width=True)

submit = st.button("Tell me about the invoice")
st.markdown("---")
footer_text = """
    <div style='text-align: center;'>
        Created by Yash Arora
    </div>
"""
st.write(footer_text, unsafe_allow_html=True)

input_prompt = '''
                You are an expert in understanding invoices.
                You will receive input images as invoices &
                you will have to answer questions based on the input image
                '''

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is: ")
    st.write(response)
