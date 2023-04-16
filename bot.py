#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openai
#from config import TOKEN_BOT, TOKEN_AI
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import os
import json

DB_JSON = "db_message.json"

# Set up ChatGPT API client
openai.api_key = os.environ['TOKEN_AI']
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Напишите первый вопрос:")


async def chat(update, context: ContextTypes.DEFAULT_TYPE):
    global state
    # Check if message is not None
    try:
        # if update.message and update.message.text:
        # Get user's message
        message = update.message.text
        if os.path.isfile(DB_JSON):
            with open(DB_JSON, 'r') as f:
                data = json.load(f)
        else:
            data = {}
        chat_id = str(update.message.chat_id)
        print(1, chat_id,data.keys())

        if chat_id in data:
            history_message = data[chat_id] + [{"role": "user", "content": message}]
        else:
            history_message = [{"role": "user", "content": message}]

        while True:
            len_m = 0
            for d in history_message:
                len_m += len(d["content"])
            if len_m < 4096:
                break
            history_message = history_message[1:]

        response = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages=history_message)

        response_text = response["choices"][0]["message"]["content"]
        data[chat_id] = history_message + [{"role": "assistant", "content": response_text}]

        print(2, chat_id,data.keys())

        print(response["model"], response["usage"])

        with open(DB_JSON, 'w') as f:
            json.dump(data, f)

        await context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)

    except Exception as e:
        print("Error chat GPT:", e)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                               text="Error")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ['TOKEN_BOT']).build()

    start_handler = CommandHandler('start', start)
    chat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chat)

    application.add_handler(start_handler)
    application.add_handler(chat_handler)

    application.run_polling()
