
# Done By Rohan Khadka
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random

class UIComponent:
    def __init__(self, master):
        self.master = master

    def create_widget(self):
        pass

class Header(UIComponent):
    def create_widget(self):
        header = tk.Frame(self.master, bg="red", height=50)
        header.pack(fill=tk.X)
        logo = tk.Label(header, text="YouTube", fg="white", bg="red", font=("Arial", 16, "bold"))
        logo.pack(side=tk.LEFT, padx=10)
        
        search_frame = tk.Frame(header, bg="red")
        search_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=20)
        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, ipady=5)
        search_button = tk.Button(search_frame, text="Search", command=self.search)
        search_button.pack(side=tk.LEFT, padx=5)

    def search(self):
        query = self.search_entry.get()
        print(f"Searching for: {query}")
        # Here you would typically update the video grid based on the search

class Sidebar(UIComponent):
    def create_widget(self):
        sidebar = tk.Frame(self.master, bg="gray", width=150)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        buttons = ["Home", "Trending", "Subscriptions", "Library"]
        for button in buttons:
            tk.Button(sidebar, text=button, width=15).pack(pady=5)

class VideoGrid(UIComponent):
    def create_widget(self):
        self.grid = tk.Frame(self.master)
        self.grid.pack(expand=True, fill=tk.BOTH)
        self.update_grid()

    def update_grid(self):
        for widget in self.grid.winfo_children():
            widget.destroy()
        
        for i in range(3):
            for j in range(3):
                frame = tk.Frame(self.grid, width=200, height=150, bg="lightgray", bd=1, relief=tk.RAISED)
                frame.grid(row=i, column=j, padx=10, pady=10)
                frame.pack_propagate(False)
                
                # Placeholder for video thumbnail
                thumbnail = tk.Label(frame, bg="gray", width=180, height=100)
                thumbnail.pack(pady=(5, 0))
                
                title = tk.Label(frame, text=f"Video {i*3+j+1}", wraplength=180)
                title.pack(pady=(5, 0))
                
                views = tk.Label(frame, text=f"{random.randint(100, 1000000)} views", fg="gray")
                views.pack()

class VideoPlayer(UIComponent):
    def create_widget(self):
        player = tk.Frame(self.master, bg="black", height=400)
        player.pack(fill=tk.X, pady=10)
        
        # Placeholder for video
        video = tk.Label(player, bg="gray", text="Video Player", fg="white", font=("Arial", 24))
        video.pack(expand=True, fill=tk.BOTH)
        
        controls = tk.Frame(player, bg="lightgray", height=30)
        controls.pack(fill=tk.X)
        play_button = tk.Button(controls, text="Play")
        play_button.pack(side=tk.LEFT, padx=5)
        pause_button = tk.Button(controls, text="Pause")
        pause_button.pack(side=tk.LEFT, padx=5)

class Comments(UIComponent):
    def create_widget(self):
        comments = tk.Frame(self.master)
        comments.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(comments, text="Comments", font=("Arial", 16, "bold")).pack(anchor=tk.W)
        
        self.comment_entry = tk.Text(comments, height=3)
        self.comment_entry.pack(fill=tk.X, pady=5)
        
        submit_button = tk.Button(comments, text="Submit Comment", command=self.submit_comment)
        submit_button.pack(anchor=tk.W)
        
        self.comments_list = tk.Frame(comments)
        self.comments_list.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Add some sample comments
        self.add_comment("User1", "Great video!")
        self.add_comment("User2", "Very informative, thanks for sharing!")

    def submit_comment(self):
        comment = self.comment_entry.get("1.0", tk.END).strip()
        if comment:
            self.add_comment("You", comment)
            self.comment_entry.delete("1.0", tk.END)

    def add_comment(self, user, text):
        comment_frame = tk.Frame(self.comments_list, bg="lightgray", bd=1, relief=tk.SUNKEN)
        comment_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(comment_frame, text=user, font=("Arial", 10, "bold"), bg="lightgray").pack(anchor=tk.W, padx=5, pady=(5,0))
        tk.Label(comment_frame, text=text, wraplength=400, justify=tk.LEFT, bg="lightgray").pack(anchor=tk.W, padx=5, pady=(0,5))

class YouTubeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube-like Interface")
        self.geometry("800x600")
        
        self.header = Header(self)
        self.sidebar = Sidebar(self)
        self.video_grid = VideoGrid(self)
        self.video_player = VideoPlayer(self)
        self.comments = Comments(self)
        
        self.create_ui()
    
    def create_ui(self):
        self.header.create_widget()
        self.sidebar.create_widget()
        self.video_grid.create_widget()
        self.video_player.create_widget()
        self.comments.create_widget()

if __name__ == "__main__":
    app = YouTubeApp()
    app.mainloop()