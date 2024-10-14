import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pygame
import os
import random  # To simulate fluctuations for the visualizer

# Initialize pygame mixer for audio playback
pygame.mixer.init()

class MusicPlayer:
    def __init__(self, window):
        self.window = window
        self.window.title("Music Player")
        self.window.geometry("1024x768")
        self.window.config(bg="#3399ff")


        # Set window icon (favicon-like)
        icon = tk.PhotoImage(file='Player.ico.PNG')  
        root.iconphoto(False, icon)
        
        # Define song list and current song index
        self.song_list = []
        self.current_song_index = 0
        self.is_paused = False
        self.is_dragging = False  # To manage manual progress control

        style = ttk.Style(self.window)
        style.configure("TScale", troughcolor="gray", background="#3399ff")

        # Create the layout
        self.create_layout()

        # Update the progress bar regularly
        self.update_progress()

        # Update the animated visual
        self.animate_visual()

    def create_layout(self):
        """Create the layout of the music player window."""
        
        # Toolbar area (simulated menu bar)
        toolbar = tk.Frame(self.window, bg="#d3d3d3", height=30, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Add a file button in the toolbar
        file_btn = tk.Button(toolbar, text="File", command=self.add_songs, bg="#d3d3d3", relief=tk.FLAT)
        file_btn.pack(side=tk.LEFT, padx=5)

        # Add a playlist button in the toolbar
        playlist_btn = tk.Button(toolbar, text="Playlist", command=self.show_playlist, bg="#d3d3d3", relief=tk.FLAT)
        playlist_btn.pack(side=tk.LEFT, padx=5)


        # Canvas for animated visual effect
        self.visual_canvas = tk.Canvas(self.window, width=1600, height=600, bg="black")
        self.visual_canvas.pack(pady=10)

                # Progress bar with time labels
        progress_frame = tk.Frame(self.window)
        progress_frame.pack(pady=10)

        # Elapsed time on the left
        self.elapsed_time_label = tk.Label(progress_frame, text="00:00",bg="#d3d3d3", fg="black", font=("Arial", 12),)
        self.elapsed_time_label.grid(row=0, column=0, padx=10)

        # Progress bar in the middle
        self.progress = ttk.Scale(progress_frame, from_=0, to=100, orient='horizontal', length=1400, command=self.on_progress_drag)
        self.progress.grid(row=0, column=1)

        # Total time on the right
        self.total_time_label = tk.Label(progress_frame, text="00:00", bg="#d3d3d3", fg="black", font=("Arial", 12))
        self.total_time_label.grid(row=0, column=2, padx=10)

        # Control Buttons (grid layout inside a frame)
        controls_frame = tk.Frame(self.window, bg="#f0f0f0")
        controls_frame.pack(pady=20)


        # Music control buttons (previous, play/pause, next)
        prev_button = tk.Button(controls_frame, text="⏮", command=self.prev_song, width=10)
        prev_button.grid(row=0, column=0, padx=10)

        self.play_button = tk.Button(controls_frame, text="⏯", command=self.play_pause_song, width=10)
        self.play_button.grid(row=0, column=1, padx=10)

        next_button = tk.Button(controls_frame, text="⏭", command=self.next_song, width=10)
        next_button.grid(row=0, column=2, padx=10)

        # Volume button
        volume_button = tk.Button(controls_frame, text="🔊", command=self.show_volume_control, width=10)
        volume_button.grid(row=0, column=3, padx=10)


        # Playlist (Listbox for the songs)
        self.playlist_box = tk.Listbox(self.window, bg="#ffffff", height=10, width=50)
        self.playlist_box.pack(pady=20)
        self.playlist_box.bind("<<ListboxSelect>>", self.on_playlist_select)

        # Status bar for showing current song or status
        self.status_bar = tk.Label(self.window, text="No song playing", bd=1, relief=tk.SUNKEN, anchor=tk.NE)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Volume control slider (hidden initially)
        self.volume_control = None

    def play_pause_song(self):
        if len(self.song_list) == 0:
            return
        
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.play_button.config(text="⏯")
            self.status_bar.config(text=f"Playing: {os.path.basename(self.song_list[self.current_song_index])}")
        elif pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_paused = True
            self.play_button.config(text="⏯")
            self.status_bar.config(text="Music Paused")
        else:
            self.play_song(self.song_list[self.current_song_index])

    def next_song(self):
        if len(self.song_list) > 0:
            self.current_song_index = (self.current_song_index + 1) % len(self.song_list)
            self.play_song(self.song_list[self.current_song_index])

    def prev_song(self):
        if len(self.song_list) > 0:
            self.current_song_index = (self.current_song_index - 1) % len(self.song_list)
            self.play_song(self.song_list[self.current_song_index])

    def play_song(self, song_path):
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(loops=0)
        self.play_button.config(text="⏯")
        self.status_bar.config(text=f"Playing: {os.path.basename(song_path)}")

        # Get song duration and update total time label
        song_length = pygame.mixer.Sound(song_path).get_length()
        self.total_time_label.config(text=self.format_time(song_length))
        self.progress.config(to=song_length)

    def format_time(self, seconds):
        """Convert time in seconds to a string format (MM:SS)."""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def add_songs(self):
        songs = filedialog.askopenfilenames(title="Choose Songs", filetypes=[("Audio Files", "*.mp3 *.wav")])
        for song in songs:
            self.song_list.append(song)

        self.update_playlist_box()

    def show_playlist(self):
        if self.playlist_box.winfo_ismapped():
            self.playlist_box.pack_forget()
        else:
            self.playlist_box.pack(pady=20)

    def update_playlist_box(self):
        self.playlist_box.delete(0, tk.END)
        for song in self.song_list:
            self.playlist_box.insert(tk.END, os.path.basename(song))

    def on_playlist_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.current_song_index = index
            self.play_song(self.song_list[index])

    def update_progress(self):
        if pygame.mixer.music.get_busy() and not self.is_dragging:
            current_time = pygame.mixer.music.get_pos() // 1000  # Convert milliseconds to seconds
            song_length = pygame.mixer.Sound(self.song_list[self.current_song_index]).get_length()
            self.progress['to'] = song_length
            self.progress.set(current_time)
            self.elapsed_time_label.config(text=self.format_time(current_time))
        self.window.after(1000, self.update_progress)

    def on_progress_drag(self, value):
        """Seek song when dragging progress bar."""
        if not self.is_dragging:
            return

        pygame.mixer.music.set_pos(float(value))

    def on_progress_click(self, event=None):
        """Start dragging progress."""
        self.is_dragging = True

    def on_progress_release(self, event=None):
        """Stop dragging progress."""
        self.is_dragging = False
        pygame.mixer.music.set_pos(self.progress.get())

    def show_volume_control(self):
        if self.volume_control:
            self.volume_control.destroy()
            self.volume_control = None
        else:
            self.volume_control = tk.Scale(self.window, from_=0, to=1, orient='horizontal', resolution=0.1, command=self.change_volume)
            self.volume_control.pack(pady=10)

    def change_volume(self, event=None):
        volume = self.volume_control.get()
        pygame.mixer.music.set_volume(volume)

    def animate_visual(self):
        """ Simulate fluctuating visual effect with random bars. """
        self.visual_canvas.delete("all")  # Clear the canvas
        if pygame.mixer.music.get_busy():
            for i in range(100):  # Draw 10 fluctuating bars
                height = random.randint(10, 1000)  # Simulate amplitude fluctuation
                x0 = 40 * i + 10
                x1 = 40 * (i + 1)
                self.visual_canvas.create_rectangle(x0, 650 - height, x1, 650, fill="green")

        self.window.after(1600, self.animate_visual)  # Update visual every 100ms


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
