import pygame
import random

class Player:
    def __init__(self):
        self._songs = [
            r'C:\Users\User\OneDrive\Desktop\project\PP2\pr9\music_player\music\Lauren Creviston, Brynn Elise - Wrong Places (SPOTISAVER).mp3',
            r'C:\Users\User\OneDrive\Desktop\project\PP2\pr9\music_player\music\Malcolm Todd - Original (SPOTISAVER).mp3',
            r'C:\Users\User\OneDrive\Desktop\project\PP2\pr9\music_player\music\Michael Jackson - You Rock My World (SPOTISAVER).mp3',
            r'C:\Users\User\OneDrive\Desktop\project\PP2\pr9\music_player\music\The Beatles - Help! - Remastered 2009 (SPOTISAVER) (1).mp3'
        ]
        self.shuffled_queue = list(self._songs)
        random.shuffle(self.shuffled_queue)
        
        self.current_track_index = 0
        self.current_song_name = 'No song playing'
        self.paused = False

    def play_current(self):
        song = self.shuffled_queue[self.current_track_index]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        some = song.replace(r'C:\\git_practice\\Practice9\\player\\music\\', '')
        self.current_song_name = some.replace('.mp3', '')

        self.paused = False

    def next_song(self):
        if self.current_track_index < len(self.shuffled_queue) - 1:
            self.current_track_index += 1
        else:
            self.current_track_index = 0
            random.shuffle(self.shuffled_queue)
        self.play_current()

    def prev_song(self):
        if self.current_track_index > 0:
            self.current_track_index -= 1
        else:
            self.current_track_index = len(self.shuffled_queue) - 1
        self.play_current()

    def pause(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True