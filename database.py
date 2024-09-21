import os
from datetime import datetime, timezone
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values
from collections import Counter
import pytz


class Database:
    def __init__(self, table_name):
        load_dotenv()
        self.connection_params = self.connection_details()
        self.table_name = table_name

    def connection_details(self):
        return {
            "dbname": os.getenv("DATABASE_NAME"),
            "user": os.getenv("DATABASE_USER"),
            "password": os.getenv("DATABASE_PASSWORD"),
            "host": os.getenv("DATABASE_HOST"),
            "port": os.getenv("DATABASE_PORT"),
        }

    def get_existing_data(self):
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    select_query = f"SELECT player_name, team, stat_type, line FROM {self.table_name};"
                    cursor.execute(select_query)
                    existing_data = cursor.fetchall()
            return existing_data
        except psycopg2.Error as e:
            print(f"Error getting data: {e}")
            return []

    def find_new_data(self, new_data, existing_data):
        existing_set = set(
            (record[0], record[1], record[2], record[3]) for record in existing_data
        )
        new_records = []

        for player in new_data:
            record = (
                player.get("player_name"),
                player.get("team"),
                player.get("stat_type"),
                player.get("line"),
                player.get("game_date"),
                player.get("league"),
            )

            if (record[0], record[1], record[2], record[3]) not in existing_set:
                new_records.append(record)

        return new_records

    def insert_new_data(self, new_data):
        new_records = self.find_new_data(
            new_data=new_data, existing_data=self.get_existing_data()
        )
        if new_records:
            try:
                with psycopg2.connect(**self.connection_params) as conn:
                    with conn.cursor() as cursor:
                        last_update = datetime.now()
                        insert_query = f"""
                        INSERT INTO {self.table_name} (player_name, team, stat_type, line, game_date, league, last_updated)
                        VALUES %s;
                        """

                        values = []

                        for record in new_records:
                            values.append(record + (last_update,))

                        execute_values(cursor, insert_query, values)
                        conn.commit()

            except psycopg2.Error as e:
                print(f"Error inserting data: {e}")

            return {"entry_amount": len(new_records), "entry_data": new_records}

        else:
            return {"entry_amount": 0, "entry_data": None}

    # Unused method for now.
    def count_lines(self, record_data):
        record_list = [record[2] for record in record_data["entry_data"]]
        count_records = Counter(record_list)
        return dict(count_records)

    def discord_notification(self, database_object, discord_object, datasource_data, datasource_object=None):
        if datasource_object:
            new_data = datasource_object.get_all_data(datasource_data)
            new_records = database_object.insert_new_data(new_data)

            if new_records["entry_amount"] > 0:
                discord_object.discord_message(
                    new_line_amount=new_records["entry_amount"],
                    league=new_records["entry_data"][0][-1],
                )

    def check_past_date_time(self):
        current_time_utc = datetime.now(timezone.utc)
        mountain_tz = pytz.timezone("America/Edmonton")
        current_time_mountain = current_time_utc.astimezone(mountain_tz)

        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    delete_query = f"""
                       DELETE FROM {self.table_name}
                       WHERE game_date < %s;
                       """

                    # Use the timezone-aware datetime object in the query
                    cursor.execute(delete_query, (current_time_mountain,))
                    conn.commit()
        except psycopg2.Error as e:
            print(f"Error deleting records: {e}")
