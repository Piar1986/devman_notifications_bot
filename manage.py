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
        bot.send_message(chat_id = telegram_chat_id, text = log_entry)


def send_bot_start_message():
    logger.warning('Бот запущен')


def send_bot_error_message():
    logger.warning('Бот упал с ошибкой:')
    logger.error(err, exc_info=True)


def send_bot_notification_message(message_text):
    bot.send_message(chat_id = telegram_chat_id, text = message_text)


def get_lesson_information(response_result):
    lesson = response_result['new_attempts'][0]
    lesson_title = lesson['lesson_title']
    lesson_url = f"https://dvmn.org{lesson['lesson_url']}"
    lesson_result = lesson['is_negative']
                      
    if lesson_result:
        lesson_comment = "К сожалению, в работе нашлись ошибки."
    else:
        lesson_comment = "Преподавателю все понравилось, можно приступать к следующему уроку!"

    return lesson_title, lesson_comment, lesson_url


def get_message_text(lesson_title, lesson_comment, lesson_url):
    text = """
    У Вас проверили работу «{}»
    
    {}
    
    {}
    """
    message_text = text.format(lesson_title, lesson_comment, lesson_url)
    return message_text


def get_response_result(timestamp):
    url_template = 'https://dvmn.org/api/long_polling/'
    headers = {"Authorization": devman_authorization_header}
    response = requests.get(url_template, headers=headers, timeout=91, params = {'timestamp': timestamp})
    response.raise_for_status()
    response_result = response.json()
    return response_result


def process_response_result(response_result):
    response_status = response_result['status']
    if response_status=="found":
        lesson_title, lesson_comment, lesson_url = get_lesson_information(response_result)
        message_text = get_message_text(
            lesson_title, 
            lesson_comment, 
            lesson_url
            )
        send_bot_notification_message(message_text)
        timestamp = response_result['last_attempt_timestamp']
                
    elif response_status=="timeout":
        timestamp = response_result['timestamp_to_request']
    return timestamp


if __name__ == '__main__':
    load_dotenv()
    devman_authorization_header = f"Token {os.environ['DEVMAN_AUTHORIZATION_TOKEN']}"
    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
    bot = telegram.Bot(token = telegram_bot_token)    
    connection_error_count = 0
    timestamp = ''

    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())
    send_bot_start_message()
    
    while True:
        try:
            while True:
                try:
                    response_result = get_response_result(timestamp)
                    process_response_result(response_result)
                
                except requests.exceptions.ReadTimeout:
                    pass
                
                except requests.ConnectionError:
                    connection_error_count += 1
                    if connection_error_count == 3:
                        sleep(60)
                        connection_error_count = 0
        except Exception as err:
            send_bot_error_message()