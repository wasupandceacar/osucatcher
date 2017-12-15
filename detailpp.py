import json

def getDetail(uid, s, bid, pp):
    ppurl = "https://osu.ppy.sh/api/get_user_best?k=cff10afa31a4a9cd85aa7bc433c20c862562ed51&u=" + str(uid) + "&limit=100"

    data = s.get(ppurl).content
    ddata = data.decode('utf-8')
    jdata=json.loads(ddata)
    for map in jdata:
        if int(map['beatmap_id'])==bid:
            if round(float(map['pp'])+0.0001)==pp:
                return float(map['pp'])
    return 0