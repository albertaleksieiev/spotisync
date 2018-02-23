import sys
import spotipy
import os
import subprocess

import tempfile

class Synchronizer(object):
    def __init__(self, client_id, client_secret, redirect_url, username, playlistid):
        self.username = username
        self.playlistid = playlistid
        self.redirect_url = redirect_url
        self.client_id = client_id
        self.client_secret = client_secret


    def requestToken(self):
        import spotipy.util as util

        scope = 'user-library-read'
        username =  self.username
        token = util.prompt_for_user_token(username, scope,
                                           client_id=self.client_id,
                                           client_secret=self.client_secret,
                                           redirect_uri=self.redirect_url)
        return token



    def searchVideo(self, text):
        import urllib
        from bs4 import BeautifulSoup
        from urllib.request import urlopen

        query = urllib.parse.quote(text)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html,  "html.parser")
        for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
           return 'https://www.youtube.com' + vid['href']
        return ""

    def downloadVideo(self, url, name):
        if url == "":
            print("Cannot find url!")
            return

        if not os.path.exists("./audio"):
            os.mkdir("./audio")

        dest = "./audio/%s.mp3" % name
        tmpdir = tempfile.mkdtemp()
        dest_tmp = "%s/%s.mp3" % (tmpdir, name)


        print(dest_tmp)
        if not os.path.exists(dest):
            subprocess.call(['/usr/local/bin/youtube-dl','--extract-audio','--audio-format',"mp3",'--audio-quality','0', url,'-o', dest_tmp])
            subprocess.call(['ffmpeg','-i', dest_tmp, dest])


    def sync(self):
        token = self.requestToken()
        sp = spotipy.Spotify(auth=token)
        results = sp.user_playlist(self.username, self.playlistid)
        result = [(i['track']['name'],i['track']['artists'][0]['name']) for i in results['tracks']['items']]


        for key, val in enumerate(result[::-1]):
            name = ("%s - %s" % (val[1], val[0]))
            print("(%d/%d) > %s" %(key + 1,len(result),name))

            url = self.searchVideo(name)
            self.downloadVideo(url, name)
