This project aims to use discord as a storage medium
by sending chunk sized files and then reconstructing it.

Additionally it contains functionalities:
1. Scraping discord server messages and saving them as text, csv or your
2. preferred format. This functionality is implemented in
3. discord.py module.

To use backup_maker:
Make sure following packages are installed by:
pip install requests
pip install beautifulsoup4

Then do python backup_maker.py in terminal to run the script
or run in directly through python or Vscode or any other means

It will ask for discord authentication code which is your token.
You can easily get it going into developer mode in any browser, then
going into network tab and sending any message in discord and inspecting the sent message in
network manager, and you will see Authorization code. Enter that into the
script when asked. And then you give guild number, the ID of the server which is just the last number in the
url of the discord chat lounge you in.

example: https://discord.com/channels/550516279652515880/1085627644994916412/1170522572379668562
here the guild ID is the last part which is:1170522572379668562

And now use it. Doing backup asks you to path to the folder you want to backup. 
Note: It will zip all the files so may take some time.

And downloading the backups is self explanatory in the script. Just enter the option as download

Made this project in a hurry. So there may be bugs or room for improvement. If you face any troubles, let me know
