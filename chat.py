import time
from langchain.llms.llamacpp import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory


callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = LlamaCpp(
    model_path="/home/elliot/Python/dolphin-2.1-mistral-7b.Q5_K_S.gguf",
    max_tokens=1024,
    n_batch=512,
    n_ctx=5000,
    top_k=40,
    top_p=1,
    verbose=True,
    temperature=0.95,
    n_gpu_layers=1,
    callback_manager=callback_manager,
)

template = """
<|im_start|>system
You are a chatbot having a conversation with a human.

{chat_history}
<|im_end|>
<|im_start|>user
{question}<|im_end|>
<|im_start|>assistant
"""

prompt = PromptTemplate(input_variables=["chat_history", "question"], template=template)

memory = ConversationBufferMemory(memory_key="chat_history")

llm_chain = LLMChain(
    llm=llm, 
    prompt=prompt, 
    verbose=True,
    memory=memory, 
    )

while True:
    user_question = input("Me: ") 

    if user_question.strip() == "quit" or user_question.strip() == "exit" or user_question.strip() == "bye":
        print("Exiting program...")
        time.sleep(2)
        break


    # formatted_prompt = prompt.format(question=user_question)

    llm_chain.run(question=user_question)

