drop table member;
create table member(
    memberno    NUMBER(8)    NOT NULL PRIMARY KEY, 
    id          VARCHAR(20)  NOT NULL, 
    passwd      VARCHAR(20)  NOT NULL, 
    mname       VARCHAR(50)  NOT NULL, 
    tel         VARCHAR(20)  NOT NULL, 
    mdate       date, 
    grade       VARCHAR(5)   default 'N'
);

DROP SEQUENCE member_seq;

CREATE SEQUENCE member_seq
  START WITH 1        -- 시작 번호
  INCREMENT BY 1      -- 증가값
  MAXVALUE 99999999   -- 최대값: 99999999 --> NUMBER(8) 대응
  CACHE 2             -- 2번은 메모리에서만 계산
  NOCYCLE;   
  

INSERT INTO member(memberno, id, passwd, mname, tel,  mdate, grade)
VALUES (member_seq.nextval, 'gpt', '1234', 'Chatting 관리자', '000-0000-0000', sysdate, 'A');

INSERT INTO member(memberno, id, passwd, mname, tel,  mdate)
VALUES (member_seq.nextval, 'user1', '1234', '김길동', '000-0000-0000', sysdate);

INSERT INTO member(memberno, id, passwd, mname, tel,  mdate)
VALUES (member_seq.nextval, 'user2', '1234', '왕눈이', '000-0000-0000', sysdate);



select * from member;


COMMIT;

-- 테이블 삭제
DROP TABLE health;


-- 테이블 생성
CREATE TABLE health(
  hno          NUMBER(8)    NOT NULL PRIMARY KEY,
  memberno     NUMBER(10)   NOT NULL, -- 회원 번호, 레코드를 구분하는 컬럼
  workout      VARCHAR(1000) NOT NULL, -- 운동
  rdate        DATE             NOT NULL, -- 가입일
  FOREIGN KEY (memberno) REFERENCES member (memberno)
);


DROP SEQUENCE health_seq;


CREATE SEQUENCE health_seq
  START WITH 1        -- 시작 번호
  INCREMENT BY 1      -- 증가값
  MAXVALUE 99999999   -- 최대값: 99999999 --> NUMBER(8) 대응
  CACHE 2             -- 2번은 메모리에서만 계산
  NOCYCLE;            -- 다시 1부터 생성되는 것을 방지

INSERT INTO health(hno, memberno, workout, rdate)
VALUES(chatting_seq.nextval, 2, '스쿼트',sysdate);

commit;

select * from health;