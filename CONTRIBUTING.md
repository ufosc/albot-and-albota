# Contributing to ALBot and ALBotA

Thank you for helping out with the Open Source Club's Discord bot project!

Please read our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) to understand our community expectations. Check out our discord for any additional questions or just to hangout!

## How do I help

Please check the [Projects](https://github.com/ufosc/albot-and-albota/projects) and [Issues](https://github.com/ufosc/albot-and-albota/issues) for current tasks. If you see something that you would like to help with ask about helping in a comment and we'll assign it too you.

## Report Bug

Check the Issues page to see if someone already reported the bug. If so just like or leave a comment on the issue. If not, please feel free to create a new issue. Make sure that you provide as much detail as possible, including: command, channel/server, which bot, any messages or error messages. Please add a bug label to the issue.

## Request a Feature

Check to see if the feature exists in our [TODO.md](TODO.md). If it is not there, describe the feature and why it would be beneficial. Create an Issue with this information and add the enhancement label.

## Adding to the bot

This section details how to add new functionality to the bot. The official documentation is a great resource [here](https://discordpy.readthedocs.io/en/rewrite/index.html).

### NOTE on asyncio

Discord.py uses asyncio a lot. Asyncio is a library for asynchronous methods and loops. You can find out more information in the offical python docs [here](https://docs.python.org/3/library/asyncio-task.html). All the commands that you define are going to be coroutines, or `async` methods. This just means that they can be ran at the same time/in any order. When you call a async method such as `ctx.send()` you have to put `await` in front of the call, like `await ctx.send()`. This just means that the method will wait for the `ctx.send()` to finish before going on to the next code.

#### Sleeping

To sleep first make sure that there is `import asyncio` in the imports at the top of the file. Then where ever you want to sleep you just have to do

```python
await asyncio.sleep(time_in_seconds)
```

#### Adding a background method

To add a method that runs in the background of your cog put the following in your `__init__` method:

```python
self.task_name = self.bot.loop.create_task(self.background_task())
```

where your background task is something like:

```python
async def background_task(self):
    # Do something here. Probably an endless loop like:
    while True:
        # Check for something
        # Do some other stuff
        await asyncio.sleep(10) # Sleep 10 seconds
```

### Adding single command

First check to see if your command fits a category in the `cogs/` folder. If not go to the next section and read how to create a cog and come back.

Commands are defined using a the decorator `@commands.command()` which can take different parameters

#### Normal command

```python
@commands.command()
async def command_name_here(self, ctx):
    # do stuff here
```

#### To change the command or for the command to not be the name of the method

```python
@commands.command(name="command_name_here")
async def not_command_name(self, ctx):
    # do stuff here
```

#### Sending a message back to the same channel the command is from

```python
@commands.command()
async def command_name_here(self, ctx):
    # Sends "Hello world" back to whoever called this command
    await ctx.send("Hello, world")
```

#### Recieving input with command

```python
@commands.command()
async def test(self, ctx, single_word : str):
    # !test bob
    # single_word = "bob"
```

```python
@commands.command()
async def test(self, ctx, *arr_of_words : str):
    # !test bob is "really cool"
    # arr_of_words = ["bob", "is", "really cool"]
```

```python
@commands.command()
async def test(self, ctx, *, all_text_following : str):
    # !test bob is really cool
    # all_text_following = "bob is really cool"
```

```python
@commands.command()
async def test(self, ctx, a_number : int, *, all_text_following : str):
    # !test 100 wow this is a lot of info
    # a_number = 100
    # all_text_following = "wow this is a lot of info"
```

#### Context

The ctx parameter is required of all commands and very important. It provides context for your command, whether that be the channel that it came from, the author of the message, the guild (server). You also use context to send messages to the channel using `await ctx.send("bla bla")`.

### Adding a Cog

A cog, or extension, is a way of breaking up the code into manageble chunks of commands/functionality. To create a new cog first create a new file in the cogs dir, such as `cogs/wow.py`.

Then create the minimal cog as follows:

```python
import discord
from discord.ext import commands

class Wow:
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Wow(bot))
```

Here you can define your commands following the instructions from the previous section.
Last you can add your cog to the bot by appending "cogs.your_cog" to the list, `startup_cogs` found in `ALBot.py`.

## Closing

If there is still something that you don't understand or think that should go here message @hjarrell .
