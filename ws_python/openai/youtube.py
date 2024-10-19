import os
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import tool
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain_community.llms import OpenAI  # langchain openai wrapper

app = Flask(__name__)  # __name__ == '__main__'
CORS(app)

@app.get("/youtube") # http://localhost:5000/youtube
def youtube_form():
    return render_template("youtube.html")

@app.post("/youtube") # http://localhost:5000/youtube
def youtube_proc():
    data = request.json # json 형식으로 데이터 읽기
    url = data["url"]
    print('-' * 80)
    print(f'{url} 처리 시작')

    print('-> url:', url)
    # return;

    # YoutubeLoader chain 생성 및 실행
    # YoutubeLoader를 사용하여 YouTube 영상의 대본 불러오고 구문 분석하기, 자막 파일을 업로드 한 경우만 가능
    # 한글일 경우 language='ko' 옵션 사용할것. 
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True, language='en')
    script = loader.load()
    print(f'-> script: {script}')

    llm = OpenAI(model_name="text-ada-001", n=1, best_of=1) # 모델 변경이 안됨
    print(f'-> llm.get_num_tokens(script[0].page_content): {llm.get_num_tokens(script[0].page_content)}') # 스크립트 크기 출력
    
    # 요약 chain 생성 및 실행, gpt-4-1106-preview
    chain = load_summarize_chain(ChatOpenAI(model='gpt-4o', temperature=0), chain_type='stuff', verbose=False)
    result = chain.run(script)
    
    # return result

    # 번역
    prompt = f"{result}\n\nTranslate this sentence into Korean"
    
    format = '''
    {
      "res": "번역된 문장"
    }
    '''
  
    response = tool.answer("you are a translater.", prompt, format)
    result_kor = response
    
    obj = {
        "result": result,
        "result_kor": result_kor
    }
    
    print('-> jsonify(obj)\n', obj)
    return jsonify(obj) # json -> json + http 응답 객체

app.run(host="0.0.0.0", port=5000, debug=True)  # 0.0.0.0: 모든 Host 에서 접속 가능, python recommend_movie.py

'''
activate ai
python youtube.py
http://localhost:5000/youtube
'''
