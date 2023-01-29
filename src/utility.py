import asyncio
import discord
from discord.ext import commands


async def get_selection_from_list(
        bot: discord.ext.commands.Bot,
        interaction: discord.Interaction,
        items: list,
        title: str,
        description: str,
        footer: str,
        get_embed_field_value,
        wait_for_timeout: int) -> any:
    if not items:
        return
    if len(items) > 6:
        items = items[:6]

    embed = discord.Embed(title=title, description=description)
    for index, item in enumerate(items):
        embed.add_field(name=f"> {index + 1}", value=get_embed_field_value(item))
    if footer:
        embed.set_footer(text=footer)

    await interaction.response.send_message(content=None, embed=embed)
    message = await interaction.original_response()
    await message.add_reaction('1️⃣')
    if len(items) >= 2:
        await message.add_reaction('2️⃣')
    if len(items) >= 3:
        await message.add_reaction('3️⃣')
    if len(items) >= 4:
        await message.add_reaction('4️⃣')
    if len(items) >= 5:
        await message.add_reaction('5️⃣')
    if len(items) >= 6:
        await message.add_reaction('6️⃣')

    try:
        def check(reaction: discord.Reaction, user: discord.User):
            return reaction.message.id == message.id and \
                   interaction.user.id == user.id and \
                   str(reaction) in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣')
        reaction, user = await bot.wait_for('reaction_add', check=check, timeout=wait_for_timeout)
        await message.clear_reactions()

        if str(reaction) == '1️⃣':
            return items[0]
        if str(reaction) == '2️⃣' and len(items) >= 2:
            return items[1]
        if str(reaction) == '3️⃣' and len(items) >= 3:
            return items[2]
        if str(reaction) == '4️⃣' and len(items) >= 4:
            return items[3]
        if str(reaction) == '5️⃣' and len(items) >= 5:
            return items[4]
        if str(reaction) == '6️⃣' and len(items) >= 6:
            return items[5]

    except asyncio.TimeoutError:
        await message.delete()


def getSkillLevelingInfo(reinforceSkill):
    result = {}
    for i in reinforceSkill:
        jobName = '모든 직업' if i['jobName'] == '공통' else i['jobName']

        # 레벨 범위+
        if i.get('levelRange') is not None:
            for j in i['levelRange']:
                result.setdefault(jobName, [])
                minLv, maxLv, value = j.values()
                result[jobName].append(f"{minLv} ~ {maxLv} 레벨 모든 스킬 Lv +{value}")

        # 단순 스킬+
        if i.get('skills') is not None:
            for j in i['skills']:
                result.setdefault(jobName, [])
                result[jobName].append(f"{j['name']} 스킬Lv +{j['value']}")

    return result


def get_volatility(prev: int, latest: int) -> str:
    if prev == 0 or latest == 0:
        return ''

    percentage = ((latest / prev) - 1) * 100
    if percentage > 0:
        result = f"▲ {format(percentage, '.2f')}%"
    elif percentage == 0:
        result = '- 0.00%'
    else:
        result = f"▼ {format(percentage, '.2f')}%"
    return result
