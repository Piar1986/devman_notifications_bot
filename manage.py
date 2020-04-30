import logging
import os
import requests
import telegram
from time import sleep
from dotenv import load_dotenv


logger = logging.getLogger("notifications_bot")

class MyLogsHandler(logging.Handler):

    def emit(self, record):
        log_entry = self.format(record)
        bot.send_message(chat_id = chat_id, text = log_entry)


def send_bot_start_message():
    logger.warning('Бот запущен')


def send_bot_error_message():
    logger.warning('Бот упал с ошибкой:')
    logger.error(err, exc_info=True)


if __name__ == '__main__':
    load_dotenv()
    authorization_token = os.environ['TELEGRAM_AUTHORIZATION_TOKEN']
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    bot = telegram.Bot(token = bot_token)    
    connection_error_count = 0
    timestamp = ''
    text = """
    У Вас проверили работу «{}»
    
    {}
    
    {}
    """
    url_template = 'https://dvmn.org/api/long_polling/'
    headers = {"Authorization": authorization_token}
    
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())
    send_bot_start_message()
    
    while True:
        try:
            while True:
                try:
                    response = requests.get(url_template, headers=headers, timeout=91, params = {'timestamp': timestamp})
                    response.raise_for_status()
                    response_result = response.json()
                    lesson_status = response_result['status']
                    
                    if lesson_status=="found":
                        lesson_information = response_result['new_attempts'][0]
                        lesson_title = lesson_information['lesson_title']
                        lesson_url = f"https://dvmn.org{lesson_information['lesson_url']}"
                        lesson_result = lesson_information['is_negative']
                      
                        if lesson_result:
                            lesson_comment = "К сожалению, в работе нашлись ошибки."
                        else:
                            lesson_comment = "Преподавателю все понравилось, можно приступать к следующему уроку!"
                
                        message_text = text.format(lesson_title, lesson_comment, lesson_url)
                        bot.send_message(chat_id = chat_id, text = message_text)
                        timestamp = response_result['last_attempt_timestamp']
                
                    elif lesson_status=="timeout":
                      timestamp = response_result['timestamp_to_request']
                
                except requests.exceptions.ReadTimeout:
                    pass
                
                except requests.ConnectionError:
                    connection_error_count += 1
                    if connection_error_count == 3:
                        sleep(60)
                        connection_error_count = 0
        except Exception as err:
            send_bot_error_message()