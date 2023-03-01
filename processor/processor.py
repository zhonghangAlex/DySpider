import wordcloud
import jieba
import pymysql
import collections
import re
import numpy as np
import matplotlib.pyplot as plt
from settings import db_conf, process_conf

# 数据库连接
db = pymysql.connect(host=db_conf["host"], port=db_conf["port"], user=db_conf["user"], password=db_conf["password"], db=db_conf["db"], charset=db_conf["charset"])
cursor = db.cursor()
print("数据库连接成功！")

# 绘图字体设置解决乱码问题
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 分词并且生成词云及词频统计相关图
def get_wordcloud():
    print('正在进行分词处理，生成词云，构造可视化数据模型')
    # 读取预处理数据
    room_id = process_conf["frequency"]["room_id"]
    room_name = process_conf["frequency"]["room_name"]
    start_time = process_conf["frequency"]["start_time"]
    end_time = process_conf["frequency"]["end_time"]
    text = get_content_text(room_id=room_id, room_name=room_name, start_time=start_time, end_time=end_time)

    # 设定词云剔除词组
    stopwords_list = ["捂脸", "比心", "鼓掌"]

    # 中文分词
    words = list(jieba.lcut(text, cut_all=False))
    words_list = []
    cuted = ' '.join(words) # 统计图使用words_list，词云使用cuted

    # 词频统计
    for item in list(words):
        if (item in stopwords_list) or (len(item) == 1)  or item.isdigit():
            continue
        words_list.append(item)

    word_counts = collections.Counter(words_list)  # 对分词做词频统计
    word_counts_top30 = word_counts.most_common(30)  # 获取前10最高频的词

    words_map = {key: value for (key, value) in word_counts_top30}

    # 生成频数条形统计图
    plt.figure(figsize=(20, 12), dpi=100) # 设置画布大小
    ys = list(words_map.values()) # 设置横纵轴数据
    xs = list(words_map.keys())

    # 将数据存储书到本地json文件中
    jsonData = {
        "roomId": room_id,
        "roomName": room_name,
        "startTime": start_time,
        "endTime": end_time,
        "xs": xs,
        "ys": ys
    }
    jsonflie = 'frequencyData.js'
    path = 'data/'
    with open(path + jsonflie, 'w' , encoding='utf-8') as f_obj:
        f_obj.write('var freDataImport = ' + str(jsonData))

    colors = ['dodgerblue' for i in range(30) ] # 设置柱状色值
    colors[0] = 'lightcoral'
    colors[1] = 'lightcoral'
    colors[2] = 'lightcoral'

    bar_result = plt.bar(xs, ys, color= colors)
    auto_text(bar_result)

    # 标题设置
    plt.ylabel('出现次数', fontsize=20, labelpad=5)
    plt.xlabel('关键词', fontsize=20, labelpad=5)
    plt.title('直播营销弹幕词频统计', fontsize=25)
    plt.tick_params(labelsize=18)
    plt.savefig('data/dy_frequency')

    # 生产频数统计雷达图
    N = len(bar_result) # 确定角度
    theta = np.arange(0.0, 2 * np.pi, 2 * np.pi / N)

    width = np.pi / 12 # 条形的宽度

    ax = plt.subplot(121, projection='polar')
    bars = ax.bar(theta, ys, width=width, bottom=0.0)
    # plt.xticks(theta + np.pi / 20, xs) # 柱形贴边
    plt.xticks(theta, xs) # 柱形沿线居中

    for r, bar in zip(ys, bars): # 颜色设置
        bar.set_facecolor(plt.cm.viridis(r / 30.))
        bar.set_alpha(0.5)

    plt.title('直播营销弹幕词频统计', fontsize=25)
    plt.tick_params(labelsize=18)
    plt.savefig('data/dy_radar')

    # 生成词云
    w = wordcloud.WordCloud(
        font_path="msyh.ttc" ,
        width=900,
        height=500,
        margin=2,
        stopwords= stopwords_list,
        background_color="white",
        collocations=False,
    )
    w.generate(cuted)
    w.to_file("data/dy_cloud.png")

    # plt.imshow(w)
    # plt.axis("off")
    # plt.show()

# 按照参数取出预处理数据
def get_content_text(room_id="80017709309", room_name="东方甄选", start_time="2023-01-01 00:00:00", end_time="2050-12-31 00:00:00"):
    all_text = []

    get_sql = """
        SELECT content FROM t_danmu
        WHERE createTime <= '{0}' AND createTime >= '{1}' AND roomId = '{2}'
        GROUP BY content
    """.format(end_time, start_time, room_id)

    result = cursor.execute(get_sql)
    for content_info in cursor.fetchall():
        all_text.append(content_info[0])

    return ','.join(all_text)

# 工具函数
# 1.取出中文字符
def getZh(str):
    line = str.strip()  # 处理前进行相关的处理，包括转换成Unicode等
    pattern = re.compile('[^\u4e00-\u9fa50-9]')  # 中文的编码范围是：\u4e00到\u9fa5
    zh = " ".join(pattern.split(line)).strip()
    # zh = ",".join(zh.split())
    outStr = zh  # 经过相关处理后得到中文的文本
    return outStr

# 2.为柱状图添加数值
def auto_text(rects):
    for rect in rects:
        plt.text(rect.get_x()+ 0.1, rect.get_height(), rect.get_height(), ha='left', va='bottom', fontdict={
            'family': 'serif',
            'color':  'black',
            'weight': 'bold',
            'size': 16,
        })

if __name__ == "__main__":
    get_wordcloud()