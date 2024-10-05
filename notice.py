from os import getenv

import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from dotenv import load_dotenv

from arguments import *


class Notice(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        self.prefix = URL[:URL.rfind("/")+1]
        self.history = []
        with open("history.txt", "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                self.history.append(line)
        channels = []
        with open("channels.txt", "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                channels.append(self.get_channel(int(line)))
        await self.check.start(channels)

    @tasks.loop(seconds=SLEEP_TIME)
    async def check(self, channels):
        response = requests.get(url=URL)
        soup = BeautifulSoup(response.text, "html.parser")
        titleDivs = soup.find_all("div", {"class": "title"})
        current = []
        for titleDiv in titleDivs:
            if titleDiv.a == None:
                continue
            title: str = titleDiv.a.text
            if title.find(TARGET_CLASS) == -1 or title.find("Re") != -1:
                continue
            href: str = titleDiv.a["href"].split("/")[-1]
            current.append(href)
            if href not in self.history:
                for channel in channels:
                    await channel.send(self.prefix+href)
        self.history = current
        with open("history.txt", "w") as file:
            for href in self.history:
                file.write(href+"\n")


def main():
    load_dotenv()
    bot = Notice(command_prefix='!', intents=discord.Intents().all())
    bot.run(token=getenv(key="TOKEN"))


if __name__ == "__main__":
    main()
