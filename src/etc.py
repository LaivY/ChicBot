import discord

async def 도움말(bot, ctx):
    def getSearchCommandsEmbed():
        eEmbed = discord.Embed(title='시크봇의 `검색` 관련 명령어들을 알려드릴게요!')
        eEmbed.add_field(name='> !등급', inline=False,
                         value='오늘의 장비 등급을 알려드릴게요. 100% 등급의 장비와 비교해서 어느 스탯이 얼마나 부족한지도 알려드려요!\n'
                               'ex) `!등급`')
        eEmbed.add_field(name="> !캐릭터 <서버> <닉네임>", inline=False,
                         value='해당 캐릭터가 장착 중인 장비와 아바타를 알려드릴게요.\n'
                               '<서버>는 생략할 수 있고 생략하지 않으면 해당 서버의 캐릭터만 검색해요.\n'
                               'ex) `!캐릭터 로리장인시크`, `!캐릭터 바칼 배메장인시크`')
        eEmbed.add_field(name="> !장비 <장비아이템이름>", inline=False,
                         value='해당 장비 아이템의 옵션을 알려드릴게요.\n'
                               '장비아이템 이름은 정확하지 않아도되요. 검색 결과 중에서 원하는 장비를 선택하면되요.\n'
                               'ex) `!장비 세계수의 요정`, `!장비 선택`')
        eEmbed.add_field(name="> !세트 <세트아이템이름>", inline=False,
                         value='해당 세트 아이템의 옵션을 알려드릴게요.\n'
                               '세트아이템 이름은 정확하지 않아도되요. 검색 결과 중에서 원하는 세트를 선택하면되요.\n'
                               'ex) `!세트 선택의 기로 세트`, `!세트 개악`')
        eEmbed.add_field(name="> !시세 <아이템이름>", inline=False,
                         value='해당 아이템의 시세와 가격 변동률을 알려드릴게요.\n'
                               '아이템이름은 최대한 정확해야 검색할 수 있어요.\n'
                               'ex) `!시세 아이올라이트`, `!시세 시간의 결정`')
        eEmbed.add_field(name="> !에픽 <서버> <닉네임>", inline=False,
                         value='해당 캐릭터가 이번 달에 획득한 에픽의 정보를 알려드릴게요.\n'
                               '<서버>는 생략할 수 있고 생략하지 않으면 해당 서버의 캐릭터만 검색해요.\n'
                               'ex) `!에픽 로리장인시크`, `!에픽 바칼 배메장인시크`')
        eEmbed.add_field(name='> !에픽랭킹', inline=False,
                         value='이번 달 획득한 에픽 개수를 기준으로한 랭킹을 보여드려요.\n'
                               'ex) `!에픽랭킹`')
        eEmbed.add_field(name='> !오던', inline=False,
                         value='오늘의 던파 게시물들을 알려드려요.\n'
                               'ex) `!오던`')
        eEmbed.set_footer(text='1페이지 / 2페이지')
        return eEmbed
    
    def getEtcCommandsEmbed():
        eEmbed = discord.Embed(title='시크봇의 `기타` 명령어들을 알려드릴게요!')
        eEmbed.add_field(name="> !출석", inline=False,
                         value='매일마다 랜덤한 골드를 얻을 수 있어요. 추후 더 많은 효과가 추가될 수 있어요!\n'
                               'ex) `!출석`, `!출첵`, `!출석체크`')
        eEmbed.add_field(name='> !청소', inline=False,
                         value='시크봇이 말한 것들을 모두 삭제해요.\n'
                               'ex) `!청소`')
        eEmbed.add_field(name='> #시크봇', inline=False,
                         value='채널 주제에 이 태그가 있는 채팅 채널에서만 사용 가능해요.\n'
                               '모든 채널에 해당 태그가 없다면 시크봇을 모든 채팅 채널에서 사용할 수 있어요.\n'
                               'ex) 채널 편집 -> 채널 주제 -> `#시크봇` 추가')
        eEmbed.add_field(name='> 1윤시크 :: 커뮤니티', inline=False,
                         value='던파와 코딩과 관련된 디스코드 커뮤니티예요!\n'
                               '던파와 디스코드봇에 관심이 있으신 분이라면 들어오면 좋을 것 같아요!\n'
                               '[여기를 누르면 초대받을 수 있어요.](https://discord.gg/ZUbjgY4jg2)')
        eEmbed.set_footer(text=f'2페이지 / 2페이지')
        return eEmbed

    SearchCommandsEmbed = getSearchCommandsEmbed()
    EtcCommandsEmbed = getEtcCommandsEmbed()
    
    await ctx.message.delete()
    message = await ctx.channel.send(embed=SearchCommandsEmbed)
    await message.add_reaction('▶️')

    # 0 : 검색
    # 1 : 기타
    page = 0
    while True:
        def check(_reaction, _user):
            return str(_reaction) in ['◀️', '▶️'] and _user.id == ctx.author.id and _reaction.message.id == message.id
        reaction, user = await bot.wait_for('reaction_add', check=check)

        # 페이지 이동
        if str(reaction) == '◀️':
            page = max(page - 1, 0)
        elif str(reaction) == '▶️':
            page = min(page + 1, 1)

        # 페이지에 따른 정보 출력
        if page == 0:
            embed = SearchCommandsEmbed
        elif page == 1:
            embed = EtcCommandsEmbed
        else: return

        await message.edit(embed=embed, content=None)
        await message.clear_reactions()
        if page > 0: await message.add_reaction('◀️')
        if page < 1: await message.add_reaction('▶️')

async def 청소(bot, ctx):
    def check(message): return message.author == bot.user
    await ctx.channel.purge(check=check)
    await ctx.message.delete()
