import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("Cover Letter Generator")
    url_input = st.text_input("Enter a URL: ", value="https://jobs.disneycareers.com/job/bristol/associate-project-manager-design-and-delivery/391/79656190512")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            page_data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(page_data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                letter = llm.write_letter(job, links)
                st.code(letter, language="markdown")
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cover Letter Generator")
    create_streamlit_app(chain, portfolio, clean_text)





