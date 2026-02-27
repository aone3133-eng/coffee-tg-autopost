import os
import random
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
TG_CHAT_ID = os.environ["TG_CHAT_ID"]

TZ = ZoneInfo("Europe/Moscow")

def tg_send_message(text: str) -> None:
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": text,
        "disable_web_page_preview": True,
    }
    r = requests.post(url, json=payload, timeout=30)
    r.raise_for_status()

def generate_post(kind: str) -> str:
    sell = [
        "☕️ Кофе + любая выпечка = 370₽.\n\nЕсли хочется посытнее — можно заменить на пирог, сэндвич или бургер с доплатой 50₽.",
        "Комбо дня: кофе и выпечка за 370₽ ☕️\n\nПросто, вкусно и без лишнего.",
    ]

    vibe = [
        "Иногда лучший план — это кофе и 10 минут тишины ☕️\n\nЗабегайте, мы на месте.",
        "Погода меняется, а хороший кофе остаётся ☕️",
    ]

    engage = [
        "Что выбираете чаще?\n\n1 — капучино\n2 — латте\n3 — раф\n4 — матча\n\nПишите цифру в комментариях 👇",
        "Какой вкус добавить в меню этой весной? Напишите идею 👇",
    ]

    contest = [
        "🎁 Конкурс!\n\nРазыгрываем 3 кофе.\n\nЧтобы участвовать:\n— поставьте реакцию\n— напишите любимый напиток в комментариях\n\nИтоги завтра вечером.",
    ]

    if kind == "sell":
        return random.choice(sell)
    if kind == "vibe":
        return random.choice(vibe)
    if kind == "engage":
        return random.choice(engage)
    return random.choice(contest)

def choose_kind(now: datetime):
    wd = now.weekday()  # 0=Mon
    if wd == 0:
        return "sell"
    if wd == 2:
        return "vibe"
    if wd == 4:
        return "engage"
    if wd == 5:
        return "contest"
    return None

def main():
    now = datetime.now(TZ)
    kind = choose_kind(now)

    if not kind:
        print("Сегодня нет публикации.")
        return

    text = generate_post(kind)
    tg_send_message(text)
    print("Пост опубликован:", kind)

if __name__ == "__main__":
    main()
