import discord
from discord.ext import commands
from dislash import InteractionClient
class Cog_Extension(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    inter_client = InteractionClient(bot)

# class Cog_Extension2(commands.Cog):
#   def __init__(self, slash):
#     self.slash = slash
#     inter_client = InteractionClient(slash)