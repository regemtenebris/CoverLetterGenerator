import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))
    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing following keys:
            'role','experience','skills' and 'description'. Do not include any responsibilites in description, only ABOUT the job.
            Only return the valid JSON. Do not give the name of the job in the beginning, only in the role. Do not put any text except the keys and their corresponding values. 
            ### VALID JSON (NO PREAMBLE):
            """
        )

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'page_data': cleaned_text})
        try:
            j_parser = JsonOutputParser()
            res = j_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse")
        return res if isinstance(res, list) else [res]

    def write_letter(self, job, links):
        prompt_letter = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION
            {job_description}
            ### INSTRUCTION
            Using the job description provided, write a cover letter that suits the requirements of the given company. Make sure that the cover 
            letter is brief, but provides all the necessary details. Start with something like: Hello, my name is Dias Daurenuly... 
            Also add the most relevant ones from the following links to showcase your portfolio {link_list}
            Do not provide a preamble.
            ### COVER LETTER (NO PREAMBLE):

            """
        )

        chain_letter = prompt_letter | self.llm
        res = chain_letter.invoke({"job_description": str(job), "link_list": links})
        return res.content
