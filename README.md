## Spotisync - download and sync your spotify playlist in 1 click

![Demo](https://raw.githubusercontent.com/albertaleksieiev/spotisync/content/demo.gif)

### Dependencies

```
Python3
ffmpeg
spotipy
youtube-dl
```

### Usage
Firstly you need to create your Spotify app and retreive keys, you can do this on this [webpage](https://beta.developer.spotify.com/dashboard/applications)<br>
##### 1. Create an app
Navigate to [https://beta.developer.spotify.com/dashboard/applications](https://beta.developer.spotify.com/dashboard/applications) and create an APP.
![](https://i.imgur.com/atEgOws.png)
##### 2. Add redirect url
Open your app in dashboard, press **EDIT SETTINGS** and add redirect url - `http://localhost/`
![](https://i.imgur.com/6Wr9OUf.png)
##### 3. Retreive keys
Open your app and retreive a keys!
![](https://i.imgur.com/LHTobIW.png)

##### 4. Launch an app and SYNC!
Navigate to the directory in which you want to sync a playlist, and run `spotisync.py sync`. In the first launch, it will prompt to enter app keys and Spotify playlist URI. Also, you can run `spotisync.py setup` to re-setup. **Note: currently each directory in which script was runned can have only 1 playlist to sync, and each directory need to have finished configuration(`spotisync.py setup`)**

![](https://i.imgur.com/vQaaRie.png)


