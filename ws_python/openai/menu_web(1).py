import os
import time
import base64
import json

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

from werkzeug.utils import secure_filename

import tool
from openai import OpenAI
with open("./GPT_Key.txt","r") as fa:
    api_key = fa.read().strip()
    
client = OpenAI(
  api_key=api_key
)

app = Flask(__name__)  # __name__ == '__main__'
CORS(app)

# app.config['UPLOAD_FOLDER']='C:/ai/deploy/whisper/storage'

# 업로드할 파일의 최대 크기 설정 (16MB로 설정 예시)
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# 허용 가능한 파일 확장자 설정 (예: 이미지 파일만 허용하도록 설정)
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'png', 'gif'}
# 파일 이름에 점(.)이 포함되어 있고,
# 점(.)을 기준으로 마지막 확장자를 분리하여 소문자로 변환한 후,
# 그 확장자가 앱 설정에 정의된 허용된 확장자 목록에 있는지 확인
def allowed_file(filename):
    return "." in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
# 25 M 제한
def allowed_size(size):
    return True if size <= 1024 * 1024 * 25 else False

# 이미지를 base64 형식으로 인코딩하는 함수
def encode_image(image_path):
    # 이미지 파일을 바이너리 모드로 열기 (바이트로 읽기)
    with open(image_path, "rb") as image_file:
        # 바이너리 이미지 데이터를 base64로 인코딩하고, 문자열로 변환하여 반환
        return base64.b64encode(image_file.read()).decode('utf-8')
  

# Ajax 기반 파일 업로드 폼    
@app.get("/menu_web") # http://localhost:5000/menu_web
def menu_web_form():
    return render_template("menu_web.html")

# Ajax 기반 파일 업로드 처리    
@app.post("/menu_web") # http://localhost:5000/menu_web
def menu_web_proc():
    time.sleep(3)
    f = request.files['file']
    file_size = len(f.read())
    f.seek(0)
    if allowed_size(file_size) == False :
        resp = jsonify({'message':"파일 사이즈가 25M를 넘습니다. 파일 용량: " + str(round(file_size/1024/1024)) + ' MB'})
        resp.status_code = 500
        return resp
    if f and allowed_file(f.filename):
        # 업로드 폴더 생성, 절대경로로 생성 (static/uploads)
        upload_folder = os.path.join(os.getcwd(),'static','uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        # 업로드 파일 저장
        f.save(os.path.join(upload_folder, f.filename))
        
        image_path = upload_folder +'/'+ f.filename
        
        # 인코딩
        base64_image = encode_image(image_path)
        response = client.chat.completions.create(
          model="gpt-4o-mini-2024-07-18",
          messages=[
              {
                  'role': 'user', # 사용자 요청
                  'content': [
                      {"type":"text",
                       "text":"메뉴 알려줘\n\n출력 형식:{\"res\"':'메뉴명}"
                      },
                      {"type":'image_url',
                       "image_url" : {"url" : f"data:image/jpeg;base64,{base64_image}"}
                      }
                  ]
              }
          ],
          max_tokens=300 # 응답 생성시 최대 300개의 단어 사용
        )
        print(response.choices[0].message.content)
        res = response.choices[0].message.content
        json_obj = json.loads(res) #json => python
        print(f"메뉴명: {json_obj['res']}")
        menu_name = json_obj['res']
        fname = f.filename
        print("fname: ",fname)
    
        resp = jsonify({"menu_name":menu_name,"fname":fname})
    else:
        resp = jsonify({"message" : '전송할 수 없는 파일 형식입니다.'})
        
    return resp
    
app.run(host="0.0.0.0", port=5000, debug=True)  # 0.0.0.0: 모든 Host 에서 접속 가능, python recommend_movie.py

'''
cd openai
python whisper_web.py
http://127.0.0.1:5000/whisper_web
'''
