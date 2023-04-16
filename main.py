#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openai
import logging
from config import TOKEN_BOT, TOKEN_AI

from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Set up ChatGPT API client
openai.api_key = TOKEN_AI
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Hello!")


async def chat(update, context: ContextTypes.DEFAULT_TYPE):
    # Check if message is not None
    try:
        # if update.message and update.message.text:
        # Get user's message
        message = update.message.text
        # Send message to ChatGPT API
        response = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages= [{"role": "user", "content": message}])
        '''
            model= "text-davinci-003",
            prompt=message,
            max_tokens=500,
            temperature=0.3
        '''

        '''
        
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}]
        '''
        print(response)
        # Get response from ChatGPT API
        response_text = response["choices"][0]["message"]["content"]

        # Send response to user
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)

    except Exception as e:
        print(e)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                               text="Error")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN_BOT).build()

    start_handler = CommandHandler('start', start)
    chat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chat)

    application.add_handler(start_handler)
    application.add_handler(chat_handler)

    application.run_polling()
