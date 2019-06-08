"""
A lot of this code is from the discord.py examples folder: https://github.com/Rapptz/discord.py/blob/rewrite/examples/playlist.py
The Youtube_DL code is from: https://github.com/CarlosFdez/SpueBox
Licenses can be found in the LICENSE file in the root dir
"""

import discord
from discord.ext import commands
import asyncio
import youtube_dl

class VoiceEntry:

    """A class that represents a song that can be played"""
    def __init__(self, message, player, title, uploader, duration):
        self.requester = message.author
        self.channel = message.channel
        self.player = player
        self.title = title
        self.uploader = uploader
        self.duration = duration

    def __str__(self):
        fmt = '*{0}* uploaded by {1} and requested by {2.display_name}'
        if self.duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(self.duration, 60))
        return fmt.format(self.title, self.uploader, self.requester)

class VoiceState:
    """Holds the queued song and players for a guild server"""
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        return self.voice.is_playing()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.voice.stop()
        self.current = None
        if not self.songs.empty():
            self.toggle_next()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.current.channel.send('Now playing ' + str(self.current))
            self.voice.play(self.current.player)
            await self.play_next_song.wait()

class Music(commands.Cog, name='Music'):
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await channel.connect()
        state = self.get_voice_state(channel.guild)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(no_pm=True)
    async def vjoin(self, ctx, *, channel : discord.VoiceChannel):
        """Joins a voice channel."""
        try:
            await self.create_voice_client(channel)
        except discord.InvalidArgument:
            await ctx.send('This is not a voice channel...')
        except discord.ClientException:
            await ctx.send('Already in a voice channel...')
        else:
            await ctx.send('Ready to play audio in ' + channel.name)

    @commands.command(no_pm=True)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        if ctx.message.author.voice:
            summoned_channel = ctx.message.author.voice.channel
            if summoned_channel is None:
                await ctx.send('You are not in a voice channel.')
                return False

            state = self.get_voice_state(ctx.message.guild)
            if state.voice is None:
                state.voice = await summoned_channel.connect()
            else:
                await state.voice.move_to(summoned_channel)

        return True

    @commands.command(no_pm=True)
    async def play(self, ctx, *, song : str):
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(ctx.message.guild)
        opts = {
            'format': 'bestaudio/best',
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        try:
            ydl = youtube_dl.YoutubeDL(opts)
            info = ydl.extract_info(song, download=False)

            if not info:
                raise Exception("Error extracting")

            if '_type' in info and info['_type'] == 'playlist':
                entries = info['entries']
            else:
                entries = [info]

            results = [(e['title'], e['url'], e['uploader'], e['duration']) for e in entries]

            player = discord.FFmpegPCMAudio(results[0][1])
            player = discord.PCMVolumeTransformer(player) # Transforms the player so volume can be changed
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await ctx.send(fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player, results[0][0], results[0][2], results[0][3])
            await ctx.send('Enqueued ' + str(entry))
            await state.songs.put(entry)

    @commands.command(no_pm=True)
    async def volume(self, ctx, value : int):
        """Sets the volume of the currently playing song."""

        state = self.get_voice_state(ctx.message.guild)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            await ctx.send('Set the volume to {:.0%}'.format(player.volume))

    @commands.command(no_pm=True)
    async def pause(self, ctx):
        """Pauses the currently played song."""
        state = self.get_voice_state(ctx.message.guild)
        if state.is_playing():
            # player = state.player
            # player.pause()
            state.voice.pause()

    @commands.command(no_pm=True)
    async def resume(self, ctx):
        """Resumes the currently played song."""
        state = self.get_voice_state(ctx.message.guild)
        if not state.is_playing():
            # player = state.player
            # player.resume()
            state.voice.resume()

    @commands.command(no_pm=True)
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        server = ctx.message.guild
        state = self.get_voice_state(server)

        if state.is_playing():
            state.voice.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass

    @commands.command(no_pm=True)
    async def skip(self, ctx):
        """Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        state = self.get_voice_state(ctx.message.guild)
        if not state.is_playing():
            await ctx.send('Not playing any music right now...')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await ctx.send('Requester requested skipping song...')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                await ctx.send('Skip vote passed, skipping song...')
                state.skip()
            else:
                await ctx.send('Skip vote added, currently at [{}/3]'.format(total_votes))
        else:
            await ctx.send('You have already voted to skip this song.')

    @commands.command(no_pm=True)
    async def playing(self, ctx):
        """Shows info about the currently played song."""

        state = self.get_voice_state(ctx.message.guild)
        if state.current is None:
            await ctx.send('Not playing anything.')
        else:
            skip_count = len(state.skip_votes)
            await ctx.send('Now playing {} [skips: {}/3]'.format(state.current, skip_count))

def setup(bot):
    if not discord.opus.is_loaded():
        # the 'opus' library here is opus.dll on windows
        # or libopus.so on linux in the current directory
        # you should replace this with the location the
        # opus library is located in and with the proper filename.
        # note that on windows this DLL is automatically provided for you
        discord.opus.load_opus('opus')
    bot.add_cog(Music(bot))
