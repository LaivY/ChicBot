import discord
from discord import app_commands
from discord.ext import commands

import search
from setting import setting

bot = commands.Bot(command_prefix='.', intents=discord.Intents.default())


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('/도움말'))
    await bot.tree.sync()
    print('구동 완료')


@bot.tree.command(name='등급', description='오늘의 등급을 알려드려요.')
async def grade(interaction: discord.Interaction):
    await search.grade(interaction)


@bot.tree.command(name='캐릭터', description='캐릭터에 대한 정보를 알려드려요.')
async def character(interaction: discord.Interaction, 서버: str, 닉네임: str):
    await search.character(bot, interaction, 서버, 닉네임)


@character.autocomplete('서버')
async def character_server_autocomplete(interaction: discord.Interaction, current: str):
    servers = ['전체', '안톤', '바칼', '카인', '카시야스', '디레지에', '힐더', '프레이', '시로코']
    return [app_commands.Choice(name=server, value=server) for server in servers]


@bot.tree.command(name='시세', description='아이템의 경매장 시세를 알려드려요.')
async def item_market_price(interaction: discord.Interaction, 아이템: str):
    await search.item_market_price(bot, interaction, 아이템)


bot.run(setting['DISCORD_BOT_TOKEN'])