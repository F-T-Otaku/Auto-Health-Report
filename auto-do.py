import math, time
import random
import requests
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

import sys
import telebot

rsa_e = "010001"
rsa_m = "008aed7e057fe8f14c73550b0e6467b023616ddc8fa91846d2613cdb7f7621e3cada4cd5d812d627af6b87727ade4e26d26208b7326815941492b2204c3167ab2d53df1e3a2c9153bdb7c8c2e968df97a5e7e01cc410f92c4c2c2fba529b3ee988ebc1fca99ff5119e036d732c368acf8beba01aa2fdafa45b21e4de4928d0d403"

e = {}

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

def loginByWebVPN(username, password):
    sess = requests.Session()
    sess.headers.update({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; H8324 Build/52.1.A.3.49; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045513 Mobile Safari/537.36 MMWEBID/7014 MicroMessenger/8.0.1840(0x2800003D) Process/tools WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "origin": "https://web-vpn.sues.edu.cn"
    })
    res = sess.get("https://web-vpn.sues.edu.cn/", verify=False)
    history = res.history
    realUrl = "https://web-vpn.sues.edu.cn" + \
        history[len(history)-1].headers["location"]
    
    soup = BeautifulSoup(res.content, "lxml")
    res = sess.get(realUrl, verify=False)
    execution = soup.find("input", {"name": "execution"}).attrs["value"]
    postTarget = "https://web-vpn.sues.edu.cn"+soup.find("form")["action"]
    data = {
        "username": username,
        "password": genRSAPasswd(password, rsa_e, rsa_m),
        "execution": execution,
        "encrypted": "true",
        "_eventId": "submit",
        "loginType": "1",
        "submit": "登 录"
    }
    
    res = sess.post(postTarget, data, verify=False)
    soup = BeautifulSoup(res.content, "lxml")
    if "健康信息填报" not in soup.text:
        return False, "loginFail", None, None
    realUrl = re.findall('(.*)/cas/login', realUrl)[0]
    targetUrl = realUrl + soup.find("div", {"title": "健康信息填报"})[
        "data-url"].replace("https://workflow.sues.edu.cn", "")

    time.sleep(5)
    return True, "success", targetUrl, sess

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

def queryToday(username, ampm, tjsj, url, referer, sess):
    try:
        queryTodayJson = {
            "params": {
                "empcode": username,
                'sd': ampm,
                'tjsj': tjsj,
            },
            "querySqlId": "com.sudytech.work.shgcd.jkxxcj.jkxxcj.queryToday"
        }
        sess.headers.update({
            "referer": referer
        })
        res = sess.post(url, json=queryTodayJson, verify=False)
        today_list = res.json()["list"]
        if len(today_list) == 0:
            return False
        else:
            global e
            e = today_list[0]
            lower_json(e)
            return True
    except:
        return False

def queryNear(username, url, referer, sess):
    try:
        queryNearJson = {
            "params": {
                "empcode": username
            },
            "querySqlId": "com.sudytech.work.shgcd.jkxxcj.jkxxcj.queryNear"
        }
        sess.headers.update({
            "referer": referer
        })
        res = sess.post(url, json=queryNearJson, verify=False)
        near_list = res.json()["list"]
        if len(near_list) == 0:
            return False
        else:
            global e
            e = near_list[0]
            lower_json(e)
            e.pop('id')
            return True
    except:
        return False

def doReport(person):
    username = person["name"]
    password = person["pwd"]
    requests.adapters.DEFAULT_RETRIES = 40
    state, msg, reportUrl, sess = loginByWebVPN(username, password)
    if not state:
        return False, msg
    reportUrl = "https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/jkxxcj.jsp"
    urlheader = "https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj"
    sess.get(reportUrl, verify=False)

    time_utc = datetime.utcnow()
    time_peking = (time_utc + timedelta(hours=8))

    if time_peking.hour % 24 < 12:
        timeType = "上午"
    else:
        timeType = "下午"
    now = time_peking.strftime("%Y-%m-%d %H:%M")
    tjsj = time_peking.strftime("%Y-%m-%d")
    log("Time Peking: " + now + " " + timeType)
    url = urlheader+"/com.sudytech.portalone.base.db.queryBySqlWithoutPagecond.biz.ext"

    # Today
    if not queryToday(username, timeType, tjsj, url, reportUrl, sess):
        if not queryNear(username, url, reportUrl, sess):
            log(username+":无最近数据")
            return False

    # 上报
    global e
    e["tw"] = str(round(random.uniform(36.0, 36.9), 1))
    updateData = {
        "params": e
    }
    log(updateData["params"]["gh"] + "\t" +
        "gentemp:" + updateData["params"]["tw"])
    url = urlheader+"/com.sudytech.work.shgcd.jkxxcj.jkxxcj.saveOrUpdate.biz.ext"
    finalRes = sess.post(url, json=updateData, verify=False)
    json = finalRes.json()
    if 'exception' in json:
        return False, "Already reported or sever down"
    elif json['result']["success"]:
        return True, None
    else:
        return False, "[" + finalRes.json()['result']['errorcode'] + "]" + finalRes.json()['result']['msg']

if __name__ == '__main__':
    output = "qtmd形式主义" + "\n\n"
    person = {
        "name": sys.argv[1],
        "pwd": sys.argv[2],
    }
    SCKEY = sys.argv[3]
    TOKEN = sys.argv[4]
    CHAT_ID = sys.argv[5]
    ServerChan = f"https://sc.ftqq.com/{SCKEY}.send"
    bot = telebot.TeleBot(TOKEN)
    requests.packages.urllib3.disable_warnings()
    requests.adapters.DEFAULT_RETRIES = 15

    try:
        state, msg, url, sess = loginByWebVPN(
            person["name"], person["pwd"])
        if state:
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
            requests.post(ServerChan, data={'text': '体温填写情况', 'desp': output})
            bot.send_message(CHAT_ID, output)

    except:
        failFlag = True
        log("执行又双叒叕有问题啦~")
        log(person["name"] + " FAILED")
        requests.post(ServerChan, data={'text': '体温填写情况', 'desp': output})
        bot.send_message(CHAT_ID, output)
