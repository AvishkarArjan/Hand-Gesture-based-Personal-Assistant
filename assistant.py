import os
import pygame
import tkinter as tk
from tkinter import filedialog

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("400x200")
        
        self.current_track = tk.StringVar()
        self.track_list = []
        
        label = tk.Label(self.root, textvariable=self.current_track)
        label.pack()
        
        # folder_path = filedialog.askdirectory()
        folder_path = r"C:\Users\Avishkar Arjan\Music"
        self.track_list.extend([os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.mp3')])
        self.current_track.set(self.track_list[0])
        
        # load_button = tk.Button(self.root, text="Load Folder", command=self.load_folder)
        # load_button.pack()
        
        play_button = tk.Button(self.root, text="Play", command=self.play_music)
        play_button.pack()
        
        pause_button = tk.Button(self.root, text="Pause", command=self.pause_music)
        pause_button.pack()
        
        # resume_button = tk.Button(self.root, text="Resume", command=self.resume_music)
        # resume_button.pack()
        
        stop_button = tk.Button(self.root, text="Stop", command=self.stop_music)
        stop_button.pack()
        
        next_button = tk.Button(self.root, text="Next", command=self.next_track)
        next_button.pack()
        
        prev_button = tk.Button(self.root, text="Previous", command=self.prev_track)
        prev_button.pack()
        
        pygame.init()
        pygame.mixer.init()
        
    # def load_folder(self):
        
        
    def play_music(self):
        pygame.mixer.music.load(self.current_track.get())
        pygame.mixer.music.play()
        
    def pause_music(self):
        if pygame.mixer.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        
    # def resume_music(self):
    #     pygame.mixer.music.unpause()
        
    def stop_music(self):
        pygame.mixer.music.stop()
        
    def next_track(self):
        pygame.mixer.music.stop()
        current_index = self.track_list.index(self.current_track.get())
        next_index = (current_index + 1) % len(self.track_list)
        self.current_track.set(self.track_list[next_index])
        pygame.mixer.music.load(self.current_track.get())
        pygame.mixer.music.play()
        
    def prev_track(self):
        pygame.mixer.music.stop()
        current_index = self.track_list.index(self.current_track.get())
        prev_index = (current_index - 1) % len(self.track_list)
        self.current_track.set(self.track_list[prev_index])
        pygame.mixer.music.load(self.current_track.get())
        pygame.mixer.music.play()

if __name__ == "__main__":
    root = tk.Tk()
    player = MusicPlayer(root)
    root.mainloop()
