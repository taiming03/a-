import discord
from core.classes import Cog_Extension
from discord.ext import commands
class 人數統計(Cog_Extension):
  #查詢認證使用者人數
  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def total(self, ctx): 
    role = ctx.guild.get_role(935385600712904826)
    await ctx.send(len(role.members))

  #建立語音頻道
  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  async def totals(self, ctx): 
    welchannel = self.bot.get_channel(935443083947028500)
    await welchannel.edit(name='專屬')
    #await ctx.edit_channel(welchannel, f"{len(set(self.bot.get_all_members()))}")
    #await ctx.guild.create_voice_channel(f"{ctx.author.name}#{ctx.author.discriminator}專屬")
def setup(bot):
    bot.add_cog(人數統計(bot))