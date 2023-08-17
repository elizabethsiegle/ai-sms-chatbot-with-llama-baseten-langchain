from flask import Flask, request
from langchain import LLMChain, PromptTemplate
from langchain.llms import Baseten
from langchain.memory import ConversationBufferWindowMemory
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import dotenv_values

config = dotenv_values(".env")

template = """Assistant is a large language model designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
Assistant is constantly learning and improving, and its capabilities are constantly evolving. 

Assistant should act as Taylor Swift referencing her songs and lyrics as much as possible when giving advice and answering questions. You will reply with what she would say.
SMS: {sms_input}
Assistant:"""

prompt = PromptTemplate(input_variables=["sms_input"], template=template)

chatgpt_chain = LLMChain(
    llm=Baseten(model=config.get("BASETEN_MODEL_ID")), 
    prompt=prompt,
    memory=ConversationBufferWindowMemory(k=2),
    llm_kwargs={"max_length": 4096}
)

app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def sms():
    resp = MessagingResponse()
    inb_msg = request.form['Body'].lower().strip()
    output = chatgpt_chain.predict(sms_input=inb_msg)
    print(output)
    resp.message(output)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
    