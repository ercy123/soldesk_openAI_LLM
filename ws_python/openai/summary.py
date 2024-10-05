from flask import Flask, request, render_template
from flask_cors import CORS
import tool

app = Flask(__name__) # __name__ == '__main__'
CORS(app)

@app.get('/summary') # GET, http://localhost:5000/summary
def summary_form():
  return render_template("summary.html")

@app.post('/summary') # POST, http://localhost:5000/summary
def summary_proc():
  # print("POST 요청 발생함.")
  data = request.json
  article = data['article']
  
  # 빈 라인 삭제
  # print(article)
 
  print('-> prompt: ' + prompt)
  
  format = '''
    {
      "res": "요약된 문장"
    }
  '''
  
  # response = tool.answer('너는 요약 시스템이야', prompt, format)
  # response = tool.answer('너는 요약 시스템이야', prompt, format, 'gpt-4-turbo')
  response = tool.answer('너는 요약 시스템이야', prompt, format, 'gpt-4o') # 가장 우수한 성능
  print(response)  # {'res': 'Hello.'}
  
  return response

app.run(host="0.0.0.0", port=5000, debug=True) # 0.0.0.0: 어디서나 접속, debug=True: 소스 변경시 자동 재시작

'''
cd openai
activate ai
python summary.py
'''
