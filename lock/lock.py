import asyncio
import discord

from discord.utils import get

from redbot.core import Config, checks, commands
from redbot.core.utils.predicates import MessagePredicate

from redbot.core.bot import Red


class Lock(commands.Cog):
    """
    Lock `@everyone` from sending messages.
    Use `[p]locksetup` first.
    """

    __author__ = "saurichable"
    __version__ = "1.0.1"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=36546565165464, force_registration=True
        )

        default_guild = {"moderator": None, "everyone": True, "ignore": []}

        self.config.register_guild(**default_guild)

    @checks.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.command()
    async def locksetup(self, ctx: commands.Context):
        """ Go through the initial setup process. """
        await ctx.send("Do you use roles to access channels? (yes/no)")
        pred = MessagePredicate.yes_or_no(ctx)
        try:
            await self.bot.wait_for("message", timeout=30, check=pred)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long. Try again, please.")
        if not pred.result:
            await self.config.guild(ctx.guild).everyone.set(True)
        else:
            await self.config.guild(ctx.guild).everyone.set(False)
        await ctx.send("What is your Moderator role?")
        role = MessagePredicate.valid_role(ctx)
        try:
            await self.bot.wait_for("message", timeout=30, check=role)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long. Try again, please.")
        mod_role = role.result
        await self.config.guild(ctx.guild).moderator.set(str(mod_role))

        await ctx.send("You have finished the setup!")

    @checks.mod_or_permissions(manage_roles=True)
    @commands.command()
    @commands.guild_only()
    @checks.bot_has_permissions(manage_channels=True)
    async def lock(self, ctx: commands.Context):
        """ Lock `@everyone` from sending messages."""
        everyone = get(ctx.guild.roles, name="@everyone")
        name_moderator = await self.config.guild(ctx.guild).moderator()
        mods = get(ctx.guild.roles, name=name_moderator)
        which = await self.config.guild(ctx.guild).everyone()

        if not name_moderator:
            return await ctx.send(
                "Uh oh. Looks like your Admins haven't setup this yet."
            )
        if which:
            await ctx.channel.set_permissions(
                everyone, read_messages=True, send_messages=False
            )
        else:
            await ctx.channel.set_permissions(
                everyone, read_messages=False, send_messages=False
            )
        await ctx.channel.set_permissions(mods, read_messages=True, send_messages=True)
        await ctx.send(":lock: Channel locked. Only Moderators can type.")
   

    @checks.mod_or_permissions(manage_roles=True)
    @commands.command()
    @commands.guild_only()
    @checks.bot_has_permissions(manage_channels=True)
    async def hide(self, ctx: commands.Context):
        """ Lock `@everyone` from sending messages."""
        everyone = get(ctx.guild.roles, name="@everyone")
        name_moderator = await self.config.guild(ctx.guild).moderator()
        mods = get(ctx.guild.roles, name=name_moderator)
        which = await self.config.guild(ctx.guild).everyone()

        if not name_moderator:
            return await ctx.send(
                "Uh oh. Looks like your Admins haven't setup this yet."
            )
        if which:
            await ctx.channel.set_permissions(
                everyone, read_messages=False, send_messages=False
            )
        else:
            await ctx.channel.set_permissions(
                everyone, read_messages=False, send_messages=False
            )
        await ctx.channel.set_permissions(mods, read_messages=True, send_messages=True)
        await ctx.send(":no_entry_sign: Channel hidden. Only Moderators can type.")

    @checks.mod_or_permissions(manage_roles=True)
    @commands.command()
    @commands.guild_only()
    @checks.bot_has_permissions(manage_channels=True)
    async def unlock(self, ctx: commands.Context):
        """ Unlock the channel for `@everyone`. """
        everyone = get(ctx.guild.roles, name="@everyone")
        name_moderator = await self.config.guild(ctx.guild).moderator()
        which = await self.config.guild(ctx.guild).everyone()

        if not name_moderator:
            return await ctx.send(
                "Uh oh. Looks like your Admins haven't setup this yet."
            )
        if which:
            await ctx.channel.set_permissions(
                everyone, read_messages=True, send_messages=True
            )
        else:
            await ctx.channel.set_permissions(
                everyone, read_messages=False, send_messages=True
            )
        await ctx.send(":unlock: Channel unlocked.")

