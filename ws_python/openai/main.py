from flask import Flask, request, render_template
from flask_cors import CORS

import tool # tool.py

app = Flask(__name__) # __name__ == '__main__'
CORS(app)

@app.get('/') # GET, http://localhost:5000
def index():
  return 'OpenAI 웹서비스 접속'


# GET, http://localhost:5000/translator
@app.get('/translator')
def translator():
  return "번역 서비스 접속"

app.run(host="0.0.0.0", port=5000, debug=True) # 0.0.0.0: 어디서나 접속, debug=True: 소스 변경시 자동 재시작

'''
activate ai
python main.py
'''