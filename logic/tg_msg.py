from telegram import Bot

def telegram_message_formatter(order_type: str, order: dict) -> str:
    if order_type != None:
        text = f"""
                    symbol:{order['s']}\n
                    market:{order['ot']}\n
                    last price:{order['ap']}\n
                    position volume:{order['ap']*order['q']}
                    """

        if order_type == 'NEW':
            before = "New Position!\n"
            after = ""
        elif order_type == 'CLOSE':
            before = "Closed Position\n"
            after = f"\nprofit:{order['rp']}"

        return before + text + after


def send_telegram_messages(telegram: dict, text: str) -> list:
    if text != None:
        telegram_response = list()
        for api in telegram:
            bot = Bot(api)
            for user_id in telegram[api]:
                response = bot.send_message(chat_id=user_id, text=text)
                telegram_response.append(response)
        return telegram_response
