import math, time
import random
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

rsa_e = "010001"
rsa_m = "008aed7e057fe8f14c73550b0e6467b023616ddc8fa91846d2613cdb7f7621e3cada4cd5d812d627af6b87727ade4e26d26208b7326815941492b2204c3167ab2d53df1e3a2c9153bdb7c8c2e968df97a5e7e01cc410f92c4c2c2fba529b3ee988ebc1fca99ff5119e036d732c368acf8beba01aa2fdafa45b21e4de4928d0d403"

def log(s: str):
    global output
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}]\t{s}")
    output = output + "[" + timestamp + "]" + s + "  " + "\n\n"


def genRSAPasswd(passwd, e, m):
    # 别问我为啥rsa加密要这么写，傻逼cas
    # 参考https://www.cnblogs.com/himax/p/python_rsa_no_padding.html
    m = int.from_bytes(bytearray.fromhex(m), byteorder='big')
    e = int.from_bytes(bytearray.fromhex(e), byteorder='big')
    plaintext = passwd[::-1].encode("utf-8")
    input_nr = int.from_bytes(plaintext, byteorder='big')
    crypted_nr = pow(input_nr, e, m)
    keylength = math.ceil(m.bit_length() / 8)
    crypted_data = crypted_nr.to_bytes(keylength, byteorder='big')
    return crypted_data.hex()


def DoSUESCasLogin(username, password, sess):
    res = sess.get("https://cas.sues.edu.cn/cas/login")
    soup = BeautifulSoup(res.content, "lxml")
    execution = soup.find("input", {"name": "execution"}).attrs["value"]
    data = {
        "username": username,
        "password": genRSAPasswd(password, rsa_e, rsa_m),
        "execution": execution,
        "encrypted": "true",
        "_eventId": "submit",
        "loginType": "1",
        "submit": "登 录"
    }
    res = sess.post("https://cas.sues.edu.cn/cas/login", data)
    soup = BeautifulSoup(res.content, "lxml")
    if soup.find("div", {"class": "success"}):
        return True
    else:
        return False


def lower_json(json_info):
    if isinstance(json_info, dict):
        for key in list(json_info.keys()):
            if key.islower():
                lower_json(json_info[key])
            else:
                key_lower = key.lower()
                json_info[key_lower] = json_info[key]
                del json_info[key]
                lower_json(json_info[key_lower])

    elif isinstance(json_info, list):
        for item in json_info:
            lower_json(item)


def doReport(person):
    username = person["CASUsername"]
    password = person["CASPassword"]
    requests.adapters.DEFAULT_RETRIES = 40
    sess = requests.Session()
    sess.keep_alive = False
    sess.headers.update({
        "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding":
            "gzip, deflate",
        "Accept-Language":
            "zh-CN,zh;q=0.9",
        "User-Agent":
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)"
    })
    res = DoSUESCasLogin(username, password, sess)
    if not res:
        return False, "LOGIN FAIL"
    url = "https://cas.sues.edu.cn/cas/login?service=https%3A%2F%2Fworkflow.sues.edu.cn%2Fdefault%2Fwork%2Fshgcd%2Fjkxxcj%2Fjkxxcj.jsp"
    res = sess.get(url)  # cas 跳转登录
    newHeader = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Content-Type": "text/json",
        "Origin": "https://workflow.sues.edu.cn",
        "Referer": "https://workflow.sues.edu.cn/default/work/shgcd/jkxxcj/jkxxcj.jsp",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest"
    }
    sess.headers.update(newHeader)

    time_utc = datetime.utcnow()
    time_peking = (time_utc + timedelta(hours=8))

    if time_peking.hour % 24 < 12:
        timeType = "上午"
    else:
        timeType = "下午"
    now = time_peking.strftime("%Y-%m-%d %H:%M")

    # 在这里你可以填写过去或者未来的日期(
    # timeType = "下午"
    # now = "2021-02-02 17:51"

    log("Time Peking: " + now + " " + timeType)

    # 1
    requestJsonFirst = {
        "params": {
            "empcode": username
        },
        "querySqlId": "com.sudytech.work.shgcd.jkxxcj.jkxxcj.queryEmp"
    }
    sess.post(
        "https://workflow.sues.edu.cn/default/work/shgcd/jkxxcj/com.sudytech.portalone.base.db.queryBySqlWithoutPagecond.biz.ext",
        json=requestJsonFirst)

    # 获取上一次的数据
    requestLastJson = {
        "params": {
            "empcode": username
        },
        "querySqlId": "com.sudytech.work.shgcd.jkxxcj.jkxxcj.queryNear"
    }
    resLast = sess.post(
        "https://workflow.sues.edu.cn/default/work/shgcd/jkxxcj/com.sudytech.portalone.base.db.queryBySqlWithoutPagecond.biz.ext",
        json=requestLastJson)

    if len(resLast.json()["list"]) == 0:
        return False, "GET LAST REPORT FAIL"
    person = resLast.json()["list"][0]
    lower_json(person)
    # 上报
    updateData = {
        "params": {
            "sqrid": person["sqrid"],
            "sqbmid": person["sqbmid"],
            "rysf": person["rysf"],
            "sqrmc": person["sqrmc"],
            "gh": person["gh"],
            "sfzh": person["sfzh"],
            "sqbmmc": person["sqbmmc"],
            "xb": person["xb"],
            "lxdh": person["lxdh"],
            "nl": person["nl"],
            "tjsj": now,
            "xrywz": person["xrywz"],
            "sheng": person["sheng"],
            "shi": person["shi"],
            "qu": person["qu"],
            "jtdzinput": person["jtdzinput"],
            "gj": person["gj"],
            "jtgj": person["jtgj"],
            "jkzk": person["jkzk"],
            "jkqk": person["jkqk"],
            "tw": str(round(random.uniform(36.1, 36.9), 1)),
            "sd": timeType,
            "bz": person["bz"],
            "_ext": "{}"
        }
    }
    log(updateData["params"]["gh"] + "\t" + "gentemp:" + updateData["params"]["tw"])
    url = "https://workflow.sues.edu.cn/default/work/shgcd/jkxxcj/com.sudytech.work.shgcd.jkxxcj.jkxxcj.saveOrUpdate.biz.ext"
    finalRes = sess.post(url, json=updateData)
    if finalRes.json()['result']["success"]:
        return True, None
    else:
        return False, "[" + finalRes.json()['result']['errorcode'] + "]" + finalRes.json()['result']['msg']


if __name__ == '__main__':
    import sys
    import telebot
    output = "体温上报成功" + "\n\n"
    person = {
        "CASUsername": sys.argv[1],
        "CASPassword": sys.argv[2],
    }
    SCKEY = sys.argv[3]
    TOKEN = sys.argv[4]
    CHAT_ID = sys.argv[5]
    ServerChan = f"https://sc.ftqq.com/{SCKEY}.send"
    bot = telebot.TeleBot(TOKEN)
    requests.adapters.DEFAULT_RETRIES = 15
    sess = requests.Session()
    sess.keep_alive = False
    sess.headers.update({
        "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding":
            "gzip, deflate",
        "Accept-Language":
            "zh-CN,zh;q=0.9",
        "User-Agent":
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)"
    })
    res = DoSUESCasLogin(person["CASUsername"], person["CASPassword"], sess)
    if res:
        log("CAS login test SUCCESS")
    else:
        log("CAS login test FAIL")
        quit()
    state, msg = doReport(person)
    if state:
        log("report success")
        requests.post(ServerChan, data={'text': '体温填写情况', 'desp': output})
        bot.send_message(CHAT_ID, output)
    else:
        log("report Fail\t" + msg)
