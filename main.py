import os
import re

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from db import Item, Session

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

#Log-in notification
@bot.event
async def on_ready():
    print(f'Bot has logged in as {bot.user}')
    synced = await bot.tree.sync()
    print(f'Synced {len(synced)} command(s)')
    
#Command to search for an equipment by query
@bot.tree.command(name='get', description='Searches for an equipment by query')
@app_commands.describe(query='Name or ID of an equipment')
async def equipdex(interaction: discord.Interaction, query: str):
    
    if interaction.channel_id not in [1147307424525590538, 1139261444353966131, 1009530969394532445, 1046188154274709598]:
        await interaction.response.send_message('You can\'t use bot commands here, use #equipdex instead', ephemeral=True)
        return
    
    session = Session()
    
    if re.match(r'^[1-9]\d*$', query):
        items: list[Item] = session.query(Item).where(Item.item_id == query).all()
    else:
        items: list[Item] = session.query(Item).where(Item.title.contains(query)).all()
        
    if not items:
        await interaction.response.send_message(f'**❌ Nothing found for** `{query}`')
        
    elif len(items) > 1:
        hint = ' (The first 20 are displayed)' if len(items) > 20 else ''
        items = items[:20]
        titles = [item.title for item in items]
        ids = [item.item_id for item in items]
        rarities = [item.rarity for item in items]
        
        response = '\n'.join(f'`- {title} [ID: {id_}] {rarity}⭐`' for title, id_, rarity in zip(titles, ids, rarities))
        
        await interaction.response.send_message(f'**✅ Multiple items found{hint}:**\n{response}\n***please use **`/get [ID]`** to select a specific item***')
        
    else:
        
        DAMAGE_TYPE_EMOJIS = {
            'Physical' : '🗡️',
            'Fire' : '🔥',
            'Ice' : '❄️',
            'Energy' : '🔯',
            'Light' : '⚡',
            'Poison' : '☠️',
            None : ''
        }
        
        item = items[0]
        dmg_type = DAMAGE_TYPE_EMOJIS[item.dmg_type]
        rarity = item.rarity * '⭐'
        embed = discord.Embed(title=f'{item.title} {dmg_type}\n{rarity}', color=discord.Color.blue())
        
        for property_ in item.properties:
            embed.add_field(name=property_.name, value=property_.value, inline=True)
            
        for skill in item.skills:
            skill_dmg_type = DAMAGE_TYPE_EMOJIS[skill.dmg_type]
            embed.add_field(name=f'{skill.title} {skill_dmg_type}', value=skill.description, inline=False)
            
        embed.set_thumbnail(url=item.icon_url)
        embed.set_footer(text=f'If you notice a typo or mistake in the description, please report it to me: @quinckky')
        embed.set_author(name=f'No. {item.item_id}')
        
        await interaction.response.send_message(embed=embed)
    
    session.close()
        
if __name__ == '__main__':
    bot.run(TOKEN)
    