自动登录Serv00服务器保活，并使用serv00邮箱发送邮件到指定邮箱的Python脚本。

## 功能

- 登录Serv00服务器
- 使用serv00邮箱发送邮件到指定邮箱

## 使用

1. 安装必要的Python库：
   ```bash
   pip install requests beautifulsoup4
2. 运行
   ```bash
   python app.py

## 配置

在脚本中设置以下全局变量：

- `sid`：服务号，即登录地址panel后的数字部分。
- `uname`：Serv00的用户名。
- `pwd`：Serv00的密码。
- `to_email`：接收邮件的邮箱地址。

## License

[MIT License](LICENSE) @ heilo.cn
