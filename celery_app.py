from celery import Celery
import task


app = Celery("Football_bot")
app.config_from_object("celeryconfig")