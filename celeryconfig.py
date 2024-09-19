import os

broker_url = os.getenv("REDIS_TLS_URL", "redis://localhost:6379/0")

imports = ('task',)

# Task to schedule
beat_schedule = {
    "add_data": {
        "task": "task.main",
        "schedule": 120, # In seconds
    }
}