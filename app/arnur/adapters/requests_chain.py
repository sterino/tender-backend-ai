import os

import openai
import pinecone
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Pinecone


class ArnurService:
    def __init__(self, api_key, pinecone_key, pinecone_env):
        self.api_key = api_key
        openai.api_key = api_key
        self.pinecone_key = pinecone_key
        self.pinecone_env = pinecone_env

    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_API_ENV = os.getenv("PINECONE_API_ENV")

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # Initialize Pinecone
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)

    # Define the index name
    index_name = "abay"

    # Connect to the existing Pinecone index
    docsearch = Pinecone.from_existing_index(
        index_name=index_name, embedding=embeddings
    )

    # Now you can use docsearch to perform similarity searches
    llm = OpenAI(temperature=0.0, openai_api_key=OPENAI_API_KEY)
    chain = load_qa_chain(llm, chain_type="stuff")

    def get_response_chat(self, input: str):
        docs = ArnurService.docsearch.similarity_search(input, 1)
        answer = ArnurService.chain.run(input_documents=docs, question=input)
        print(answer)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {
                    "role": "user",
                    "content": """Ты виртуальный помощник по вопросам государственных грантов,
                    используй эту информацию для ответа на вопрос пользователя:"""
                    + answer
                    + ", но не добавляй ничего лишнего и отвечай как есть.",
                }
            ],
            temperature=0.0,
        )
        return completion.choices[0].message
