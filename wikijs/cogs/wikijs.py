# Cog used by https://github.com/pvyParts/allianceauth-discordbot

# Cog Stuff
from discord.ext import commands
from discord.embeds import Embed
from discord.colour import Color

# AA Contexts
from aadiscordbot.cogs.utils.decorators import sender_has_perm
from aadiscordbot.app_settings import get_site_url
from wikijs.manager import WikiJSManager
from django.conf import settings

import re

import logging
logger = logging.getLogger('wikijs.cogs.wikijs')


class Wikijs(commands.Cog):
    """
    WikiJS relevant cogs for AADiscordbot
    Currently onlt implements minimal search
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @sender_has_perm('wikijs.access_wikijs')
    async def wiki(self, ctx, search_string):
        """
        Returns the top Wiki Article search result for a string
        """
        await ctx.channel.trigger_typing()
        await ctx.message.add_reaction(chr(0x231B))

        try:
            pagesearchresponse = WikiJSManager.search_for_page(search_string)
        except Exception as e:
            logger.error(e)

        embed = Embed(title=f"WikiJS Search: {search_string}")

        for result in pagesearchresponse["data"]["pages"]["search"]["results"]:
            title = result["title"]
            path = result["path"]
            embed.add_field(
                name=title,
                value=f"{settings.WIKIJS_URL}{path}"
            )

        return embed


def setup(bot):
    bot.add_cog(Wikijs(bot))
