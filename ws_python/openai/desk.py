# desk.py
import json
import random
import time

from flask import Flask, request, render_template
from flask_cors import CORS

import tool


app = Flask(__name__)  # __name__ == '__main__'
CORS(app)
# GET, http://localhost:5000  =>OpenAI 웹서비스 접속

@app.get('/')
def index():
  return "openAI 웹사이트 접속"

# http://localhost:5000/desk
@app.get('/desk')
def desk_form():
  imgs = [i for i in range(1,51)]
  # filenames =random.choices(imgs,k=50) # 중복 -> 복원 추출
  filenames = random.sample(imgs,k=50)
  
  return render_template("desk.html",filenames=filenames)

# 
# http://localhost:5000/desk
@app.post('/desk')
def desk_proc():
    
    # 3 second
    time.sleep(3)
    data = request.json
    desk = data['desk']
    desk = desk.split(",")
    print("-> desk :",desk)
    # 배열의 요소를 정수로 변경하여 list로 변경
    desk = list(map(int,desk))     # map: 배열의 요소에 함수를 적용하는 기능을 함.
    print("-> desk :",desk) 
    
    items =[]
    for index in range(len(desk)) : #range(8) => 0~7
      item = f'{desk[index]}.jpg'
      items.append(item)

    items_join = ",".join(items)
    print("->items_join",items_join) 
    
    prompt='''
    사용자를 3가지 그룹으로 분류하는 중이야, 가장 선호도가 높은 그룹 3가지를 추천하고 아래의 기준을 적용하여 분류해줘.

    [분류 기준]
    brown: 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg
    cozy: 6.jpg, 7.jpg, 8.jpg, 9.jpg, 10.jpg
    ivory: 11.jpg, 12.jpg, 13.jpg, 14.jpg, 15.jpg
    kitsch: 16.jpg, 17.jpg, 18.jpg, 19.jpg, 20.jpg
    modern: 21.jpg, 22.jpg, 23.jpg, 24.jpg, 25.jpg
    nature: 26.jpg, 27.jpg, 28.jpg, 29.jpg, 30.jpg
    pink: 31.jpg, 32.jpg, 33.jpg, 34.jpg, 35.jpg
    study: 36.jpg, 37.jpg, 38.jpg, 39.jpg, 40.jpg
    work: 41.jpg, 42.jpg, 43.jpg, 44.jpg, 45.jpg
    y2k: 46.jpg, 47.jpg, 48.jpg, 49.jpg, 50.jpg

    [사용자가 선택한 이미지]
    ''' + items_join

   
    format = '{ "res": "최우선 추천/중간 추천/마지막 추천"}'

    response = tool.answer(role='너는 방을 꾸며주는 회사 직원이야', prompt=prompt, output='json', format=format) 
    print(response) # {'res': 'cozy/nature/work'}
    
    labels = ['ivory', 'brown', 'pink', 'study', 'nature', 'modern', 'kitsch', 'y2k', 'cozy', 'work']
    
    recommends = response['res'].split('/')
    print(recommends) # ['cozy', 'nature', 'work']
    
    for seq, recom in enumerate(recommends):
      for i, item in enumerate(labels):
        if recom.strip() == item:
          print(f'추천 우선 순위: {seq+1}, 추천 카테고리: {i+1}, 추천 레이블: {item}')
    
          # 추천 우선 순위: 1, 추천 카테고리: 6, 추천 레이블: modern
          # 추천 우선 순위: 2, 추천 카테고리: 5, 추천 레이블: nature
          # 추천 우선 순위: 3, 추천 카테고리: 10, 추천 레이블: work
          
          # SQL
          
    
    return response  # json 객체 전달

app.run(host="0.0.0.0", port=5000, debug=True)  # 0.0.0.0: 모든 Host 에서 접속 가능, debug=True: 소스 변경시 자동 restart

'''
activate ai
python desk.py
'''

