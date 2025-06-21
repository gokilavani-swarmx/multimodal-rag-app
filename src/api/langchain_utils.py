from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import OllamaLLM
from typing import List
from langchain_core.documents import Document
import os
from chroma_utils import vectorstore
from chroma_utils import multi_vector_img, multimodal_embd, multi_vector_text, baseline_retriver

from langchain_ollama import ChatOllama, OllamaLLM

from multimodal_pipeline import *

from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough

llm_llama3 = ChatOllama(
    model="llama3.2:1b",
    temperature=0,
    # other params...
)

# retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

output_parser = StrOutputParser()

# Build
def get_rag_chain(model=None):
    chain_baseline = text_rag_chain(baseline_retriver.as_retriever())
    chain_mv_text = text_rag_chain(multi_vector_text.as_retriever())

    # Multi-modal RAG chains
    chain_multimodal_mv_img = multi_modal_rag_chain(multi_vector_img.as_retriever())
    chain_multimodal_embd = multi_modal_rag_chain(multimodal_embd.as_retriever())

    return chain_baseline, chain_mv_text, chain_multimodal_mv_img, chain_multimodal_embd


def summarize_result(answer_dict):
    answer_txt = ''
    for idx, itms in enumerate(answer_dict.items()):
        key, val = itms
        answer_txt += val['output'] + "\n"

    template = '''summarize the text concisely while retaining all critical information.
    Strictly Return only the summary. Do not add anything on your own.

    TEXT: {text}
    '''

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm_llama3 
    answer = chain.invoke({'text':answer_txt})
    return answer.content