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
  START WITH 1        -- ���� ��ȣ
  INCREMENT BY 1      -- ������
  MAXVALUE 99999999   -- �ִ밪: 99999999 --> NUMBER(8) ����
  CACHE 2             -- 2���� �޸𸮿����� ���
  NOCYCLE;   
  

INSERT INTO member(memberno, id, passwd, mname, tel,  mdate, grade)
VALUES (member_seq.nextval, 'gpt', '1234', 'Chatting ������', '000-0000-0000', sysdate, 'A');

INSERT INTO member(memberno, id, passwd, mname, tel,  mdate)
VALUES (member_seq.nextval, 'user1', '1234', '��浿', '000-0000-0000', sysdate);

INSERT INTO member(memberno, id, passwd, mname, tel,  mdate)
VALUES (member_seq.nextval, 'user2', '1234', '�մ���', '000-0000-0000', sysdate);



select * from member;


COMMIT;

-- ���̺� ����
DROP TABLE health;


-- ���̺� ����
CREATE TABLE health(
  hno          NUMBER(8)    NOT NULL PRIMARY KEY,
  memberno     NUMBER(10)   NOT NULL, -- ȸ�� ��ȣ, ���ڵ带 �����ϴ� �÷�
  workout      VARCHAR(1000) NOT NULL, -- �
  rdate        DATE             NOT NULL, -- ������
  FOREIGN KEY (memberno) REFERENCES member (memberno)
);


DROP SEQUENCE health_seq;


CREATE SEQUENCE health_seq
  START WITH 1        -- ���� ��ȣ
  INCREMENT BY 1      -- ������
  MAXVALUE 99999999   -- �ִ밪: 99999999 --> NUMBER(8) ����
  CACHE 2             -- 2���� �޸𸮿����� ���
  NOCYCLE;            -- �ٽ� 1���� �����Ǵ� ���� ����

INSERT INTO health(hno, memberno, workout, rdate)
VALUES(chatting_seq.nextval, 2, '����Ʈ',sysdate);

commit;

select * from health;