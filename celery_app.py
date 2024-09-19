from celery import Celery
import task


app = Celery("Football_Bot")
app.config_from_object("celeryconfig")