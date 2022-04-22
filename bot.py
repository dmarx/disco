import gc
import os
import random
from dotenv import load_dotenv


# generate random integer values
from random import seed
from random import randint

# 1
from discord.ext import commands
import discord
import torch
from generator_disco.generator import GeneratorDisco
from generator_ld.generator import GeneratorLatentDiffusion
from manager.chain.chain import Chain

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 2
bot = commands.Bot(command_prefix='!')

chain = Chain()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# @bot.command(name='roll_dice', help='Simulates rolling dice.')
# async def roll(ctx, number_of_dice: int, number_of_sides: int):
#     dice = [
#         str(random.choice(range(1, number_of_sides + 1)))
#         for _ in range(number_of_dice)
#     ]
#     await ctx.send(', '.join(dice))
    
# @bot.command(name='make', help='Makes art.')
# async def make(ctx, prompt: str, input_seed:str=""):
#     # dice = [
#     #     str(random.choice(range(1, number_of_sides + 1)))
#     #     for _ in range(number_of_dice)
#     # ]
#     print ("making " + prompt)


#     seed(1)
#     prefix = str(random())
#     #os.system("python glid-3-xl/sample.py --width 512 --height 512 --model_path glid-3-xl/finetune.pt --kl_path glid-3-xl/kl-f8.pt --bert_path glid-3-xl/bert.pt --prefix " + prefix +" --batch_size 1 --num_batches 1 --text \"" + prompt + "\"")
#     os.system("python glid-3-xl/sample.py --ddim --width 512 --height 512 --clip_guidance" + (" --seed " + input_seed +" " if len(input_seed)>0 else "") + " --model_path glid-3-xl/finetune.pt --kl_path glid-3-xl/kl-f8.pt --bert_path glid-3-xl/bert.pt --prefix " + prefix +" --batch_size 1 --num_batches 1 --text \"" + prompt + "\"")
#     os.system("cp output/" + prefix + "00000.png static/output")
#     #print('display_video filename: ' + filename)
#     #return send_file("static/output/" + prefix + "00000.png", mimetype='image/png')

#     #await ctx.send("http://art.v3la.com/static/output/" + prefix + "00000.png")
#     await ctx.send(file=discord.File("static/output/" + prefix + "00000.png"))


@bot.command(name='make', help='Makes art.')
async def make(ctx, prompt: str, input_seed:str=""):
    print ("making " + prompt)

    # seed(1)
    # prefix = str(randint(0,1000000))#--steps 50
    # filename = gen.do_run(prompt,prefix,input_seed)
    # chain = Chain()
    filename = chain.run_chain(prompt)
    
    # filename = run_gen(prompt)
    #os.system("python glid-3-xl/sample.py --model_path glid-3-xl/finetune.pt --kl_path glid-3-xl/kl-f8.pt --bert_path glid-3-xl/bert.pt --prefix " + prefix +" --batch_size 1 --num_batches 1 --text \"" + prompt + "\"")
    #os.system("cp output/" + prefix + "00000.png static/output")

    # filename_gen =prefix + "00000.png"
    # filename_out =prefix + "_" + str(input_seed) + "_00000.png"
    # #os.system("python glid-3-xl/sample.py --width 512 --height 512 --model_path glid-3-xl/finetune.pt --kl_path glid-3-xl/kl-f8.pt --bert_path glid-3-xl/bert.pt --prefix " + prefix +" --batch_size 1 --num_batches 1 --text \"" + prompt + "\"")
    # os.system("python glid-3-xl/sample.py --width 256 --height 256 --steps 30  --clip_guidance" + (" --seed " + input_seed +" " if len(input_seed)>0 else "") + " --model_path glid-3-xl/finetune.pt --kl_path glid-3-xl/kl-f8.pt --bert_path glid-3-xl/bert.pt --prefix " + prefix +" --batch_size 1 --num_batches 1 --text \"" + prompt + "\"")
    # os.system("cp output/" + filename_gen + " static/output/" + filename_out)
    #print('display_video filename: ' + filename)
    #return send_file("static/output/" + prefix + "00000.png", mimetype='image/png')

    #await ctx.send("http://art.v3la.com/static/output/" + prefix + "00000.png")
    await ctx.send(file=discord.File("static/output/" + filename))
    

# @bot.command(name='makefast', help='Makes art.')
# async def makefast(ctx, prompt: str, input_seed:str=""):
#     print ("making fast " + prompt)

#     seed(1)
#     prefix = str(randint(0,1000000))#--steps 50
#     filename_gen =prefix + "00000.png"
#     filename_out =prefix + "_" + str(input_seed) + "_00000.png"
#     #os.system("python glid-3-xl/sample.py --width 512 --height 512 --model_path glid-3-xl/finetune.pt --kl_path glid-3-xl/kl-f8.pt --bert_path glid-3-xl/bert.pt --prefix " + prefix +" --batch_size 1 --num_batches 1 --text \"" + prompt + "\"")
#     os.system("python glid-3-xl/sample.py --width 256 --height 256  " + (" --seed " + input_seed +" " if len(input_seed)>0 else "") + " --model_path glid-3-xl/finetune.pt --kl_path glid-3-xl/kl-f8.pt --bert_path glid-3-xl/bert.pt --prefix " + prefix +" --batch_size 1 --num_batches 1 --text \"" + prompt + "\"")
#     os.system("cp output/" + filename_gen + " static/output/" + filename_out)
#     #print('display_video filename: ' + filename)
#     #return send_file("static/output/" + prefix + "00000.png", mimetype='image/png')
#     #python sample.py --model_path finetune.pt --batch_size 6 --num_batches 6 --text "a cyberpunk girl with a scifi neuralink device on her head"

#     #await ctx.send("http://art.v3la.com/static/output/" + prefix + "00000.png")
#     await ctx.send(file=discord.File("static/output/" + filename_out))
    

    
bot.run(TOKEN)
