import math, time
import random
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

import sys

rsa_e = "010001"
rsa_m = "008aed7e057fe8f14c73550b0e6467b023616ddc8fa91846d2613cdb7f7621e3cada4cd5d812d627af6b87727ade4e26d26208b7326815941492b2204c3167ab2d53df1e3a2c9153bdb7c8c2e968df97a5e7e01cc410f92c4c2c2fba529b3ee988ebc1fca99ff5119e036d732c368acf8beba01aa2fdafa45b21e4de4928d0d403"

e = {}

def log(s: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}]\t{s}")

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
        "origin": "https://webvpn.sues.edu.cn"
    })
    res = sess.get("https://webvpn.sues.edu.cn/")
    soup = BeautifulSoup(res.content, "lxml")
    casUrlByWebVPN = soup.find("a")["href"]
    res = sess.get(casUrlByWebVPN)
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
    postTarget = soup.find("form")["action"]
    res = sess.post(postTarget, data)
    soup = BeautifulSoup(res.content, "lxml")
    if "健康信息填报" not in soup.text:
        return False, "loginFail", None, None
    targetUrl = "https://webvpn.sues.edu.cn" + \
        soup.find("a", {"title": "健康信息填报"})["href"]
    sess.get(targetUrl)
    time.sleep(5)
    res = sess.get(targetUrl)
    return True, "success", res.url, sess

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
        res = sess.post(url, json=queryTodayJson)
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
        res = sess.post(url, json=queryNearJson)
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
    sess.get(reportUrl)
    urlheader = "/".join(reportUrl.split("/")[:-1])

    time_utc = datetime.utcnow()
    time_now = (time_utc + timedelta(hours=8))
    time_start = datetime(2021, 1, 29, 0, 1)

    # 在这里你可以填写你想开始自动填写的时间，默认是从2021年1月29日上午开始填
    # time_start = datatime(2021, 1, 29, 0, 1)

    while True:
        diff = time_start - time_now
        if (diff.days * 86400 + diff.seconds) > 0:
            break
        time_start += timedelta(hours=12)
        up_time = time_start + timedelta(hours=int(random.uniform(0, 10))) + timedelta(minutes=int(random.uniform(1, 30)))
        if up_time.hour < 12:
            timeType = "上午"
        else:
            timeType = "下午"
        now = up_time.strftime("%Y-%m-%d %H:%M")
	tjsj = up_time.strftime("%Y-%m-%d")
        log("Time Peking: " + now + " " + timeType)
	url = urlheader+"/com.sudytech.portalone.base.db.queryBySqlWithoutPagecond.biz.ext"
    	# 上报
	global e
	e["tw"] = str(round(random.uniform(36.0, 36.9), 1))
    	updateData = {
            "params": e
    	}
    	log(updateData["params"]["gh"] + "\t" + "gentemp:" + updateData["params"]["tw"])
    	url = urlheader+"/com.sudytech.work.shgcd.jkxxcj.jkxxcj.saveOrUpdate.biz.ext"
    	finalRes = sess.post(url, json=updateData)
 		json = finalRes.json()
		if 'exception' in json:
        	return False, "Already reported or sever down"
    	elif json['result']["success"]:
        	return True, None
    	else:
        	return False, "[" + finalRes.json()['result']['errorcode'] + "]" + finalRes.json()['result']['msg']


if __name__ == '__main__':
    person = {
        "name": sys.argv[1],
        "pwd": sys.argv[2],
    }
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
        else:
            log("report Fail\t" + msg)

    except:
        failFlag = True
        log("执行又双叒叕有问题啦~")
        log(person["name"] + " FAILED")
