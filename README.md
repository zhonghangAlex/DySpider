# 一、Protobuf

![image-20221228183821128](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228183821128.png)



protobuf是Google公司提出的一种轻便**高效**的结构化数据存储**格式**，常用于结构化数据的序列化，具有语言无关、平台无关、可扩展性特性，常用于通讯协议、服务端数据交换场景。

# 1.下载安装

## 1.1 Windows

https://github.com/protocolbuffers/protobuf/releases

![image-20221228151056342](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228151056342.png)

![image-20221228152014152](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228152014152.png)

![image-20221228152019324](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228152019324.png)

![image-20221228184136129](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228184136129.png)

## 1.2 Mac

```
brew install protobuf@3
```

如果电脑未安装brew，则请先去安装：

```
>>>/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
>>>brew --version
```

![image-20221227174851108](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221227174851108.png)

![image-20221227174933342](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221227174933342.png)

将目录加入环境变量：

```
PATH="/usr/local/opt/protobuf@3.20/bin:${PATH}"
export PATH
```

![image-20221227175050770](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221227175050770.png)

# 2.Pycharm插件

![image-20221227175241772](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221227175241772.png)

# 3.定义数据结构

官方文档：https://developers.google.com/protocol-buffers/docs/pythontutorial

```protobuf
syntax = "proto3";

package wupeiqi;

message Person {
    string name = 1;
    int32 age = 2;
}

message Info {
    string method = 1;
    string payload = 2;
}
```

![image-20221227175627234](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221227175627234.png)

# 6.转换Python版本

在命令行执行：

```
protoc  --python_out=.   v1.proto
```

![image-20221227175742749](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221227175742749.png)

# 7.Python操作模块

```
pip install protobuf
```

![image-20221227181740218](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221227181740218.png)

```python
from google.protobuf import json_format

# 1.创建对象转换成字节，用于后续网络传输（序列化）
from v1_pb2 import Person, Message

p1 = Person()
p1.name = "微信：wupeiqi666"
p1.age = 19

info = p1.SerializeToString()
print(info)

p2 = Message()
p2.method = "POST"
p2.payload = "太NB了"
info = p2.SerializeToString()
print(info)

# 2.根据字节转化对象，用于业务处理（反序列化）
obj = Message()
obj.ParseFromString(info)
print(obj.method)
print(obj.payload)


# 3.对象转字典
from google.protobuf import json_format

data_dict = json_format.MessageToDict(obj)
print(data_dict, type(data_dict))

data_string = json_format.MessageToJson(obj,ensure_ascii=False)
print(data_string, type(data_string))
```

# 二、抖音协议结构

# 1.搜索

搜索：new websocket

![image-20221228003903017](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228003903017.png)





![image-20221228003944766](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228003944766.png)





![image-20221228004047812](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228004047812.png)







# 2.PushFrame

![image-20221228004303121](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228004303121.png)



![image-20221228003747727](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228003747727.png)

![image-20221228004636413](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228004636413.png)

![image-20221228004731796](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228004731796.png)



```protobuf
message HeadersList {
  string key = 1;
  string value = 2;
}

message PushFrame {
  uint64 seqid = 1;
  uint64 logid = 2;
  uint64 service = 3;
  uint64 method = 4;
  repeated HeadersList headersList = 5;
  string payloadEncoding = 6;
  string payloadType = 7;
  bytes payload = 8;  // 内部数据
}
```



# 3.Response

![image-20221228005122751](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228005122751.png)

![image-20221228005146495](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228005146495.png)



![image-20221228005748088](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228005748088.png)





```protobuf
message Message{
    string method = 1;
    bytes payload = 2;
    int64 msgId = 3;
    int32 msgType = 4;
    int64 offset = 5;
    bool needWrdsStore = 6;
    int64 wrdsVersion = 7;
    string wrdsSubKey = 8;
}

message Response {
  repeated Message messagesList = 1;
  string cursor = 2;
  uint64 fetchInterval = 3;
  uint64 now = 4;
  string internalExt = 5;
  uint32 fetchType = 6;
  map<string, string> routeParams = 7;
  uint64 heartbeatDuration = 8;
  bool needAck = 9;
  string pushServer = 10;
  string liveCursor = 11;
  bool historyNoMore = 12;
}
```



# 4.消息处理

![image-20221228005610548](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228005610548.png)

![image-20221228005657416](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228005657416.png)

![image-20221228010034016](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228010034016.png)

![image-20221228010527876](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228010527876.png)



![image-20221228010558160](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228010558160.png)



## 4.1 MemberMessage

![image-20221228010629162](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228010629162.png)



## 4.2 ChatMessage

![image-20221228010805757](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228010805757.png)

![image-20221228010843698](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228010843698.png)

![image-20221228010928343](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228010928343.png)



# 5.ACK心跳

![image-20221228011354423](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228011354423.png)







payload是什么？

![image-20221228011639242](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228011639242.png)

![image-20221228012104999](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228012104999.png)

```javascript
function getPayLoad(e) {
    const t = [];
    for (const o of e) {
        const e = o.charCodeAt(0);
        e < 128 ? t.push(e) : e < 2048 ? (t.push(192 + (e >> 6)),
            t.push(128 + (63 & e))) : e < 65536 && (t.push(224 + (e >> 12)),
            t.push(128 + (e >> 6 & 63)),
            t.push(128 + (63 & e)))
    }
    return Uint8Array.from(t)
}

const arg = "internal_src:pushserver|wss_push_room_id:7181868093256338235|wss_push_did:7181865126873220619|wss_push_log_id:8166207734905913069|wss_fetch_ms:1672159517145|wss_push_ms:1672159517209|wss_msg_type:r|wrds_kvs:RoomLinkMicAnchorSettingsSyncData-1672159139787371174_RoomLinkMicSyncData-1672159515222677464_WebcastRoomRankMessage-1672159367938299538_WebcastRoomStatsMessage-1672159511846110620"
const payload = getPayLoad(arg);
console.log(payload);
```



![image-20221228185720913](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228185720913.png)

![image-20221228185745862](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228185745862.png)







# 6.结构示例（简化）

```protobuf
syntax = "proto3";

package douyin;

message HeadersList {
    string key = 1;
    string value = 2;
}

message PushFrame {
    uint64 seqId = 1;
    uint64 logId = 2;
    uint64 service = 3;
    uint64 method = 4;
    repeated HeadersList headersList = 5;
    string payloadEncoding = 6;
    string payloadType = 7;
    bytes payload = 8;
}


message Message {
    string method = 1;
    bytes payload = 2;
    int64 msgId = 3;
    int32 msgType = 4;
    int64 offset = 5;
    bool needWrdsStore = 6;
    int64 wrdsVersion = 7;
    string wrdsSubKey = 8;
}

message Response {
    repeated Message messagesList = 1;
    string cursor = 2;
    uint64 fetchInterval = 3;
    uint64 now = 4;
    string internalExt = 5;
    uint32 fetchType = 6;
    map<string, string> routeParams = 7;
    uint64 heartbeatDuration = 8;
    bool needAck = 9;
    string pushServer = 10;
    string liveCursor = 11;
    bool historyNoMore = 12;
}


message ChatMessage {
    User user = 2;
    string content = 3;
    bool visibleToSender = 4;
}


message User {
    uint64 id = 1;
    uint64 shortId = 2;
    string nickName = 3;
    uint32 gender = 4;
    string Signature = 5;
    uint32 Level = 6;
    uint64 Birthday = 7;
    string Telephone = 8;
    string city = 14;
}

```





# 7.解析抖音数据

```
protoc  --python_out=.  douyin.proto
```

![image-20221228121735913](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228121735913.png)



```python
import gzip
import binascii
from douyin_pb2 import PushFrame, Response, ChatMessage

# WebcastChatMessage
hexStr = "08bf0510e292e6bcb1958e8d7918b84520082a150a0d636f6d70726573735f747970651204677a69702ae2020a0f696d2d696e7465726e616c5f65787412ce02696e7465726e616c5f7372633a707573687365727665727c7773735f707573685f726f6f6d5f69643a373138313832333430383336323031353534307c7773735f707573685f6469643a373134303435393934333735363330313835347c7773735f707573685f6c6f675f69643a383732363334393533353437303235383533307c7773735f66657463685f6d733a313637323135373038313834317c7773735f707573685f6d733a313637323135373038313932307c7773735f6d73675f747970653a727c777264735f6b76733a41756469656e63654769667453796e63446174612d313637323135373037393430393233333936385f57656263617374526f6f6d52616e6b4d6573736167652d313637323135373037373039303839333937345f57656263617374526f6f6d53746174734d6573736167652d313637323135373037373035383332383131312a440a09696d2d637572736f721237742d313637323135373038313932305f722d373138313835393937363636393836353731325f642d315f752d315f682d315f7264632d322a170a06696d2d6e6f77120d313637323135373038313932302a190a0e696d2d6c6976655f637572736f721207642d315f752d31320270623a036d736742de081f8b08000000000000ffe4565d685b551cdf49ba255eb659af0f86f96058df0649ceb9e77e06fc48d30f1bfbb1b5daba821c6fee479236c9bddc7b9336a588b859566bd7e183639b03ad8c49b56c9622b59b43441f36410652f455489ab688b03e8a0fd2366bb611d1aa45d1fb7239e7ff3bbfdff9fffe7f0e7feaf54729ba4f8b2bb2ed4493b2d3a1d9b69cd0e8224d31b502f58b1f2c9d995cff6a49f1cdbf7d62e1c75b9f2d2910bc38b70e3e072b5efabd47bcdf8ddf1ebbfee62550fffd9d93cb3f8343079617e69767af95cf9f5cfdf87ad00f62a3d448d2714c3b1c0a990c1f548d5c219535534a503132217948cb682104e13082706b1590f3b2235b21c7b0034a3620e79d00848823a2a8aa2a62b02a4930ceb02c5445468deb2c94385dd7242538606a89a775cbc83c89212ff002c2989d0123d40b1bf21bea3830b495e00397486512a14a2494b3358b242c59d5485acb6b6992e70862836636f18a63a6f301233e104c65e484e6abf7fb21687cdc77f0f0632b93efafcc8c9767c7cb8b97115b5ebc5c9a98287ff8ee0c3805a8ee9da8eb72d656d2b9f85d6d9e7035a4a1a711520fad4e9f2ddf385d3e3d4e7b1a5a363fdfdec3beedddf2dc7871e162e9c2f4d65de680c77bc2557fc00716c197001e3c0f5eda5563a601a1fa76c2bf597b62ca858a08334c10fc0d85fdfefd107c01bef55045f73d46d4eff581c337ddd41af0d6d12540f5fe45ebc970c6ac215fe5e5ff565ebae10f9ce9de47d5edd9f314dd5ff953df00af8bbeb92b7d56e5fc9389d64af289dfc1d3d57ac29fc65e9d2a4efeb28f5e757b015db3d6ffb5f4ff57cd5babd6afb9f6ccb93ccff7238421bfee123a7ad8a1f6814863241289b4b546f91eb539cd633ddee934a128968ff73101fd98dedb859d967e22c6da638d562ca10e5e75bbd7dcffe0dbbfe6fef7bcfd6bee7776ad9f20def97d1e6c83337560baeefeb9e1565deb56e1bbb826a68b353bd17022ab1e6d563b8eb5750826db36d81b159f8b75377614743dd73b820b46a7291e4f9b9ade251acd4e7b53dbd1f6be162da91cf297cfdd289d1a2b7e3a816069ea4af1daa5f285f9e5b7664b936f94ae4e2d9ffd2416a75ede79a3a4e5b896269696c8a5658b2849d9a9e1ce114f43341ac1113c7ceeca4717f7f9b6a7293ae304102f308813a0884416112b202011899c24093ccf4b22cf098821eae6ae200a10618424816131c42457c1321287788ee3781e319024ef32f01009104b10320c2496aa0418df8ac77fe787dbd34bf0c8d7ae54d6d1acac9c26b6a584cd9c9db4352baf59a343b64d3696c4328c0c49a9e14d3a06b350c43c0311c7b1b00a52536a18b13c2b8918439663b108b96a346d2436184481e1312b71986305c8708284d12646d71c25493276f83e0faac76b463276823805530b5ba343966a93c1bc1d8ee4d4949655b4d694eef414b24a93ecc8dbc60a120b25066389174965b4ed368c4cb79c1dac8cb755a80025284a5812d87ba13d8eecd835b09c88191121f4ccc3cf825f010000ffff010000ffffa1814e1c530b0000"

# 1.将16进制字符串转换为原始字节
body_bytes = binascii.unhexlify(hexStr)

# 2.根据PushFrame结构 + 原始自己，生成数据对象
frame = PushFrame()
frame.ParseFromString(body_bytes)

# 3.对PushFrame的 payload 内容进行gzip解压
origin_bytes = gzip.decompress(frame.payload)

# 4.根据Response+gzip解压数据，生成数据对象
response = Response()
response.ParseFromString(origin_bytes)

# 5.获取数据内容（需根据不同method，使用不同的结构对象对 数据 进行解析）
#   注意：此处只处理 WebcastChatMessage ，其他处理方式都是类似的。

for item in response.messagesList:
    if item.method != "WebcastChatMessage":
        continue

    message = ChatMessage()
    message.ParseFromString(item.payload)
    info = f"【{message.user.nickName}】{message.content}"
    print(info)
```

# 三、WebSocket

# 1.抖音请求分析

如何基于python模拟浏览器中的WebSocket，实现实时获取弹幕信息。

![image-20221228123343183](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228123343183.png)

![image-20221228123900622](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228123900622.png)

```
"wss://webcast3-ws-web-hl.douyin.com/webcast/im/push/v2/?app_name=douyin_web&version_code=180800&webcast_sdk_version=1.3.0&update_version_code=1.3.0&compress=gzip&internal_ext=internal_src:dim|wss_push_room_id:7182033004422777634|wss_push_did:7140459943756301854|dim_log_id:20221228123152F91F995F9399B10A6BCE|fetch_time:1672201912392|seq:1|wss_info:0-1672201912392-0-0|wrds_kvs:HighlightContainerSyncData-26_InputPanelComponentSyncData-1672197463167325819_WebcastRoomStatsMessage-1672201909261979591_WebcastRoomRankMessage-1672201891335849188_AudienceGiftSyncData-1672201860106107162&cursor=r-1_d-1_u-1_h-1_t-1672201912392&host=https://live.douyin.com&aid=6383&live_id=1&did_rule=3&debug=false&endpoint=live_pc&support_wrds=1&im_path=/webcast/im/fetch/&device_platform=web&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Mozilla&browser_version=5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36&browser_online=true&tz_name=Asia/Shanghai&identity=audience&room_id=7182033004422777634&heartbeatDuration=0"
```

![image-20221228124117890](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228124117890.png)

![image-20221228124251422](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228124251422.png)

# 2.ws模块

安装Python模拟发送websocket请求的模块：

```
pip install websocket-client
```



基于 `websocket-client` 的示例代码：

![image-20221228124848517](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228124848517.png)

```python
from websocket import WebSocketApp


def on_open(ws, message):
    pass


def on_message(ws, message):
    pass


def on_error(ws, message):
    pass


def on_close(ws, message):
    pass


def run():
    ws = WebSocketApp(
        url="",
        header={},
        cookie="",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever()


if __name__ == '__main__':
    run()
```

# 3.抖音直播

## 3.1 ws地址

![image-20221228125215663](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228125215663.png)

![image-20221228131211409](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228131211409.png)

![image-20221228131243456](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228131243456.png)

ws的地址中 `room_id` 代表直播间的ID，其他的固定就行，关于 `room_id`的获取

![image-20221228134902618](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228134902618.png)

```python
import json
import re
from urllib.parse import unquote_plus
import requests

res = requests.get(
    url="https://live.douyin.com/80017709309",
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

print(room_title, room_user_count)
print(room_id)
```

所以，wss的最终地址是：

```python
wss_url = f"wss://webcast3-ws-web-lq.douyin.com/webcast/im/push/v2/?app_name=douyin_web&version_code=180800&webcast_sdk_version=1.3.0&update_version_code=1.3.0&compress=gzip&internal_ext=internal_src:dim|wss_push_room_id:{room_id}|wss_push_did:7140459943756301854|dim_log_id:202212281349305A73D850664DB518C21B|fetch_time:1672206570185|seq:1|wss_info:0-1672206570185-0-0|wrds_kvs:WebcastRoomStatsMessage-1672206566915058992_InputPanelComponentSyncData-1672187049066887013_WebcastRoomRankMessage-1672206560973484605&cursor=t-1672206570185_r-1_d-1_u-1_h-1&host=https://live.douyin.com&aid=6383&live_id=1&did_rule=3&debug=false&endpoint=live_pc&support_wrds=1&im_path=/webcast/im/fetch/&device_platform=web&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Mozilla&browser_version=5.0%20(Macintosh;%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/108.0.0.0%20Safari/537.36&browser_online=true&tz_name=Asia/Shanghai&identity=audience&room_id={room_id}&heartbeatDuration=0"
print(wss_url)

```

## 3.2 on_message

在 on_message 中接收直播间的数据。

注意：一会就会自动断开（因为没有心跳）

![image-20221228140500506](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228140500506.png)

```python
from websocket import WebSocketApp
import json
import re
import gzip
from urllib.parse import unquote_plus
import requests
from douyin_pb2 import PushFrame, Response, ChatMessage

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

    wss_url = f"wss://webcast3-ws-web-lq.douyin.com/webcast/im/push/v2/?app_name=douyin_web&version_code=180800&webcast_sdk_version=1.3.0&update_version_code=1.3.0&compress=gzip&internal_ext=internal_src:dim|wss_push_room_id:{room_id}|wss_push_did:7140459943756301854|dim_log_id:202212281349305A73D850664DB518C21B|fetch_time:1672206570185|seq:1|wss_info:0-1672206570185-0-0|wrds_kvs:WebcastRoomStatsMessage-1672206566915058992_InputPanelComponentSyncData-1672187049066887013_WebcastRoomRankMessage-1672206560973484605&cursor=t-1672206570185_r-1_d-1_u-1_h-1&host=https://live.douyin.com&aid=6383&live_id=1&did_rule=3&debug=false&endpoint=live_pc&support_wrds=1&im_path=/webcast/im/fetch/&device_platform=web&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Mozilla&browser_version=5.0%20(Macintosh;%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/108.0.0.0%20Safari/537.36&browser_online=true&tz_name=Asia/Shanghai&identity=audience&room_id={room_id}&heartbeatDuration=0"
    # print(wss_url)

    ttwid = res.cookies.get_dict()['ttwid']
    return room_id, room_title, room_user_count, wss_url, ttwid


def on_open(ws, content):
    print('on_open')


def on_message(ws, content):
    frame = PushFrame()
    frame.ParseFromString(content)

    # 对PushFrame的 payload 内容进行gzip解压
    origin_bytes = gzip.decompress(frame.payload)

    # 根据Response+gzip解压数据，生成数据对象
    response = Response()
    response.ParseFromString(origin_bytes)

    # 获取数据内容（需根据不同method，使用不同的结构对象对 数据 进行解析）
    #   注意：此处只处理 WebcastChatMessage ，其他处理方式都是类似的。
    for item in response.messagesList:
        if item.method != "WebcastChatMessage":
            continue
        message = ChatMessage()
        message.ParseFromString(item.payload)
        info = f"【{message.user.nickName}】{message.content} "
        print(info)


def on_error(ws, content):
    print("on_error")


def on_close(ws, content):
    print("on_close")


def run():
    web_url = "https://live.douyin.com/80017709309"

    room_id, room_title, room_user_count, wss_url, ttwid = fetch_live_room_info(web_url)
    ws = WebSocketApp(
        url=wss_url,
        header={},
        cookie=f"ttwid={ttwid}",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever()


if __name__ == '__main__':
    run()
```

## 3.3 心跳相关


![image-20221228140819325](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228140819325.png)

![image-20221228142352486](https://typora-1256091168.cos.ap-nanjing.myqcloud.com/image-20221228142352486.png)

# 4.最终实现

## 4.1 douyin.proto

```protobuf
syntax = "proto3";

package douyin;

message HeadersList {
    string key = 1;
    string value = 2;
}

message PushFrame {
    uint64 seqId = 1;
    uint64 logId = 2;
    uint64 service = 3;
    uint64 method = 4;
    repeated HeadersList headersList = 5;
    string payloadEncoding = 6;
    string payloadType = 7;
    bytes payload = 8;
}


message Message {
    string method = 1;
    bytes payload = 2;
    int64 msgId = 3;
    int32 msgType = 4;
    int64 offset = 5;
    bool needWrdsStore = 6;
    int64 wrdsVersion = 7;
    string wrdsSubKey = 8;
}

message Response {
    repeated Message messagesList = 1;
    string cursor = 2;
    uint64 fetchInterval = 3;
    uint64 now = 4;
    string internalExt = 5;
    uint32 fetchType = 6;
    map<string, string> routeParams = 7;
    uint64 heartbeatDuration = 8;
    bool needAck = 9;
    string pushServer = 10;
    string liveCursor = 11;
    bool historyNoMore = 12;
}


message ChatMessage {
    User user = 2;
    string content = 3;
    bool visibleToSender = 4;
}


message User {
    uint64 id = 1;
    uint64 shortId = 2;
    string nickName = 3;
    uint32 gender = 4;
    string Signature = 5;
    uint32 Level = 6;
    uint64 Birthday = 7;
    string Telephone = 8;
    string city = 14;
}
```

## 4.2 demo.py

```python
"""
讲师：武沛齐
微信：wupeiqi666
"""
from websocket import WebSocketApp
import json
import re
import gzip
from urllib.parse import unquote_plus
import requests
from douyin_pb2 import PushFrame, Response, ChatMessage


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

    wss_url = f"wss://webcast3-ws-web-lq.douyin.com/webcast/im/push/v2/?app_name=douyin_web&version_code=180800&webcast_sdk_version=1.3.0&update_version_code=1.3.0&compress=gzip&internal_ext=internal_src:dim|wss_push_room_id:{room_id}|wss_push_did:7140459943756301854|dim_log_id:202212281349305A73D850664DB518C21B|fetch_time:1672206570185|seq:1|wss_info:0-1672206570185-0-0|wrds_kvs:WebcastRoomStatsMessage-1672206566915058992_InputPanelComponentSyncData-1672187049066887013_WebcastRoomRankMessage-1672206560973484605&cursor=t-1672206570185_r-1_d-1_u-1_h-1&host=https://live.douyin.com&aid=6383&live_id=1&did_rule=3&debug=false&endpoint=live_pc&support_wrds=1&im_path=/webcast/im/fetch/&device_platform=web&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Mozilla&browser_version=5.0%20(Macintosh;%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/108.0.0.0%20Safari/537.36&browser_online=true&tz_name=Asia/Shanghai&identity=audience&room_id={room_id}&heartbeatDuration=0"
    # print(wss_url)

    ttwid = res.cookies.get_dict()['ttwid']
    return room_id, room_title, room_user_count, wss_url, ttwid


def on_open(ws, content):
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
        info = f"【{message.user.nickName}】{message.content} "
        print(info)


def on_error(ws, content):
    print("on_error")


def on_close(ws, content):
    print("on_close")


def run():
    web_url = "https://live.douyin.com/80017709309"

    room_id, room_title, room_user_count, wss_url, ttwid = fetch_live_room_info(web_url)
    ws = WebSocketApp(
        url=wss_url,
        header={},
        cookie=f"ttwid={ttwid}",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever()


if __name__ == '__main__':
    run()
```

# 四、数据库
先安装包，如spider.py里面的内容一样进行引入
```shell
pip3 install pymysql
```
数据库表文件为t_danmu.sql

# 五、数据分析
processor模块用于数据处理和分析

# 六、服务器部署
```shell
nohup python3 spider.py &
```







































