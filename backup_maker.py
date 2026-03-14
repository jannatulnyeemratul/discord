import requests
from pathlib import Path
import os
from pathlib import Path
import zipfile
import discord
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0',
    
}

POST_SESSION = requests.Session()

'''requests.post('https://discord.com/api/v9/channels/1481251139759374411/messages',headers=headers,json={'content':'Works'})'''


'''h = requests.post('https://discord.com/api/v9/channels/1481251139759374411/messages', headers=headers,files = {'file': open('ggg.txt', 'rb')})'''




def file_sender(file_path, guild, session_use = False):
    
    if session_use:
        with open(file_path, 'rb') as file:
            POST_SESSION.post('https://discord.com/api/v9/channels/'+str(guild) + '/messages' , headers=headers, files= {'file' : file})
    else:
        with open(file_path, 'rb') as file:
            requests.post('https://discord.com/api/v9/channels/'+str(guild) + '/messages' , headers=headers, files= {'file': file})


def file_sender_2(file,file_name, guild, session_use = False):
    
    if session_use:
        
        POST_SESSION.post('https://discord.com/api/v9/channels/'+str(guild) + '/messages' , headers=headers, files= {'file' : (file_name, file)})
    else:
        
        requests.post('https://discord.com/api/v9/channels/'+str(guild) + '/messages' , headers=headers, files= {'file' : (file_name, file)})



def zip_path(path_to_zip, name_of_the_zip):
    main_path = Path(path_to_zip).resolve()
    with zipfile.ZipFile(name_of_the_zip, 'w') as zipped_file:
        for folder, subfolders, files in os.walk(main_path):
            for file in files:
                if file not in [name_of_the_zip, 'backup.py']:
                    
                    file_path = Path(folder)/file
                    print(file_path)
                    zipped_file.write(file_path,Path.relative_to(file_path, main_path),compress_type=zipfile.ZIP_DEFLATED)
                    print(f'Added {file} in zipp')
                


def part_file_upload(file_name, size_to_partition):
    global guild_id
    total_size = os.path.getsize(file_name) / (1024*1024)

    new_size = size_to_partition

    with open(file_name, 'rb') as file:
        start = 0
        while True:
            content = file.read(1024*1024*size_to_partition)
            if content == b'':
                break

            file_sender_2(content, file_name+ ' ' + str(start),guild_id, session_use=True)
            print(f'{new_size}mb/{total_size}mb Uploaded')

           

            start += 1
            new_size += size_to_partition


def show_data():
    all_data = discord.get_messages(guild_id,message_limit=None)
    formateted_data = []
    initial_name = ''
    started = 0
    track = 0
    for data in all_data:
       
        filename = '_'.join(data['attachments'][0]['filename'].split('_')[0:-1])
        
        if filename != initial_name:
            if started:
                track += 1
            started = 0
            formateted_data.append([])
        if not started:
          
            formateted_data[track].append(filename)
            started = 1
            initial_name = filename

        
    
        
        file_url = data['attachments'][0]['url']
        time_posted = data['timestamp']

        formateted_data[track].append((file_url, time_posted))

    choice = 1
    for data in formateted_data:
        total_size = len(data[1:]) * 10
        time_data = datetime.fromisoformat(data[1][1]).astimezone()
        initial_name = f"{choice}.{data[0]}({total_size}mb)"
        print(f"{initial_name}{(50-len(initial_name))*' '}Posted on  {time_data.strftime('%d %B,%Y  %A %I:%M%p')} ")
        choice+=1

    choice = input('Choose which backup to download(enter x to exit menu) : ')
    if choice == 'x':
        return 0
    data_to_download = formateted_data[int(choice)-1]

    session1 = requests.Session()
    part_count = 1
    with open(data_to_download[0], 'wb') as file:
        total_parts = len(data_to_download) - 1
        total_size = total_parts * 10
        for file_part in range(total_parts, 0, -1):
            
            chunk = session1.get(data_to_download[file_part][0])

            file.write(chunk.content)
            print(f'{10 * part_count}/{total_size}mb downloaded')
            part_count+=1


#Initialization of the program
if Path('Authorization_Token').exists():
    with open('Authorization_Token', 'r') as file:
        AUTHORIZATION_TOKEN = file.read()

else:
    with open('Authorization_Token', 'w') as file:
        AUTHORIZATION_TOKEN = input('Enter Authorization_Token : ')
        file.write(AUTHORIZATION_TOKEN)
    
headers['Authorization'] = AUTHORIZATION_TOKEN
discord.AUTHORIZATION_TOKEN = AUTHORIZATION_TOKEN
guild_id = input('Guild ID : ')


while True:

    print('\n1.Backup Data\n2.Download Backups\n')
    choice = input('choose(enter x to exit menu) : ')
    print()

    if choice == '1':
        filepath = input('Enter The file Path To Backup : ')
        name = input('Name of the Zip : ')
        zip_path(filepath, name)
        part_file_upload(name, 10)

    elif choice == '2':
        show_data()

    elif choice == 'x':
        break

    else:
        print('Invalid Input')

