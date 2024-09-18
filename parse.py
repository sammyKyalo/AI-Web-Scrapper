from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
import json
import re
import streamlit as st
import time

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key = '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'
    )


template = (
    "You are tasked with oextracting specific information from the following text content: {dom_content}."
    "Please follow this instruction carefully: \n\n"
    "1. **Extract Information:** Only extract information that directly matches the provided description: {parse_description}."
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response (NO PREAMBLE)."
    "3. **Empty Responses: ** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your script should contain only the data that is explicitly requested."
    "5. Always have a paragraph structure that is clearly understable when answering questions."
    "6. AVOID REPETITION."
)

@st.cache_data
def parse_with_groq(dom_chunks, parse_description):
    prompt = PromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})

        parsed_results.append(response.content) 
        print(f"parsed batch {i} of {len(dom_chunks)}")
        time.sleep(1)

    return "\n".join(parsed_results)


