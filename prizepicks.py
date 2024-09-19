from datetime import datetime, timedelta
from unidecode import unidecode
import requests

class PrizePicks:
    def api_call(self, projection_id):
        return requests.get(f"https://partner-api.prizepicks.com/projections?league_id={projection_id}").json()


    def get_stats(self, football_data):
        player_stats = []

        for stats in football_data["data"]:
            if stats["attributes"]["odds_type"] == "standard":
                start_time_str = stats["attributes"]["start_time"]
                prizepick_time = datetime.fromisoformat(start_time_str)
                formatted_timestamp = prizepick_time.isoformat()

                player_stats.append({
                    "player_id": stats["relationships"]["new_player"]["data"]["id"],
                    "game_date": formatted_timestamp,
                    "line": stats["attributes"]["line_score"],
                    "stat_type": stats["attributes"]["stat_type"],
                })

        return player_stats

    def get_player_information(self, player_stats, football_data):
        for player_id in player_stats:
            for player in football_data["included"]:
                if player_id["player_id"] == player["id"]:
                    player_id["player_name"] = unidecode(player["attributes"]["display_name"])
                    player_id["team"] = f"{player['attributes']['market']} {player['attributes']['team_name']}"
                    player_id["league"] = player["attributes"]["league"]
                    break

        return player_stats


    def get_all_data(self, league_data):
        player_stats_data = self.get_stats(league_data)
        all_league_data = self.get_player_information(player_stats=player_stats_data, football_data=league_data)
        return all_league_data