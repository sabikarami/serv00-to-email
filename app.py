import requests
from bs4 import BeautifulSoup

'''
!!!务必将serv00的邮箱密码改为和你登录密码相同的密码!!!
sid为服务器编号，比如https://panel1.serv00.com,这就填panel后面的数字1
uname = ""  # 用户名
pwd = ""  # 密码
to_email = ""  # 接收邮箱地址
'''
# 账户信息列表
accounts = [
    {"sid": 0, "uname": "", "pwd": "", "to_email": ""},
    {"sid": 1, "uname": "", "pwd": "", "to_email": ""},
    # 添加更多账号
]

sess = requests.Session()

# 获取CSRF令牌
def get_csrf(url):
    resp = sess.get(url)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        token_i = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        if token_i:
            return token_i['value']
        else:
            raise ValueError("未找到csrfmiddlewaretoken")
    else:
        raise ConnectionError(f"无法访问 {url}，err：{resp.status_code}")

# 登录serv00服务器
def login(uname, pwd, url):
    csrf = get_csrf(url)
    payload = {
        "username": uname,
        "password": pwd,
        "csrfmiddlewaretoken": csrf,
    }
    headers = {
        "Referer": url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36",
    }
    resp = sess.post(url, data=payload, headers=headers, allow_redirects=False)

    if resp.status_code == 302:
        redirect_url = resp.headers.get('Location')
        if redirect_url == '/':
            redirect_resp = sess.get(f"https://panel0.serv00.com{redirect_url}", headers=headers)
            if redirect_resp.status_code == 200:
                print("登录成功！")
                return redirect_resp.text
            else:
                print(f"登录失败，err：{redirect_resp.status_code}")
        else:
            print(f"登录失败，err：{redirect_url}")
    elif resp.status_code == 200:
        print("登录失败")
    else:
        print(f"登录失败，err：{resp.status_code}")

    return None

# 获取email用户名
def get_email(uname, sid):
    url = f"https://panel{sid}.serv00.com/mail/details/{uname}.serv00.net"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36",
        "Referer": f"https://panel{sid}.serv00.com/login/",
    }
    resp = sess.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        email = soup.find(attrs={"data-email": True})
        if email:
            email_val = email['data-email']
            print(f"找到email：{email_val}")
            return email_val
        else:
            print("未找到email")
            return None
    else:
        print(f"打开页面失败，err：{resp.status_code}")
        return None

# 获取邮件登录页的CSRF令牌
def mail_login(email, pwd):
    resp = sess.get(mail_url)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        token_i = soup.find('input', {'name': '_token'})
        if token_i:
            token = token_i['value']
        else:
            raise ValueError("未找到 _token")
    else:
        raise ConnectionError(f"无法访问 {mail_url}，err：{resp.status_code}")

    payload = {
        "_token": token,
        "_task": "login",
        "_action": "login",
        "_timezone": "Asia/Shanghai",
        "_url": "_task=login",
        "_user": email,
        "_pass": pwd,
        "_language": "zh_CN"
    }
    headers = {
        "Referer": mail_url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36",
    }
    resp = sess.post(mail_url, data=payload, headers=headers, allow_redirects=False)
    if resp.status_code == 302:
        print("邮件登录成功！")
        return True
    else:
        print(f"邮件登录失败，err：{resp.status_code}")
        return False

# 获取发邮件真实地址
def get_cp_url():
    resp = sess.get(cp_url, allow_redirects=True)
    if resp.status_code == 200:
        return resp.url
    else:
        print(f"无法访问发邮件页面，err：{resp.status_code}")
        return None

# 获取发邮件所需参数源码
def get_cp_form(url):
    resp = sess.get(url, allow_redirects=True)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        form = soup.find('form', {'name': 'form'})
        if form:
            return form
        else:
            raise ValueError("未找到form")
    else:
        raise ConnectionError(f"无法访问 {url}，err：{resp.status_code}")

# 发邮件
def send_email(cp_url, to_email, uname):
    print(f"开始发送邮件")
    form = get_cp_form(cp_url)
    token = form.find('input', {'name': '_token'})
    id = form.find('input', {'name': '_id'})
    from_select = form.find('select', {'name': '_from'})
    from_option = from_select.find('option', {'selected': ''})

    if token and id and from_option:
        token_val = token['value']
        id_val = id['value']
        from_val = from_option['value']
    else:
        raise ValueError("未找到form字段")

    payload = {
        "_token": token_val,
        "_task": "mail",
        "_action": "send",
        "_id": id_val,
        "_attachments": "",
        "_from": from_val,
        "_to": to_email,
        "_cc": "",
        "_bcc": "",
        "_replyto": "",
        "_followupto": "",
        "_subject": f"你的serv00账号{uname}已成功续期",
        "_draft_saveid": "",
        "_draft": "",
        "_is_html": "0",
        "_framed": "1",
        "_message": f"你的serv00账号{uname}已成功续期",
        "editorSelector": "plain",
        "_mdn": "",
        "_dsn": "",
        "_keepformatting": "",
        "_priority": "0",
        "_store_target": "Sent"
    }

    headers = {
        "Referer": cp_url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36",
    }

    resp = sess.post(cp_url, data=payload, headers=headers)

    if resp.status_code == 200:
        print("邮件发送成功！")
    else:
        print(f"邮件发送失败，err：{resp.status_code}")

if __name__ == "__main__":
    for account in accounts:
        sid = account["sid"]
        uname = account["uname"]
        pwd = account["pwd"]
        to_email = account["to_email"]
        login_url = f"https://panel{sid}.serv00.com/login/"
        mail_url = "https://mail.serv00.com/?_task=login"
        cp_url = "https://mail.serv00.com/?_task=mail&_action=compose"

        if login(uname, pwd, login_url):
            email_data = get_email(uname, sid)
            if email_data:
                if mail_login(email_data, pwd):
                    cp_url_real = get_cp_url()
                    if cp_url_real:
                        send_email(cp_url_real, to_email, uname)
                    else:
                        print("访问发邮件页面失败")
                else:
                    print(f"使用{email_data} 登录失败")
            else:
                print("未能获取email")
        else:
            print(f"账户 {uname} 登录失败")
