import streamlit as st
import json
import PyPDF2
from pdf2image import convert_from_path
from pytesseract import image_to_string 
import pytesseract
# import re
# import requests
import PyMuPDF
import openai
import fitz
# import time
# import uuid

openai.api_key = "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"
pytesseract.pytesseract.tesseract_cmd = 'C://Program Files//Tesseract-OCR//tesseract.exe'


# Title and instructions


# Sidebar with three buttons
with st.sidebar:
    st.write("Sidebar")
    selected_option = st.selectbox("Select an option", ["Language_Convertor", "Pdf_Convertor", "Research Paper"])


# File uploader widget

# Display content based on button clicks


# Check if a file was uploaded
# if uploaded_file is not None:
#     # Display some information about the uploaded file
#     st.write("File name:", uploaded_file.name)
#     st.write("File size:", uploaded_file.size, "bytes")

if selected_option=="Language_Convertor":
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_file is not None:
    # Display some information about the uploaded file
        st.write("File name:", uploaded_file.name)
        st.write("File size:", uploaded_file.size, "bytes")

        def get_completion(prompt, model="gpt-3.5-turbo-16k"):
            messages = [{"role": "user", "content": prompt}]
            response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
                
            temperature=0,
            #      temperature=0, # this is the degree of randomness of the model's output
            )
            return response.choices[0].message["content"]
        
        pdfFileObject = open(uploaded_file.name, 'rb')
# creating a pdf reader object
        pdfReader = PyPDF2.PdfReader(pdfFileObject)
        text=[]

        for i in range(0,len(pdfReader.pages)):
        # creating a page object
            pageObj = pdfReader.pages[i].extract_text()
            pageObj= pageObj.replace('\t\r','')
            pageObj= pageObj.replace('\xa0','')
            # extracting text from page
            text.append(pageObj)
                
        # for i in range(len(text)):
        prompt =f"""UserinputData in japanese converted to english "

        ```{text}```
            """
        try:
                response = get_completion(prompt)
        except:
                response = get_completion(prompt)
        prompt1 =f"""
        Your task is to convert the data into json format. 
        Check if the details are related to each other for example someone's details,
        which can inlcude name, date of birth, age, gender, weight, height etc then those should be included as a sub dict.' 
        Entire json format should be editable as this is a pdf editable form.

        ```{response}``
        """
        response1 = get_completion(prompt1)
        json_data = json.loads(response1)

        st.write("Output:")
        st.json(json_data)
        


        # Function to ask questions and get answers from the chatbot API
        
        


        
       

if selected_option=="Pdf_Convertor":
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_file is not None:
        st.write("File name:", uploaded_file.name)
        st.write("File size:", uploaded_file.size, "bytes")
    # Display some information about the uploaded file
        def convert_pdf_to_img(pdf_file):
          return convert_from_path(pdf_file, poppler_path=r'C://Users//Laptop//Downloads//Release-23.07.0-0 (2)//poppler-23.07.0//Library//bin')


        def convert_image_to_text(file):
        
            
            text = image_to_string(file)
            return text


        def get_text_from_any_pdf(pdf_file):
        
            images = convert_pdf_to_img(pdf_file)
            final_text = ""
            for pg, img in enumerate(images):
                
                final_text += convert_image_to_text(img)
                #print("Page n°{}".format(pg))
                #print(convert_image_to_text(img))
            
            return final_text



        def get_completion(prompt, model="gpt-3.5-turbo-16k"):
            messages = [{"role": "user", "content": prompt}]
            response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, # this is the degree of randomness of the model's output
        )
            return response

        ext_text = get_text_from_any_pdf(uploaded_file.name) 


        input_text = f""" Your task is to convert the data into json format. 
        Check if the details are related to each other for example someone's details,
                        if the data contains any boxes, do create the proper check boxes for someone to tick or untick it.' 
        which can inlcude name, date of birth, age, gender, weight, height etc then those should be included as a sub dict
        Entire json format should be editable as this is a pdf editable form.
                
                
                Context: {ext_text}
            

            
            """
        response = get_completion(input_text)
        with open("response2.json", "w") as f:
            f.write(response)
if selected_option=="Research Paper":
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_file is not None:
        def get_completion(prompt, model="gpt-3.5-turbo-16k"):
            messages = [{"role": "user", "content": prompt}]
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0.7,
            )
            return response

        def extract_text_from_pdf(pdf_path):
            text = ""
            with fitz.open(pdf_path) as pdf_document:
                for page_num in range(pdf_document.page_count):
                    page = pdf_document.load_page(page_num)
                    text += page.get_text()
            return text
        extracted_text = extract_text_from_pdf(uploaded_file.name)

        
        
        
                
    
 # st.write("You can ask your questions here:")
        user_input=("1- list of drugs prescribed to the patient"
                    "2- What side effects were experienced by the patient after he started taking the drugs ? What was the diagnosis",
                    "3- Which drug was responsible for this side effect? Which sentences demonstrate the causality between the drug and the side effect?",
                    "4- Is Peripheral Neuropathy a listed / known side effect?"
        )
        prompt = f""" Mention all the  question and answer the question wise first question then give them answert
        

        que:```{user_input}``` 
        data: '''{extracted_text}'''
        """
        response = get_completion(prompt)
        st.write(response)
        # st.write(response.choices[0].message['content'])
