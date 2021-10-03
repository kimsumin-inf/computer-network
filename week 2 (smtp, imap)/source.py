#sending
import smtplib, socket 
import imaplib
# getpass: 비밀번호 같이 숨겨야 하는 값일 경우에 사용
import getpass 
import email
from email.mime.text import MIMEText
from datetime import datetime
from email import message_from_string, policy

#mode : send / receive /quit
ID ,PASSWORD, MODE,IP,TIME = (0,0,0,0,0)

def setting(Id, Password,Mode, Ip, Time):
    Id = str(input("ID: "))
    Password = str(getpass.getpass("PASSWORD: "))
    Mode = str(input("Mode: \n send or receive or quit\n choose one :"))
    Ip = socket.gethostbyname(socket.gethostname())

    Time= datetime.now()
    Time = Time.strftime("%Y.%m.%d %H:%M:%S") 
    return Id, Password, Mode, Ip, Time

def send(ip, time):
    receiver_address = str(input("TYPE receiver_address : "))
    subject = str(input("TYPE SUBJECT :  "))
    contents = str(input("TYPE CONTENTS : "))
    host = 'smtp.gmail.com'
    sender= ID

    msg = MIMEText(contents, _charset='euc-kr')
    msg['subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver_address

    smtp = smtplib.SMTP_SSL(host, 465)
    smtp.login(ID, PASSWORD)
    smtp.sendmail(sender, receiver_address, msg.as_string())
    smtp.quit()

def findEncodingInfo(txt):    
    info = email.header.decode_header(txt)
    s, encoding = info[0]
    return s, encoding
    
def receive():
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(ID, PASSWORD)
    imap.select('inbox')
    result, data = imap.uid('search', None,"ALL")
    latest_email_uid = data[0].split()[-1]
    result, data = imap.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = data[0][1]
    email_message= email.message_from_string(raw_email.decode('utf-8'),policy=policy.default)
    
    print('FROM:', email_message['From'])
    print('SENDER:', email_message['Sender'])
    print('TO:', email_message['To'])
    print('DATE:', email_message['Date'])

    b, encode = findEncodingInfo(email_message['Subject'])
    print('SUBJECT:',b, encode)
 
    #이메일 본문 내용 확인
    print('[CONTENT]')
    print('='*80)
    if email_message.is_multipart():
        for part in email_message.get_payload():        
            bytes = part.get_payload(decode = True)    
            encode = part.get_content_charset()        
            print(str(bytes, encode))

    else :
        if email_message.get_content_type() == 'text/plain':
            bytes = email_message.get_payload(decode=True)
            encode = email_message.get_content_charset()
            message = str(bytes,encode)

        html_message=f'''
        <!DOCTYPE html>
        <html>
            <head>
        <title>Receive</title>
            </head>
        <body>
    
        <h1>receive file</h1>
        <p>
        FROM: {email_message['From']}
        SENDER: {email_message['Sender']}
        TO: {email_message['To']}
        DATE: {email_message['Date']}
        {'='*80}
        CONTENTS:
        {message}
        {'='*80}
        </p>
        </body>
        </html>
        '''
        html_file = open("receive.html",'w')
        html_file.write(html_message)
        html_file.close()
        print(message)
    print('='*80)

    imap.close()
    imap.logout()




def process(ID ,PASSWORD, MODE, IP, TIME):
    
    if MODE == "send":
        print("send mode ")
        send(IP, TIME)
        print("send sucess")
        MODE = str(input("Mode: \n send or receive or quit\n choose one :"))
        process(ID ,PASSWORD, MODE, IP, TIME)
    elif MODE == "receive":
        print("receive mode ")
        receive()
        print("receive sucess")
        MODE = str(input("Mode: \n send or receive or quit\n choose one :"))
        process(ID ,PASSWORD, MODE, IP, TIME)
        
    elif MODE == "quit":
        print("program exit! \n good bye~ \n")
        return 0
    else :
        print("retype Mode")
        MODE = str(input("Mode: \n send or receive or quit\n choose one :"))
        process(ID ,PASSWORD, MODE, IP, TIME)



ID ,PASSWORD, MODE, IP, TIME = setting(ID ,PASSWORD, MODE,IP,TIME)
process(ID ,PASSWORD, MODE, IP, TIME)