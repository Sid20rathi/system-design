## we are using strategy, factory , singletion, facade , adapter pattern in the code

from abc import ABC, abstractmethod
import random


class song:
    def __init__(self,name,artist):
        self.name = name
        self.artist = artist 


class playlist:
    def __init__(self,name):
        self.name = name
        self.songs =[]
    
    def add_song(self,song:song):
        self.songs.append(song)

class playerstrategy(ABC):
    @abstractmethod
    def play(self,songs:list[song]):
        pass   
class sequenplayer(playerstrategy):
    def play(self,songs:list[song]):
        return songs

class randomplayer(playerstrategy):
    def play(self,songs:list[song]):
        suffled_songs = songs[:]
        random.shuffle(suffled_songs)
        return suffled_songs
class outputdevice(ABC):
    @abstractmethod
    def play(self,song:song):
    
        pass

class bluetoothoutput(outputdevice):
    def play(self,song:song):
        print(f"playing {song.name} by {song.artist} on bluetooth")

class speakeroutput(outputdevice):
    def play(self,song:song):
        print(f"playing {song.name} by {song.artist} on speaker")

class Player:
    def __init__(self, device: outputdevice):
        self.device = device
        self.is_playing = False

    def play_song(self, song: song):
        self.is_playing = True
        self.device.play(song)

    def pause(self):
        self.is_playing = False
        print("Playback paused")


class PlaylistPlayer:
    def __init__(self, player: Player, strategy: playerstrategy):
        self.player = player
        self.strategy = strategy

    def play_playlist(self, playlist: playlist):
        ordered_songs = self.strategy.play(playlist.songs)
        for song in ordered_songs:
            self.player.play_song(song)



class MusicApp:
    def __init__(self, player: Player):
        self.player = player
        self.playlists = {}

    def create_playlist(self, name: str):
        self.playlists[name] = playlist(name)

    def add_song_to_playlist(self, playlist_name: str, song: song):
        self.playlists[playlist_name].add_song(song)

    def play_playlist(self, playlist_name: str, strategy: playerstrategy):
        playlist_player = PlaylistPlayer(self.player, strategy)
        playlist_player.play_playlist(self.playlists[playlist_name])


speaker = speakeroutput()
player = Player(speaker)

spotify = MusicApp(player)

song1 = song("Believer", "Imagine Dragons")
song2 = song("Numb", "Linkin Park")

spotify.create_playlist("Workout")
spotify.add_song_to_playlist("Workout", song1)
spotify.add_song_to_playlist("Workout", song2)

spotify.play_playlist("Workout", sequenplayer())
spotify.play_playlist("Workout", randomplayer())
