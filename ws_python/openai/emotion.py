from flask import Flask, request, render_template
from flask_cors import CORS
import tool

app = Flask(__name__) # __name__ == '__main__'
CORS(app)

@app.get('/')
def index():
  return "기사의 호재,악재 구별서비스"

@app.get('/emotion') # GET, http://localhost:5000/emotion
def emotion_form():
  return render_template("emotion.html")

@app.post('/emotion') # POST, http://localhost:5000/emotion
def emotion_proc():
  # print("POST 요청 발생함.")
  data = request.json
  article = data['article']
#  print(article)
  article = tool.remove_empty_lines(article)
  
  prompt = f"아래 뉴스가 호재인지 악재인지 알려줘, '호재'면 1, '악재'면 0을 출력해줘 \n\n {article}"
  format = ''' 
    {
      "res" = "1" 또는 "0"
    }
  '''
  
  response = tool.answer("너는 증권 투자 권유 대행인 및 투자 컨설턴트야.", prompt, format)
  print(response)
  return response

app.run(host="0.0.0.0", port=5000, debug=True) # 0.0.0.0: 어디서나 접속, debug=True: 소스 변경시 자동 재시작

'''
activate ai
python emotion.py
'''