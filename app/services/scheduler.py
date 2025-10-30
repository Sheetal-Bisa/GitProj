from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from pytz import timezone
import os

from app.services.notifications import notify_broadcast

_scheduler: BackgroundScheduler | None = None


def start_scheduler(app: FastAPI) -> None:
	global _scheduler
	if _scheduler is not None:
		return
	tz_name = os.getenv("TIMEZONE", "Asia/Kolkata")
	ist = timezone(tz_name)
	_scheduler = BackgroundScheduler(timezone=ist)

	# 6:00 AM IST
	_scheduler.add_job(
		lambda: notify_broadcast(
			"morning",
			"Good morning! 😄 Here's a fun message to start your day! Don't forget water 💧"
		),
		CronTrigger(hour=6, minute=0, timezone=ist),
		id="morning-6am",
		replace_existing=True,
	)

	# 1:00 PM IST
	_scheduler.add_job(
		lambda: notify_broadcast(
			"afternoon",
			"Hi! 🍱 Did you have lunch? How are you feeling right now?"
		),
		CronTrigger(hour=13, minute=0, timezone=ist),
		id="afternoon-1pm",
		replace_existing=True,
	)

	# 9:00 PM IST
	_scheduler.add_job(
		lambda: notify_broadcast(
			"night",
			"Good night 🌙 How was your day today? Want to jot it down?"
		),
		CronTrigger(hour=21, minute=0, timezone=ist),
		id="night-9pm",
		replace_existing=True,
	)

	_scheduler.start()


def shutdown_scheduler() -> None:
	global _scheduler
	if _scheduler:
		_scheduler.shutdown(wait=False)
		_scheduler = None





