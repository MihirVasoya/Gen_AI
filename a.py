import streamlit as st
import openai
import os
import fitz
from PIL import Image

import json
import PyPDF2
# from pdf2image import convert_from_path
from pytesseract import image_to_string

import pytesseract
import re
import requests
from functions1 import function as fc

st.set_page_config(page_title="Python OCR")
with st.sidebar:
   openai.api_key = st.text_input('OpenAI API Key', type='password')
   
# pytesseract.pytesseract.tesseract_cmd = 'C://Program Files//Tesseract-OCR//tesseract.exe'

st.write("Path of streamlit:", os.path.dirname(st.__file__))
def get_completion(prompt, model="gpt-3.5-turbo-16k"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
    return text

def chat_interface(extracted_text):
    # st.write("You can ask your questions here:")
    user_input=("Give me the List of drugs according to case wise?",
                "Which demonstrate the causality between the drug and the side effect according to case wise ?",
                "what is the side effect the patient experienced? Which drug was responsible for it?"
                )
    prompt = f""" Mention all the answers case wise for example
        case 1:
            answer all three questions
        case 2:
            answer all three questions
         que:```{user_input}```
         data: '''{extracted_text}'''
         """
    response = get_completion(prompt)
    st.write(response)
   

    user_input3 = st.text_area("You can ask your questions: ")

    if user_input3:
        prompt1 = f"""
         que:```{user_input3}```
         data: '''{extracted_text}'''
         """
        response2 = get_completion(prompt1)
        st.write("Answer", response2)
       
        #st.json(output_data)

def main():
   

    # Sidebar with the dropdown menu
    with st.sidebar:
           
        st.write("Sidebar")
        selected_option = st.selectbox("Select an option", ["Select Option","Translate_OCR", "Dynamic_OCR", "Research Paper Summary"],index=0)


    if selected_option == 'Select Option':
        st.title("GenrativeAI")
        st.write("Welcome")
        st.write(("👈Pick an option for left"))

    elif selected_option == "Research Paper Summary":
        st.title(" IQVIA DEMO")
        # st.write("You selected Research Paper.")
        # st.write("Please upload a Research Paper (PDF).")
        uploaded_file = st.file_uploader("Upload a Document", type=["pdf"])

        if uploaded_file is not None:
            st.write("Document Uploaded Successfully!")

            # Extract text from the uploaded PDF
            extracted_text = extract_text_from_pdf(uploaded_file.name)

            # Display the file details (optional)
            st.write("File name:", uploaded_file.name)
            st.write("File size:", uploaded_file.size, "bytes")

            # Chat interface
            chat_interface(extracted_text)  # Pass the extracted text to the chat interface



    elif selected_option == "Translate_OCR":
       
        #st.write("You selected Research Paper.")
            st.title(" IQVIA DEMO")
            # st.write("Please upload a Language Paper (PDF).")
            uploaded_file = st.file_uploader("Upload a Document", type=["pdf"])

            if uploaded_file is not None:
                st.write("Document Uploaded Successfully!")

                # Extract text from the uploaded PDF
               
                # Display the file details (optional)
                st.write("File name:", uploaded_file.name)
                st.write("File size:", uploaded_file.size, "bytes")

                # Chat interface
                # chat_interface(extracted_text)

               
# creating a pdf reader object

                def get_completion(prompt, model="gpt-3.5-turbo-16k"):
                    messages = [{"role": "user", "content": prompt}]
                    response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                       
                    temperature=0.7,
                    #      temperature=0, # this is the degree of randomness of the model's output
                    )
                    return response.choices[0].message["content"]
               
                pdfFileObject = open(uploaded_file.name, 'rb')
                pdfReader = PyPDF2.PdfReader(pdfFileObject)
                text=[]
                summary=' '
                for i in range(0,len(pdfReader.pages)):
               
                    pageObj = pdfReader.pages[i].extract_text()
                    pageObj= pageObj.replace('\t\r','')
                    pageObj= pageObj.replace('\xa0','')
                   
                    text.append(pageObj)
                # for i in range(len(text)):
                prompt =f"""UserinputData in japanese converted to english "

                {text}"""
                try:
                    response = get_completion(prompt)
                except:
                    response = get_completion(prompt)

                prompt1 =f"""
                Your task is to convert the data into json format
            Format the json proper key value pair.
            Check if the details are related to each other for example someone's details,
                            if the data contains any boxes, do create the proper check boxes for someone to tick or untick it.'
            which can inlcude name, date of birth, age, gender, weight, height etc then those should be included as a sub dict
            Entire json format should be editable as this is a pdf editable form

                ```{response}``
                """
                response1 = get_completion(prompt1)

                json_data1 = json.loads(response1)
       
                # with open("response2.json", "w") as f:
                st.write("Output:")
                st.json(json_data1)
                    #st.write(response)
                    #summary= summary+' ' +json_data1 +'\n\n'

                # Function to ask questions and get answers from the chatbot API
               

                # data = get_text_from_any_pdf(uploaded_file.name)
                # st.write(data)
                # input_text = f"""
                #         UserInput Data is spanish or japanese convert into english
                       
                #         Context: {data}
                   

                #     Answer:
                #     """

                # response = get_completion(input_text)
                # st.write(response)


    else:
        class OCR:
                

                def __init__(self):
                    # Change page title
                    
                    # Initialize variables
                    self.text = ""
                    self.analyze_text = False
            
                def initial(self):
                    # Initial page content
                    st.title("OCR Program")
                    st.write("Optical Character Recognition (OCR) implemented with Python")
                    image = st.file_uploader("Select an image", type=["png","jpg"])
                    # If an image is selected...
                    if image:
                        img = Image.open(image)
                        st.image(img, width=350)
                        st.info("Text extracted")
                        self.text = self.extract_text(img)
                        st.write("{}".format(self.text))
                        
                        # Option to analyze text
                        self.analyze_text = st.sidebar.checkbox("Analyze text")
                        if self.analyze_text == True:
                            self.show_analysis()
                
                def extract_text(self, img):
                    # The command that extracts text from the image
                    text = pytesseract.image_to_string(img, lang="eng")
                    return text
                
                def show_analysis(self):
                    # Search for CPF numbers, dates, good words, and bad words in the extraction
                    cpf = fc.search_cpf(self.text)
                    dates = fc.search_date(self.text)
                    good_words, good_words_percent = fc.search_good_words(self.text)
                    bad_words, bad_words_percent = fc.search_bad_words(self.text)
                    
                    if cpf == None:
                        st.warning("No CPF found.")
                    else:
                        cpf = fc.summarize_cpf(cpf)
                        st.success("CPF found:")
                        st.write(cpf)
            
                    if dates == None:
                        st.warning("No dates found.")
                    else:
                        dates = fc.summarize_dates(dates)
                        st.success("Dates found:")
                        st.write(dates)
                    
                    if good_words == 0:
                        st.warning("No good words identified.")
                    else:
                        st.success("Good words:")
                        st.write("{} word(s). Represent {:.2f}% of the text's words.".format(good_words, good_words_percent))
                    
                    if bad_words == 0:
                        st.warning("No bad words identified.")
                    else:
                        st.success("Bad words:")
                        st.write("{} word(s). Represent {:.2f}% of the text's words.".format(bad_words, bad_words_percent))
            
        ocr = OCR()
        ocr.initial()

        # st.write("Please upload a CIOMS Paper (PDF).")
        # uploaded_file = st.file_uploader("Upload a Document", type=["pdf"])

        # if uploaded_file is not None:
        #     st.write("Document Uploaded Successfully!")

       

        #     st.write("File name:", uploaded_file.name)
        #     st.write("File size:", uploaded_file.size, "bytes")

        #     # Chat interface
        #     # Display the file details (optional)
        #     # chat_interface(extracted_text)

        #     def convert_pdf_to_img(pdf_file):
        #         return convert_from_path(pdf_file,poppler_path=r'..//bin')


            # def convert_image_to_text(file):  
            #     text = image_to_string(file)
            #     return text


            # def get_text_from_any_pdf(pdf_file):
               
            #     images = convert_pdf_to_img(pdf_file)
            #     final_text = ""
            #     for pg, img in enumerate(images):
                   
            #         final_text += convert_image_to_text(img)
            #         #print("Page n°{}".format(pg))
            #         #print(convert_image_to_text(img))
               
            #     return final_text



            # def get_completion(prompt, model="gpt-3.5-turbo-16k"):
            #     messages = [{"role": "user", "content": prompt}]
            #     response = openai.ChatCompletion.create(
            #     model=model,
            #     messages=messages,
            #     temperature=0, # this is the degree of randomness of the model's output
            #     )
            #     return response.choices[0].message["content"]

            # ext_text = get_text_from_any_pdf(uploaded_file.name)


            # input_text = f""" Your task is to convert the data into json format
            # Format the json proper key value pair.
            # Check if the details are related to each other for example someone's details,
            #  if the data contains any checkboxes if it is tick or untick then true and false Should come,.'
            # which can inlcude name, date of birth, age, gender, weight, height etc then those should be included as a sub dict
            # Entire json format should be editable as this is a pdf editable form.
                   
                   
            #         Context: {ext_text}
               

               
            #     """
            # response = get_completion(input_text)
            # json_data = json.loads(response)
           
            # # with open("response2.json", "w") as f:
            # st.write("Output:")
            # st.json(json_data)

if __name__ == "__main__":
    main()
