from datetime import date, timedelta
import time

# print date and time in yyyy-mm-dd hh:mm format


# print the time 1 minute ago
print(
    date.today() - timedelta(minutes=1),
    time.strftime("%H:%M", time.localtime(time.time() - 60)),
)

