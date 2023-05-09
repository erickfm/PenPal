import streamlit as st
import os
from PenPal.functions import generate, get_prompt
from PenPal.constants import penpal_image_path, github_image_path, patreon_image_path, error_response, default

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title='PenPal', page_icon="🖋️", layout="wide", initial_sidebar_state='collapsed')
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
    cola.markdown(f"""<a target="_self" href="{'https://penpal.streamlit.app/'}"><img src="{penpal_image_path}" style="display:block;" width="100%" height="100%"></a>""", unsafe_allow_html=1)
    colb.markdown('# PenPal \nAn AI Cover Letter Writer')
    form = st.form('form')
    col1, col2 = form.columns([1,1])
    name = col1.text_input('Name', default['name'])
    resume = col1.text_area('Resume', default['resume'], height=340)
    company = col2.text_input('Company', default['company'])
    title = col2.text_input('Title', default['title'])
    skills = col2.text_area('Desired Skills', default['skills'])
    description = col2.text_area('Job Description', default['description'])
    if form.form_submit_button('Submit'):
        prompt = get_prompt(company, title, skills, description, resume, name)
        try:
            generate(prompt)
        except Exception as e:
            try:
                generate(prompt)
            except Exception as e:
                st.error(error_response)
if about_page:
    st.markdown('# About \n')
    st.write('Built by [Erick Martinez](https://github.com/erickfm) using OpenAI, LangChain, and Streamlit. PenPal icons by me'
             '\n\nModel is tuned for more variety in answers. ChatGPT is trained on data limited to September 2021.')
    st.markdown(f"""<div><a href="https://github.com/erickfm/PenPal"><img src="{github_image_path}" style="padding-right: 10px;" width="6%" height="6%"></a> 
    <a href="https://www.patreon.com/ErickFMartinez"><img src="{patreon_image_path}" style="padding-right: 10px;" width="6%" height="6%"></a></div>""", unsafe_allow_html=1)
