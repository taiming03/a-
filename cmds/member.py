import discord
import json
from core.classes import Cog_Extension
from discord.ext import commands
from discord import Embed
class 成員出入(Cog_Extension):
  @commands.Cog.listener()
  async def on_member_join(self, member):
      channel = self.bot.get_channel(935368792186429571)
      embed=discord.Embed(color=0xf5e26b) 
      embed.set_author(name=member,   icon_url=member.avatar_url_as(size=1024))
      embed.set_thumbnail(url=member.avatar_url_as(size=1024))
      embed.add_field(name="通知", value=f"歡迎  <@!{member.id}>  來到 **冒險領域** 😎", inline=True)

      await channel.send(embed=embed)
  @commands.Cog.listener()
  async def on_member_remove(self, member):
    try:
      channel = self.bot.get_channel(935368792186429571)
      embed=discord.Embed(color=0xf5e26b) 
      embed.set_author(name=member,   icon_url=member.avatar_url_as(size=1024))
      embed.set_thumbnail(url=member.avatar_url_as(size=1024))
      embed.add_field(name="通知", value=f" <@!{member.id}>  離開了**{member.guild.name}**🥲", inline=True)
      await channel.send(embed=embed)
    except IndexError:
      pass
def setup(bot):
    bot.add_cog(成員出入(bot))
    