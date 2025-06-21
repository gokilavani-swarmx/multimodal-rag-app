from crewai import Agent, Task,Crew
from pydantic import BaseModel

class Blog(BaseModel):
    final_answer: str
from crewai import LLM

# Basic configuration
defined_llm = LLM(
    model="ollama/llama3.2:1b",
    base_url="http://localhost:11434"
)

# answer_identifier = Agent(
#     role='Answer Identifier',
#     goal='Identify the answer that appears in multiple inputs for a given question {question}. Inputs - {inputs}',
#     backstory='You are an expert in identifying consistent answers across multiple inputs',
#     llm = defined_llm,
#     verbose=True,
#     allow_delegation=False,
# )

# test_task = Task(
#     description="Review the inputs and identify the common answer across them",
#     agent=answer_identifier,
#     expected_output='Identify the answer that is common across all input. Return the summarized answer. DO not add any other things. Strictly Give only the answer',
#     # expected_output="Identify the answer that appears in more than one input. Return the result as a JSON object with field 'final_answer'",
#     # expected_output="Identify the answer that appears in more than one input and return a JSON object with 'inputs' fields.",
#     # output_json = Blog,
#     llm = defined_llm
# )


answer_identifier = Agent(
    role='Answer Summarizer',
    goal='Summarize the answer across multiple inputs for the given question: {question}. Inputs - {inputs}',
    backstory='You are an expert in summarizing answers from multiple sources, Strictly summarize the answer. Do not provide all the inputs.',
    llm=defined_llm,
    verbose=True,
    allow_delegation=False,
)


test_task = Task(
    description='''summarize the text concisely while retaining all critical information.
    Strictly Return only the summary. Do not add anything on your own.''',
    agent=answer_identifier,
    expected_output='summarized answer',
    llm=defined_llm
)

crew = Crew(
    agents=[answer_identifier],
    tasks=[test_task]
)

def crew_kickoff(question, answer_comb):
    output_accmltd = ''
    for idx, dct_itms in enumerate(answer_comb.items()):
        key, val = dct_itms
        # print(key)
        # if key != 'output':
        #     continue
        output_accmltd += F'OUTPUT{idx} : {val['output']}' + "\n\n"
    rslt = crew.kickoff(inputs={"inputs": output_accmltd, 'question': question})
    return rslt.raw