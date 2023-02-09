from discord_webhook import DiscordWebhook, DiscordEmbed
from bs4 import BeautifulSoup
from bot.utils import feed as feed_func
from dotenv import load_dotenv
import asyncio
from os import environ
from json import loads

load_dotenv(".env")
blacklisted_words = loads(environ["BLACKLISTED_WORDS"])
last_triggered_id = None


async def main():
    while True:
        data = feed_func()
        feed = data[0]
        thread_ids = data[1]

        webhook = DiscordWebhook(url=environ["WEBHOOK_URL"], rate_limit_retry=True)
        for entry in feed:
            thread_ids.append(entry["id"])
            embed = DiscordEmbed(color=0x7289da)
            embed.set_author(name="Hypixel - Minecraft Server and Maps")
            embed.set_title(entry["title"])
            embed.set_url(entry["link"])

            soup = BeautifulSoup(entry["summary"], "html.parser")
            text = soup.get_text()

            for word in blacklisted_words:
                text.replace(word, "<REDACTED>")

            embed.set_description(text)
            webhook.add_embed(embed)
            webhook.avatar_url = "https://cdn.discordapp.com/attachments/746444509226991686/937884437482455060/" \
                                 "Screenshot_2022-01-15_163712.png"
            webhook.execute()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
