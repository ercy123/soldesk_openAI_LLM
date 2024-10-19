import os
import time
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import openai
import tool
from werkzeug.utils import secure_filename

app = Flask(__name__)  # __name__ == '__main__'
CORS(app)

# app.config['UPLOAD_FOLDER']='C:/ai/deploy/whisper/storage'

# 업로드할 파일의 최대 크기 설정 (16MB로 설정 예시)
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Flask 환경 변수 설정, 허용 가능한 파일 확장자 설정 (예: 이미지 파일만 허용하도록 설정)

<<<<<<< HEAD
app.config['ALLOWED_EXTENSIONS'] = {'jpg','png','gif'}

# '.'을 기준으로 확장자를 분리하여 소문자로 변경후 업로드 가능한 파일형식인지 체크
# rsplit 으로 맨 오른쪽의 '.' 을 기준으로 2개로 나누어 리스트로 반환. 그리고 [1] 을 사용하여 두번째 인자를 사용
def allowed_file(filename):     # ccc.bbb.aaa.jpg => [ccc.bbb.aaa, jpg]
=======

# '.'을 기준으로 확장자를 분리하여 소문자로 변경후 업로드 가능한 파일형식인지 체크
def allowed_file(filename):
>>>>>>> ed7d2a002230aa834c637958e4abb5ddc8a11c16
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# 25 M 제한
def allowed_size(size):
    return True if size <= 1024 * 1024 * 25 else False

<<<<<<< HEAD
# 기본페이지 http://127.0.0.1:5000
@app.get("/") #http://localhost:5000/
def index():
    return "파일 업로드 서비스"

# 파일 전송 폼
@app.get("/fileupload") # http://localhost:5000/fileupload
def fileupload_form():
    return render_template("fileupload.html")

# # 파일 전송 처리
@app.post("/fileupload") # http://localhost:5000/fileupload
def fileupload_proc():
    time.sleep(3) #3초 중지
    f = request.files['file']
    file_size = len(f.read()) # len 으로 파일의 사이즈 확인 가능
    f.seek(0) # file 포인터가 read를 통해 맨 밑으로 내려갔는데, 다시 맨 위로 올림 (처음으로 이동)
    
    if allowed_size(file_size) == False:
        resp = jsonify({'message': "파일 사이즈가 25M를 넘습니다." + str(file_size/1024/1024) + ' M'})  # dict -> json string
        resp.status_code = 500 # 서버 에러
    
    # 허용 가능한 파일 확장자인지 확인
    if f and allowed_file(f.filename): # if f = 파일이 존재하는지 확인하는 구문
        # 저장할 경로 지정 (예: 'storage' 폴더에 저장)
        upload_folder = 'storage'
        if not os.path.exists(upload_folder): # storage 라는 디렉토리가 없을 시 생성해줌
            os.makedirs(upload_folder)
        f.save(os.path.join(upload_folder,f.filename)) # 파일저장

        resp = jsonify({'message': '파일을 저장했습니다.'}) # dict -> json string

    else:
        resp = jsonify({'message': '전송 할 수 없는 파일 형식입니다.'})  # dict -> json string
        # resp.status_code = 500 # 서버 에러
        
    return resp
=======
# 파일 전송 폼
# @app.get("/fileupload") # http://localhost:5000/fileupload

# # 파일 전송 처리
# @app.post("/fileupload") # http://localhost:5000/fileupload
   
#     if allowed_size(file_size) == False:
#         resp = jsonify({'message': "파일 사이즈가 25M를 넘습니다." + str(file_size/1024/1024) + ' M'})  # dict -> json string
#         resp.status_code = 500 # 서버 에러
    
#     # 허용 가능한 파일 확장자인지 확인
#     if f and allowed_file(f.filename):
#         # 저장할 경로 지정 (예: 'storage' 폴더에 저장)


#         resp = jsonify({'message': '파일을 저장했습니다.'}) # dict -> json string

#     else:
#         resp = jsonify({'message': '전송 할 수 없는 파일 형식입니다.'})  # dict -> json string
#         # resp.status_code = 500 # 서버 에러
        
#     return resp
>>>>>>> ed7d2a002230aa834c637958e4abb5ddc8a11c16

    
app.run(host="0.0.0.0", port=5000, debug=True)  # 0.0.0.0: 모든 Host 에서 접속 가능, python recommend_movie.py

'''
activate ai
python fileupload.py
http://localhost:5000/fileupload
'''

