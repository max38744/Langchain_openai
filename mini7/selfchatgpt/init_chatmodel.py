from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, SystemMessage, Document
import pandas as pd
import openai

# 데이터 로드 (필요시)
# data = pd.read_csv("./news_chris.csv")
# text_list = data['QA'].tolist()
# documents = [Document(page_content=text) for text in text_list]

# 전역 변수로 Embeddings와 Database 초기화
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
database = Chroma(persist_directory="./database", embedding_function=embeddings)
# database.add_documents(documents)

# Chat 모델과 Retriever 초기화
chat = ChatOpenAI(model="gpt-3.5-turbo")
retriever = database.as_retriever(search_kwargs={"k": 3})

# ConversationBufferMemory 초기화
memory = ConversationBufferMemory(memory_key="chat_history", input_key="question", output_key="answer", return_messages=True)

# ConversationalRetrievalQA 체인 초기화
qa = ConversationalRetrievalChain.from_llm(llm=chat, retriever=retriever, memory=memory, return_source_documents=True, output_key="answer")


def summary(chat_history):
    talk = ""
    for qa in chat_history:
        talk += '질문 : ' + qa['question'] + '\n'
        talk += '대답 : ' + qa['response'] + '\n'
        
    # # API를 사용하여 'gpt-3.5-turbo' 모델로부터 응답을 생성합니다.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "다음의 대화의 가장 중요한 키워드를 3개 이하로 알려줘"},  # 기본 역할 부여
            {"role": "user", "content": talk},
        ]
    )

    return response.choices[0].message.content