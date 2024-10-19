from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import tool
import cx_Oracle

app = Flask(__name__)
CORS(app)


@app.route('/get_workout', methods=['POST'])
def get_workout():
    # 클라이언트로부터 JSON 형식의 데이터를 받아오기
    data = request.get_json()
    user_info = f"체중: {data['weight']} kg\n체지방: {data['bodyFat']}%\n신장: {data['height']} cm\n골격근량: {data['muscleMass']} kg"
    goal_info = f"체중: {data['goalWeight']}kg\n체지방: {data['goalBodyFat']}%\n신장: {data['height']}cm\n골격근량: {data['goalMuscleMass']}kg"

    prompt = f"아래의 [회원 건강 정보]를 바탕으로 [운동 목표]를 설정해서 운동 중이야, [운동 추천 목록]에서 운동 목표를 달성하기 위해 필요한 운동 종류 5가지를 추천해줘, 출력 형식은 JSON으로 해줘.\n\n[회원 건강 정보]\n{user_info}\n\n[운동 목표]\n{goal_info}\n\n[운동 추천 목록]\n벤치 프레스, 푸시업, 다이아몬드 푸시업, 덤벨 플라이, 케이블 크로스오버, 풀업, 와이드 그립, 클로즈 그립, 차이업, 랫 풀다운, 바벨 로우, 원 암 덤벨 로우, 케이블 로우, 어깨 근육, 오버헤드 프레스, 사이드 레터럴 레이즈, 프론트 레이즈, 리어 델트 플라이, 페이스 풀, 바벨 컬, 덤벨 컬, 해머 컬, 케이블 컬, 프리처 컬, 트라이셉스 익스텐션, 트라이셉스 딥스, 클로즈 그립 벤치 프레스, 케이블 푸시다운, 다리 근육, 스쿼트, 바벨 백 스쿼트, 프론트 스쿼트, 덤벨 스쿼트, 레그 프레스, 런지, 레그 익스텐션, 레그 컬, 카프 레이즈, 스탠딩, 시티드 카프 레이즈, 크런치, 바이시클 크런치, 리버스 크런치, 플랭크, 프론트 플랭크, 사이드 플랭크, 레그 레이즈, 앱 롤아웃, 앱 휠, 마운틴 클라이머, 데드리프트, 트래디셔널, 스모 데드리프트, 케틀벨 스윙, 러시안 트위스트"
    role = "헬스클럼 트레이너"

    # GPT 추천 운동 받기
    result = tool.answer(role,prompt)
    print("result:",result)
    # Oracle 데이터베이스에 연결, 'ai' 계정으로 'XE' 데이터베이스에 접속
    conn = cx_Oracle.connect('ai/1234@3.146.175.211:1521/XE')
    cursor = conn.cursor()  # SQL 실행을 위한 커서 객체 생성
    workout = result['운동추천목록']
    # workout 리스트의 값들을 쉼표(,)로 구분된 문자열로 변환
    # 리스트의 각 항목을 하나의 문자열로 변환
    # 예시 형식: '운동명: 스쿼트, 설명/목표: 하체 근육을 강화하고 체중 감량에 도움을 줍니다.'
    workout_str = ', '.join([f"운동명: {item['운동명']}, 설명: {item['목표']}" for item in workout])
    memberno = data['memberno']
    
    # SQL 쿼리: 'health' 테이블에 새로운 채팅 메시지를 삽입하는 쿼리
    sql = """
    INSERT INTO health(hno, memberno, workout, rdate)
    VALUES(health_seq.nextval, :memberno, :workout, sysdate)
    """
    # GPT의 응답을 'health' 테이블에 저장, memberno,workout 저장
    cursor.execute(sql, (memberno, workout_str))
        
    conn.commit()  # 변경 사항을 DB에 커밋
     
    return result

@app.route('/health_form') #http://127.0.0.1:5000/health_form?memberno=2
def health_form():
    memberno= request.args.get('memberno')
    print(f'-> {memberno}')
    data = {'memberno': memberno}
    return render_template('health.html',data=data)

app.run(host="0.0.0.0", port=5000, debug=True)

