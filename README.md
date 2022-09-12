# gkd-auto-report

使用指南：
- 右上角 fork 本仓库

- Settings -> Secrets -> Actions -> New repository secret，添加五项信息（此数据经过加密仅本人可见）

  - `EMAIL`：UCAS 邮箱

  - `NAME`：姓名

  - `NUMBER`：学号

  - `PASSWORD`：密码

  - `PUSH_TOKEN`：[pushplus](http://www.pushplus.plus/) 推送 Token

  ![help1](img/help1.png)

- 在 main.py 文件中修改住址、核酸、疫苗等信息

- 手动测试：Actions -> Workflows -> Report -> Run Workflow -> Run Workflow

  ![help2](img/help2.png)

  - 成功：微信收到推送
  - 失败：在 Actions 中查看失败原因

- 等待每天零点一分自动签到
