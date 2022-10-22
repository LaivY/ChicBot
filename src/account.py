# Import discord module
import discord

# Import common module
from datetime import datetime

# Import my module
from src import utility
#from src.database import c

async def 출석(ctx):
    await ctx.message.delete()
    did, name = str(ctx.message.author.id), ctx.message.author.display_name
    message = await ctx.channel.send(f'> {name}님의 출석을 확인하고있어요...')

    # 계정 불러오기
    account = c.getAccount(did)
    if account is None:
        c.iniAccount(did)
        account = c.getAccount(did)

    today = datetime.now().strftime('%Y-%m-%d')
    embed = discord.Embed(title=f'{name}님의 출석체크!')

    # 이미 출석한 경우
    if str(account['checkDate']) == today:
        embed.add_field(name='> 출석 보상', value='X')
        embed.set_footer(text='오늘은 이미 출석체크를 했어요.')
        check = False
    else:
        c.updateDailyCheck(did)
        reward = utility.getDailyReward()
        c.gainGold(did, reward)
        check = True

        embed.add_field(name='> 출석 보상', value=f"{format(reward, ',')}골드")
        embed.set_footer(text='출석체크 완료!')
    embed.add_field(name='> 출석 일수', value=f"{account['checkCount'] + check}일")
    embed.add_field(name='> 보유 골드', value=f"{format(c.getGold(did), ',')}골드")
    await message.edit(embed=embed, content=None)
