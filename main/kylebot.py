import asyncio

import aiofiles
from discord.ext import tasks
import twitch_bot
import discord


class KyleBot(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        f = open("msg.txt", 'r')
        self.data = f.readline()
        print("initial data: " + self.data)


    # async def setup_hook(self):
    #     self.jank.start()

    async def send_message(self, msg):
        print("Sending message")
        channel = self.get_channel(1067680876265226252)
        await channel.send(msg)

    async def on_ready(self):
        print("Discord bot ready")
        await self.send_message("Kylebot is ready")
        self.jank.start()

    @tasks.loop(seconds=5)
    async def jank(self):
        async with aiofiles.open("msg.txt", 'r') as f:
            async for line in f:
                if line != self.data:
                    self.data = line
                    await self.send_message(line)

                print(line)
            await f.close()


if __name__ == "__main__":
    client = KyleBot(intents=discord.Intents.all())
    loop = asyncio.new_event_loop()
    loop.create_task(client.start("MTA2NzY4MTI5MjU5MTgyOTAzNQ.GGvhMO.A-HxbqS9Y1qegngHB9XuvUEOFv5Pl4MoyG5F_A"))
    loop.create_task(twitch_bot.run())
    loop.run_forever()
