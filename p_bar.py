import time
import os
from pyrogram.errors import FloodWait
from datetime import timedelta

class Timer:
    def __init__(self, time_between=5):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

def hrb(value, digits=2, delim="", postfix=""):
    if value is None:
        return None
    chosen_unit = "B"
    for unit in ("KiB", "MiB", "GiB", "TiB"):
        if value > 1024:
            value /= 1024
            chosen_unit = unit
        else:
            break
    return f"{value:.{digits}f}{delim}{chosen_unit}{postfix}"

def hrt(seconds, precision=0):
    pieces = []
    if seconds is None:
        return "-"
    value = timedelta(seconds=int(seconds))

    if value.days:
        pieces.append(f"{value.days}d")

    s = value.seconds

    if s >= 3600:
        hours = int(s / 3600)
        pieces.append(f"{hours}h")
        s -= hours * 3600

    if s >= 60:
        minutes = int(s / 60)
        pieces.append(f"{minutes}m")
        s -= minutes * 60

    if s > 0 or not pieces:
        pieces.append(f"{s}s")

    if not precision:
        return "".join(pieces)

    return "".join(pieces[:precision])

timer = Timer()

# Designed by Mendax (fixed syntax & safe progress message)
async def progress_bar(current, total, reply, start):
    try:
        if not timer.can_send():
            return

        now = time.time()
        diff = now - start
        if diff < 1:
            return

        perc = f"{current * 100 / total:.1f}%"
        elapsed_time = max(1, int(diff))
        speed = current / elapsed_time if elapsed_time > 0 else 0
        remaining_bytes = max(0, total - current)

        if speed > 0:
            eta_seconds = remaining_bytes / speed
            eta = hrt(eta_seconds, precision=1)
        else:
            eta = "-"

        sp = hrb(speed) + "/s"
        tot = hrb(total)
        cur = hrb(current)

        # progress bar
        bar_length = 10
        completed_length = int(current * bar_length / total) if total > 0 else 0
        completed_length = min(bar_length, max(0, completed_length))
        remaining_length = bar_length - completed_length
        progress_bar_str = "▰" * completed_length + "▱" * remaining_length

        message = (
            "╭──⌯════🌟 U P L O A D I N G 🌟════⌯──╮\n"
            f"├ {progress_bar_str} {perc}\n"
            f"├ Speed ➜ {sp}\n"
            f"├ ETA ➜ {eta}\n"
            f"├ {cur} / {tot}\n"
            "╰──────────────────────────────────╯"
        )

        # Use edit_text for Pyrogram message editing
        await reply.edit_text(message)

    except FloodWait as e:
        time.sleep(e.x)
    except Exception:
        # ignore other transient errors to avoid crashing progress updates
        pass
