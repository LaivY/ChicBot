import json
import requests
from datetime import datetime

from setting import setting

apikey = setting['DNF_API_KEY']

# DnF Server
SERVER_NAME_TO_ID = {
    '안톤': 'anton',
    '바칼': 'bakal',
    '카인': 'cain',
    '카시야스': 'casillas',
    '디레지에': 'diregie',
    '힐더': 'hilder',
    '프레이': 'prey',
    '시로코': 'siroco',
    '전체': 'all'
}


def searchItem(itemName, wordType='full', itemType=None):
    url = 'https://api.neople.co.kr/df/items'
    params = {
        'limit': 30,
        'itemName': itemName,
        'wordType': wordType,
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    itemsInfo = response.json()

    result = []
    for i in itemsInfo['rows']:
        # 아이템 이름에 [영혼], [결투장] 이 들어가는 것은 패스
        if ('[영혼]' in i['itemName']) or ('[결투장]' in i['itemName']): continue

        # 해당하는 아이템 타입이 아닌 경우 패스
        if itemType is not None and itemType != i['itemType']: continue

        # 이름이 중복된 아이템이 있을경우 패스
        isOverride = False
        for j in result:
            if i['itemName'] == j['itemName']:
                isOverride = True
                break
        if isOverride: continue

        # 무기, 방어구, 액세서리, 추가장비, 레전더리, 에픽, 신화 아이템만 검색
        if (i['itemType'] in ['무기', '방어구', '액세서리', '추가장비']) and (i['itemRarity'] in ['레전더리', '에픽', '신화']):
            result.append(i)

    return result


def getItemImageUrl(itemId):
    return f"https://img-api.neople.co.kr/df/items/{itemId}"


def getChrImageUrl(server, chrId):
    return f"https://img-api.neople.co.kr/df/servers/{SERVER_NAME_TO_ID[server]}/characters/{chrId}"


def getSimilarItemInfo(itemName):
    url = 'https://api.neople.co.kr/df/items'
    params = {
        'limit': 1,
        'itemName': itemName,
        'wordType': 'front',
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    result = response.json()

    if not result['rows']:
        return None
    else:
        return result['rows'][0]


def getItemDetailInfo(itemId):
    url = f"https://api.neople.co.kr/df/items/{itemId}"
    params = {
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    return response.json()


def getItemsDetail(itemIds):
    url = 'https://api.neople.co.kr/df/multi/items'
    params = {
        'itemIds': itemIds,
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    data = json.loads(response.text)
    return data['rows']


def getItemStatInfo(itemStatus):
    itemStatInfo = ''
    for i in itemStatus:
        if i['name'] in ['무게', '내구도']: continue
        itemStatInfo += i['name'] + ' : ' + str(i['value']) + '\r\n'
    return itemStatInfo


def getItemSkillLvInfo(jobName, levelRange):
    itemSkillInfo = ''
    if jobName == '공통':
        itemSkillInfo += '모든 직업 '
    else:
        itemSkillInfo += jobName

    for i in levelRange:
        if i['minLevel'] == i['maxLevel']:
            itemSkillInfo += str(i['minLevel']) + '레벨 모든 스킬 Lv+' + str(i['value']) + '\r\n'
        else:
            itemSkillInfo += str(i['minLevel']) + '~' + str(i['maxLevel']) + '레벨 모든 스킬 Lv+' + str(i['value']) + '\r\n'
    return itemSkillInfo


def getItemMythicInfo(options, buff=False):
    itemMythicInfo = ''
    for i in options:
        if buff:
            itemMythicInfo += i['buffExplainDetail'] + '\r\n'
        else:
            itemMythicInfo += i['explainDetail'] + '\r\n'
    return itemMythicInfo


def getItemAuction(itemName):
    url = 'https://api.neople.co.kr/df/auction-sold'
    params = {
        'limit': 100,
        'itemName': itemName,
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    data = json.loads(response.text)
    return data['rows']


def get_shop_item_info(itemId):
    url = 'https://api.neople.co.kr/df/items/' + itemId + '/shop?apikey=' + apikey
    response = requests.get(url=url)
    return json.loads(response.text)


def searchSetItem(setItemName):
    url = 'https://api.neople.co.kr/df/setitems'
    params = {
        'setItemName': setItemName,
        'limit': 30,
        'wordType': 'full',
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    data = json.loads(response.text)
    return data['rows']


def getSetItemInfo(setItemId):
    url = f"https://api.neople.co.kr/df/setitems/{setItemId}"
    params = {
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    return json.loads(response.text)


def getSetItemsInfo(setItemIds):
    url = 'https://api.neople.co.kr/df/multi/setitems?setItemIds=' + setItemIds + '&apikey=' + apikey
    response = requests.get(url=url)
    data = json.loads(response.text)
    return data['rows']


def get_character_info(server, name):
    url = f"https://api.neople.co.kr/df/servers/{SERVER_NAME_TO_ID[server]}/characters"
    params = {
        'characterName': name,
        'jobId': None,
        'jobGrowId': None,
        'wordType': 'match' if len(name) == 1 else 'full',
        'limit': 15,
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)

    SERVER_ID_TO_NAME = {
        'anton': '안톤',
        'bakal': '바칼',
        'cain': '카인',
        'casillas': '카시야스',
        'diregie': '디레지에',
        'hilder': '힐더',
        'prey': '프레이',
        'siroco': '시로코'
    }

    result = []
    for i in response.json()['rows']:
        i['serverId'] = SERVER_ID_TO_NAME[i['serverId']]
        result.append(i)
    return result


def get_character_equipment(server: str, chrId: str):
    url = f"https://api.neople.co.kr/df/servers/{SERVER_NAME_TO_ID[server]}/characters/{chrId}/equip/equipment"
    params = {
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    return response.json()


def getEquipActiveSet(itemIds):
    url = 'https://api.neople.co.kr/df/custom/equipment/setitems?itemIds=' + itemIds + '&apikey=' + apikey
    response = requests.get(url=url)
    return json.loads(response.text)


def getChrEquipCreature(server, chrId):
    url = 'https://api.neople.co.kr/df/servers/' + SERVER_NAME_TO_ID[
        server] + '/characters/' + chrId + '/equip/creature?apikey=' + apikey
    response = requests.get(url=url)
    return json.loads(response.text)


def getChrBuffCreature(server, chrId):
    url = f'https://api.neople.co.kr/df/servers/{SERVER_NAME_TO_ID[server]}/characters/{chrId}/skill/buff/equip/creature?apikey={apikey}'
    res = requests.get(url=url)
    return json.loads(res.text)


def getChrBuffEquip(server, chrId):
    url = 'https://api.neople.co.kr/df/servers/' + SERVER_NAME_TO_ID[
        server] + '/characters/' + chrId + '/skill/buff/equip/equipment?apikey=' + apikey
    response = requests.get(url=url)
    return json.loads(response.text)


def get_character_status(server, chrId):
    url = f"https://api.neople.co.kr/df/servers/{SERVER_NAME_TO_ID[server]}/characters/{chrId}/status"
    params = {
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    return json.loads(response.text)


def getChrTimeLine(server, chrId, *codes):
    today = datetime.today()
    startDate = f"{today.year}-{today.month}-01 00:00"
    endDate = f"{today.year}-{today.month}-{today.day} {today.hour}:{today.minute}"

    result = []

    url = f"https://api.neople.co.kr/df/servers/{SERVER_NAME_TO_ID[server]}/characters/{chrId}/timeline"
    params = {
        'startDate': startDate,
        'endDate': endDate,
        'limit': 100,
        'code': ','.join(codes),
        'apikey': apikey
    }

    response = requests.get(url=url, params=params)
    timeline = response.json()
    result += timeline['timeline']['rows']

    while timeline['timeline']['next'] is not None:
        params['next'] = timeline['timeline']['next']
        response = requests.get(url=url, params=params)
        timeline = response.json()
        result += timeline['timeline']['rows']

    return result


def getChrSkillStyle(server, chrId):
    url = 'https://api.neople.co.kr/df/servers/' + SERVER_NAME_TO_ID[
        server] + '/characters/' + chrId + '/skill/style?apikey=' + apikey
    response = requests.get(url=url)
    return json.loads(response.text)


def get_character_avatar(server, chrId):
    url = f"https://api.neople.co.kr/df/servers/{SERVER_NAME_TO_ID[server]}/characters/{chrId}/equip/avatar"
    params = {
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    return json.loads(response.text)


def getChrBuffAvatar(server, chrId):
    url = f'https://api.neople.co.kr/df/servers/{SERVER_NAME_TO_ID[server]}/characters/{chrId}/skill/buff/equip/avatar?apikey={apikey}'
    response = requests.get(url=url)
    return json.loads(response.text)


def getSkillDetailInfo(jobId, skillId):
    url = 'https://api.neople.co.kr/df/skills/' + jobId + '/' + skillId + '?apikey=' + apikey
    response = requests.get(url=url)
    return json.loads(response.text)


def getSkillInfo(jobId, skillId):
    url = 'https://api.neople.co.kr/df/skills/' + jobId + '/' + skillId + '?apikey=' + apikey
    response = requests.get(url=url)
    return json.loads(response.text)
