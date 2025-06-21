import re

from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama, OllamaLLM
import base64
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


llm_llava = OllamaLLM(model="llava")

llm_llama3 = ChatOllama(
    model="llama3.2",
    temperature=0,
    # other params...
)

# Prompt
template = """Answer the question based only on the following context, which can include text and tables:
{context}
Question: {question}
"""
rag_prompt_text = ChatPromptTemplate.from_template(template)

def looks_like_base64(sb):
    """Check if the string looks like base64."""
    return re.match("^[A-Za-z0-9+/]+[=]{0,2}$", sb) is not None


def is_image_data(b64data):
    """Check if the base64 data is an image by looking at the start of the data."""
    image_signatures = {
        b"\xff\xd8\xff": "jpg",
        b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a": "png",
        b"\x47\x49\x46\x38": "gif",
        b"\x52\x49\x46\x46": "webp",
    }
    try:
        header = base64.b64decode(b64data)[:8]  # Decode and get the first 8 bytes
        for sig, format in image_signatures.items():
            if header.startswith(sig):
                return True
        return False
    except Exception:
        return False


def split_image_text_types(docs):
    """Split base64-encoded images and texts."""
    b64_images = []
    texts = []
    for doc in docs:
        # Check if the document is of type Document and extract page_content if so
        if isinstance(doc, Document):
            doc = doc.page_content
        if looks_like_base64(doc) and is_image_data(doc):
            b64_images.append(doc)
        else:
            texts.append(doc)
    return {"images": b64_images, "texts": texts}


def img_prompt_func(data_dict):
    # Joining the context texts into a single string
    formatted_texts = "\n".join(data_dict["context"]["texts"])
    messages = []

    # Adding image(s) to the messages if present
    if data_dict["context"]["images"]:
        image_message = {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{data_dict['context']['images'][0]}"
            },
        }
        messages.append(image_message)

    # Adding the text message for analysis
    text_message = {
        "type": "text",
        "text": (
            "Answer the question based only on the provided context, which can include text, tables, and image(s). "
            "If an image is provided, analyze it carefully to help answer the question.\n"
            f"User-provided question / keywords: {data_dict['question']}\n\n"
            "Text and / or tables:\n"
            f"{formatted_texts}"
        ),
    }
    messages.append(text_message)
    return [HumanMessage(content=messages)]


def multi_modal_rag_chain(retriever):
    """Multi-modal RAG chain"""

    # Multi-modal LLM
    # model = ChatOpenAI(temperature=0, model="gpt-4-vision-preview", max_tokens=1024)

    # RAG pipeline
    # chain = (
    #     {
    #         "context": retriever | RunnableLambda(split_image_text_types),
    #         "question": RunnablePassthrough(),
    #     }
    #     | RunnableLambda(img_prompt_func)
    #     | llm_llava
    #     | StrOutputParser()
    # )

    generation_chain = RunnableLambda(img_prompt_func) | llm_llava | StrOutputParser()
    retrieval_chain = {"context": retriever | RunnableLambda(split_image_text_types), "question": RunnablePassthrough()
                       } | RunnablePassthrough.assign(output=generation_chain)
 
    return retrieval_chain

    # return chain

def text_rag_chain(retriever):
    """RAG chain"""

    # LLM
    # model = ChatOpenAI(temperature=0, model="gpt-4")

    # RAG pipeline
    # chain = (
    #     {"context": retriever, "question": RunnablePassthrough()}
    #     | rag_prompt_text
    #     | llm_llama3
    #     | StrOutputParser()
    # )
    generation_chain = rag_prompt_text | llm_llama3 | StrOutputParser()
    retrieval_chain = {"context": retriever, "question": RunnablePassthrough()
                       } | RunnablePassthrough.assign(output=generation_chain)
 
    return retrieval_chain

    # return chain