# import os
# import random
# from dotenv import load_dotenv

# # generate random integer values
# from random import seed
# from random import randint

# from discord.ext import commands
# import discord
# from generator.generator import Generator

# load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')

# bot = commands.Bot(command_prefix='!')
# gen = Generator()

# @bot.event
# async def on_ready():
#     print(f'{bot.user.name} has connected to Discord!')

# @bot.command(name='make', help='Makes art.')
# async def make(ctx, prompt: str, input_seed:str=""):
#     print ("making " + prompt)

#     seed(1)
#     prefix = str(randint(0,1000000))#--steps 50
#     filename = gen.do_run(prompt,prefix,input_seed)
    
#     await ctx.send(file=discord.File("static/output/" + filename))
    
    
# bot.run(TOKEN)
