import json

def getDetail(uid, s, bid, pp):
    ppurl = "https://osu.ppy.sh/api/get_user_best?k=41b91bdb921841db7e56ddb23b2142998eaee76e&u=" + str(uid) + "&limit=100"

    data = s.get(ppurl).content
    ddata = data.decode('utf-8')
    jdata=json.loads(ddata)
    for map in jdata:
        if int(map['beatmap_id'])==bid:
            if round(float(map['pp']))==pp:
                return float(map['pp'])
    return 0