import discord
import asyncio
import os
import sqlite3
import random
import datetime
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TOKENS = [os.getenv(f"TOKEN_{i}") for i in range(1, 5)]
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

PERSONALITIES = [
    "You are a degenerate from Reddit's r/wallstreetbets. Talk about stocks, crypto, and 'to the moon'. Use slang like 'HODL', 'Apes', 'Loss porn'. Be aggressive, use 💀, and never give financial advice. Keep it short.",
    "You are a typical r/technology user. Be a cynical, 'actually...' type of person. Demand sources, talk about privacy/AI, and look down on everyone else. Use nerd emojis like 🤓 occasionally.",
    "You are an r/cringe regular. Your job is to find everything second-hand embarrassing. Use 'yikes', 'bruh', 'down bad', or 'touch grass'. Keep it cold and use 🤡.",
    "You are an r/gaming sweat. Everyone is a 'noob' with a 'skill issue'. Use 'L', 'Ratio', 'GG'. Talk in gaming metaphors. Very toxic but funny. Use 'kek' or 'lmao'."
]

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

class RedditBot(discord.Client):
    def __init__(self, token, p_idx, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.personality = PERSONALITIES[p_idx]

    async def on_message(self, message):
        if message.channel.id != CHANNEL_ID or message.author == self.user:
            return

        chance = 0.7 if not message.author.bot else 0.15 
        if random.random() < chance:
           prompt = f"System: {self.personality}\n\nRecent Chat Log:\n{context}\n\nLatest message: {message.content}\n\nReply as your persona in 1 short sentence (max 15 words). No polite AI bullshit."
            response = model.generate_content(prompt)
            await asyncio.sleep(random.uniform(2, 5))
            await message.reply(response.text)

async def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bots = [RedditBot(tk, i, intents=intents) for i, tk in enumerate(TOKENS)]
    await asyncio.gather(*[bot.start(bot.token) for bot in bots])

if __name__ == "__main__":
    asyncio.run(main())
