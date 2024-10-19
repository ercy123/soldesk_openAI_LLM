from flask import Flask, request, render_template
from flask_cors import CORS

import tool
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import json

app = Flask(__name__)  # __name__ == '__main__'
CORS(app)
# Gmail SMTP 서버 설정
SENDER_EMAIL = "tekjin01@gmail.com"
SENDER_PASSWORD = 'pgci upzh qfne eodb'  # Gmail 앱 비밀번호 또는 2단계 인증 시 생성한 비밀번호 사용

# 텍스트가 한글인지 확인하는 함수
def is_korean(text):
    return bool(re.search("[가-힣]", text))

# 이메일 전송 함수
def send_email(subject, recipient_email, message):
    # MIMEMultipart 객체 생성
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # # 이메일 본문을 번역된 텍스트로 추가
    msg.attach(MIMEText(message, "html"))

    # SMTP 서버에 연결하여 이메일 전송
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()  # TLS 사용
        server.login(SENDER_EMAIL, SENDER_PASSWORD)  # 로그인
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())  # 이메일 전송
        print("Email sent successfully with translated content!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
    finally:
        server.quit()


# 번역을 위한 GPT API 사용
def use_api(msg):
    if is_korean(msg):
        language = "영어"
    else:
        language = "한국어"

    prompt = f'아래 문장을 {language}로 번역해줘.\n{msg}'
    print('-> prompt: ' + prompt)
  
    format = '''
    {
      "res": "번역된 문장"
    }
  '''

    response = tool.answer('너는 번역기야', prompt, format) 
    
    return response['res']


# http://localhost:5000/ - 기본페이지 : "번역해서 메일 보내기"
@app.get('/')  
def index():
    return "번역해서 메일 보내기"
    

# http://localhost:5000/mail - 메일작성 폼 페이지 보여주기
@app.get('/mail')
def mail_form():
    # html template으로 데이터 전달
    
    return render_template("mail.html")

# post: http://localhost:5000/mail - 비동기 통신요청 받음: 폼입력데이터(subject, recipient_email,message) 전달받아서 처리
@app.post('/mail')
def mail_proc():
    # JSON 데이터 받음
    data = request.json
    subject = data['subject']
    recipient_email = data['recipient_email']
    message = data['message']
    
    # 번역 처리 (제목, 내용)

    subject = use_api(subject)
    message = use_api(message)

    # 데이터가 존재하면 메일보내기 처리
    if (subject and recipient_email and message):
       if send_email(subject,recipient_email,message):
           print("이메일 보내기 성공")
       else:
           print("이메일 보내기 실패")               
    return {"subject":subject, "recipient_email":recipient_email, "message":message}

app.run(host="0.0.0.0", port=5000, debug=True)  # 0.0.0.0: 모든 Host 에서 접속 가능, debug=True: 소스 변경시 자동 restart

'''
activate ai
python mail.py
'''
