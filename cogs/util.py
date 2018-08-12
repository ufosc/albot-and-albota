import discord

def is_officer_check(ctx):
    '''Check to see if the author is an officer'''
    return discord.utils.get(ctx.message.author.roles, name='officer') is not None
