import os
import requests
import telegram
from time import sleep
#from dotenv import load_dotenv


if __name__ == '__main__':
#    load_dotenv()
    chat_id="204897991"
    #authorization_token = os.getenv("AUTHORIZATION_TOKEN")
    #bot_token = os.getenv("BOT_TOKEN")
    authorization_token = os.environ("AUTHORIZATION_TOKEN")
    bot_token = os.environ("BOT_TOKEN")
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
    
    while True:
        try:
            response = requests.get(url_template, headers=headers, timeout=91, params = {'timestamp': timestamp})
            response.raise_for_status()
            json_data = response.json()
        
            if json_data['status']=="found":
                lesson_data = json_data['new_attempts'][0]
                lesson_title = lesson_data['lesson_title']
                lesson_url = "https://dvmn.org" + lesson_data['lesson_url']
                lesson_result = lesson_data['is_negative']
              
                if lesson_result:
                    lesson_comment = "К сожалению, в работе нашлись ошибки."
                else:
                    lesson_comment = "Преподавателю все понравилось, можно приступать к следующему уроку!"
        
                message_text = text.format(lesson_title, lesson_comment, lesson_url)
                bot.send_message(chat_id = chat_id, text = message_text)
                timestamp = json_data['last_attempt_timestamp']
        
            elif json_data['status']=="timeout":
              timestamp = json_data['timestamp_to_request']
        
        except requests.exceptions.ReadTimeout:
            pass
        
        except requests.ConnectionError:
            connection_error_count += 1
            if connection_error_count == 3:
                sleep(60)
                connection_error_count = 0