import discord
from discord.ext import commands
import youtube_dl
import pafy

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.song_queue = {}        
        for guild in self.bot.guilds: # Keeps track of the song queue for each discord server that uses the bot. Server if is used as the key.
            self.song_queue[guild.id] = []

    # Stops the current song, plays the next song at the start of the queue, then removes that song from the queue
    async def next_song(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            ctx.voice_client.stop()
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    # Uses youtube_dl to search youtube for what the user inputted. Can return list of URLs or all info available for the search results.
    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    # Uses pafy to play song in the current discord channel. Requires FFMPEG to be installed on machine running the bot.
    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)))
        ctx.voice_client.source.volume = 0.5

    # Join voice channel, must be run before using bot to play music.
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("Must be connected to a voice channel for bot to join")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()

    # Leave voice channel
    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send("Bot is not in a voice channel")

    # Play song from either URL provided or plays the first result when user input is provided to youtube.
    @commands.command()
    async def play(self, ctx, *, song=None):
        if song is None:
            return await ctx.send("Provide a song for the bot to play")

        if ctx.voice_client is None:
            return await ctx.send("Bot must be in a voice channel to play a song")

        # Find URL from youtube for search terms if input is not a URL
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("Searching for song")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send("Could not find a song for that search term")

            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            # Queue Length limited to 10
            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(f"This song is currently at position: {queue_len+1} in the queue")

            else:
                return await ctx.send("Can only queue upto 10 songs at a time")

        await self.play_song(ctx, song)
        await ctx.send("Now playing song")

    # Pause currently playing song
    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_paused():
            return await ctx.send("Song is already paused")

        ctx.voice_client.pause()
        await ctx.send("Current song has been paused.")

    # Resume song
    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("Bot is not in a voice channel")

        if not ctx.voice_client.is_paused():
            return await ctx.send("Song is already playing.")
        
        ctx.voice_client.resume()
        await ctx.send("Song has been resumed")

    # Skip currently playing song
    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("Bot is not playing a song")

        if ctx.author.voice is None:
            return await ctx.send("You must be in a voice channel")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("You are not in the correct voice channel")

        ctx.voice_client.stop()
        await self.next_song(ctx)

    # Searches youtube for users search term and returns URLs for first 5 results
    @commands.command()
    async def search(self, ctx, *, song=None):
        if song is None: return await ctx.send("Please provide a search term")

        await ctx.send("Searching for song")

        info = await self.search_song(5, song)

        embed = discord.Embed(title=f"Results for '{song}':", description="*Use these URLs with the play command to play them*\n", colour=discord.Colour.red())
        
        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1

        embed.set_footer(text=f"Showing the top {amount} results.")
        await ctx.send(embed=embed)

    # Displays the song queue for the server this command was run from
    @commands.command()
    async def queue(self, ctx): 
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("Queue is empty")

        embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.dark_gold())
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"

            i += 1

        embed.set_footer(text="Only 10 songs can be queued at a time.")
        await ctx.send(embed=embed)