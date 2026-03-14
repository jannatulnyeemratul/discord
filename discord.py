
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0',
    
}

AUTHORIZATION_TOKEN = ''
TEMP_SESSION_SEND_MESSAGE = False


BASE_LINK = 'https://discord.com/api/v9/channels/'


def get_messages(guild_id,message_limit = 100, save=False, into_parts = False):

    global AUTHORIZATION_TOKEN
    headers['Authorization'] = AUTHORIZATION_TOKEN
    base_url = BASE_LINK + str(guild_id) + '/messages?limit=100'
    messages = []
    content_chunk = ''
    addition = ''
    url_before = '&before='
    session1 = requests.Session()
    
    total_message = 0
    temp_total = 0

    if save:

        with open('discord_data.csv', 'a') as file:
            file.write('Username,Message,TimeStamp,User_ID,Message_ID\n')

    while True:
        try:
            site = session1.get(base_url + addition, headers = headers)
            content_chunk = site.json()
            if content_chunk == [] or total_message == message_limit:
                if save:
                    print('Saving all data')
                    with open('discord_data.csv', 'a') as file:
                        for data in messages:
                            username = data['author']['username']
                            timestamp = data['timestamp']
                            id = data['author']['id']
                            message = data['content']
                            message_id = data['id']

                            to_save = ','.join([username, message, timestamp,id, message_id]) +'\n'
                            file.write(to_save)
                return messages
            
            if into_parts and (temp_total >= into_parts):
                print('Saving all data')
                with open('discord_data.csv', 'a') as file:
                    for data in messages:
                        username = data['author']['username']
                        timestamp = data['timestamp']
                        id = data['author']['id']
                        message = data['content']
                        message_id = data['id']

                        to_save = ','.join([username, message, timestamp,id, message_id]) +'\n'
                        file.write(to_save)
                    
                messages = []
                    
                print(total_message, 'messages are collected in total')
                   
                temp_total = 0
                addition = url_before + content_chunk[-1]['id']
                continue
            
            
            
            messages += content_chunk

            total_message += 100
            temp_total += 100

                

            addition = url_before + content_chunk[-1]['id']

        except:
            if save:
                print('Saving all data')
                with open('discord_data.csv', 'a') as file:
                    file.write('data=' + str(messages))
            return messages



def send_message(guild_id, json_data):

    global TEMP_SESSION_SEND_MESSAGE
    headers['Authorization'] = AUTHORIZATION_TOKEN

    if TEMP_SESSION_SEND_MESSAGE:
        session1 = TEMP_SESSION_SEND_MESSAGE
    else:
        session1 = requests.Session()

    
    session1.post('https://discord.com/api/v9/channels/' + str(guild_id) + '/messages', json=json_data, headers=headers)


