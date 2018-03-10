import sys
import spotipy
import os
import subprocess
from multiprocessing import Pool
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
        dest_tmp = "%s/%s" % (tmpdir, name)


        if not os.path.exists(dest):
            subprocess.call(['/usr/local/bin/youtube-dl','-f','bestaudio', url,'-o',dest_tmp])
            subprocess.call(['ffmpeg','-i', dest_tmp,'-codec:a','libmp3lame','-qscale:a','0', dest])

    def searchAndDownload(self, name):
        print("> %s" % name)
        url = self.searchVideo(name)
        self.downloadVideo(url, name)
    
    def sync(self):
        token = self.requestToken()
        sp = spotipy.Spotify(auth=token)
        results = sp.user_playlist(self.username, self.playlistid)
        result = [(i['track']['name'],i['track']['artists'][0]['name']) for i in results['tracks']['items']]

        pool = Pool(8)
        pool.map(self.searchAndDownload, [("%s - %s" % (val[1], val[0])) for val in result[::-1]])
