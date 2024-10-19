import json
import os
import requests
from datetime import datetime
import random

import tool

from openai import OpenAI

with open("./GPT_KEY.txt","r") as f:
  api_key = f.read().strip()






client = OpenAI(
  api_key=api_key
)

from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)  # __name__ == '__main__'
CORS(app)

@app.get('/')
def index():
  return "이미지 생성 서비스"

# http://localhost:5000/member_img
@app.get('/member_img')
def member_img_form():  # /templates/member_img.html
  return render_template("member_img.html")

# http://localhost:5000/member_img
@app.post('/member_img')
def member_img_proc():
 
    data = request.json
    prompt = data['prompt']
    print('-> prompt :', prompt)
    
    response = client.images.generate(
      model='dall-e-3',
      prompt=prompt,
      size='1024x1024',
      quality="standard",
      n=1
    )
    
    image_url = response.data[0].url
    print(image_url)

    # URL에서 이미지를 가져옴
    response = requests.get(image_url)

    # 현재 시간을 가져옴
    now = datetime.now()

    # '년월일시분초' 형식의 문자열 생성
    date_time_string = now.strftime("%Y%m%d%H%M%S")

    # 1부터 1000까지의 난수 생성
    random_number = random.randint(1, 1000)

    if os.path.exists('./static/member_img') == False:
        os.mkdir('./static/member_img')

    # 파일명 생성 (년월일시분초_난수.txt 형식)
    file_name = f"./static/member_img/{date_time_string}_{random_number}.jpg"
    print(f'-> file_name: {file_name}')
    
    # 응답이 성공적인지 확인
    if response.status_code == 200:
        # 이미지 데이터를 파일로 저장
        with open(file_name, "wb") as file:
            file.write(response.content)
        print("이미지가 성공적으로 저장되었습니다.")
    else:
        print("이미지를 가져오는데 문제가 발생했습니다.")

    file_name = {"file_name": file_name}

    # return json.loads(file_name) # str -> json(dict)
    # json(dict) -> str
    return json.dumps(file_name)

app.run(host="0.0.0.0", port=5000, debug=True)  # 0.0.0.0: 모든 Host 에서 접속 가능, debug=True: 소스 변경시 자동 restart

'''
activate ai
python member_img.py
http://localhost:5000/member_img
'''