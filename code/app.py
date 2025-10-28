import pdfplumber
import google.generativeai as genai
import streamlit as st
from docx import Document

#Setup API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-flash")

#Extracting text from pdf
def extract_text_from_pdf(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text="".join(page.extract_text() for page in pdf.pages if page.extract_text())
        return text if text else "NO TEXT FOUND IN RESUME!!"
    except Exception as e:
        return f"ERROR READING IN PDF:{e}"
    
#Extracting text from word file
def extract_text_from_docx(uploaded_file):
    try:
        doc=Document(uploaded_file)
        text="\n".join([para.text for para in doc.paragraphs])
        return text if text.strip() else "NO TEXT FOUND IN RESUME!!!"
    except Exception as e:
        return f"ERROR READING IN WORD FILE:{e}"

#Sending text to AI to roast the resume
def roast_resume(resume_text):
    prompt=f"Here is a resume:\n\n{resume_text}\n\nRoast this resume in a offensive, harsh,go 18+ but don't use inappropriate words and no mercy way."
    try:
        response = model.generate_content(prompt)
        return response.text if response and hasattr(response, "text") else "❌ No response from AI."
    except Exception as e:
        return f"ERROR GENERATING RESPONSE:{e}"
    
st.set_page_config(page_title="AI RESUME ROASTER BY AJITESH",page_icon="🔥")
st.title("AI RESUME ROASTER BY AJITESH")
st.write("UPLOAD YOUR RESUME TO GET ROASTED!!")
st.divider()


uploaded_file=st.file_uploader("📂 Upload your Resume (PDF/DOCX only)",type=["pdf","docx"])

if uploaded_file is not None:
    st.write("📄 **Resume uploaded successfully! Processing...**")
    #Extract resume
    file_type=uploaded_file.name.split(".")[-1]
    if file_type=="pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    elif file_type=="docx":
        resume_text=extract_text_from_docx(uploaded_file)
    else:
        st.error("FILE IMPORTED IS OF UNSUPPORTED FORMAT!!")


    if resume_text.startswith("❌"):
        st.error(resume_text)  # Display error if PDF couldn't be processed
    else:
        st.write("✅ **Extracted Resume Content:**")
        st.text_area("Resume Text", resume_text, height=150)

if st.button("Roast My Resume"):
    with st.spinner("ROASTING YOUR RESUME.."):
        roast=roast=roast_resume(resume_text)
        st.subheader("!!ROAST!!")
        st.write(roast)




# import google.generativeai as genai

# # Configure API key
# genai.configure(api_key="AIzaSyCfmygwggJss-_ZXz9KbmU7yr7GGXxj1kk")

# # List available models
# models = genai.list_models()
# for model in models:
#     print(model.name)
