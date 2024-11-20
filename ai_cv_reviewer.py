import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
import os

class CVReviewBot:
    def __init__(self):
        self.system_prompt = """You are an expert CV/Resume reviewer with years of experience in HR and recruitment. 
        Your task is to provide detailed, constructive feedback on CVs in a friendly and professional manner.
        
        When reviewing a CV, you should:
        1. Analyze the overall structure and format
        2. Check for essential components (contact info, education, experience, skills)
        3. Evaluate the content quality and impact
        4. Provide specific, actionable feedback
        5. Give examples of improvements where relevant
        
        Please be encouraging but honest, and always maintain a professional tone.
        Provide feedback in Bahasa Indonesia."""

    def initialize_chat(self):
        # Initialize HuggingChat (free alternative to GPT)
        try:
            # Login to huggingface and grant authorization to huggingchat
            sign = Login("daffagt123@gmail.com", "Sakdunia@123")  # Replace with your credentials
            cookies = sign.login()
            return hugchat.ChatBot(cookies=cookies)
        except Exception as e:
            st.error(f"Error initializing chat: {str(e)}")
            return None

    def review_cv(self, cv_text):
        chatbot = self.initialize_chat()
        if not chatbot:
            return "Maaf, terjadi kesalahan dalam menginisialisasi sistem."

        prompt = f"""{self.system_prompt}

        Berikut adalah CV yang perlu direview:

        {cv_text}

        Berikan review yang detail dengan format berikut:
        
        1. Kesan Pertama & Format
        2. Analisis Komponen:
           - Informasi Kontak
           - Pengalaman
           - Pendidikan
           - Skills & Kompetensi
        3. Saran Perbaikan Spesifik
        4. Kesimpulan & Skor (0-100)"""

        try:
            response = chatbot.chat(prompt)
            return response.text
        except Exception as e:
            return f"Maaf, terjadi kesalahan dalam proses review: {str(e)}"

def main():
    st.set_page_config(page_title="AI CV Reviewer", page_icon="📄", layout="wide")
    
    st.title("🤖 SAKAMERS CV Review Assistant")
    st.markdown("""
    ### Selamat datang di AI CV Review Assistant! 
    Upload CV Anda dan dapatkan feedback detail dari AI yang akan membantu meningkatkan kualitas CV Anda.
    """)

    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    reviewer = CVReviewBot()

    # File upload
    cv_file = st.file_uploader("Upload CV Anda (PDF/DOC/TXT)", type=['pdf', 'doc', 'docx', 'txt'])
    
    # Text input as alternative
    cv_text = st.text_area("Atau paste isi CV Anda di sini:", height=300)

    if st.button("Review CV"):
        with st.spinner("AI sedang menganalisis CV Anda..."):
            if cv_file is not None:
                # Add file processing logic here
                # For now, we'll just use text input
                feedback = reviewer.review_cv(cv_text)
            elif cv_text:
                feedback = reviewer.review_cv(cv_text)
            else:
                st.warning("Mohon upload file CV atau paste isi CV terlebih dahulu.")
                return

            # Display feedback
            st.markdown("### 📋 Hasil Review")
            st.markdown(feedback)

            # Add to chat history
            st.session_state.chat_history.append(("CV", cv_text))
            st.session_state.chat_history.append(("AI", feedback))

    # Chat interface for follow-up questions
    st.markdown("### 💬 Tanya Lebih Lanjut")
    question = st.text_input("Ada pertanyaan tentang feedback yang diberikan?")
    
    if st.button("Tanya"):
        if question:
            with st.spinner("AI sedang memproses pertanyaan Anda..."):
                follow_up_prompt = f"""Berdasarkan CV dan review sebelumnya, tolong jawab pertanyaan berikut:
                {question}
                
                Berikan jawaban yang spesifik dan helpful dalam Bahasa Indonesia."""
                
                response = reviewer.review_cv(follow_up_prompt)
                st.markdown(response)
                
                # Add to chat history
                st.session_state.chat_history.append(("User", question))
                st.session_state.chat_history.append(("AI", response))

    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 📝 Riwayat Diskusi")
        for role, content in st.session_state.chat_history:
            if role in ["AI", "User"]:
                st.markdown(f"**{role}:** {content}")

if __name__ == "__main__":
    main()