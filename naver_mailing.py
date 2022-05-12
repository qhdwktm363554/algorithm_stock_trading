import smtplib
# 이메일 메시지에 다양한 형식을 중첩하여 담기 위한 객체
from email.mime.multipart import MIMEMultipart

# 이메일 메시지를 이진 데이터로 바꿔주는 인코더
from email import encoders

# 텍스트 형식
from email.mime.text import MIMEText
# 이미지 형식
from email.mime.image import MIMEImage
# 오디오 형식
from email.mime.audio import MIMEAudio

# 위의 모든 객체들을 생성할 수 있는 기본 객체
# MIMEBase(_maintype, _subtype)
# MIMEBase(<메인 타입>, <서브 타입>)
from email.mime.base import MIMEBase

# https://ai-creator.tistory.com/306 여기 블로그에서 보고 그대로 복사해서 붙여 넣었다. (2021년도 12월 22일)
def send_email(smtp_info, msg):
    with smtplib.SMTP(smtp_info["smtp_server"], smtp_info["smtp_port"]) as server:
        # TLS 보안 연결
        server.starttls()
        # 로그인
        server.login(smtp_info["smtp_user_id"], smtp_info["smtp_user_pw"])

        # 로그인 된 서버에 이메일 전송
        response = server.sendmail(msg['from'], msg['to'],
                                   msg.as_string())  # 메시지를 보낼때는 .as_string() 메소드를 사용해서 문자열로 바꿔줍니다.

        # 이메일을 성공적으로 보내면 결과는 {}
        if not response:
            print('이메일을 성공적으로 보냈습니다.')
        else:
            print(response)
def bong(text):
    print(text)

def make_multimsg(msg_dict):
    multi = MIMEMultipart(_subtype='mixed')

    for key, value in msg_dict.items():
        # 각 타입에 적절한 MIMExxx()함수를 호출하여 msg 객체를 생성한다.
        if key == 'text':
            with open(value['filename'], encoding='utf-8') as fp:
                msg = MIMEText(fp.read(), _subtype=value['subtype'])
        elif key == 'image':
            with open(value['filename'], 'rb') as fp:
                msg = MIMEImage(fp.read(), _subtype=value['subtype'])
        elif key == 'audio':
            with open(value['filename'], 'rb') as fp:
                msg = MIMEAudio(fp.read(), _subtype=value['subtype'])
        else:
            with open(value['filename'], 'rb') as fp:
                msg = MIMEBase(value['maintype'], _subtype=value['subtype'])
                msg.set_payload(fp.read())
                encoders.encode_base64(msg)
        # 파일 이름을 첨부파일 제목으로 추가
        msg.add_header('Content-Disposition', 'attachment', filename=value['filename'])

        # 첨부파일 추가
        multi.attach(msg)

    return multi

from email.mime.text import MIMEText

smtp_info = dict({"smtp_server" : "smtp.naver.com", # SMTP 서버 주소
                  "smtp_user_id" : "qhdwktm3635@naver.com",
                  "smtp_user_pw" : "zxcv12",
                  "smtp_port" : 587}) # SMTP 서버 포트

import datetime
# BONG: 날짜 추가한거다.
today = datetime.datetime.today().strftime("%Y%m%d")

# 메일 내용 작성
title = f"봉현아 {today} 1_naver crawling 1차 끝났다. 한발 더 가보자~!!"
content = "너는 짱이다"
sender = "qhdwktm3635@naver.com"
receiver = "qhdwktm3635@gmail.com"
# 메일 객체 생성 : 메시지 내용에는 한글이 들어가기 때문에 한글을 지원하는 문자 체계인 UTF-8을 명시해줍니다.
msg = MIMEText(_text = content, _charset = "utf-8") # 메일 내용
msg['Subject'] = title     # 메일 제목
msg['From'] = sender       # 송신자
msg['To'] = receiver       # 수신자


# 메일 내용 작성
title_2 = f"큰일 났다~!!! {today} column selector가 바꼈나보다~!!!!!!"
content_2 = "봉현아 얼른 다시 해라"
sender = "qhdwktm3635@naver.com"
receiver = "qhdwktm3635@gmail.com"
# 메일 객체 생성 : 메시지 내용에는 한글이 들어가기 때문에 한글을 지원하는 문자 체계인 UTF-8을 명시해줍니다.
msg_2 = MIMEText(_text = content_2, _charset = "utf-8") # 메일 내용
msg_2['Subject'] = title_2     # 메일 제목
msg_2['From'] = sender       # 송신자
msg_2['To'] = receiver       # 수신자

# 메일 내용 작성
title_3 = f"봉현아 {today} naver crawling 2차도 끝났다. 오늘도 고생 많았어 ^^"
content_3 = "이것까지 다 했다~!!"
sender = "qhdwktm3635@naver.com"
receiver = "qhdwktm3635@gmail.com"
# 메일 객체 생성 : 메시지 내용에는 한글이 들어가기 때문에 한글을 지원하는 문자 체계인 UTF-8을 명시해줍니다.
msg_3 = MIMEText(_text = content_3, _charset = "utf-8") # 메일 내용
msg_3['Subject'] = title_3     # 메일 제목
msg_3['From'] = sender       # 송신자
msg_3['To'] = receiver       # 수신자

# 메일 내용 작성
title_4 = f"봉현아 {today} 4_collecting 끝났다. 그 다음 navercrawling 가보자!! ^^"
content_4 = "collecting 정상완료^^"
sender = "qhdwktm3635@naver.com"
receiver = "qhdwktm3635@gmail.com"
# 메일 객체 생성 : 메시지 내용에는 한글이 들어가기 때문에 한글을 지원하는 문자 체계인 UTF-8을 명시해줍니다.
msg_4 = MIMEText(_text = content_4, _charset = "utf-8") # 메일 내용
msg_4['Subject'] = title_4     # 메일 제목
msg_4['From'] = sender       # 송신자
msg_4['To'] = receiver       # 수신자

# 메일 내용 작성
title_5 = f"봉현아 {today} 3_yahoo_crawling 끝났다. 계속 돌거라 나의 프로그램아!!!"
content_5 = "yahoo_finance_crawling 정상완료^^"
sender = "qhdwktm3635@naver.com"
receiver = "qhdwktm3635@gmail.com"
# 메일 객체 생성 : 메시지 내용에는 한글이 들어가기 때문에 한글을 지원하는 문자 체계인 UTF-8을 명시해줍니다.
msg_5 = MIMEText(_text = content_5, _charset = "utf-8") # 메일 내용
msg_5['Subject'] = title_5     # 메일 제목
msg_5['From'] = sender       # 송신자
msg_5['To'] = receiver       # 수신자

# 메일 내용 작성
title_6 = f"봉현아 {today} YahooFinanceCrawling에 문제가 생겼다!!!"
content_6 = "case1: yahoo column명 바뀜, case2: 제 날짜의 crawling아님, case3: 이미 crawling 완료함"
sender = "qhdwktm3635@naver.com"
receiver = "qhdwktm3635@gmail.com"
# 메일 객체 생성 : 메시지 내용에는 한글이 들어가기 때문에 한글을 지원하는 문자 체계인 UTF-8을 명시해줍니다.
msg_6 = MIMEText(_text = content_6, _charset = "utf-8") # 메일 내용
msg_6['Subject'] = title_6     # 메일 제목
msg_6['From'] = sender       # 송신자
msg_6['To'] = receiver       # 수신자


if __name__ == "__main__":
    send_email(smtp_info, msg )
