import discord
import asyncio
import os
import random
from flask import Flask
from threading import Thread
import google.generativeai as genai

app = Flask('')
@app.route('/')
def home(): return "I'm alive!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

BOT_CONFIGS = [
    {"token": os.getenv("TOKEN_1"), "key": os.getenv("GEMINI_KEY_1"), "idx": 0},
    {"token": os.getenv("TOKEN_2"), "key": os.getenv("GEMINI_KEY_2"), "idx": 1},
    {"token": os.getenv("TOKEN_3"), "key": os.getenv("GEMINI_KEY_3"), "idx": 2},
    {"token": os.getenv("TOKEN_4"), "key": os.getenv("GEMINI_KEY_4"), "idx": 3},
]
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

PERSONALITIES = [
    "r/wallstreetbets degen. Aggressive, loves 'Stonks', uses 💀. Short, toxic.",
    "r/technology nerd. Pretentious, 'actually...' attitude, asks for sources. 🤓",
    "r/cringe user. Cold, judgmental, uses 'yikes', 'bruh'. 🤡",
    "r/gaming sweat. Everyone is a 'noob'. Uses 'L', 'Ratio', 'Skill issue'."
]

class RedditBot(discord.Client):
    def __init__(self, token, api_key, p_idx, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.personality = PERSONALITIES[p_idx]
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')

    async def on_ready(self):
        print(f"Logged in: {self.user.name} with its own API Key.")

    async def on_message(self, message):
        if message.channel.id != CHANNEL_ID or message.author == self.user:
            return

        chance = 0.7 if not message.author.bot else 0.15
        if random.random() < chance:
            async with message.channel.typing():
                prompt = f"System: {self.personality}\nUser said: {message.content}\nReply as a toxic Reditor (max 15 words)."
                try:
                    response = self.model.generate_content(prompt)
                    await asyncio.sleep(random.uniform(2, 4))
                    await message.reply(response.text)
                except Exception as e:
                    print(f"Error for {self.user.name}: {e}")

async def start_bots():
    intents = discord.Intents.default()
    intents.message_content = True

    tasks = []
    for config in BOT_CONFIGS:
        if config["token"] and config["key"]:
            bot = RedditBot(config["token"], config["key"], config["idx"], intents=intents)
            tasks.append(bot.start(bot.token))
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    keep_alive() 
    asyncio.run(start_bots())
