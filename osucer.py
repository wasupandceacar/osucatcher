import requests
import re
import pymysql

s = requests.Session()

#阈值
high=300

#获取用户名
def getUserName(uid):
    userurl = 'https://osu.ppy.sh/u/' + str(uid)
    data = s.get(userurl).content
    user = data.decode('utf-8')
    userlist = re.compile('<title>(.*?)\'s profile', re.S)
    return re.findall(userlist, user)[0]

#获取用户top ranks信息
def getUserTopRanks(uid):
    userurl='https://osu.ppy.sh/pages/include/profile-leader.php?u='+str(uid)+'&m=0'
    data = s.get(userurl).content
    userranks1 = data.decode('utf-8')
    findHighPPs(userranks1, uid)
    userurl+='&pp=1'
    data = s.get(userurl).content
    userranks2 = data.decode('utf-8')
    findHighPPs(userranks2, uid)

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
            writetoDB(int(bids[i]),uid,user,int(pps[i]),newmaps[i])

#写入数据库
def writetoDB(bid, uid, user, pp, map):
    db = pymysql.connect("138.68.41.21", "root", "1248163264128", "osu")
    cursor = db.cursor()
    sql = """INSERT INTO osu_High_pps
              (bid, uid, user, pp, map_info)
              VALUES ("%d", "%d", "%s" ,"%d", "%s")""" % (bid, uid, user, pp, map)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

if __name__=="__main__":
    getUserTopRanks(3863328)