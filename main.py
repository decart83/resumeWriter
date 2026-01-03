import streamlit as st
import google.generativeai as genai

# App Configuration
st.set_page_config(page_title="Career Tools LLC | Michael Lemke", page_icon="💼")

# --- UI Header ---
st.title("Career Builder")
st.subheader("Generate tailored Resumes and Cover Letters")

# --- Sidebar: API Configuration ---
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    st.info("Your API key is used only for this session.")

# --- Step 1: User Inputs ---
col1, col2 = st.columns(2)

with col1:
    experience_bank = st.text_area(
        "Experience Bank",
        height=300,
        placeholder="Paste your resume or list of professional achievements here..."
    )

with col2:
    job_description = st.text_area(
        "Target Job Description",
        height=300,
        placeholder="Paste the job description you are applying for here..."
    )

# --- Step 2: Choose Document Type ---
doc_type = st.radio(
    "What would you like to build?",
    ["Resume", "Cover Letter"],
    horizontal=True
)

# --- Step 3: Generation Logic ---
if st.button(f"Generate {doc_type}"):
    if not api_key:
        st.error("Please enter an API Key in the sidebar.")
    elif not experience_bank or not job_description:
        st.warning("Please provide both your Experience Bank and the Job Description.")
    else:
        try:
            # Configure Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')

            # Construct the prompt based on your requirements
            if doc_type == "Resume":
                prompt = f"""
                
                Role & Objective
                You are an expert Resume Writer and Career Strategist with decades of experience in technical recruitment and Applicant Tracking Systems (ATS). Your goal is to rewrite the provided [Job Experience] to perfectly align with the [Job Description], ensuring the final document is achievement-oriented, high-impact, and ATS-optimized.
                
                Input Data
                Target Job Description: [PASTE JOB DESCRIPTION HERE] {job_description}
                
                Current Experience/Resume: [PASTE YOUR EXPERIENCE OR CURRENT RESUME HERE] {experience_bank}
                
                Execution Instructions
                Keyword Analysis: Identify the top 5 essential hard skills and 3 core soft skills mentioned in the Job Description. Integrate these naturally into the resume.
                
                Strategic Mapping: Reorder and reword the experience bullet points so the most relevant responsibilities to the new role appear first.
                
                Quantifiable Impact: For every bullet point, use the Google XYZ Formula: "Accomplished [X] as measured by [Y], by doing [Z]." If specific numbers aren't provided in my experience, use placeholders like [X]% or $[Y] and add a comment asking me for the data.
                
                Action Verbs: Start every bullet point with a strong, diverse action verb (e.g., Spearheaded, Orchestrated, Optimized, Surpassed). Avoid passive language like "Responsible for."
                
                The "Professional Summary": Write a 3-line summary that positions me as the exact solution to the company's specific problems mentioned in the JD.
                
                Formatting Requirements
                Use a clean, reverse-chronological layout.
                
                Do not use tables, columns, or graphics (to ensure ATS compatibility).
                
                Include a dedicated "Technical Skills" or "Core Competencies" section.
                
                Tone
                Professional, confident, and results-driven.                         
                """
            else:
                prompt = f"""
                
                Role: You are an expert Career Coach and Executive Resume Writer with 20 years of experience in technical recruitment and headhunting.
                Objective: Write a high-conversion, achievement-oriented cover letter that positions me as the ideal solution for the [Job Title] role at [Company Name].
                Input Data:
                Job Description: [Paste the Job Description here] {job_description}
                My Resume/Experience: [Paste your Resume or specific bullet points here] {experience_bank}
                Execution Guidelines:
                The Hook: Start with a strong opening paragraph that avoids clichés like "I am writing to apply." Instead, mention a specific company challenge or a shared value.
                The "Why Me" (Bridge): Identify the top 3 requirements in the Job Description and write 1–2 short paragraphs showing how my specific past achievements (using the Google XYZ formula: Accomplished X as measured by Y, by doing Z) prove I can do the job.
                The "Why Them": Briefly mention why I am specifically interested in [Company Name]'s mission or current projects.
                Tone: Professional, confident, and energetic. Avoid "fluff" and "flowery" language. Keep it under 300 words.
                Formatting: Use a standard business letter format.
                Constraint: Do not hallucinate experiences I don't have. If you need more data to make a point stronger, put a placeholder in brackets like [Insert specific metric here].
                
                """

            with st.spinner(f"Gemini is architecting your {doc_type}..."):
                response = model.generate_content(prompt)

            st.success("Generation Complete!")
            st.markdown("---")
            st.markdown(response.text)

            # Option to download
            st.download_button(
                label=f"Download {doc_type} as Text File",
                data=response.text,
                file_name=f"{doc_type}_Justin_Lemke.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.caption("Justin Lemke | Strategic Operations & Program Management")
