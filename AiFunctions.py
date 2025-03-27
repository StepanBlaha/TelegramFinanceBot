from binance.client import Client

from CryptoFunctions import Crypto
from UtilsFunctions import Utils

from openai import OpenAI
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()


api_key = os.getenv("OPENAI_KEY")
client = OpenAI(
    api_key=api_key,
)

class AI:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def gptTradeAdvice(self, symbol, period, prices, recent_trades, market_depth):
        """
        Function for determining whether it would be better to buz or sell with the halp of OpenAi
        :param symbol: symbol
        :param period: period of days the data was measured
        :param prices: list of prices
        :param recent_trades: data about recent trades
        :param market_depth: data about market depth
        :return:
        """
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a crypto finance helper. Im gonna give you data about a given crypto and your job is to say whether it would be better to sell or buy. Return only sell or buy"
                },
                {
                    "role": "user",
                    "content": f'Here are the prices of {symbol} over the span of {period} days: {prices}',
                },
                {
                    "role": "user",
                    "content": f'Here are the trade of {symbol} over the span of {period} days: {recent_trades}',
                },
                {
                    "role": "user",
                    "content": f'Here are the market data of {symbol} over the span of {period} days: {market_depth}',
                },
                {
                    "role": "user",
                    "content": f'Based on the data, should i buy or sell',
                },
            ],
        )
        return completion.choices[0].message.content

    def msgChatbot(self, message):
        """
        Function for chating OpenAi
        :param message: message to send to open ai
        :return:
        """
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a crypto finance helper. Keep answers short and simple"
                },
                {
                    "role": "user",
                    "content": message,
                }
            ],
        )
        return completion.choices[0].message.content