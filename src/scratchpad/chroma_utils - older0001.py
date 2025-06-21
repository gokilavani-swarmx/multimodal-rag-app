from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.open_clip import OpenCLIPEmbeddings
# from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryStore
from langchain_core.documents import Document
from PIL import Image

import base64
import io
import uuid
import os
from io import BytesIO

# docling modules import
import datetime
import tempfile
import logging
import time
from pathlib import Path

from db_utils import insert_latency_metrics

import pandas as pd

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.utils.export import generate_multimodal_pages
from docling.utils.utils import create_hash

_log = logging.getLogger(__name__)

IMAGE_RESOLUTION_SCALE = 3.0
from docling_core.types.doc import ImageRefMode, PictureItem, TableItem

pipeline_options = PdfPipelineOptions()
pipeline_options.images_scale = IMAGE_RESOLUTION_SCALE
pipeline_options.generate_page_images = True
pipeline_options.generate_picture_images = True
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
    WordFormatOption,
)
from docling.pipeline.simple_pipeline import SimplePipeline
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline

doc_converter = (
    DocumentConverter(  # all of the below is optional, has internal defaults.
        allowed_formats=[
            InputFormat.PDF,
            InputFormat.IMAGE,
            InputFormat.DOCX,
            InputFormat.HTML,
            InputFormat.PPTX,
            InputFormat.ASCIIDOC,
            InputFormat.MD,
        ],  # whitelist formats, non-matching files are ignored.
        format_options={
        #     InputFormat.PDF: PdfFormatOption(
        #         pipeline_cls=StandardPdfPipeline, backend=PyPdfiumDocumentBackend
        #     )
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        ,
            InputFormat.DOCX: WordFormatOption(
                pipeline_cls=SimplePipeline  # , backend=MsWordDocumentBackend
            ),
        },
    )
)
# docling modules import end

from langchain_ollama import ChatOllama, OllamaLLM

llm_llama3 = ChatOllama(
    model="llama3.2",
    temperature=0,
    # other params...
)

llm_llava = OllamaLLM(model="llava", 
    temperature=0,)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
sntnc_trnsfrmr_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# embedding_function = OpenAIEmbeddings()
# embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# Create chroma w/ multi-modal embeddings
# baseline_retriver = Chroma(persist_directory="./baseline_retriver", collection_name="baseline", embedding_function=sntnc_trnsfrmr_embeddings)
# multimodal_embd = Chroma(persist_directory="./multimodal_embd_db", collection_name="multimodal_embd", embedding_function=OpenCLIPEmbeddings())
# multi_vector_img = Chroma(persist_directory="./multi_vector_img_db",  collection_name="multi_vector_img", embedding_function=sntnc_trnsfrmr_embeddings)
# multi_vector_text = Chroma(persist_directory="./multi_vector_text", collection_name="multi_vector_text", embedding_function=sntnc_trnsfrmr_embeddings)


baseline_retriver = Chroma(persist_directory="./src/vector_dbs/baseline_retriver", embedding_function=sntnc_trnsfrmr_embeddings)
multimodal_embd = Chroma(persist_directory="./src/vector_dbs/multimodal_embd_db", embedding_function=OpenCLIPEmbeddings())
multi_vector_img = Chroma(persist_directory="./src/vector_dbs/multi_vector_img_db", embedding_function=sntnc_trnsfrmr_embeddings)
multi_vector_text = Chroma(persist_directory="./src/vector_dbs/multi_vector_text", embedding_function=sntnc_trnsfrmr_embeddings)

vectorstore = Chroma(persist_directory="./src/vector_dbs/chroma_db", embedding_function=sntnc_trnsfrmr_embeddings)

def encode_image(image_input):
    """
    Convert image file path or PIL image to Base64 encoded string.

    :param image_input: Path to the image file or a PIL image object
    :return: Base64 encoded string
    """
    if isinstance(image_input, str):
        # Assume the input is a file path
        with open(image_input, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    elif isinstance(image_input, Image.Image):
        # Assume the input is a PIL image
        buffered = BytesIO()
        image_input.save(buffered, format="JPEG")  # You can change the format if needed
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    else:
        raise TypeError("Unsupported input type. Please provide a file path or a PIL image.")

def load_and_split_document(file_path: str) -> List[Document]:

    # Prompt
    prompt_text = """You are an assistant tasked with summarizing tables and text for retrieval. \
    These summaries will be embedded and used to retrieve the raw text or table elements. \
    Give a concise summary of the table or text that is well optimized for retrieval. Table or text: {element} """
    prompt = ChatPromptTemplate.from_template(prompt_text)

    # Text summary chain
    # model = ChatOpenAI(temperature=0, model="gpt-4")
    summarize_chain = {"element": lambda x: x} | prompt | llm_llama3 | StrOutputParser()

    latency_dict = {}
    # if file_path.endswith('.pdf'):
    #     loader = PyPDFLoader(file_path)
    # elif file_path.endswith('.docx'):
    #     loader = Docx2txtLoader(file_path)
    # elif file_path.endswith('.html'):
    #     loader = UnstructuredHTMLLoader(file_path)
    # else:
    #     raise ValueError(f"Unsupported file type: {file_path}")
    
    # documents = loader.load()
    # return text_splitter.split_documents(documents)

    fldr_nm = "_".join(Path(file_path).name.replace("temp_","").split('.')[:-1])
    output_dir = Path(f"./src/prcsd_docs/docling/{fldr_nm}")
    os.makedirs(output_dir, exist_ok=True)

    # docling code
    table_strt_time = time.time()
    conv_results = doc_converter.convert_all([file_path])
    tables = [i.export_to_markdown() for conv_res in conv_results for i in conv_res.document.tables]
    numn_tables = len(tables)
    table_end_time = time.time()
    table_creation_time = table_end_time - table_strt_time

    # Apply to tables
    table_summaries = summarize_chain.batch(tables, {"max_concurrency": 5})

    table_smry_time = time.time() - table_end_time

    texts = []
    tmp = ''
    cntr = 0
    not_prcsd = []

    text_strt_time = time.time()
    conv_results = doc_converter.convert_all([file_path])
    for conv_res in conv_results:
        for idx, txt in enumerate(conv_res.document.texts):
            if txt.label != 'section_header':
                tmp += ' ' + txt.text
            elif txt.label == 'section_header':
                texts.append(tmp)
                tmp = txt.text + "\n"
            else:
                not_prcsd.append([idx, txt])


    text_end_time = time.time()
    text_creation_time = text_end_time - text_strt_time
    # Apply to text
    text_summaries = summarize_chain.batch(texts, {"max_concurrency": 5})
    text_smry_time = time.time() - text_end_time


    # Store base64 encoded images
    img_base64_list = []

    # Store image summaries
    image_summaries = []

    llm_llava = OllamaLLM(model="llava")

    img_smry_prompt = "Describe the image in detail. Be specific about graphs, such as bar plots."


    image_smry_start_time = time.time()
    # Apply to images
    conv_results = doc_converter.convert_all([file_path])
    print(type(file_path))
    os.makedirs(f"{output_dir}/images/", exist_ok=True)
    for conv_res in conv_results:
        doc_filename = conv_res.input.file.stem
        # tmp_res = conv_res
        picture_counter = 0
        for idx, element in enumerate(conv_res.document.pictures):
            # break
            img = element.get_image(conv_res.document)
            element_image_filename = (
                 output_dir / f"images/{doc_filename.replace("temp_","")}-picture-{picture_counter}.png"
            )
            with element_image_filename.open("wb") as fp:
                element.get_image(conv_res.document).save(fp, "PNG")
            picture_counter += 1
            # Plot the image using matplotlib 
            # plt.imshow(img)
            # plt.axis('off')
            # plt.show()
            image_b64 = encode_image(img)
            img_base64_list.append(image_b64)
            llm_with_image_context = llm_llava.bind(images=[image_b64])
            mdl_rstl = llm_with_image_context.invoke(img_smry_prompt)
            image_summaries.append(mdl_rstl)
    num_images = len(img_base64_list)

    image_smry_time = image_smry_start_time - time.time()

    text_extract_strt_time = time.time()
    conv_results = doc_converter.convert_all([file_path])
    
    for res in conv_results:
        with (output_dir / f"{res.input.file.stem.replace(" ","_")}.md").open("w", encoding="utf-8") as fp:
            fp.write(res.document.export_to_markdown())

    loader = DirectoryLoader(output_dir, glob="*.md")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    all_splits_pypdf = text_splitter.split_documents(docs)
    all_splits_pypdf_texts = [d.page_content for d in all_splits_pypdf]
    text_extrac_time = time.time() - text_extract_strt_time

    latency_dict["table_creation_time"] = table_creation_time
    latency_dict["table_smry_time"] = table_smry_time
    latency_dict["text_creation_time"] = text_creation_time
    latency_dict["text_smry_time"] = text_smry_time
    latency_dict["image_smry_time"] = image_smry_time
    latency_dict["md_text_extrac_time"] = text_extrac_time

    return all_splits_pypdf_texts, text_summaries, texts, table_summaries, tables, image_summaries, img_base64_list, latency_dict

def create_multi_vector_retriever(
    vectorstore, text_summaries, texts, table_summaries, tables, image_summaries, images
):
    # Initialize the storage layer
    store = InMemoryStore()
    id_key = "doc_id"

    # Create the multi-vector retriever
    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=store,
        id_key=id_key,
    )

    # Helper function to add documents to the vectorstore and docstore
    def add_documents(retriever, doc_summaries, doc_contents):
        doc_ids = [str(uuid.uuid4()) for _ in doc_contents]
        summary_docs = [
            Document(page_content=s, metadata={id_key: doc_ids[i]})
            for i, s in enumerate(doc_summaries)
        ]
        retriever.vectorstore.add_documents(summary_docs)
        retriever.docstore.mset(list(zip(doc_ids, doc_contents)))

    # Add texts, tables, and images
    # Check that text_summaries is not empty before adding
    if text_summaries:
        print("Adding texts")
        add_documents(retriever, text_summaries, texts)
    # Check that table_summaries is not empty before adding
    if table_summaries:
        print("Adding tables")
        add_documents(retriever, table_summaries, tables)
    # Check that image_summaries is not empty before adding
    if image_summaries:
        print("Adding images")
        add_documents(retriever, image_summaries, images)

    return retriever

def index_document_to_chroma(file_path: str, file_id: int) -> bool:
    # try:
    #     splits = load_and_split_document(file_path)
        
    #     # Add metadata to each split
    #     for split in splits:
    #         split.metadata['file_id'] = file_id
        
    #     vectorstore.add_documents(splits)
    #     # vectorstore.persist()
    #     return True
    # except Exception as e:
    #     print(f"Error indexing document: {e}")
    #     return False

    try:
        all_splits_pypdf_texts, text_summaries, texts, table_summaries, tables, image_summaries, img_base64_list, latency_dict = load_and_split_document(file_path)

        Text_Table_Image_TexEembd_MMdl_strat_time = time.time()
        retriever_multi_vector_img = create_multi_vector_retriever(
            multi_vector_img,
            text_summaries,
            texts,
            table_summaries,
            tables,
            image_summaries,
            img_base64_list,
        )
        Text_Table_Image_TexEembd_MMdl_creation_time = time.time() - Text_Table_Image_TexEembd_MMdl_strat_time

        # Create retriever
        Text_Table_Image_Summary_LLM_strat_time = time.time()
        retriever_multi_vector_img_summary = create_multi_vector_retriever(
            multi_vector_text,
            text_summaries,
            texts,
            table_summaries,
            tables,
            image_summaries,
            image_summaries,
        )
        Text_Table_Image_Summary_LLM_creation_time = time.time() - Text_Table_Image_Summary_LLM_strat_time

        fldr_nm = "_".join(Path(file_path).name.replace("temp_","").split('.')[:-1])
        fp_path = f"./src/prcsd_docs/docling/{fldr_nm}/images/"

        Text_Table_Image_MmdlEmbd_MMdl_strat_time = time.time()
        # Get image URIs
        image_uris = sorted(
            [
                os.path.join(fp_path, image_name)
                for image_name in os.listdir(fp_path)
                # if image_name.endswith(".jpg")
            ]
        )
        
        # Add images and documents
        if image_uris:
            multimodal_embd.add_images(uris=image_uris)
        if texts:
            multimodal_embd.add_texts(texts=texts)
        if tables:
            multimodal_embd.add_texts(texts=tables)
        Text_Table_Image_MmdlEmbd_MMdl_creation_time = time.time() - Text_Table_Image_MmdlEmbd_MMdl_strat_time

        # Make retriever
        # retriever_multimodal_embd = multimodal_embd.as_retriever()
        # Add metadata to each split
        # for split in splits:
        #     split.metadata['file_id'] = file_id
        
        # vectorstore.add_documents(splits)
        # vectorstore.persist()

        # multi_vector_img.persist()
        # multi_vector_text.persist()
        # multimodal_embd.persist()

        Text_Only_Data_LLM_strat_time = time.time()
        baseline_retriver.add_texts(all_splits_pypdf_texts)
        Text_Only_Data_LLM_creation_time = time.time() - Text_Only_Data_LLM_strat_time

        latency_dict['Text_Table_Image_TexEembd_MMdl_creation_time'] = Text_Table_Image_TexEembd_MMdl_creation_time
        latency_dict['Text_Table_Image_Summary_LLM_creation_time'] = Text_Table_Image_Summary_LLM_creation_time
        latency_dict['Text_Table_Image_MmdlEmbd_MMdl_creation_time'] = Text_Table_Image_MmdlEmbd_MMdl_creation_time
        latency_dict['Text_Only_Data_LLM_creation_time'] = Text_Only_Data_LLM_creation_time

        insert_latency_metrics(file_id, latency_dict)

        return True
    
    except Exception as e:
        print(f"Error indexing document: {e}")
        return False



def delete_doc_from_chroma(file_id: int):
    try:
        docs = vectorstore.get(where={"file_id": file_id})
        print(f"Found {len(docs['ids'])} document chunks for file_id {file_id}")
        
        vectorstore._collection.delete(where={"file_id": file_id})
        print(f"Deleted all documents with file_id {file_id}")
        
        return True
    except Exception as e:
        print(f"Error deleting document with file_id {file_id} from Chroma: {str(e)}")
        return False
