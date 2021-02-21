import discord

# from discord import Forbidden
import csv
from discord.ext.commands import has_permissions
import config
from discord.ext import commands
from modules import new_user
from modules.AddCourseChannel import add_course
from modules.new_user import utils


class AddCourseChannelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(manage_channels=True)
    # except discord.Forbidden:
    #     await ctx.send('I do not have permission to delete this role')
    @commands.command(name="addcourse")
    async def add_course(self, ctx: commands.Context, *args):
        # log in console that a ping was received
        # checking if user is an admin, ie has an admin ID
        # if utils.get_discord_obj(ctx.guild.roles, "ADMIN_ROLE-ID") not in ctx.author.roles:
        #     await ctx.send(
        #         "Sorry, you're not an admin, you are not allowed to add a course. Please contact an admin if you "
        #         "require further assistance.")
        #     # log in console that a ping was received
        #     print("Received addcourse inside IF")
        # else:
        #     # log in console that a ping was received
        names = " ".join(args)
        split_names = names.split(",")

        course_name = split_names[0]
        update_course_name = course_name.strip().replace(" ", "-")
        # update_course_name = "-".join(course_name)  # does this correctly input name?
        update_course_name.lower()
        category_name = split_names[1]
        if not category_name:
            await ctx.send("Please try again with a category name.")
        else:
            update_category_name = "".join(category_name)
            update_category_name.upper()
            await add_course.create_channel(
                ctx, update_course_name, update_category_name
            )
        # log in console that a ping was received


def setup(bot):
    bot.add_cog(AddCourseChannelCog(bot))