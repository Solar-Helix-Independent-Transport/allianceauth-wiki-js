# Cog used by https://github.com/pvyParts/allianceauth-discordbot

# Cog Stuff
from discord.ext import commands
from discord.embeds import Embed
from discord.colour import Color

# AA Contexts
from aadiscordbot.cogs.utils.decorators import sender_has_perm
from wikijs.manager import WikiJSManager
from django.conf import settings

import re

import logging
logger = logging.getLogger('aadiscordbot.cogs.wikijs')


class Wikijs(commands.Cog):
    """
    WikiJS relevant cogs for AADiscordbot
    Currently onlt implements minimal search
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @sender_has_perm('wikijs.access_wikijs')
    async def wiki(self, ctx):
        """
        Returns the top Wiki Article search result for a string
        """
        logger.debug("WikiJS Cog: !wikijs received")
        await ctx.channel.trigger_typing()
        await ctx.message.add_reaction(chr(0x231B))

        search_string = ctx.message.content[6:]
        if search_string == "":
            embed = Embed(title="WikiJS")
            embed.colour = Color.blue()
            embed.add_field(
                name="Wiki Link",
                value=f"{settings.WIKIJS_URL}"
            )
            await ctx.message.clear_reaction(chr(0x231B))
            return await ctx.reply(embed=embed, mention_author=False)

        try:
            pagesearchresponse = WikiJSManager().search_for_page(search_string)
            logger.debug(f"WikiJS Cog: page search response {pagesearchresponse}")
        except Exception as e:
            logger.error(e)

        embed = Embed(title=f"WikiJS Search: {search_string}")

        for result in pagesearchresponse["data"]["pages"]["search"]["results"]:
            logger.debug(f"WikiJS Cog: single page {result}")
            title = result["title"]
            path = result["path"]
            embed.add_field(
                name=title,
                value=f"{settings.WIKIJS_URL}{path}"
            )

        await ctx.message.clear_reaction(chr(0x231B))
        return await ctx.reply(embed=embed, mention_author=False)


def setup(bot):
    bot.add_cog(Wikijs(bot))
