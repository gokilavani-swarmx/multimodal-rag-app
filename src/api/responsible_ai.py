from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer, pipeline
from langchain_ollama import ChatOllama, OllamaLLM

# Using https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2
model_path = "protectai/deberta-v3-base-prompt-injection-v2"
revision = None  # We recommend specifiying the revision to avoid breaking changes or supply chain attacks
tokenizer = AutoTokenizer.from_pretrained(
    model_path, revision=revision, model_input_names=["input_ids", "attention_mask"], device="cpu"
)
model = ORTModelForSequenceClassification.from_pretrained(
    model_path, revision=revision, subfolder="onnx", provider="CPUExecutionProvider"
)

prmpt_injctn_classifier = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer,
    truncation=True,
    max_length=512,
    device='cpu'
)

llm_llama_gaurd3 = ChatOllama(
    model="llama-guard3:1b",
    temperature=0,
    # other params...
)

def responsible_ai_validation(question):
    llama_gaurd_labels = '''S1: Violent Crimes
    S3: Sex-Related Crimes
    S5: Defamation
    S7: Privacy
    S9: Indiscriminate Weapons
    S11: Suicide & Self-Harm
    S13: Elections
    S2: Non-Violent Crimes
    S4: Child Sexual Exploitation
    S6: Specialized Advice
    S8: Intellectual Property
    S10: Hate
    S12: Sexual Content
    S14: Code Interpreter Abuse'''.splitlines()
    llama_gaurd_label_dict = dict([vl.strip().split(": ") for vl in llama_gaurd_labels])
    grd_rslt = llm_llama_gaurd3.invoke(question).content.splitlines()
    if len(grd_rslt) > 1:
        llama_gaurd_rslt = llama_gaurd_label_dict[grd_rslt[-1]]
        return llama_gaurd_rslt
    else:
        return "safe"