import gc
import os
import random
from types import SimpleNamespace
from dotenv import load_dotenv

from random import seed
from random import randint

from discord.ext import commands
import discord
import torch

from modules.manager.chain.chain import Chain
from modules.manager.projects.project import Project
# from generator_disco.generator import GeneratorDisco
# from generator_ld.generator import GeneratorLatentDiffusion
# from manager.chain.chain import Chain

import openai   


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

openai.api_key = os.getenv("OPENAI_API_KEY")

# 2
bot = commands.Bot(command_prefix='!',description='Lets talk about art baby.!')

project = Project(-1)
project.generators = [
    SimpleNamespace(**
    {
        "id":0,
        "type":1,
        "settings":{
            
            "prompt":"",
            "steps":30,
            "width":256,
            "height":256,
            # 'ViTB32': True,
            # 'ViTB16': True,
            # 'ViTL14': False, # True
            # 'ViTL14_336px':False,
            # 'RN101': False,
            # 'RN50': False,
            # 'RN50x4': False,
            # 'RN50x16': False,
            # 'RN50x64': False,
        }
    }),
    # SimpleNamespace(**{
    #     "id":1,
    #     "type":2,
    #     "settings":{
    #         "text_prompts": [{
    #         "start": 0,
    #         "prompt": ""
    #         }], 
    #         "steps":50,
    #         "width":512,
    #         "height":512,
    #         }
    # })
]
chain = Chain()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='make', help='Makes art.')
async def make(ctx, *, prompt):
    global project, chain
    prompt = " ".join(prompt.split())
    print (prompt)
    
    project.generators[0].settings["prompt"] = prompt
    #project.generators[1].settings["prompt"] = prompt
    filename = chain.run_project(project)
    # filename = chain.run_chain(prompt)

    await ctx.send( file=discord.File("static/output/" + filename))
    
@bot.command(name='paint', help='Makes art from topics.')
async def paint(ctx, *, prompt):
    prompt = " ".join(prompt.split())
    print (prompt)
    
    answer = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Write an imaginary description of a scene to use to generate art:\n\Scene Description: " + prompt,
        temperature=0.5,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    answer = "".join(answer.choices[0]['text']).strip()
    answer = answer.replace("“","").replace("”","").replace("\"","") + ", by Asher Brown Durand, matte painting trending on artstation",
    answer = answer[0]
    
    global project, chain
    
    project.generators[0].settings["prompt"] = answer
    #project.generators[1].settings["prompt"] = prompt
    filename = chain.run_project(project)
    #await ctx.send(answer, file =discord.File("static/output/" + filename))
    await ctx.send(discord.utils.escape_mentions(answer))# , files: [discord.File("static/output/" + filename)]})
    await ctx.send(file =discord.File("static/output/" + filename))
    
@bot.command(name='horror', help='Makes a horror scene.')
async def horror(ctx, *, prompt):
    prompt = " ".join(prompt.split())
    print (prompt)

    answer = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Topic: " +  prompt  + "\nTwo-Sentence Horror Story:",
        temperature=0.8,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )
    answer = "".join(answer.choices[0]['text']).strip()
    return await ctx.send(discord.utils.escape_mentions(answer))
    
        
@bot.command(name='answer', help='Q&A to the moon.')
async def answer(ctx, *, prompt):
    prompt = " ".join(prompt.split())
    print (prompt)
        
    start_sequence = "\nA:"
    restart_sequence = "\n\nQ: "

    answer = openai.Completion.create(
        engine="text-davinci-002",
        prompt="I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\nQ: " + prompt + "\nA:",
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )
    
    answer = "".join(answer.choices[0]['text']).strip()
    return await ctx.send(discord.utils.escape_mentions(answer))
    
    
@bot.command(name='poem', help='Makes a poem.')
async def poem(ctx, *, prompt):
    prompt = " ".join(prompt.split())
    print (prompt)

    answer = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Topic: " +  prompt  + "\n16 lines of poetry:",
        temperature=0.8,
        max_tokens=120,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )
    answer = "".join(answer.choices[0]['text']).strip()
    return await ctx.send(discord.utils.escape_mentions(answer))
    
    
        
@bot.command(name='marv', help='Reluctantly, I will chat with you.')
async def marv(ctx, *, prompt):
    prompt = " ".join(prompt.split())
    print (prompt)

    answer = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Marv is a chatbot that reluctantly answers questions with sarcastic responses:\n\nYou: How many pounds are in a kilogram?\nMarv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nMarv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nMarv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou: What is the meaning of life?\nMarv: I’m not sure. I’ll ask my friend Google.\nYou: " + prompt + "\nMarv:",
        temperature=0.5,
        max_tokens=60,
        top_p=0.3,
        frequency_penalty=0.5,
    presence_penalty=0
    )
    answer = "".join(answer.choices[0]['text']).strip()
    return await ctx.send(discord.utils.escape_mentions(answer))
    
    
        
@bot.command(name='emojify', help='Emoji heaven.')
async def emojify(ctx, *, prompt):
    prompt = " ".join(prompt.split())
    print (prompt)

    answer = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Convert movie titles into emoji.\n\nBack to the Future: 👨👴🚗🕒 \nBatman: 🤵🦇 \nTransformers: 🚗🤖 \n" + prompt + ":",
        temperature=0.5,
        max_tokens=60,
        top_p=0.3,
        frequency_penalty=0.5,
    presence_penalty=0
    )
    answer = "".join(answer.choices[0]['text']).strip()
    return await ctx.send(discord.utils.escape_mentions(answer))



@bot.command(name='explaincode', help='Explain this code to me now! (need codex)')
async def explaincode(ctx, *, prompt):
    prompt = " ".join(prompt.split())
    print (prompt)

    answer = openai.Completion.create(
        engine="code-davinci-001",
        prompt=prompt + "\n\n\"\"\"\nHere's what the above class is doing:\n1.",
        temperature=0,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\"\"\""]
    )
    answer = "".join(answer.choices[0]['text']).strip()
    return await ctx.send(discord.utils.escape_mentions(answer))



@bot.command(name='brandgen', help='Make me a brand name from a description')
async def brandgen(ctx, *, prompt):
    prompt = " ".join(prompt.split())
    print (prompt)
    
    answer = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Product description: A home milkshake maker\nProduct names: HomeShaker, Fit Shaker, QuickShake, Shake Maker\n\nProduct description: " + prompt + "\nProduct names:",
        # prompt="Product description: A home milkshake maker\nSeed words: fast, healthy, compact.\nProduct names: HomeShaker, Fit Shaker, QuickShake, Shake Maker\n\nProduct description: A pair of shoes that can fit any foot size.\nSeed words: adaptable, fit, omni-fit.\nProduct names:",
        temperature=0.8,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    answer = prompt + "\n"  + "".join(answer.choices[0]['text']).strip()
    return await ctx.send(discord.utils.escape_mentions(answer))



@bot.command(name='fixpy', help='Fix dodgy code that nin wrote. (need codex)')
async def fixpy(ctx, *, prompt):
    prompt = " ".join(prompt.split())
    print (prompt)

    answer = openai.Completion.create(
        engine="code-davinci-002",
        prompt="##### Fix bugs in the below function\n \n### Buggy Python\nimport Random\na = random.randint(1,12)\nb = random.randint(1,12)\nfor i in range(10):\n    question = \"What is \"+a+\" x \"+b+\"? \"\n    answer = input(question)\n    if answer = a*b\n        print (Well done!)\n    else:\n        print(\"No.\")\n    \n### Fixed Python",
        temperature=0,
        max_tokens=182,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["###"]
    )

    answer = prompt + "\n"  + "".join(answer.choices[0]['text']).strip()
    return await ctx.send(discord.utils.escape_mentions(answer))




@bot.command(name='mkscifi', help='Come up with sci-fi titles.')
async def scifibookmaker(ctx, *, prompt):
    prompt = " ".join(prompt.split())
    print (prompt)

    answer = openai.Completion.create(
        engine="text-davinci-002",
        prompt="List 10 science fiction books:",
        temperature=0.5,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0.52,
        presence_penalty=0.5,
        stop=["11."]
    )

    answer = prompt + "\n"  + "".join(answer.choices[0]['text']).strip()
    return await ctx.send(discord.utils.escape_mentions(answer))



bot.run(TOKEN)
