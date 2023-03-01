from websocket import WebSocketApp
import json
import re
import gzip
import datetime
from urllib.parse import unquote_plus
import requests
from douyin_pb2 import PushFrame, Response, ChatMessage
import pymysql

# 定义直播间号：
# 东方甄选直播间：80017709309
# 交个朋友直播间：168465302284
live_id = "80017709309"

# 数据库连接
db = pymysql.connect(host='sh-cynosdbmysql-grp-dy68nzyy.sql.tencentcdb.com',
                     port=,
                     user='root',
                     password='',
                     db='DY_Spider_DB',
                     charset='utf8mb4')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
print("数据库连接成功！")

# 获取直播间的基本信息
def fetch_live_room_info(url):
    res = requests.get(
        url=url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        },
        cookies={
            "__ac_nonce": "063abcffa00ed8507d599"  # 可以是任意值
        }
    )
    data_string = re.findall(r'<script id="RENDER_DATA" type="application/json">(.*?)</script>', res.text)[0]
    data_dict = json.loads(unquote_plus(data_string))

    room_id = data_dict['app']['initialState']['roomStore']['roomInfo']['roomId']
    room_title = data_dict['app']['initialState']['roomStore']['roomInfo']["room"]['title']
    room_user_count = data_dict['app']['initialState']['roomStore']['roomInfo']["room"]['user_count_str']

    # print(room_id)
    wss_url = f"wss://webcast3-ws-web-lq.douyin.com/webcast/im/push/v2/?app_name=douyin_web&version_code=180800&webcast_sdk_version=1.3.0&update_version_code=1.3.0&compress=gzip&internal_ext=internal_src:dim|wss_push_room_id:7204471273437760314|wss_push_did:7140459943756301854|dim_log_id:202302262321404283BF425CD3004243D4|fetch_time:1677424900407|seq:1|wss_info:0-1677424900407-0-0|wrds_kvs:RoomLinkMicSyncData-1677424899240771392_WebcastRoomStatsMessage-1677424900157809312_InputPanelComponentSyncData-1677423998211004512_RoomLinkMicAnchorSettingsSyncData-1677424182191971552_WebcastRoomRankMessage-1677424870201661066&cursor=r-1_d-1_u-1_h-1_t-1677424900407&host=https://live.douyin.com&aid=6383&live_id=1&did_rule=3&debug=false&endpoint=live_pc&support_wrds=1&im_path=/webcast/im/fetch/&user_unique_id=7140459943756301854&device_platform=web&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Mozilla&browser_version=5.0%20(Macintosh;%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/110.0.0.0%20Safari/537.36&browser_online=true&tz_name=Asia/Shanghai&identity=audience&room_id={room_id}&heartbeatDuration=0&signature=RZal/L9xj457uiOG"

    ttwid = res.cookies.get_dict()['ttwid']
    return room_id, room_title, room_user_count, wss_url, ttwid

def save_data_to_db(message):
    global live_id
    try:
        sql = f"insert into t_danmu(roomId,shortId,nickName,gender,content,createTime) values (%s,%s,%s,%s,%s,%s)"
        # 运行sql语句
        cursor.execute(sql, (live_id, message.user.shortId, message.user.nickName, message.user.gender, message.content, datetime.datetime.now()))
        # 修改
        db.commit()
        info = f"{datetime.datetime.now()}【{message.user.nickName}】:{message.content} "
        print(info)
    except Exception as e:
        print("数据存储错误", message.user.nickName, e)

def on_open(ws):
    print('on_open')


def on_message(ws, content):
    frame = PushFrame()
    frame.ParseFromString(content)

    # 对PushFrame的 payload 内容进行gzip解压
    origin_bytes = gzip.decompress(frame.payload)

    # 根据Response+gzip解压数据，生成数据对象
    response = Response()
    response.ParseFromString(origin_bytes)

    if response.needAck:
        s = PushFrame()
        s.payloadType = "ack"
        s.payload = response.internalExt.encode('utf-8')
        s.logId = frame.logId

        ws.send(s.SerializeToString())

    # 获取数据内容（需根据不同method，使用不同的结构对象对 数据 进行解析）
    #   注意：此处只处理 WebcastChatMessage ，其他处理方式都是类似的。
    for item in response.messagesList:
        if item.method != "WebcastChatMessage":
            continue

        message = ChatMessage()
        message.ParseFromString(item.payload)
        if message.content == "":
            continue
        if message.user.gender == None:
            message.user.gender = 0

        save_data_to_db(message)


def on_error(ws, content):
    print(content)
    print("on_error")


def on_close(*args, **kwargs):
    print(args, kwargs)
    print("on_close")


def run():
    web_url = "https://live.douyin.com/" + live_id
    room_id, room_title, room_user_count, wss_url, ttwid = fetch_live_room_info(web_url)
    print(room_id, room_title, room_user_count, wss_url, ttwid)

    ws = WebSocketApp(
        url=wss_url,
        header={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        },
        cookie=f"ttwid={ttwid}",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever()


if __name__ == '__main__':
    run()
