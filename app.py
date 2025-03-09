from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import base64
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_resposne(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit APP

st.set_page_config(page_title="ATS Resume Using Gemini Vision")
st.header("ATS Tracking System")
input_text=st.text_area("Job Descripton: ",key="input")
uploaded_file=st.file_uploader("Upload Your Resume(PDF)....",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Sucessfully")

submit1 = st.button("Tell Me About the Resume")

#submit2 = st.button("How can I Improve my Skills")

submit3 = st.button("Percentage match")

input_prompt1= """
You are a Experienced HR With Tech Expereince in the field of any one job role from Data Science, Data Analytics, Data Engineering, Artificial Intileginece Engineering, Machine Learning Engineering or
Full Stack Web Development, Big Data Engineering, DEVOPS,Project Management, your task is to review the provided resume against the job description for these profiles.
Please Share your professional evaluation on wether the candidate's profile aligns with the role.
Highlight the strengths and weeknesses of the applicant in relation to the specifield job requirements.
"""

input_prompt3= """
You are skilled ATS (Applicant Tracking System) scanner with deep understanding of any one job role Data Science, Data Analytics, Data Engineering, Artificial Intileginece Engineering, Machine 
Learning Engineering or Full Stack Web Development, Big Data Engineering, DEVOPS,Project Management and deep ATS functionality,
your task is to evaluate the resume against the provided job description. 
Give me the percentage of match if the resume matches the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content= input_pdf_setup(uploaded_file)
        response=get_gemini_resposne(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content= input_pdf_setup(uploaded_file)
        response=get_gemini_resposne(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the resume")