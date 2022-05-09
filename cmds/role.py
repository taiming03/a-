import discord
import json
import asyncio
import time
import datetime
from discord.ext import commands
from core.classes import Cog_Extension#, Cog_Extension2
from discord_slash import cog_ext, SlashContext

class 身分組管理(Cog_Extension):
  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def guildrole(self, ctx):
    out = ""
    bb = ctx.guild.roles
    for ba in bb:
      if 'everyone' in str(ba):
        out += f"{ba}\n\n"
      else:
        ba = discord.utils.get(bb,name=str(ba))
        out += f"<@&{ba.id}>\n\n"
    embed=discord.Embed(title=f"以下是 {ctx.guild.name} 的身分組列表", description=out, color=0x57e6ff, timestamp=datetime.datetime.now())
    embed.set_footer(text=f"呼叫人:{ctx.author.name}")
    await ctx.send(embed=embed)

  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def roleadd(self, ctx, channel_id:int, arg:int, role:int, emoji:str = None): 
      """新增反應身分組資訊"""
      with open("./set/role.json",mode="r",encoding="utf8") as f:
        data = json.load(f)
      if role in data["role"] and ctx.guild.id != 935367902960451625:
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="錯誤", value="```這個身分組已經設定過了\n為確保資料庫完整及可讀性，故禁止新增此筆數據```", inline=False)
        await ctx.send(embed=embed)
      elif emoji != None and role not in data["role"] and ctx.guild.id == 935367902960451625:
        data["channel_id"].append(channel_id)
        data["message_id"].append(arg)
        data["role"].append(role)
        data["emoji"].append(emoji)
        data["guild_id"].append(ctx.guild.id)
        with open("./set/role.json",mode="w",encoding="utf8") as f:  
          json.dump(data,f,indent=4,ensure_ascii=False)
        embed=discord.Embed(color=0x36c4c2)
        embed = discord.Embed(title="登入成功", color=0x00a8ff)
        embed.add_field(name=f"訊息id", value=arg, inline=False)
        embed.add_field(name=f"身分組ID", value=role, inline=False)
        embed.add_field(name=f"貼圖", value=emoji, inline=False)
        send=await ctx.send(embed=embed)
        time.sleep(2)
        await send.delete()
        await ctx.message.delete()
        channels = self.bot.get_channel(channel_id)
        msgs = await channels.fetch_message(arg)
        await msgs.add_reaction(emoji)

  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def roledel(self, ctx,a:int,b:int): 
      """刪除反應身分組資訊"""
      with open("./set/role.json",mode="r",encoding="utf8") as f:
        data = json.load(f)
      mg = len(data["message_id"])
      n=0
      while n< mg: 
        msgpair = int(data["message_id"][n])
        role = int(data["role"][n])
        guild_id = int(data["guild_id"][n])
        id1 = int(ctx.guild.id)
        if a == msgpair and b == role and guild_id == id1 and ctx.guild.id == 935367902960451625:
          a = int(data["message_id"][n])
          b = str(data["role"][n])
          c = str(data["emoji"][n])
          e = int(data["channel_id"][n])
          s = int(data["guild_id"][n])
          indexa = data["message_id"].index(a)
          del data["message_id"] [indexa]
          indexc = data["emoji"].index(c)
          del data["emoji"] [indexc]
          b=int(data["role"][n])
          indexb = data["role"].index(b)
          del data["role"] [indexb]
          indexa = data["guild_id"].index(s)
          del data["guild_id"] [indexa]
          indexa = data["channel_id"].index(e)
          del data["channel_id"] [indexa]
          with open("./set/role.json",mode="w",encoding="utf8") as f:  
            json.dump(data,f,indent=4,ensure_ascii=False)
          embed = discord.Embed(title="成功刪除", color=0x00a8ff)
          embed.add_field(name=f"訊息id", value=a, inline=False)
          embed.add_field(name=f"身分組ID", value=b, inline=False)
          embed.add_field(name=f"貼圖", value=c, inline=False)
          send=await ctx.send(embed=embed)
          time.sleep(5)
          await send.delete()
          await ctx.message.delete()
          break
        else:
          n+=1

  @cog_ext.cog_slash(name="rolelist")
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def rolelist(self,ctx: SlashContext):
    """列出反應身分組資訊"""
    invites=""
    await ctx.guild.invites()
    with open("./set/role.json",mode="r",encoding="utf8") as f:
      data = json.load(f)
    if int(ctx.guild.id) in data["guild_id"]:
      a = len(data["message_id"])
      b = len(data["role"])
      c = len(data["emoji"])
      d = len(data["guild_id"])
      if a==b and b==c and a==c and a!=0 and a==d:
        n=0
        while n<a:
          y=n+1
          if int(ctx.guild.id) == data["guild_id"][n]:
            f = int(data["message_id"][n])
            g = int(data["role"][n])
            h = str(data["emoji"][n])
            invites += f"編號-{y}\n"
            invites += f"訊息id: {f}\n"
            invites += f"身分組ID: {g}\n"
            invites += f"貼圖: {h}\n"
            invites += ("-"*50) + "\n"
            
          n+=1
        embed1 = discord.Embed(title="以下是系統中紀錄的觸發身分組資料", color=0x12f3ef, description=invites)
        await ctx.channel.send(embed=embed1)
    else:
      await ctx.channel.purge(limit =1)
      abc=await ctx.send("查無資料")
      time.sleep(5)
      await abc.delete()

  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def test(self,ctx):
    """測試"""
    with open('./set/role.json', 'r', encoding='utf8') as file:
	    data = json.load(file)
    roletotal = len(data["role"])
    n = 0
    while n < roletotal:
      all = []
      channel = self.bot.get_channel(data["channel_id"][n])
      message = await channel.fetch_message(data["message_id"][n])
      for reaction in message.reactions:
          async for user in reaction.users():
              # users.add(user)
            if user.id not in all:
              all.append(user.id)
              #await ctx.send(user.id)
      # await ctx.send(f"users: {', '.join(user.name for user in users)}")
      guild = self.bot.get_guild(data["guild_id"][n])
      role = guild.get_role(data["role"][n])
      total1 = len(role.members)
      if total1!=len(all):
        names = []
        for item in role.members:
            names.append(item.id)
        all_check = len(all)
        check = 0
        while check < all_check:
          if all[check] not in names:
            member = guild.get_member(all[check])
            if all[check] != None and str(type(member)) != "<class 'NoneType'>":
              role = discord.utils.get(member.guild.roles, id=int(data["role"][n])) 
              await member.add_roles(role)
          check += 1
      n+=1
  

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload:discord.RawReactionActionEvent):
      n = 0
      with open("./set/role.json",mode="r",encoding="utf8") as f:
        data = json.load(f)
      await asyncio.sleep(1)
      guild = self.bot.get_guild(payload.guild_id)
      member = guild.get_member(payload.user_id)
      emoji = payload.emoji.name
      message_id = payload.message_id
      mg = len(data["message_id"])
      n = 0
      while n < mg:
        msgpair = int(data["message_id"][n])
        emojipair = str(data["emoji"][n])
        if message_id == msgpair and (emoji == emojipair or emoji in emojipair):
          role = discord.utils.get(member.guild.roles, id=int(data["role"][n])) 
          await member.add_roles(role)
          embed=discord.Embed(color=0x37e65a)
          embed.add_field(name="執行成功", value=f"成功將 {role} 身分給 <@{member.id}>", inline=False)
          await self.bot.get_user(member.id).send(embed=embed)
          break 
        else:
          n+=1


  @commands.Cog.listener()
  async def on_raw_reaction_remove(self, payload:discord.RawReactionActionEvent):
      with open("./set/role.json",mode="r",encoding="utf8") as f:
        data = json.load(f)
      await asyncio.sleep(1)
      guild = self.bot.get_guild(payload.guild_id)
      member = guild.get_member(payload.user_id)
      emoji = payload.emoji.name
      message_id = payload.message_id
      mg = len(data["message_id"])
      n = 0
      while n < mg:
        msgpair = int(data["message_id"][n])
        emojipair = str(data["emoji"][n])
        if message_id == msgpair and (emoji == emojipair or emoji in emojipair):
          role = discord.utils.get(member.guild.roles, id=int(data["role"][n])) 
          await member.remove_roles(role)
          embed=discord.Embed(color=0xe63737)
          embed.add_field(name="執行成功", value=f"成功將 <@{member.id}> 的 {role} 身分移除 ", inline=False)
          await self.bot.get_user(member.id).send(embed=embed)
          break 
        else:
          n+=1

def setup(bot):
    bot.add_cog(身分組管理(bot))