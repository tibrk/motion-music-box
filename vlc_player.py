import os
from vlc import Instance


class VLC:
    def __init__(self):
        self.Player = Instance('--loop')

    def addPlaylist(self, path: str):
        self.mediaList = self.Player.media_list_new()
        songs = os.listdir(path)
        for s in songs:
            self.mediaList.add_media(
                self.Player.media_new(os.path.join(path, s)))
        self.listPlayer = self.Player.media_list_player_new()
        self.listPlayer.set_media_list(self.mediaList)

    def play(self):
        self.listPlayer.play()

    def next(self):
        self.listPlayer.next()

    def pause(self):
        self.listPlayer.pause()

    def previous(self):
        self.listPlayer.previous()

    def stop(self):
        self.listPlayer.stop()
