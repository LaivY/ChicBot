import discord.ext.commands
import dnfapi
import utility
from database import database


async def grade(interaction: discord.Interaction):
    item_max_option = {
        '8e0233bd504efc762b76a476d0e08de4': {
            '물리 방어력': 4475,
            '힘': 57,
            '지능': 37,
            '모든 속성 강화': 22
        },
        '52b3fac226cfa92cba9cffff516fb06e': {
            '물리 방어력': 2983,
            '힘': 47,
            '지능': 47,
            '정신력': 52,
            '모든 속성 강화': 14
        },
        '7fae76b5a3fd513001a5d40716e1287f': {
            '물리 공격력': 1113,
            '마법 공격력': 1348,
            '독립 공격력': 719,
            '지능': 78
        }
    }
    shop_item_info = [dnfapi.get_shop_item_info(i) for i in item_max_option]

    embed = discord.Embed(title='오늘의 아이템 등급을 알려드릴게요!')
    for info in shop_item_info:
        value = f"{info['itemGradeName']} ({info['itemGradeValue']}%)\n"
        for item_status in info['itemStatus']:
            if item_status['name'] in item_max_option[info['itemId']]:
                diff = item_status['value'] - item_max_option[info['itemId']][item_status['name']]
                value += f"{item_status['name']} : {item_status['value']}({diff})\n"
        embed.add_field(name=f"> {info['itemName']}", value=value)
    await interaction.response.send_message(content=None, embed=embed)


async def character(bot: discord.ext.commands.Bot, interaction: discord.Interaction, server: str, name: str):
    def get_character_equipment_info_embed(
            character_name_: str,
            character_equip_info_: dict,
            character_status_info_: dict) -> discord.Embed:
        character_equipment_info_embed = discord.Embed(title=f"{character_name_}님의 아이템 정보를 알려드릴게요.")

        # 강화, 재련, 마법부여
        for equip_info in character_equip_info_['equipment']:
            if equip_info['slotName'] in ['칭호', '보조무기']:
                continue

            value_ = ''
            if equip_info['reinforce'] > 0:
                value_ += f"+{equip_info['reinforce']}"
            if equip_info['refine'] > 0:
                value_ += f"({equip_info['refine']})"
            value_ += f" {equip_info['itemName']}\n"

            if equip_info.get('enchant') is not None:
                if equip_info['enchant'].get('status') is not None:
                    for eEnchant in equip_info['enchant']['status']:
                        value_ += f"{eEnchant['name']} +{eEnchant['value']}\n"
                if equip_info['enchant'].get('explain') is not None:
                    value_ += equip_info['enchant']['explain']

            character_equipment_info_embed.add_field(name=f"> {equip_info['slotName']}", value=value_)

        # 스탯
        stats = {
            '모험가 명성': 0,
            '힘': 0,
            '지능': 0,
            '체력': 0,
            '정신력': 0,
            '물리 공격': 0,
            '마법 공격': 0,
            '독립 공격': 0,
            '물리 크리티컬': 0,
            '마법 크리티컬': 0,
            '화속성 강화': 0,
            '수속성 강화': 0,
            '명속성 강화': 0,
            '암속성 강화': 0,
            '화속성 저항': 0,
            '수속성 저항': 0,
            '명속성 저항': 0,
            '암속성 저항': 0,
        }
        for i in character_status_info_['status']:
            if i['name'] in stats:
                stats[i['name']] = i['value']

        value = f"모험가 명성 : {stats['모험가 명성']: ,}\n" \
                f"힘 : {stats['힘']} | 지능 : {stats['지능']} | 체력 : {stats['체력']} | 정신력 : {stats['정신력']}\n" \
                f"물리공격 : {stats['물리 공격']} | 마법공격 : {stats['마법 공격']} | 독립 공격 : {stats['독립 공격']}\n" \
                f"물리크리티컬 : {stats['물리 크리티컬']}% | 마법크리티컬 : {stats['마법 크리티컬']}%\n" \
                f"속성강화 : 화({stats['화속성 강화']})/수({stats['수속성 강화']})/명({stats['명속성 강화']})/암({stats['암속성 강화']})\n" \
                f"속성저항 : 화({stats['화속성 저항']})/수({stats['수속성 저항']})/명({stats['명속성 저항']})/암({stats['암속성 저항']})"
        character_equipment_info_embed.add_field(name='> 스탯', value=value, inline=False)
        character_equipment_info_embed.set_footer(text='1페이지 / 2페이지')
        return character_equipment_info_embed

    def get_character_avatar_info_embed(eServer, eChrId, eChrName, eAvatar):
        eEmbed = discord.Embed(title=f"{eChrName}님의 캐릭터 정보를 알려드릴게요.")
        for avatar in eAvatar['avatar']:
            eValue = f"{avatar['itemName']}\n"
            if avatar['clone']['itemName'] is not None:
                eValue += f"{avatar['clone']['itemName']}"
            eEmbed.add_field(name=f"> {avatar['slotName']}", value=eValue)
        eEmbed.set_image(url=dnfapi.get_character_image_url(eServer, eChrId))
        eEmbed.set_footer(text='2페이지 / 2페이지')
        return eEmbed

    def get_embed_field_value(element):
        value = f"Lv.{element['level']} {element['characterName']}\n"
        value += f"서버 : {element['serverId']}\n"
        value += f"직업 : {element['jobGrowName']}"
        return value

    character_info = await utility.get_selection_from_list(
        bot=bot,
        interaction=interaction,
        items=dnfapi.get_character_info(server, name),
        title='원하는 캐릭터 번호의 이모지를 눌러주세요.',
        description='15초 안에 입력하지 않으면 자동으로 취소되요.',
        footer='',
        get_embed_field_value=get_embed_field_value,
        wait_for_timeout=15)
    message = await interaction.original_response()

    if character_info is None:
        await message.edit(content='오류가 발생했어요. 다시 시도해주세요.', embed=None)
        return

    server_id = character_info['serverId']
    character_id = character_info['characterId']
    character_name = character_info['characterName']
    equipment_info = dnfapi.get_character_equipment_info(server_id, character_id)
    status_info = dnfapi.get_character_status_info(server_id, character_id)
    avatar_info = dnfapi.get_character_avatar_info(server_id, character_id)
    equipment_info_embed = get_character_equipment_info_embed(character_name, equipment_info, status_info)
    avatar_info_embed = get_character_avatar_info_embed(server_id, character_id, character_name, avatar_info)

    await message.edit(content=None, embed=equipment_info_embed)
    await message.add_reaction('▶️')

    # 0 : 본템
    # 1 : 아바타
    page = 0
    while True:
        def check(reaction_: discord.Reaction, user_: discord.User):
            return reaction_.message.id == message.id and \
                   interaction.user.id == user_.id and \
                   str(reaction_) in ['◀️', '▶️']

        reaction, user = await bot.wait_for('reaction_add', check=check)

        # 페이지 이동
        if str(reaction) == '◀️':
            page = max(page - 1, 0)
        elif str(reaction) == '▶️':
            page = min(page + 1, 1)

        # 페이지에 따른 정보 출력
        if page == 0:
            embed = equipment_info_embed
        elif page == 1:
            embed = avatar_info_embed
        else:
            return

        await message.edit(content=None, embed=embed)
        await message.clear_reactions()
        if page > 0: await message.add_reaction('◀️')
        if page < 1: await message.add_reaction('▶️')


async def item_market_price(bot: discord.ext.commands.Bot, interaction: discord.Interaction, name: str):
    def get_market_price_embed(item_name: str) -> discord.Embed or None:
        market_price_embed = discord.Embed(title=f"'{item_name}' 시세를 알려드릴게요")
        item_auction_info = dnfapi.get_auction_item_sold_info(item_name)

        # 판매 데이터가 없을 경우
        if not item_auction_info:
            return None

        if item_name.endswith('카드'):
            statistic = {}
            for i in item_auction_info:
                statistic.setdefault(i['upgrade'], [0, 0, 0])
                statistic[i['upgrade']][0] += i['price']  # 총 가격
                statistic[i['upgrade']][1] += i['count']  # 총 판매량
            statistic = dict(sorted(statistic.items()))

            # 카드 업그레이드 수치 마다 따로 표기
            for i in statistic:
                average_price = statistic[i][0] // statistic[i][1]
                database.update_auction_item_price(f"{item_name} +{i}", average_price)
                prev_price_info = database.get_auction_second_latest_item_info(f"{item_name} +{i}")

                value = '데이터 없음'
                if prev_price_info is not None:
                    value = f"{utility.get_volatility(prev_price_info['price'], average_price)}" \
                            f"({prev_price_info['date'].strftime('%Y-%m-%d')})"

                market_price_embed.add_field(name=f"> +{i} 평균 가격", value=f"{average_price: ,}골드")
                market_price_embed.add_field(name='> 최근 판매량', value=f"{statistic[i][1]: ,}개")
                market_price_embed.add_field(name='> 가격 변동률', value=value)
        else:
            itme_price_sum, item_sold_count = 0, 0
            for i in item_auction_info:
                itme_price_sum += i['price']
                item_sold_count += i['count']
            average_price = itme_price_sum // item_sold_count
            database.update_auction_item_price(item_name, average_price)
            prev_price_info = database.get_auction_second_latest_item_info(item_name)

            value = '데이터 없음'
            if prev_price_info is not None:
                value = f"{utility.get_volatility(prev_price_info['price'], average_price)}" \
                        f"({prev_price_info['date'].strftime('%Y-%m-%d')})"

            market_price_embed.add_field(name='> 평균 가격', value=f"{average_price: ,}골드")
            market_price_embed.add_field(name='> 최근 판매량', value=f"{item_sold_count: ,}개")
            market_price_embed.add_field(name='> 가격 변동률', value=value)

        market_price_embed.set_footer(text=f"{item_auction_info[-1]['soldDate']} 부터"
                                           f"{item_auction_info[0]['soldDate']} 까지 집계된 자료예요.")
        market_price_embed.set_thumbnail(url=dnfapi.get_item_image_url(item_auction_info[0]['itemId']))
        return market_price_embed

    def get_embed_field_value(element):
        return element['itemName']

    item_info = await utility.get_selection_from_list(
        bot=bot,
        interaction=interaction,
        items=dnfapi.get_item_info(name),
        title='원하는 아이템 번호의 이모지를 눌러주세요.',
        description='15초 안에 입력하지 않으면 자동으로 취소되요.',
        footer='',
        get_embed_field_value=get_embed_field_value,
        wait_for_timeout=15)

    if item_info is None:
        await interaction.response.send_message(content='> 해당 아이템의 정보를 얻어오지 못했어요.', embed=None)
        return

    message = await interaction.original_response()

    embed = get_market_price_embed(item_info['itemName'])
    if embed is None:
        await message.edit(content='> 해당 아이템의 정보를 얻어오지 못했어요.', embed=None)
        return

    await message.edit(content=None, embed=embed)


async def 장비(bot, ctx, *inputs):
    def getItemInfoEmbed(eItemInfo):
        eEmbed = discord.Embed(title=eItemInfo['itemName'],
                               description=f"{eItemInfo['itemAvailableLevel']} Lv {eItemInfo['itemRarity']} {eItemInfo['itemTypeDetail']}")

        # 스탯
        eStatInfo = dnfapi.getItemStatInfo(eItemInfo['itemStatus'])
        eEmbed.add_field(name='> 스탯', value=eStatInfo, inline=False)

        # 시로코 옵션
        try:
            sirocoInfo = ''
            for i in eItemInfo['sirocoInfo']['options']:
                sirocoInfo += f"{i['explainDetail']}\n"
            eEmbed.add_field(name='> 시로코 옵션', value=sirocoInfo, inline=False)
        except:
            pass

        # 스킬 레벨
        try:
            eSkillLvInfo = utility.getSkillLevelingInfo(eItemInfo['itemReinforceSkill'])
            eSkillLvInfoValue = ''
            for i in eSkillLvInfo.keys():
                if i != '모든 직업':
                    eSkillLvInfoValue += f"{i}\n"
                for j in eSkillLvInfo[i]:
                    eSkillLvInfoValue = f"{j}\n" if i != '모든 직업' else f"{i} {j}\n"
            eEmbed.add_field(name='> 스킬', value=eSkillLvInfoValue)
        except:
            pass

        # 기본 옵션
        if eItemInfo['itemExplainDetail'] != '':
            eEmbed.add_field(name='> 옵션', value=eItemInfo['itemExplainDetail'], inline=False)

        # 변환 옵션
        try:
            eTransformInfo = eItemInfo['transformInfo']['explain']
            eEmbed.add_field(name='> 변환 옵션', value=eTransformInfo, inline=False)
        except:
            pass

        # 신화옵션
        try:
            eMythicInfo = dnfapi.getItemMythicInfo(eItemInfo['mythologyInfo']['options'])
            eEmbed.add_field(name='> 신화 전용 옵션', value=eMythicInfo, inline=False)
        except:
            pass

        # 플레이버 텍스트
        try:
            eEmbed.set_footer(text=eItemInfo['itemFlavorText'])
        except:
            pass

        # 아이콘
        eEmbed.set_thumbnail(url=dnfapi.get_item_image_url(eItemInfo['itemId']))

        return eEmbed

    def getItemBuffInfoEmbed(eItemInfo):
        eEmbed = discord.Embed(title=eItemInfo['itemName'],
                               description=f"{eItemInfo['itemAvailableLevel']} Lv {eItemInfo['itemRarity']} {eItemInfo['itemTypeDetail']}")

        # 스탯
        statInfo = dnfapi.getItemStatInfo(eItemInfo['itemStatus'])
        eEmbed.add_field(name='> 스탯', value=statInfo, inline=False)

        # 시로코 옵션
        try:
            sirocoInfo = ''
            for i in eItemInfo['sirocoInfo']['options']:
                buffExplainDetail = i['buffExplainDetail'].replace('\n\n', '\n')
                sirocoInfo += f"{buffExplainDetail}\n"
            eEmbed.add_field(name='> 시로코 옵션', value=sirocoInfo, inline=False)
        except:
            pass

        # 버프 스킬 레벨 옵션
        try:
            buffLvInfo = utility.getSkillLevelingInfo(eItemInfo['itemBuff']['reinforceSkill'])
            buffLvInfoValue = ''
            for i in buffLvInfo.keys():
                if i != '모든 직업':
                    buffLvInfoValue += f"{i}\n"
                for j in buffLvInfo[i]:
                    buffLvInfoValue = f"{j}\n" if i != '모든 직업' else f"{i} {j}\n"

            # 버프 옵션
            buffInfo = eItemInfo['itemBuff']['explain']
            eEmbed.add_field(name='> 버퍼 전용 옵션', value=buffLvInfoValue + buffInfo, inline=False)
        except:
            pass

        # 신화 옵션
        try:
            mythicInfo = dnfapi.getItemMythicInfo(eItemInfo['mythologyInfo']['options'], buff=True)
            eEmbed.add_field(name='> 신화 전용 옵션', value=mythicInfo)
        except:
            pass

        # 플레이버 텍스트
        try:
            eEmbed.set_footer(text=eItemInfo['itemFlavorText'])
        except:
            pass

        # 아이콘
        eEmbed.set_thumbnail(url=dnfapi.get_item_image_url(eItemInfo['itemId']))

        return eEmbed

    # 아이템 이름 유효성 확인
    itemName = ' '.join(inputs)
    if len(itemName) == 0:
        await ctx.message.delete()
        await ctx.channel.send('> `!장비 <장비아이템이름>` 의 형태로 적어야해요.\n'
                               '> ex) `!장비 세계수의 요정`')
        return

    # 입력한 채팅 삭제
    await ctx.message.delete()

    def embedFieldValueFunc(i):
        return i['itemName']

    def waitForCheckFunc(msg):
        return ctx.channel.id == msg.channel.id and ctx.author.id == msg.author.id and msg.content.isnumeric()

    # 목록 중 원하는 아이템 선택
    item = await utility.get_selection_from_list(
        bot,
        ctx,
        items=dnfapi.get_equip_item_info(itemName),
        title='원하는 장비 아이템의 번호를 입력해주세요.',
        description='15초 안에 입력하지 않으면 자동으로 취소되요.',
        footer=None,
        get_embed_field_value=embedFieldValueFunc,
        wait_for_check_func=waitForCheckFunc,
        wait_for_timeout=15
    )
    if item is None:
        await ctx.channel.send('오류가 발생했어요. 다시 시도해주세요.')
        return

    message = await ctx.channel.send(f"> 해당 장비의 정보를 불러오고 있어요...")
    itemInfo = dnfapi.get_item_detail_info(item['itemId'])
    embed = getItemInfoEmbed(itemInfo)
    await message.edit(embed=embed, content=None)
    await message.add_reaction('▶️')

    page = 0
    while True:
        def check(_reaction, _user):
            return str(_reaction) in ['◀️', '▶️'] and _user == ctx.author and _reaction.message.id == message.id

        reaction, user = await bot.wait_for('reaction_add', check=check)

        # 페이지 이동
        if str(reaction) == '◀️':
            page = max(page - 1, 0)
        elif str(reaction) == '▶️':
            page = min(page + 1, 1)

        # 페이지에 따른 정보 출력
        if page == 0:
            embed = getItemInfoEmbed(itemInfo)
        elif page == 1:
            embed = getItemBuffInfoEmbed(itemInfo)
        else:
            return

        # 메세지 수정, 리액션 재설정
        await message.edit(embed=embed, content=None)
        await message.clear_reactions()
        if page > 0: await message.add_reaction('◀️')
        if page < 1: await message.add_reaction('▶️')


async def 세트(bot, ctx, *inputs):
    def getSetItemInfoEmbed(eSetItemInfo):
        eEmbed = discord.Embed(title=eSetItemInfo['setItemName'] + '의 정보를 알려드릴게요.')

        # 레어리티, 부위, 이름
        for i in eSetItemInfo['setItems']:
            eEmbed.add_field(name=f"> {i['itemRarity']} {i['slotName']}", value=i['itemName'])

        # 세트 옵션
        for i in eSetItemInfo['setItemOption']:
            value = ''
            try:
                for j in i['status']:
                    value += f"{j['itemName']} {j['value']}\n"
            except:
                pass
            eEmbed.add_field(name=f"> {i['optionNo']}세트 옵션", value=f"{value}{i['explain']}", inline=False)
        eEmbed.set_thumbnail(url=dnfapi.get_item_image_url(eSetItemInfo['setItems'][0]['itemId']))
        return eEmbed

    def getSetItemBuffInfoEmbed(eSetItemInfo):
        eEmbed = discord.Embed(title=f"{eSetItemInfo['setItemName']}의 정보를 알려드릴게요.")

        for i in eSetItemInfo['setItems']:
            eName = f"> {i['itemRarity']} {i['slotName']}"
            eValue = i['itemName']
            eEmbed.add_field(name=eName, value=eValue)

        for i in eSetItemInfo['setItemOption']:
            skill = utility.getSkillLevelingInfo(i['itemBuff']['reinforceSkill'])
            value = ''
            for j in skill.keys():
                if j != '모든 직업':
                    value += f"{j}\n"
                for k in skill[j]:
                    value += f"{k}\n" if j != '모든 직업' else f"{j} {k}\n"
            value += i['itemBuff']['explain']
            eEmbed.add_field(name=f"> {i['optionNo']}세트 옵션", value=value, inline=False)

        eEmbed.set_thumbnail(url=dnfapi.get_item_image_url(eSetItemInfo['setItems'][0]['itemId']))
        return eEmbed

    # 세트템 이름 유효성 확인
    setName = ' '.join(inputs)
    if len(setName) == 0:
        await ctx.message.delete()
        await ctx.channel.send('> !세트 <세트옵션이름> 의 형태로 적어야해요!')
        return

    await ctx.message.delete()

    def embedFieldValueFunc(i):
        return i['setItemName']

    def waitForCheckFunc(msg):
        return ctx.channel.id == msg.channel.id and ctx.author.id == msg.author.id and msg.content.isnumeric()

    setItem = await utility.get_selection_from_list(
        bot=bot,
        interaction=ctx,
        items=dnfapi.get_set_item_info(setName),
        title='원하는 세트 옵션의 번호를 입력해주세요.',
        description='15초 안에 입력하지 않으면 자동으로 취소되요.',
        footer=None,
        get_embed_field_value=embedFieldValueFunc,
        wait_for_check_func=waitForCheckFunc,
        wait_for_timeout=15
    )
    if setItem is None:
        await ctx.channel.send('오류가 발생했어요. 다시 시도해주세요.')
        return

    message = await ctx.channel.send(f"> 해당 세트의 정보를 불러오고 있어요...")
    setItemInfo = dnfapi.get_set_item_detail_info(setItem['setItemId'])
    embed = getSetItemInfoEmbed(setItemInfo)
    await message.edit(embed=embed, content=None)
    await message.add_reaction('▶️')

    page = 0
    while True:
        def check(_reaction, _user):
            return str(_reaction) in ['◀️', '▶️'] and _user == ctx.author and _reaction.message.id == message.id

        reaction, user = await bot.wait_for('reaction_add', check=check)

        # 페이지 이동
        if str(reaction) == '◀️':
            page = max(page - 1, 0)
        elif str(reaction) == '▶️':
            page = min(page + 1, 1)

        # 페이지에 따른 정보 출력
        if page == 0:
            embed = getSetItemInfoEmbed(setItemInfo)
        elif page == 1:
            embed = getSetItemBuffInfoEmbed(setItemInfo)
        else:
            return

        # 메세지 수정, 리액션 재설정
        await message.edit(embed=embed, content=None)
        await message.clear_reactions()
        if page > 0: await message.add_reaction('◀️')
        if page < 1: await message.add_reaction('▶️')


async def 에픽(bot, ctx, *inputs):
    def getEpicEmbed(eChrName, eTimeline, eChannel, ePage):
        if eChannel is None:
            eEmbed = discord.Embed(title=f'{eChrName} 님은 이번 달에 {len(eTimeline)}개의 에픽을 획득했어요.')
        else:
            eEmbed = discord.Embed(title=f'{eChrName} 님은 이번 달에 {len(eTimeline)}개의 에픽을 획득했어요.',
                                   description=f'`{eChannel}`에서 에픽을 가장 많이 획득했어요!')

        for i in eTimeline[ePage * 15:ePage * 15 + 15]:
            if i['code'] == 505:
                eName = f"> {i['date'][:10]}\n" \
                        f"ch{i['data']['channelNo']}.{i['data']['channelName']}"
                eValue = i['data']['itemName']
            elif i['code'] == 513:
                eName = f"> {i['date'][:10]}\n" \
                        f"{i['data']['dungeonName']}"
                eValue = i['data']['itemName']
            else:
                continue
            eEmbed.add_field(name=eName, value=eValue)

        eEmbed.set_footer(text=f"{ePage + 1}페이지 / {(len(eTimeline) - 1) // 15 + 1}페이지")
        return eEmbed

    def getBestChannel(eTimeline):
        eChannels = {}
        for i in eTimeline:
            if i['code'] == 505:
                eChannels.setdefault(f"ch{i['data']['channelNo']}.{i['data']['channelName']}", 0)
                eChannels[f"ch{i['data']['channelNo']}.{i['data']['channelName']}"] += 1
        return sorted(eChannels.items(), key=lambda x: x[1], reverse=True)[0][0] if eChannels != {} else None

    if not inputs:
        await ctx.message.delete()
        await ctx.channel.send('> `!에픽 <닉네임>` 또는 `!에픽 <서버> <닉네임>` 의 형태로 적어야해요!')
        return

    if len(inputs) == 2:
        server = inputs[0]
        name = inputs[1]
    else:
        server = '전체'
        name = inputs[0]

    # --------------------------

    await ctx.message.delete()

    def embedFieldValueFunc(item):
        value = f"Lv.{item['level']} {item['characterName']}\n"
        value += f"서버 : {item['serverId']}\n"
        value += f"직업 : {item['jobGrowName']}"
        return value

    def waitForCheckFunc(msg):
        return ctx.channel.id == msg.channel.id and ctx.author.id == msg.author.id and msg.content.isnumeric()

    character = await utility.get_selection_from_list(
        bot=bot,
        interaction=ctx,
        items=dnfapi.get_character_info(server, inputs),
        title='원하는 캐릭터의 번호를 입력해주세요.',
        description='15초 안에 입력하지 않으면 자동으로 취소되요.',
        footer=None,
        get_embed_field_value=embedFieldValueFunc,
        wait_for_check_func=waitForCheckFunc,
        wait_for_timeout=15
    )
    if character is None:
        await ctx.channel.send('오류가 발생했어요. 다시 시도해주세요.')
        return

    # --------------------------

    server, chrId, chrName = character['serverId'], character['characterId'], character['characterName']
    message = await ctx.channel.send(f"> {name}님의 타임라인을 불러오고 있어요...")

    # 획득한 에픽이 없는 경우
    timeline = dnfapi.getChrTimeLine(server, chrId, '505', '513')
    if len(timeline) == 0:
        await message.edit(content=f'> {name}님은 이번 달 획득한 에픽이 없어요...')
        return

    # 에픽을 가장 많이 획득한 채널
    channel = getBestChannel(timeline)

    # 에픽랭킹 등록
    c.updateEpicRank(server, name, len(timeline), channel)

    page, minPage, maxPage = 0, 0, (len(timeline) - 1) // 15
    embed = getEpicEmbed(name, timeline, channel, page)
    await message.edit(embed=embed, content=None)
    if len(timeline) > 15:
        await message.add_reaction('▶️')

    while len(timeline) > 15:
        def check(_reaction, _user):
            return str(_reaction) in ['◀️', '▶️'] and _user == ctx.author and _reaction.message.id == message.id

        reaction, user = await bot.wait_for('reaction_add', check=check)

        # 페이지 이동
        if str(reaction) == '◀️':
            page = max(page - 1, minPage)
        elif str(reaction) == '▶️':
            page = min(page + 1, maxPage)

        # 페이지에 따른 정보 출력
        embed = getEpicEmbed(name, timeline, channel, page)

        # 메세지 수정, 리액션 재설정
        await message.edit(embed=embed)
        await message.clear_reactions()
        if page > minPage: await message.add_reaction('◀️')
        if page < maxPage: await message.add_reaction('▶️')


async def 에픽랭킹(bot, ctx):
    # Import common module
    from datetime import datetime

    def getEpicRankEmbed(eRanks, ePage):
        eToday = datetime.today()
        eRank = eRanks[ePage * 15:ePage * 15 + 15]
        eEmbed = discord.Embed(title=f"{eToday.year}년 {eToday.month}월 기린 랭킹을 알려드릴게요!")
        for idx, i in enumerate(eRank):
            eEmbed.add_field(name=f"> {ePage * 15 + idx + 1}등\n"
                                  f"> {i['server']} {i['name']}",
                             value=f"개수 : {i['count']}개\n"
                                   f"채널 : {i['channel']}")
        eEmbed.set_footer(text=f"{ePage + 1}페이지 / {(len(eRanks) - 1) // 15 + 1}페이지")
        return eEmbed

    await ctx.message.delete()
    message = await ctx.channel.send('> 에픽 랭킹을 불러오는 중이예요...')
    epicRanks = c.getEpicRanks()
    epicRanks = list(sorted(epicRanks, key=lambda x: x['count'], reverse=True))

    # 랭킹 데이터가 없을 경우 종료
    if not epicRanks:
        today = datetime.today()
        eEmbed = discord.Embed(title=f'{today.year}년 {today.month}월 에픽 랭킹을 알려드릴게요!',
                               description='> 에픽 랭킹 데이터가 없어요.\n'
                                           '> `!에픽` 명령어를 사용해서 랭킹에 등록해보세요!')
        await message.edit(embed=eEmbed, content=None)
        return

    embed = getEpicRankEmbed(epicRanks, 0)
    await message.edit(embed=embed, content=None)
    if len(epicRanks) > 15: await message.add_reaction('▶️')

    page, minPage, maxPage = 0, 0, (len(epicRanks) - 1) // 15
    while len(epicRanks) > 15:
        def check(_reaction, _user):
            return str(_reaction) in ['◀️', '▶️'] and _user == ctx.author and _reaction.message.id == message.id

        reaction, user = await bot.wait_for('reaction_add', check=check)

        # 페이지 이동
        if str(reaction) == '◀️':
            page = max(page - 1, minPage)
        elif str(reaction) == '▶️':
            page = min(page + 1, maxPage)

        # 페이지에 따른 정보 출력
        embed = getEpicRankEmbed(epicRanks, page)

        # 메세지 수정, 리액션 재설정
        await message.edit(embed=embed)
        await message.clear_reactions()
        if page > minPage: await message.add_reaction('◀️')
        if page < maxPage: await message.add_reaction('▶️')


async def 오던(ctx):
    await ctx.message.delete()
    message = await ctx.channel.send('> 오늘의 던파 정보를 불러오고있어요...')

    # 오던 정보
    todayDNF = []

    res = requests.get('http://df.nexon.com/df/home')
    soup = BeautifulSoup(res.text, 'lxml')
    result = soup.find('div', 'df_today rpt_today')
    for i in result.findAll('dd'):
        data = {
            'title': i.find('a').text,
            'url': f"http://df.nexon.com{i.find('a').get('href')}",
            'desc': i.find('p', 'txt').text,
            'name': i.find('p', 'blog').text,
            'like': 0
        }

        # 던파 조선일 경우 url 수정
        if data['name'] == '던파 조선':
            data['url'] = i.find('a').get('href')

        # 좋아요
        _res = requests.get(data['url'])
        _soup = BeautifulSoup(_res.text, 'lxml')
        like = _soup.find('strong', id='like_count')  # 네이버 블로그
        if like is None: like = _soup.find('em', id='recom_count')  # 던파 내 게시판
        if like is not None: data['like'] = like.text  # 좋아요 개수 저장

        # 데이터 추가
        todayDNF.append(data)

    # 출력
    embed = discord.Embed(title='오늘의 던파 게시물들을 알려드릴게요!')
    for index, i in enumerate(todayDNF):
        embed.add_field(name=f"> {i['title']}",
                        value=f"[{i['desc']}]({i['url']})\n"
                              f"{i['name']}\n"
                              f"좋아요 : {i['like']}개")
    embed.set_footer(text='마음에 드는 게시물은 좋아요를 눌러주세요!')
    await message.edit(embed=embed, content=None)
