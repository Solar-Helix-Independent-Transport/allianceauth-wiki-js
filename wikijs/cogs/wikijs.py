# Cog used by https://github.com/pvyParts/allianceauth-discordbot
import logging

from aadiscordbot.cogs.utils.decorators import sender_has_perm
from discord.commands import SlashCommandGroup
from discord.embeds import Embed
from discord.ext import commands

from django.conf import settings

from wikijs.manager import WikiJSManager

logger = logging.getLogger('aadiscordbot.cogs.wikijs')


class Wikijs(commands.Cog):
    """
    WikiJS relevant cogs for AADiscordbot
    Currently only implements minimal search
    """
    def __init__(self, bot):
        self.bot = bot

    wikijs_commands = SlashCommandGroup("wiki", "Wiki JS", guild_ids=[
                                int(settings.DISCORD_GUILD_ID)])

    @wikijs_commands.command(name="search", description="Search WikiJS", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    @sender_has_perm('wikijs.access_wikijs')
    async def search(self, ctx, search_string: str ):
        """
        Returns the top Wiki Article search result for a string
        """
        await ctx.respond(content=f"Searching for {search_string}", ephemeral=True)
        try:
            pagesearchresponse = WikiJSManager().search_for_page(search_string)
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
        return await ctx.respond(embed=embed)

    @wikijs_commands.command(name="link", description="Link to the Wiki", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    async def link(self, ctx):
        await ctx.respond(f"{settings.WIKIJS_URL}")


def setup(bot):
    bot.add_cog(Wikijs(bot))
