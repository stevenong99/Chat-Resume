import json

from langchain.chains.summarize import load_summarize_chain
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.llms import OpenAI
from langchain.prompts import load_prompt

from configs import RESOURCES

# Initializing GPT3.5-turbo
# Setting the maximum length of the output to 1000 tokens
max_output_length = 256
llm = OpenAI(model="text-davinci-003", temperature=0.9, max_tokens=max_output_length)

# Loading the prompt template
prompt = load_prompt(RESOURCES / "prompt.yaml")

# Loading the documents
file_path = RESOURCES / "cv.md"
loader = UnstructuredMarkdownLoader(file_path)
pages = loader.load_and_split()
# print(type(pages))
# print(pages)

# Summarizing the documents
# chain = load_summarize_chain(llm, chain_type="map_reduce")
# summary = chain.run(pages)
# print(type(pages))
# print(pages)

# Main function
def get_answer(question):
    # Creating the doc qa chain that will process the prompt together with all the context
    stuff_chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt, verbose=True)

    # Passing the pdf and question into the chain. Then it should output the answer
    stuff_answer = stuff_chain({"input_documents": pages[:], "question":question}, return_only_outputs=True)
    answer_dict = json.loads(stuff_answer["output_text"])
    answer = answer_dict["answer"]

    return answer