import os
from typing import Literal
import sys

Channel = Literal["morning", "afternoon", "night", "custom"]


def _safe_text(s: str) -> str:
	try:
		# On Windows consoles, emojis may cause UnicodeEncodeError; fallback replaces unencodable chars
		return s.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(sys.stdout.encoding or "utf-8", errors="replace")
	except Exception:
		return s


def notify_broadcast(channel: Channel, message: str) -> None:
	print(f"[NOTIFY][{channel}] {_safe_text(message)}")


def notify_user(user_contact: str, message: str) -> None:
	print(f"[NOTIFY][user:{user_contact}] {_safe_text(message)}")

