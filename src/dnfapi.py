import json
import requests
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


def get_item_info(item_name: str) -> list:
    url = 'https://api.neople.co.kr/df/items'
    params = {
        'limit': 3,
        'itemName': item_name,
        'wordType': 'full',
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    result = response.json()
    return result['rows']


def get_equip_item_info(item_name: str) -> list:
    url = 'https://api.neople.co.kr/df/items'
    params = {
        'limit': 6,
        'itemName': item_name,
        'wordType': 'full',
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    item_info = response.json()

    result = []
    for row in item_info['rows']:
        # 아이템 이름에 [영혼], [결투장] 이 들어가는 것은 패스
        if ('[영혼]' in row['itemName']) or ('[결투장]' in row['itemName']):
            continue

        # 이름이 중복된 아이템이 있을경우 패스
        is_duplicated = False
        for j in result:
            if row['itemName'] == j['itemName']:
                is_duplicated = True
                break
        if is_duplicated: continue

        # 무기, 방어구, 액세서리, 추가장비, 레전더리, 에픽, 신화 아이템만 검색
        if (row['itemType'] in ['무기', '방어구', '액세서리', '추가장비']) and \
           (row['itemRarity'] in ['레전더리', '에픽', '신화']):
            result.append(row)

    return result


def get_item_detail_info(item_id: str) -> dict:
    url = f"https://api.neople.co.kr/df/items/{item_id}"
    params = {
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    return response.json()


def get_item_image_url(item_id: str) -> str:
    return f"https://img-api.neople.co.kr/df/items/{item_id}"


def get_character_image_url(server_name: str, character_id: str) -> str:
    return f"https://img-api.neople.co.kr/df/servers/{SERVER_NAME_TO_ID[server_name]}/characters/{character_id}"


def get_auction_item_sold_info(item_name: str) -> list:
    url = 'https://api.neople.co.kr/df/auction-sold'
    params = {
        'limit': 100,
        'itemName': item_name,
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    data = json.loads(response.text)
    return data['rows']


def get_shop_item_info(item_id: str) -> dict:
    url = f"https://api.neople.co.kr/df/items/{item_id}/shop"
    params = {
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    return json.loads(response.text)


def get_set_item_info(set_item_name: str) -> list:
    url = 'https://api.neople.co.kr/df/setitems'
    params = {
        'setItemName': set_item_name,
        'limit': 6,
        'wordType': 'full',
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    data = json.loads(response.text)
    return data['rows']


def get_set_item_detail_info(set_item_id: str) -> dict:
    url = f"https://api.neople.co.kr/df/setitems/{set_item_id}"
    params = {
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    return json.loads(response.text)


def get_character_info(server_name: str, character_name: str) -> list:
    url = f"https://api.neople.co.kr/df/servers/{SERVER_NAME_TO_ID[server_name]}/characters"
    params = {
        'characterName': character_name,
        'jobId': None,
        'jobGrowId': None,
        'wordType': 'match' if len(character_name) == 1 else 'full',
        'limit': 6,
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
    for row in response.json()['rows']:
        row['serverId'] = SERVER_ID_TO_NAME[row['serverId']]
        result.append(row)
    return result


def get_character_equipment_info(server_name: str, character_id: str) -> dict:
    url = f"https://api.neople.co.kr/df/servers/{SERVER_NAME_TO_ID[server_name]}/characters/{character_id}/equip/equipment"
    params = {
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    return response.json()


def get_character_status_info(server_name: str, character_id: str) -> dict:
    url = f"https://api.neople.co.kr/df/servers/{SERVER_NAME_TO_ID[server_name]}/characters/{character_id}/status"
    params = {
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    return json.loads(response.text)


def get_character_avatar_info(server_name: str, character_id: str) -> dict:
    url = f"https://api.neople.co.kr/df/servers/{SERVER_NAME_TO_ID[server_name]}/characters/{character_id}/equip/avatar"
    params = {
        'apikey': apikey
    }
    response = requests.get(url=url, params=params)
    return json.loads(response.text)


# ---------------------

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