from abc import ABC, abstractmethod

class song():
    def __init__(self,name):
        self.name = name


class Playlist():
    def __init__(self):
        self.songs=[]
    

    def add_song(self,song):
        self.songs.append(song)


class Iterator(ABC):
    @abstractmethod
    def hasNext(self):
        pass
    def Next(self):
        pass


class Playlist_iterator(Iterator):

    def __init__(self,playlist):
        self.songs = playlist.songs
        self.index =0

    
    def hasNext(self):
        return self.index <len(self.songs)
    
    def Next(self):

        song = self.songs[self.index]
        self.index +=1
        return song


song1 = song("beliver")
song2 = song("thunder")

playlist = Playlist()
playlist.add_song(song1)
playlist.add_song(song2)

it = Playlist_iterator(playlist)

while it.hasNext():
    song = it.Next()
    print(song.name)

