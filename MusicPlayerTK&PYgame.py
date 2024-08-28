import tkinter as tk
from tkinter import filedialog
import pygame

pygame.mixer.init()  # first ma mixer initialize garako
pygame.display.init()  # tyo display ko initialize garako

class MusicPlayer:
    def __init__(self, root):  # root is the main window, constructor of the class
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("450x350")
        self.root.configure(bg="light blue")
        self.root.resizable(False, False)

        # Create frame for buttons
        frame = tk.Frame(self.root, bg="light blue")
        frame.pack(pady=20)

        # Create buttons according to the needs
        self.play_button = tk.Button(frame, text="Play", command=self.play_music)
        self.play_button.grid(row=0, column=0, padx=10)

        self.pause_button = tk.Button(frame, text="Pause", command=self.pause_music)
        self.pause_button.grid(row=0, column=1, padx=10)

        self.stop_button = tk.Button(frame, text="Stop", command=self.stop_music)
        self.stop_button.grid(row=0, column=2, padx=10)

        self.resume_button = tk.Button(frame, text="Resume", command=self.resume_music)
        self.resume_button.grid(row=0, column=3, padx=10)

        self.load_button = tk.Button(frame, text="Load", command=self.load_music)
        self.load_button.grid(row=0, column=4, padx=10)

        # Label to display the music file path
        self.song_label = tk.Label(self.root, text="No song Loaded", font=("Helvetica", 12))
        self.song_label.pack(fill="x")

        # Listbox to display the list of loaded songs
        self.song_listbox = tk.Listbox(self.root, font=("Helvetica", 12))
        self.song_listbox.pack(fill="both", expand=True)
        self.song_listbox.bind('<<ListboxSelect>>', self.on_song_select)

        # Variable to hold the song paths
        self.song_paths = []
        self.current_song_index = 0

        # Check for pygame events
        self.check_pygame_events()

    def load_music(self):
        self.song_paths = filedialog.askopenfilenames(filetypes=[("Music Files", "*.mp3")])
        if self.song_paths:
            self.song_label.config(text=f"Loaded: {len(self.song_paths)} songs")
            self.display_loaded_songs()

    def display_loaded_songs(self):
        self.song_listbox.delete(0, tk.END)
        for song_path in self.song_paths:
            self.song_listbox.insert(tk.END, song_path.split('/')[-1])

    def on_song_select(self, event):   # yo chai kina gareako vanda aaba maile song select gare vane tyo play garna lai
        selected_index = self.song_listbox.curselection()
        if selected_index:
            self.current_song_index = selected_index[0]

    def play_music(self):
        if self.song_paths:
            pygame.mixer.music.load(self.song_paths[self.current_song_index])
            pygame.mixer.music.play()
            pygame.mixer.music.set_endevent(pygame.USEREVENT)

    def play_next_song(self):
        self.current_song_index += 1
        if self.current_song_index < len(self.song_paths):
            pygame.mixer.music.load(self.song_paths[self.current_song_index])
            pygame.mixer.music.play()
        else:
            self.current_song_index = 0

    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_song_index = 0

    def resume_music(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()

    def check_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.play_next_song()
        self.root.after(100, self.check_pygame_events)

# Create root window
root = tk.Tk()
music_player = MusicPlayer(root)
root.mainloop()