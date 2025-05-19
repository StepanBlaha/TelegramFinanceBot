# TelegramFinanceBot
Telegram bot for tracking prices of crypto currencies and getting useful insights on the current market.

## Key Features
- Price of currency over time
- Graphs, dataframes and more informations about various indicators
- Tracking of price changes
- Automated periodical digests of market changes 
- Custom account system for keeping track of users assets
  
## Built with
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

## Requirements
- OpenAI api key
- Telegram Bot api token
- MongoDB uri
- Python version 3.11 or newer
- You can find the list of required libraries and packages in requirements.txt

## Installation Guide
```
git clone https://github.com/StepanBlaha/TelegramFinanceBot
cd TelegramFinanceBot
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```

## Configuration
In OOP/Bot.py change "BOT_KEY" for your telegram bot token:
```
class SBBot:
    def __init__(self):
        self.application = Application.builder().token(os.getenv("BOT_KEY")).build()
        self.add_handlers()
        self.bot = Bot(os.getenv("BOT_KEY"))
        self.create_objects()
```
In OOP/AiFunctions.py change "OPENAI_KEY" for your OpenAI api key:
```
class AI:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_KEY")
        self.client = OpenAI(api_key=self.api_key)
```
In OOP/DatabaseFunctions.py change "MONGO_URI" for your MongoDB uri:
```
class DBBase(abc.ABC):
    def __init__(self, uri=None, db_name="TelegramFinance"):
        """
        Initializes the MongoDB connection.
        """
        if uri is None:
            uri = os.getenv("MONGO_URI")
```
You can find the full setup guide with tips on how to get the telegram bot token in Documentation.pdf

## To run
```
python OOP/Bot.py
```
