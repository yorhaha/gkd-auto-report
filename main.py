import requests
import time
import os

s = requests.Session()

GKD_EMAIL = os.environ["GKD_EMAIL"]    # sep账号
GKD_PASSWORD = os.environ["GKD_PASSWORD"]   # sep密码
GKD_NUMBER = os.environ["GKD_NUMBER"]
GKD_NAME = os.environ["GKD_NAME"]
PUSH_TOKEN = os.environ["PUSH_TOKEN"]

time_now = time.time()
if time.timezone == 0:
    time_now += 28800
time_now = time.localtime(time_now)
time_str = time.strftime('%Y-%m-%d %H:%M:%S', time_now)


def login(s: requests.Session):
    r = s.post("https://app.ucas.ac.cn/uc/wap/login/check", data={
        "username": GKD_EMAIL,
        "password": GKD_PASSWORD
    })

    if r.json().get('m') == "操作成功":
        print("登录成功")
    else:
        send_message('登录失败', r.json())
        exit(1)


def submit(s: requests.Session):
    new_daily = {
        "number": GKD_NUMBER,
        "realname": GKD_NAME,

        # submitted date
        "date": time.strftime(r"%Y-%m-%d", time_now),
        "jzdz": "北京市怀柔区中国科学院大学雁栖湖校区西区一公寓",     # Residential Address
        "zrzsdd": "1",                       # Yesterday place to stay    1.雁栖湖  8.京外
        # Whether you are in school or not  1.是, 主要是在雁栖湖校区   5.否
        "sfzx": "1",
        "szgj": "中国",                       # current country
        "szdd": "国内",                       # current address
        "dqszdd": "1",                       # current location

        #
        "address": "北京市怀柔区",
        "area": "怀柔区",
        "province": "北京市",
        "city": "",
        "geo_api_info": "{\"address\":\"北京市怀柔区\",\"details\":\"怀北镇中国科学院大学雁栖湖校区公寓中国科学院大学雁栖湖校区西区\",\"province\":{\"label\":\"北京市\",\"value\":\"\"},\"city\":{\"label\":\"\",\"value\":\"\"},\"area\":{\"label\":\"怀柔区\",\"value\":\"\"}}",
        "szgj_api_info": "{\"area\":{\"label\":\"\",\"value\":\"\"},\"city\":{\"label\":\"\",\"value\":\"\"},\"address\":\"\",\"details\":\"\",\"province\":{\"label\":\"\",\"value\":\"\"}}",
        "szgj_select_info": {},
        #

        # whether you are in high or medium risk area or not  4. 无上述情况
        "dqsfzzgfxdq": "4",
        # do you have a travel history in risk area  4. 无上述情况
        "zgfxljs": "4",
        "tw": "1",                           # Today’s body temperature 1.37.2℃及以下
        # Do you have such symptoms as fever, fatigue, dry cough or difficulty in breathing today?
        "sffrzz": "0",
        "dqqk1": "1",                        # current situation      1.正常
        "dqqk1qt": "",
        "dqqk2": "1",                        # current situation      1.无异常
        "dqqk2qt": "",
        # 昨天是否接受核酸检测
        "sfjshsjc": "1",                     # PCR test?       1.是 0.否
        # 第一针接种
        "dyzymjzqk": "3",                    # first vaccination situation  3.已接种
        "dyzjzsj": "2021-03-07",             # date of first vaccination
        "dyzwjzyy": "",
        # 第二针接种
        "dezymjzqk": "3",                    # second vaccination situation  3.已接种
        "dezjzsj": "2021-03-28",             # date of second vaccination
        "dezwjzyy": "",
        # 第三针接种
        "dszymjzqk": "6",                    # third vaccination situation  6.未接种
        "dszjzsj": "2000-01-01",             # default time
        "dszwjzyy": "在吃其他药物",            # reason of non-vaccination

        "gtshryjkzk": "1",                   # health situation
        "extinfo": "",                       # other information
        # personal information

        # "created_uid":"0",
        # "todaysfhsjc":"",
        # "is_daily":1,
        "geo_api_infot": "{\"address\":\"北京市怀柔区\",\"details\":\"怀北镇中国科学院大学雁栖湖校区公寓中国科学院大学雁栖湖校区西区\",\"province\":{\"label\":\"北京市\",\"value\":\"\"},\"city\":{\"label\":\"\",\"value\":\"\"},\"area\":{\"label\":\"怀柔区\",\"value\":\"\"}}",

        # yesterday information
        "old_szdd": "国内",
        "old_city": "{\"address\":\"北京市怀柔区\",\"details\":\"怀北镇中国科学院大学雁栖湖校区公寓中国科学院大学雁栖湖校区西区\",\"province\":{\"label\":\"北京市\",\"value\":\"\"},\"city\":{\"label\":\"\",\"value\":\"\"},\"area\":{\"label\":\"怀柔区\",\"value\":\"\"}}",
    }

    r = s.post("https://app.ucas.ac.cn/ucasncov/api/default/save", data=new_daily)
    print("提交信息:", new_daily)

    result = r.json()
    if result.get('m') == "操作成功":
        if time_now.tm_hour >= 6:
            send_message('打卡成功', '打卡成功！')
    elif result.get('m') == '今天已经填报了':
        print(time_str + '今天已经填报了')
        if time_now.tm_hour >= 6:
            send_message('打卡成功', '打卡成功！')
    else:
        send_message('打卡失败', r.json().get("m"))


def send_message(title: str, content: str):
    content = time_str + content
    print(time_now)
    print(title)
    print(content)
    res = requests.get(
        url='http://www.pushplus.plus/send',
        params={
            'token': PUSH_TOKEN,
            'title': title,
            'content': content
        }
    )
    if res.status_code != 200:
        print('推送失败: ' + res.text)


if __name__ == "__main__":
    try:
        login(s)
        submit(s)
    except Exception as e:
        send_message('执行错误', str(e))
