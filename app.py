import streamlit as st
import os
from PenPal.functions import ask, get_letter_prompt, get_job_details_prompt, get_job_details
from PenPal.constants import penpal_image_path, github_image_path, patreon_image_path, error_response, default
import pdfplumber





os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title='PenPal', page_icon="🖋️", layout="centered", initial_sidebar_state='collapsed')
st.markdown(f'''
    <style>
        section[data-testid="stSidebar"] .css-ng1t4o {{width: 14rem;}}
        section[data-testid="stSidebar"] .css-1d391kg {{width: 14rem;}}
    </style>
''', unsafe_allow_html=True)


with st.sidebar:
    main_page = st.button('PenPal', use_container_width=1)
    about_page = st.button('About', use_container_width=1)
    if not about_page:
        main_page = True

if main_page:
    cola, colb = st.columns([2,9])
    cola.markdown(
        f"""<a target="_self" href="{'https://penpal.streamlit.app/'}"><img src="{penpal_image_path}" style="display:block;" width="100%" height="100%"></a>""",
        unsafe_allow_html=1)
    colb.markdown('# PenPal \nAn AI Cover Letter Writer')
    auto, manual = st.tabs(['Automatic', 'Manual'])
    with auto:
        form = st.form('form')
        resume_file = form.file_uploader('Resume', 'pdf')
        url = form.text_input('Job URL', default['url'])
        if form.form_submit_button('Submit'):
            with pdfplumber.open(resume_file) as pdf:
                resume = ''
                for page in pdf.pages:
                    resume += page.extract_text(x_tolerance=1, y_tolerance=1)
            with st.spinner("Gathering job details..."):
                job_details_prompt = get_job_details_prompt(url)
                try:
                    job_details_raw = ask(job_details_prompt)
                    company, title, skills, description = get_job_details(job_details_raw)
                except Exception as e:
                    st.write(e)
                    st.write(job_details_raw)
            with st.spinner("Writing cover letter..."):
                letter_prompt = get_letter_prompt(company, title, skills, description, resume)
                ask(letter_prompt, write=True)
    with manual:
        form = st.form('form_manual')
        col1, col2 = form.columns([1,1])
        resume = col1.text_area('Resume', default['resume'], height=425)
        company = col2.text_input('Company', default['company'])
        title = col2.text_input('Title', default['title'])
        skills = col2.text_area('Desired Skills', default['skills'])
        description = col2.text_area('Job Description', default['description'])
        if form.form_submit_button('Submit'):
            prompt = get_letter_prompt(company, title, skills, description, resume)
            with st.spinner("Writing cover letter..."):
                ask(prompt, write=True)
if about_page:
    st.markdown('# About \n')
    st.write('Built by [Erick Martinez](https://github.com/erickfm) using OpenAI, LangChain, and Streamlit. PenPal icons by me'
             '\n\nModel is tuned for more variety in answers. ChatGPT is trained on data limited to September 2021.')
    st.markdown(f"""<div><a href="https://github.com/erickfm/PenPal"><img src="{github_image_path}" style="padding-right: 10px;" width="6%" height="6%"></a> 
    <a href="https://www.patreon.com/ErickFMartinez"><img src="{patreon_image_path}" style="padding-right: 10px;" width="6%" height="6%"></a></div>""", unsafe_allow_html=1)
