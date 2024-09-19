# Football Line Notification Bot

This Discord bot sends notifications when new betting lines for NFL and College Football are released on a gambling website. It uses webhooks to notify users in a Discord channel, indicating how many new lines have been added compared to previously existing ones.

### Features
- Sends notifications to a Discord channel via webhooks when new lines are released.
- Notifies users of the number of new betting lines added for NFL and College Football.
- Utilizes the gambling website’s API to check and compare new lines to existing ones. 

### Installation
1. Clone the repository
2. Create .env variables for your database + discord webhook link.
3. Program was built to be run on a server with Celery/Redis.
