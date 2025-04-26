from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9 va undan yuqori

timestamp_ms = int(input())
dt_uz = datetime.fromtimestamp(timestamp_ms / 1000, tz=ZoneInfo("Asia/Tashkent"))

print(dt_uz)