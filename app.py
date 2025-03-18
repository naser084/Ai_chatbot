import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import tempfile

# Configure the Gemini API with your API key
genai.configure(api_key="AIzaSyCe1uBjYi7iAJoL8yGQRCPKP8I_dV3ofDA")

model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = ""
if "candidate_details" not in st.session_state:
    st.session_state["candidate_details"] = {}

# Styling
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        color: #007bff;
        font-size: 50px;
        margin-top: 20px;
        margin-bottom: 30px;
    }
    .description {
        font-size: 18px;
        margin: 20px;
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='title'>Welcome to TalentScout AI Hiring Assistant</h1>", unsafe_allow_html=True)

# Candidate Details Form
st.sidebar.title("Candidate Details")
full_name = st.sidebar.text_input("Full Name")
email = st.sidebar.text_input("Email")
phone = st.sidebar.text_input("Phone Number")
years_experience = st.sidebar.number_input("Years of Experience", min_value=0, max_value=50, step=1)
location = st.sidebar.text_input("Current Location")
desired_position = st.sidebar.text_input("Desired Position")
tech_stack = st.sidebar.text_area("Tech Stack (Languages, Frameworks, Tools)")

if st.sidebar.button("Submit Details"):
    if full_name and email and phone and desired_position and tech_stack:
        st.session_state["candidate_details"] = {
            "Full Name": full_name,
            "Email": email,
            "Phone": phone,
            "Experience": years_experience,
            "Location": location,
            "Position": desired_position,
            "Tech Stack": tech_stack,
        }
        st.sidebar.success("Candidate details submitted successfully!")
    else:
        st.sidebar.error("Please fill in all required fields.")

# Chat History Management
if st.sidebar.button("Show Chat History"):
    if st.session_state["chat_history"]:
        st.sidebar.text_area("Chat History", st.session_state["chat_history"], height=300)
    else:
        st.sidebar.write("No chat history available.")

if st.sidebar.button("Delete Chat History"):
    st.session_state["chat_history"] = ""
    st.sidebar.success("Chat history deleted.")

# PDF Generation Function
def generate_pdf(chat_history):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, chat_history)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

if st.sidebar.button("Download Chat as PDF"):
    if st.session_state["chat_history"]:
        pdf_file = generate_pdf(st.session_state["chat_history"])
        with open(pdf_file, "rb") as file:
            st.sidebar.download_button(
                label="Download PDF",
                data=file,
                file_name="chat_history.pdf",
                mime="application/pdf"
            )
    else:
        st.sidebar.error("No chat history to download.")

# Chat Interaction
user_input = st.text_input("Ask something about the hiring process or your application:")

if user_input:
    if user_input.lower() == "delete chat history":
        st.session_state["chat_history"] = ""
        st.success("Chat history deleted.")
    else:
        candidate_info = "\n".join([f"{key}: {value}" for key, value in st.session_state["candidate_details"].items()])
        hiring_prompt = (
            f"You are an AI Hiring Assistant for TalentScout. Candidate details:\n{candidate_info}\n"
            f"Answer professionally and generate 3-5 technical questions based on their tech stack."
        )
        
        try:
            response = model.generate_content(hiring_prompt + f" Query: {user_input}")
            response_text = response.text if response and response.text else "I'm here to help!"
            st.session_state["chat_history"] += f"\nUser: {user_input}\nAI: {response_text}\n"
        except Exception as e:
            response_text = f"Error: {str(e)}"
            st.session_state["chat_history"] += f"\nUser: {user_input}\nAI: {response_text}\n"
        
        st.markdown(f"<div class='description'><strong>AI Response:</strong><br>{response_text}</div>", unsafe_allow_html=True)

# Footer
st.sidebar.markdown("### Next Steps")
st.sidebar.markdown("Our recruiters will contact you shortly!")