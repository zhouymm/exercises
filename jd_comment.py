import requests
import json
import xlrd
import pymysql

# db = pymysql.connect("rm-bp1wlg5jh7jb42c29o.mysql.rds.aliyuncs.com", "quality", "quality@302", "quality-site-19", charset='utf8')
# cursor = db.cursor()

s = requests.session()
params = {
    "productId": "2794498",
    "score": 0,
    "sortType": 6,
    "page": 0,
    "pageSize": 10,
    "isShadowSku": 0,
    # "rid": 0,
    # "fold": 1
}
headers = {
    "referer": "https://item.jd.com/2794498.html",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"

}
data = xlrd.open_workbook(u"D:\study\京东-商品搜索-建议本地采集.xlsx")
table = data.sheets()[0]
file = open('comment.txt', 'a+', encoding='utf-8')
for i in range(165, 5940):
    url = table.cell(i+1, 2).value
    headers['referer'] = "https://item.jd.com/" + url + ".html"
    params['productId'] = url
    for j in range(100):
        params['page'] = j
        r = s.get('https://sclub.jd.com/comment/productPageComments.action', params=params, headers=headers)
        # r.encoding = 'gbk'
# r = s.get('https://club.jd.com/discussion/getProductPageImageCommentList.action?', params=params, headers=headers)
        # print(r.text)
        # print(r.text)
        try:
            product_json = json.loads(r.text)
        except Exception as e:
            print('error', i, j)
            continue
# print(product_json[key])
        if len(product_json['comments']) == 0:
            break
        for comment in product_json['comments']:
            content = comment['content'].replace(' ', '').replace('\n', '')
            nick_name = comment['nickname']
            source_link = headers['referer']
            create_time = comment['creationTime']
            product_name = comment['referenceName'].replace(' ', '').replace('\n', '')
            # print(nick_name, source_link, content, create_time, product_name)
            file.write(content + ' ' + nick_name + ' ' + create_time + ' ' + source_link + ' ' + product_name + '\n')
    print(i, 'success')
        # sql = "insert into news_storehouse (source_link, content, title, create_date, author, source_name) values ('%s', " \
        #       "'%s', '%s', '%s', '%s', '%s')" % (source_link, pymysql.escape_string(summary), pymysql.escape_string(title), create_date, author, source_name)
        # try:
        #     cursor.execute(sql)
        #     db.commit()
        # except Exception as e:
        #     print(e)
        #     db.rollback()
        #     print(i + 1, j, source_link, "error!")
        #     continue