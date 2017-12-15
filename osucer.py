import requests
import re
import pymysql
from detailpp import *
import traceback

s = requests.Session()

#阈值
high=600

#页数
page=20

#获取用户名
def getUserName(uid):
    userurl = 'https://osu.ppy.sh/u/' + str(uid)
    data = s.get(userurl).content
    user = data.decode('utf-8')
    userlist = re.compile('<title>(.*?)\'s profile', re.S)
    return re.findall(userlist, user)[0]

#获取用户top ranks信息
def getUserTopRanks(uid):
    try:
        userurl='https://osu.ppy.sh/pages/include/profile-leader.php?u='+str(uid)+'&m=0'
        data = s.get(userurl).content
        userranks1 = data.decode('utf-8')
        findHighPPs(userranks1, uid)
        userurl+='&pp=1'
        data = s.get(userurl).content
        userranks2 = data.decode('utf-8')
        findHighPPs(userranks2, uid)
    except:
        getUserTopRanks(uid)

#找到高于某值的地图
def findHighPPs(info, uid):
    #pp
    pplist = re.compile('<b>(.*?)pp</b>')
    pps = re.findall(pplist, info)
    #地图id
    bidlist = re.compile('href="/b/(.*?)\?m=0">', re.S)
    bids = re.findall(bidlist, info)
    #地图信息
    maplist = re.compile('href="/b/.*?>(.*?)<div class="c">', re.S)
    maps = re.findall(maplist, info)
    newmaps=[]
    #地图字符串处理
    for map in maps:
        map=map[:-8]
        map=map.replace('</a>','')
        map=map.replace('</b>', '')
        map = map.replace('&#039;', '\'')
        map = map.replace('&amp;', '&')
        map = map.replace('&quot;', '"')
        newmaps.append(map)
    user=getUserName(uid)
    for i in range(len(pps)):
        if int(pps[i])>=high:
            print(getDetail(uid, s, int(bids[i]), int(pps[i])))
            writetoDB(int(bids[i]),uid,user,getDetail(uid, s, int(bids[i]), int(pps[i])),newmaps[i])

#写入数据库
def writetoDB(bid, uid, user, pp, map):
    try:
        db = pymysql.connect("138.68.57.30", "root", "1248163264128", "osu")
        cursor = db.cursor()
        sql = """INSERT INTO osu_High_pps
              (bid, uid, user, pp, map_info)
              VALUES ("%d", "%d", "%s" ,"%s", "%s") on duplicate key update user="%s", pp="%s", map_info="%s" """ % (bid, uid, user, pp, map, user, pp, map)
        cursor.execute(sql)
        db.commit()
        db.close()
    except:
        traceback.print_exc()

#获得排行榜
def getRanks(page):
    userurl = 'https://osu.ppy.sh/p/pp/?m=0&s=3&o=1&f=0&page='+str(page)
    data = s.get(userurl).content
    ranks = data.decode('utf-8')
    uidlist = re.compile('href=\'/u/(.*?)\'>')
    uids = re.findall(uidlist, ranks)
    for uid in uids:
        print(uid)
        getUserTopRanks(int(uid))


def getAll():
    for i in range(page):
        getRanks(i+1)

if __name__=="__main__":
    getAll()
    print('finished')