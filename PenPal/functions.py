from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI
import streamlit as st
chat = ChatOpenAI(temperature=1, model_name='gpt-3.5-turbo')


def chatgpt(content, sys="You are a helpful assistant."):
    """Useful knowledgeable assistant. Input should be a search query."""
    messages = [
        SystemMessage(content=sys),
        HumanMessage(content=content)
    ]
    return chat(messages).content


def generate(prompt):
    with st.spinner("Thinking..."):
        response = chatgpt(prompt)
        st.write(response)
    # with st.spinner("Fetching results..."):
    #     for film in films:
    #         search_results = movie.search(film)
    #         n = 0
    #         result = search_results[n]
    #         while result.release_date.split('-')[0] != films[film]["release year"]:
    #             n += 1
    #             result = search_results[n]
    #         col1, col2 = st.columns([1, 1])
    #         col1.image("https://image.tmdb.org/t/p/w500/" + result.poster_path)
    #         col2.write(f"### [{result.title}](https://www.themoviedb.org/movie/{result.id}) ({result.release_date.split('-')[0]})")
    #         col2.write(result.overview)


def get_prompt(company, title, skills, description, resume, name):
    prompt = f"""Given a company, job title, desired skills, job description, resume, and applicant name, return a cover letter likely to get the applicant an interview. 
    Company: {company}
    Job title: {title}
    Desired skills: {skills}
    Job description: {description}
    Resume: {resume}
    Applicant Name: {name}
    
    
    Cover Letter: """
    return prompt
