import discord, json, os, asyncio
import keep_alive
from discord.ext import commands, tasks
from discord_slash import SlashCommand
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
prefix='/'
bot = commands.Bot(command_prefix=prefix, intents=intents) #, help_command=None)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
token= os.getenv("TOKEN")
guild_ids = [935367902960451625]


@bot.event
async def on_ready():
  with open('./set/role.json', 'r', encoding='utf8') as file:
    data = json.load(file)
  roletotal = len(data["role"])
  n = 0
  while n < roletotal:
    all = []
    channel = bot.get_channel(data["channel_id"][n])
    message = await channel.fetch_message(data["message_id"][n])
    for reaction in message.reactions:
        async for user in reaction.users():
            # users.add(user)
          if user.id not in all:
            all.append(user.id)
            #await ctx.send(user.id)
    # await ctx.send(f"users: {', '.join(user.name for user in users)}")
    guild = bot.get_guild(data["guild_id"][n])
    role = guild.get_role(data["role"][n])
    total1 = len(role.members)
    if total1!=len(all):
      names = []
      for item in role.members:
          names.append(item.id)
      all_check = len(all)
      check = 0
      while check < all_check:
        print('check')
        if all[check] not in names:
          member = guild.get_member(all[check])
          if all[check] != None and str(type(member)) != "<class 'NoneType'>":
            role = discord.utils.get(member.guild.roles, id=int(data["role"][n])) 
            await member.add_roles(role)
        check += 1
    n+=1
  status_task.start()
  total.start()
  print(">> 機器人啟動 <<")
  print(f"機器人名稱:{bot.user.name}")
  print(f'前綴:{prefix}')
  # window.mainloop()
@slash.slash(name="load", description="加載文件", guild_ids=guild_ids)
async def load(ctx, extension):
  """載入文件"""
  bot.load_extension(f'cmds.{extension}')
  await ctx.send(f'加載 **{extension}.py** ')
@slash.slash(name="reload", description="重新加載文件")
async def reload(ctx, extension):
  #"""重新加載文件"""
	bot.reload_extension(f'cmds.{extension}')
	await ctx.send(f"重載 **{extension}.py** ")
@slash.slash(name="unload", description="移除文件", guild_ids=guild_ids)
async def unload(ctx, extension):
  #"""載卸文件""""
	bot.unload_extension(f'cmds.{extension}')
	await ctx.send(f"卸載 **{extension}.py** ")
@bot.command()
async def ping(ctx):
  """獲取機器人延遲"""
  await ctx.send(f'🏓 機器人延遲 {round(bot.latency*1000)} ms')
@tasks.loop(seconds=1)
async def status_task():
    await bot.change_presence(status=discord.Status.idle,activity=discord.Activity(type=discord.ActivityType.watching, name=F"系統運作中"))
    #await asyncio.sleep(5)
@tasks.loop(seconds=3600)
async def total():
  guild = bot.get_guild(935367902960451625)
  role = guild.get_role(935385600712904826)
  total1 = len(role.members)
  with open('./set/total.json', 'r', encoding='utf8') as jfile:
	  data = json.load(jfile)
  total2 = data['total']
  print(total1)
  print(total2)
  if total1 != total2:
    print('edit')
    welchannel = bot.get_channel(972174453771468910)
    await welchannel.edit(name=f'認證玩家人數:{total1}')
    data['total'] = total1
    with open('./set/total.json', 'w', encoding='UTF8') as jfile:
      json.dump(data, jfile, ensure_ascii=False, indent=4)

for filename in os.listdir('./cmds'):
	if filename.endswith('.py'):
		bot.load_extension(f'cmds.{filename[:-3]}')
if __name__ == "__main__":
    keep_alive.keep_alive()
    bot.run(token)