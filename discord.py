from discordwebhook import Discord


class DiscordBot:
    def __init__(self, webhook_url):
        self.discord = Discord(url=webhook_url)
        self.discord_color = int('3498db', 16)

    def discord_message(self, new_line_amount, league):
        message = f"{new_line_amount} New Line Added For {league}" if new_line_amount == 1 \
            else f"{new_line_amount} New Lines Added For {league} on PrizePicks"

        embed = {
            "title": f"{league} Notification",
            "description": message,
            "color": self.discord_color,
        }

        self.discord.post(embeds=[embed])