import streamlit as st
from transformers import pipeline
import re

def initialize_model():
    # Menggunakan model BERT multilingual yang gratis
    analyzer = pipeline(
        "text-classification",
        model="bert-base-multilingual-uncased",
        return_all_scores=True
    )
    return analyzer

def preprocess_cv(cv_text):
    # Membersihkan text CV
    cv_text = re.sub(r'\s+', ' ', cv_text)
    cv_text = cv_text.strip()
    return cv_text

def analyze_cv(cv_text):
    # Analisis komponen CV
    sections = {
        'personal_info': check_personal_info(cv_text),
        'education': check_education(cv_text),
        'experience': check_experience(cv_text),
        'skills': check_skills(cv_text)
    }
    return generate_feedback(sections)

def check_personal_info(text):
    has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+', text))
    has_phone = bool(re.search(r'[\d\-\+\(\)]{10,}', text))
    return {
        'complete': has_email and has_phone,
        'missing': [] if (has_email and has_phone) else 
                  ['Email' if not has_email else None,
                   'Phone' if not has_phone else None]
    }

def check_education(text):
    edu_keywords = ['pendidikan', 'education', 'gelar', 'sarjana', 's1', 's2', 'diploma']
    has_education = any(keyword in text.lower() for keyword in edu_keywords)
    return {
        'present': has_education,
        'suggestions': [] if has_education else ['Tambahkan riwayat pendidikan formal']
    }

def check_experience(text):
    exp_keywords = ['pengalaman', 'experience', 'kerja', 'magang', 'internship']
    has_experience = any(keyword in text.lower() for keyword in exp_keywords)
    return {
        'present': has_experience,
        'suggestions': [] if has_experience else ['Tambahkan pengalaman kerja atau magang']
    }

def check_skills(text):
    skill_keywords = ['skills', 'keahlian', 'kemampuan', 'kompetensi']
    has_skills = any(keyword in text.lower() for keyword in skill_keywords)
    return {
        'present': has_skills,
        'suggestions': [] if has_skills else ['Tambahkan bagian skills dan kompetensi']
    }

def generate_feedback(analysis):
    feedback = []
    score = 0
    max_score = 100
    
    # Personal Info
    if analysis['personal_info']['complete']:
        score += 25
    else:
        feedback.append(f"⚠️ Informasi kontak kurang lengkap. Tambahkan: {', '.join(filter(None, analysis['personal_info']['missing']))}")
    
    # Education
    if analysis['education']['present']:
        score += 25
    else:
        feedback.extend(analysis['education']['suggestions'])
    
    # Experience
    if analysis['experience']['present']:
        score += 25
    else:
        feedback.extend(analysis['experience']['suggestions'])
    
    # Skills
    if analysis['skills']['present']:
        score += 25
    else:
        feedback.extend(analysis['skills']['suggestions'])
    
    return {
        'score': score,
        'feedback': feedback,
        'summary': generate_summary(score, feedback)
    }

def generate_summary(score, feedback):
    if score >= 90:
        return "CV Anda sudah sangat baik! Beberapa penyempurnaan kecil mungkin bisa dilakukan."
    elif score >= 70:
        return "CV Anda cukup baik, tapi masih ada beberapa hal yang bisa ditingkatkan."
    elif score >= 50:
        return "CV Anda memerlukan beberapa perbaikan untuk mencapai standar profesional."
    else:
        return "CV Anda memerlukan banyak perbaikan. Ikuti saran-saran yang diberikan untuk meningkatkan kualitasnya."

# Streamlit UI
def main():
    st.title("CV Review Assistant 📄")
    st.write("Paste CV Anda di bawah ini untuk mendapatkan feedback")
    
    cv_text = st.text_area("CV Text", height=300)
    
    if st.button("Analyze CV"):
        if cv_text:
            cv_text = preprocess_cv(cv_text)
            results = analyze_cv(cv_text)
            
            st.header("Hasil Analisis")
            st.metric("Skor CV", f"{results['score']}/100")
            
            st.subheader("Summary")
            st.write(results['summary'])
            
            st.subheader("Saran Perbaikan")
            if results['feedback']:
                for item in results['feedback']:
                    st.write(f"• {item}")
            else:
                st.write("CV Anda sudah memenuhi kriteria dasar! 🎉")
        else:
            st.error("Please input your CV text first!")

if __name__ == "__main__":
    main()