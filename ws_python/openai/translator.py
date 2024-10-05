from flask import Flask, request, render_template
from flask_cors import CORS
import tool
import time
 
app = Flask(__name__) # __name__ == '__main__'
CORS(app)
@app.get('/') # GET, http://localhost:5000
def index():
  return 'OpenAI 웹서비스 접속'

@app.get('/translator') # GET, http://localhost:5000/translator
def translator_form(): 
  return render_template('translator.html')

@app.post('/translator') # POST, http://localhost:5000/translator
def translator_proc():
  # time.sleep(5) # 3 second 대기
  
  # print("POST 요청 발생함.")
  data = request.json
  sentence = data['sentence']
  language = data['language']
  age = data['age']
  
  sentence = tool.remove_empty_lines(sentence) # 빈 라인 삭제
  # print(sentence)
  prompt = f'아래 문장을 {age}살 수준의 {language}로 번역해줘.\n\n{sentence}'
  print('-> prompt: ' + prompt)
  
  format = '''
    {
      "res": "번역된 문장"
    }
  '''
   
  response = tool.answer('너는 번역기야', prompt, format) # gpt-3.5-turbo
  # response = tool.answer('너는 번역기야', prompt, format, llm='gpt-4-turbo')
  # response = tool.answer('너는 번역기야', prompt, format, llm='gpt-4o')
  print(response)  # {'res': 'Hello.'}
  
  # return '{"res": "POST 요청 처리함"}'
  return response

app.run(host="0.0.0.0", port=5000, debug=True) # 0.0.0.0: 어디서나 접속, debug=True: 소스 변경시 자동 재시작

'''
activate ai
python translator.py
'''