import streamlit as st
import os
from PenPal.functions import ask, get_letter_prompt, get_job_details_prompt, get_job_details, get_webpage_text
from PenPal.constants import penpal_image_path, github_image_path, patreon_image_path, default
import pdfplumber
from urllib.error import HTTPError

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
        url = form.text_input('Job URL')
        if form.form_submit_button('Submit'):
            try:
                with pdfplumber.open(resume_file) as pdf:
                    resume = ''
                    for page in pdf.pages:
                        resume += page.extract_text(x_tolerance=1, y_tolerance=1)
            except AttributeError as e:
                st.error('Please upload a resume or try out the manual input method.')
                st.stop()
            with st.spinner("Gathering job details..."):
                try:
                    job_details_prompt = get_job_details_prompt(get_webpage_text(url))
                except HTTPError as e:
                    st.error(f"**HTTPError:** {url} \n\n PenPal doesn't currently handle dynamically generated text. "
                             f"Please try copy-pasting using the manual method.")
                    st.stop()
                job_details_raw = ask(job_details_prompt, write=True)
                company, title, skills, description = get_job_details(job_details_raw)
            with st.spinner("Writing cover letter..."):
                letter_prompt = get_letter_prompt(company, title, skills, description, resume)
                ask(letter_prompt, write=True)
    with manual:
        pass
        form = st.form('form_manual')
        col1, col2 = form.columns([1,1])
        resume = col1.text_area('Resume', default['resume'], height=425)
        job_post = col2.text_area('Job Post', default['job post'], height=425)

        if form.form_submit_button('Submit'):
            with st.spinner("Gathering job details..."):
                job_details_prompt = get_job_details_prompt(job_post)
                job_details_raw = ask(job_details_prompt, write=True)
                company, title, skills, description = get_job_details(job_details_raw)
            with st.spinner("Writing cover letter..."):
                letter_prompt = get_letter_prompt(company, title, skills, description, resume)
                ask(letter_prompt, write=True)
if about_page:
    st.markdown('# About \n')
    st.write('Built by [Erick Martinez](https://github.com/erickfm) using OpenAI, LangChain, and Streamlit. PenPal icons by me'
             '\n\nModel is tuned for more variety in answers. ChatGPT is trained on data limited to September 2021.')
    st.markdown(f"""<div><a href="https://github.com/erickfm/PenPal"><img src="{github_image_path}" style="padding-right: 10px;" width="6%" height="6%"></a> 
    <a href="https://www.patreon.com/ErickFMartinez"><img src="{patreon_image_path}" style="padding-right: 10px;" width="6%" height="6%"></a></div>""", unsafe_allow_html=1)
