import os
import win32com.client as win32
import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
attachment_path = os.path.join(script_dir, 'versions.xlsx')

def send_email(subject, to, attachment_path, sender=None):
    """
    发送带有附件的邮件。

    参数：
    subject: 邮件主题。
    body: 邮件正文。
    to: 收件人地址，多个地址可以使用分号 ";" 分隔。
    attachment_path: 附件文件的完整路径。
    sender: 发件人地址和名称，格式为 "name <email>"。如果未指定，则默认使用当前用户。

    返回值：
    无。
    """
    # 获取当前工作目录
    cwd = os.getcwd()

    # 创建 Outlook 应用程序对象
    outlook = win32.Dispatch('Outlook.Application')

    # 创建邮件对象
    mail = outlook.CreateItem(0)

    # 设置邮件主题和正文
    mail.Subject = subject

    # 创建 pandas 数据帧从附件读取数据
    df = pd.read_excel(attachment_path)

    # 创建表格 table_html
    #table_html = df.to_html(index=False)
    body = """
    <html>
    <body style="font-family:Calibri;font-size:11pt;">
    <p>Hi all,</p>

    <p>This is the comparison result of the latest port-version, please refer to the attachment for the actual content.</p>

    <p>Thanks,<br>
    Frank</p>
    </body>
    </html>
    """
    #body = '<html><body style="font-family:Calibri;font-size:11pt;">第一次测试的vcpkg结果.' + table_html + '</body></html>'

    # 设置正文中包含HTML内容
    mail.HTMLBody = body
    attachment = mail.Attachments.Add(attachment_path)

    # 添加收件人
    mail.To = to

    # 指定发件人的地址和名称
    if sender:
        mail.SentOnBehalfOfName = sender

    # 发送邮件
    mail.Send()
    print("邮件发送成功！！")


"""
subject='Vcpkg Verison Check',
to='vcpkgcti@microsoft.com',
#sender='frank <v-frankxie@microsoft.com>'

send_email(subject, to, attachment_path)
"""
