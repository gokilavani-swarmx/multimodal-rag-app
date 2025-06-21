from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic_models import QueryInput, QueryResponse, DocumentInfo, DeleteFileRequest
from langchain_utils import get_rag_chain, summarize_result
from db_utils import insert_application_logs, get_chat_history, get_all_documents, insert_document_record, delete_document_record, insert_vec_db_creation_time
from chroma_utils import index_document_to_chroma, delete_doc_from_chroma, cache_update, cache_retrival
from responsible_ai import prmpt_injctn_classifier, responsible_ai_validation
from crewAI_utils import crew_kickoff
import os, time
import uuid
import logging
import uvicorn, json
logging.basicConfig(filename='app.log', level=logging.INFO)
app = FastAPI()

@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    print(query_input)
    session_id = query_input.session_id
    logging.info(f"Session ID: {session_id}, User Query: {query_input.question}, Model: {query_input.model.value}")
    if not session_id:
        session_id = str(uuid.uuid4())

    rspn_ai_lbl_clsfr = responsible_ai_validation(query_input.question)
    prmpt_injc_lbl = prmpt_injctn_classifier(query_input.question)[0]['label']

    if rspn_ai_lbl_clsfr.lower() != 'safe' or prmpt_injc_lbl.lower() != 'safe':  # If the user input is offensive, return an error
        answer = f"Either prompt injection or {rspn_ai_lbl_clsfr} detected, Please rephrase your query."
        return QueryResponse(answer={"invalid prompt": answer}, session_id=session_id, model=query_input.model)
    
    cache_retrival_rslt = cache_retrival(query_input.question)
    if cache_retrival_rslt:
        return QueryResponse(answer={"AI Message": cache_retrival_rslt}, session_id=session_id, model=query_input.model)

    chat_history = get_chat_history(session_id)
    chain_baseline, chain_mv_text, chain_multimodal_mv_img, chain_multimodal_embd = get_rag_chain(query_input.model.value)
    # rtrvr_rslt = as_retriever.invoke(query_input.question)
    # rtvr_rslt_len = len(rtrvr_rslt)
    # print(f"Retriever result length: {rtvr_rslt_len}")
    # answer = rag_chain.invoke({
    #     "input": query_input.question,
    #     "chat_history": chat_history
    # })['answer']

    answer = dict()
    for var_name, rag_chain in zip(['Text_Only_Data_LLM', 'Text_Table_Image_Summary_LLM', 'Text_Table_Image_TexEembd_MMdl', 'Text_Table_Image_MmdlEmbd_MMdl']
    # for var_name, rag_chain in zip(['chain_baseline', 'chain_mv_text', 'chain_multimodal_mv_img', 'chain_multimodal_embd']
                                    , [chain_baseline, chain_mv_text, chain_multimodal_mv_img, chain_multimodal_embd]):
        answer_mthd = rag_chain.invoke(query_input.question)
        answer[var_name] = answer_mthd

    answer_dct = answer.copy()
    # ensemble_answer = summarize_result(answer)
    ensemble_answer = crew_kickoff(query_input.question, answer)

    answer = dict()
    answer['AI Message'] = ensemble_answer
    cache_update(query_input.question, ensemble_answer)
    dict_string = json.dumps(answer)

    insert_application_logs(session_id, query_input.question, dict_string, query_input.model.value)
    logging.info(f"Session ID: {session_id}, AI Response: {answer}")
    return QueryResponse(answer=answer, session_id=session_id, model=query_input.model)

from fastapi import UploadFile, File, HTTPException
import os
import shutil

@app.post("/upload-doc")
def upload_and_index_document(file: UploadFile = File(...)):
    allowed_extensions = ['.pdf', '.docx', '.html']
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed types are: {', '.join(allowed_extensions)}")
    
    temp_file_path = f"temp_{file.filename}"
    
    try:
        # Save the uploaded file to a temporary file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_id = insert_document_record(file.filename)
        if type(file_id) is not tuple:
            index_start_time = time.time()
            success = index_document_to_chroma(temp_file_path, file_id)
            index_end_time = time.time() - index_start_time
            insert_vec_db_creation_time(file_id, index_end_time)

        elif type(file_id) is tuple:
            return {"message": f"File {file.filename} has been uploaded already and indexed.", "file_id": file_id}
        
        if success:
            return {"message": f"File {file.filename} has been successfully uploaded and indexed in {round(index_end_time,2)} seconds or {round(index_end_time/60,2)} minutes", "file_id": file_id}
        else:
            delete_document_record(file_id)
            raise HTTPException(status_code=500, detail=f"Failed to index {file.filename}.")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/list-docs", response_model=list[DocumentInfo])
def list_documents():
    return get_all_documents()

@app.post("/delete-doc")
def delete_document(request: DeleteFileRequest):
    # Delete from Chroma
    chroma_delete_success = delete_doc_from_chroma(request.file_id)

    if chroma_delete_success:
        # If successfully deleted from Chroma, delete from our database
        db_delete_success = delete_document_record(request.file_id)
        if db_delete_success:
            return {"message": f"Successfully deleted document with file_id {request.file_id} from the system."}
        else:
            return {"error": f"Deleted from Chroma but failed to delete document with file_id {request.file_id} from the database."}
    else:
        return {"error": f"Failed to delete document with file_id {request.file_id} from Chroma."}

if __name__ == "__main__": 
    uvicorn.run(app, host="127.0.0.1", port=8000) # reload=True, workers=1