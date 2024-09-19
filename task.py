from celery_app import app
from database import Database
from cfb import CFB
from nfl import NFL
from discord import DiscordBot
import os
from dotenv import load_dotenv


@app.task()
def main():
    load_dotenv()

    cfb_data = CFB()
    cfb_db = Database(table_name="CFB")
    discord = DiscordBot(os.getenv("DISCORD_WEBHOOK"))
    cfb_db.check_past_date_time()
    cfb_db.discord_notification(
        database_object=cfb_db,
        discord_object=discord,
        datasource_data=cfb_data.cfb_data,
        datasource_object=cfb_data,
    )

    nfl_data = NFL()
    nfl_db = Database(table_name="NFL")
    nfl_db.check_past_date_time()
    nfl_db.discord_notification(
        database_object=nfl_db,
        discord_object=discord,
        datasource_data=nfl_data.nfl_data,
        datasource_object=nfl_data,
    )
