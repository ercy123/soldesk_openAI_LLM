from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings  # 새 경로로 수정
from langchain_openai import OpenAI  # 새 경로로 수정
from langchain_community.vectorstores import FAISS
from langchain.indexes import VectorstoreIndexCreator

# API 키 설정
with open("./GPT_Key.txt", "r") as f:
    api_key = f.read().strip()

# LLM과 임베딩을 설정
embeddings = OpenAIEmbeddings(openai_api_key=api_key)
llm = OpenAI(temperature=0, openai_api_key=api_key)

# PDF 로드
loader = PyPDFLoader("★ 서울특별시 스마트도시 및 정보화 기본계획(홈페이지 게시용).pdf")

# 텍스트 데이터를 로드하고 벡터 스토어를 생성
documents = loader.load()
vectorstore = FAISS.from_documents(documents, embeddings)

# 사용자 질문 받기
print("질문을 입력하세요")
user_input = input()

# 쿼리 실행
result = vectorstore.similarity_search(user_input)

# LLM으로 결과 처리
if result:
    answer = llm.invoke(result[0].page_content)
    print(answer)
else:
    print("관련된 답변을 찾지 못했습니다.")
