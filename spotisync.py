#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import argparse
import json
import os
from sync import Synchronizer

parser = argparse.ArgumentParser()

CONFIG_FILE = ".spotysinc"


parser.add_argument("action", help='action can be - setup or sync')


args = parser.parse_args()

if args.action not in ['setup','sync']:
    print("Action need to be setup or sync")
    exit()



def SETUP():
    if(os.path.exists(CONFIG_FILE)):
        print("NOTE: config file already exists")

    print("Please create an app https://beta.developer.spotify.com/dashboard/applications")

    client_id = ''
    while client_id == '':
        client_id = input("client_id(Spotify API): ")

    client_secret = ''
    while client_secret == '':
        client_secret = input("client_secret(Spotify API): ")

    redirect_uri = input("redirect_uri(Spotify API, default = 'http://localhost/'): ")

    spotify_playlist = ''
    while spotify_playlist == '' or len(spotify_playlist.split(':'))!=5:
        spotify_playlist = input("Spotify playlist(Open playlist in Spotify app -> Share -> Copy Spotify URI, spotify:user:username:playlist:rxTBAdD1dzrS5BlOJd1AjE) ")
        if(len(spotify_playlist.split(':'))!=5):
            print('Incorrect playlist URI, it need to be in format - `spotify:user:username:playlist:rxTBAdD1dzrS5BlOJd1AjE`')

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': 'http://localhost/' if redirect_uri == '' else redirect_uri,
        'spotify_playlist': spotify_playlist.split(':')[-1],
        'user_name': spotify_playlist.split(":")[2]
    }

    with open(CONFIG_FILE,"w") as outfile:
        json.dump(data, outfile)

    print("DONE!")
def getSetup():
    with open(CONFIG_FILE) as json_data_file:
        return json.load(json_data_file)



if args.action == 'setup':
    SETUP()
elif args.action == 'sync':
    if not os.path.exists(CONFIG_FILE):
        SETUP()

    setup = getSetup()
    synchronizer = Synchronizer(client_id=setup['client_id'], client_secret=setup['client_secret'], username=setup['user_name'],
                                playlistid=setup['spotify_playlist'], redirect_url=setup['redirect_uri'])
    synchronizer.sync()


