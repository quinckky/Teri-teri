'''
Discord bot with all equipdex from the game Guns Girl - Houkai Gakuen translated to English
Designed specifically for Foxgirl and Catgirl guilds discord servers by @quinckky
'''

import os
import re

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from db import Item, Parameter, Session, Skill

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
session = Session()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

#Log-in notification
@bot.event
async def on_ready():
    print(f'Bot has logged in as {bot.user}')
    synced = await bot.tree.sync()
    print(f'Synced {len(synced)} command(s)')
    
#Command to search for an item by query
@bot.tree.command(name='eq', description='Searches for an equipment by query')
@app_commands.describe(query='Name or ID of an equipment')
async def equipdex(interaction: discord.Interaction, query: str):
    
    EMOJI_TYPES = {
        'physic' : '🗡️',
        'fire' : '🔥',
        'light' : '⚡',
        'power' : '🔯',
        'snow' : '❄️',
        'poison' : '☠️',
        None : ''
    }
    
    #If the query is a number, search by ID; otherwise search by name
    if re.match(r'^[1-9]\d*$', query):
        items: list[Item] = session.query(Item).where(Item.id == query).all()
    else:
        items: list[Item] = session.query(Item).where(Item.name.contains(query)).all()
        
    #If no such item is found, report it
    if not items:
        await interaction.response.send_message(f'**❌ Nothing found for** `{query}`')
        
    #If more than one item is found, output a list of the first 20 items
    elif len(items) > 1:
        hint = ' (The first 20 are displayed)' if len(items) > 20 else ''
        items = items[:20]
        names = [item.name for item in items]
        ids = [item.id for item in items]
        stars_counts = [item.stars_count for item in items]
        
        response = '\n'.join(f'`- {name} [ID: {id_}] {stars_count}⭐`' for name, id_, stars_count in zip(names, ids, stars_counts))
        
        await interaction.response.send_message(f'**✅ Multiple items found{hint}:**\n{response}\n***please use **`/eq [ID]`** to select a specific item***')
        
    #If only one item is found, output its detailed information
    else:
        item = items[0]
        dmg_type = EMOJI_TYPES[item.dmg_type]
        stars = item.stars_count * '⭐'
        embed = discord.Embed(title=f'{item.name} {dmg_type}\n{stars}', color=discord.Color.blue())
        
        for parameter in item.parameters:
            embed.add_field(name=parameter.name, value=parameter.value, inline=True)
            
        for skill in item.skills:
            skill_dmg_type = EMOJI_TYPES[skill.dmg_type]
            embed.add_field(name=f'{skill.name} {skill_dmg_type}', value=skill.description, inline=False)
            
        embed.set_thumbnail(url=item.img_url)
        embed.set_footer(text=f'If you notice a flaw in the description, please report it to me: @quinckky')
        embed.set_author(name=f'No. {item.id}')
        
        await interaction.response.send_message(embed=embed)
        
if __name__ == '__main__':
    bot.run(TOKEN)