 
import streamlit as st
import google.generativeai as genai

# Configure the Gemini API with your API key
genai.configure(api_key="AIzaSyCe1uBjYi7iAJoL8yGQRCPKP8I_dV3ofDA")

model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize session state for storing chat history and candidate details
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = ""
if "candidate_details" not in st.session_state:
    st.session_state["candidate_details"] = {}

# Styling
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f8ff;
    }
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

# Collecting Candidate Information
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
        st.sidebar.error("Please fill in all the required fields.")

# Chat history button and display
if st.sidebar.button("Show Chat History"):
    if st.session_state["chat_history"]:
        st.sidebar.text_area("Chat History", st.session_state["chat_history"], height=300)
    else:
        st.sidebar.write("No chat history available.")

# Delete chat history button
if st.sidebar.button("Delete Chat History"):
    st.session_state["chat_history"] = ""
    st.sidebar.success("Chat history has been deleted.")

# Chatbot Input
user_input = st.text_input("Ask something about the hiring process or your application:")

if user_input:
    if user_input.lower() == "delete chat history":
        st.session_state["chat_history"] = ""
        st.success("Chat history has been deleted.")
    else:
        candidate_info = "".join([f"{key}: {value}\n" for key, value in st.session_state["candidate_details"].items()])
        hiring_prompt = (
            f"You are an AI-powered Hiring Assistant for 'TalentScout,' a recruitment agency specializing in technology placements. "
            f"You are currently screening a candidate with the following details:\n{candidate_info} "
            f"Answer their query professionally and concisely. If applicable, ask technical screening questions based on their tech stack."
        )
        
        try:
            response = model.generate_content(hiring_prompt + f" Query: {user_input}")
            response_text = response.text if response and response.text else "I am here to assist you in the hiring process!"
            st.session_state["chat_history"] += f"\nUser: {user_input}\nAI: {response_text}\n"
        except Exception as e:
            response_text = f"An error occurred: {str(e)}"
        
        st.markdown(f"<div class='description'><strong>AI Response:</strong><br>{response_text}</div>", unsafe_allow_html=True)

# Next Steps
st.sidebar.markdown("### Next Steps")
st.sidebar.markdown("Our recruiters will review your details and contact you shortly!")
