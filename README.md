# CoverLetterGenerator
Training Llama 3.1-8b to generate a cover letter, according to job posting URL

![image](https://github.com/user-attachments/assets/4f845089-f649-4c69-98e3-344f44c65809)

I used Groq for fast inference of an llm model - Llama 3.1-8b-instant. It gives fast response times.

Langchain was used to process the job posting from the URL, extract key requirements and handle Groq API

Chromadb was used for its ability to capture semantic meaning, so that I can match the correct portfolio to the job posting (according to its description)

