# -*- coding: utf-8 -*-
import smtplib, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header


to_list = ["long.yan@zatech.com"]
cc_list = ["long.yan@zatech.com"]

content = '''
<p> Dear All:</p>
<p> Here is automation testing report summary, for more details please check the attachment.</p>
<p> Any questions please contact QA team.</p>
<p> No need to reply this email.</p>
<p></p>
'''


class MailUtils:
    def __init__(self, subject, report_path, attachment,
                 mail_host="smtp.office365.com",
                 mail_user="fusion_qa@zatech.com",
                 mail_pwd="Fusion2019"):
        self.subject = subject
        self.report_path = report_path
        self.attachment = attachment
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_pwd = mail_pwd
        self.to_list = to_list
        self.cc_list = cc_list
        self.content = content

    def send(self):
        root_msg = MIMEMultipart()
        root_msg['Subject'] = Header(self.subject, 'utf-8')
        root_msg['From'] = Header(self.mail_user, 'utf-8')
        root_msg['To'] = ';'.join(self.to_list)
        root_msg['Cc'] = ';'.join(self.cc_list)

        with open(self.report_path, "r", encoding="UTF-8") as f:
            data = f.read()
        start = data.index("<div><strong>1.概要信息</strong></div>")
        end = data.index("<div><strong>2.用例执行失败汇总</strong></div>")
        html = content + "\n" + data[start:end] + "<p> ...... </p>"
        message = MIMEText(html, 'html', 'utf-8')

        if self.attachment:
            file_name = self.report_path.split("/")[-1]
            attachment_msg = MIMEApplication(open(self.report_path, 'rb').read())
            attachment_msg.add_header('content-disposition', 'attachment', filename=file_name)
            root_msg.attach(attachment_msg)

        root_msg.attach(message)
        smtp_server = smtplib.SMTP(host=self.mail_host, port=587)

        smtp_server.set_debuglevel(1)
        smtp_server.connect(self.mail_host, 587)
        smtp_server.starttls()
        smtp_server.login(self.mail_user, self.mail_pwd)
        smtp_server.sendmail(self.mail_user, self.to_list, root_msg.as_string())


subject = "Automation Daily Report (" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ")"
report_path = "./api_test_report.html"
MailUtils(subject=subject, report_path=report_path, attachment=True).send()


