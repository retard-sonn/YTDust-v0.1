import tkinter as tk
from tkinter import ttk
from pytube import YouTube
import threading
import os
from tkinter import filedialog
from ttkthemes import ThemedTk

def select_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(tk.END, folder_path)

def download_video():
    video_url = url_entry.get()
    selected_format = format_var.get()
    download_folder = folder_entry.get()

    try:
        yt = YouTube(video_url)
        video_title = yt.title
        if selected_format == 'MP4':
            video = yt.streams.filter(file_extension='mp4').first()
            file_extension = 'mp4'
        elif selected_format == 'MP3':
            video = yt.streams.filter(only_audio=True).first()
            file_extension = 'mp3'
        elif selected_format == 'WAV':
            video = yt.streams.filter(file_extension='wav').first()
            if not video:
                raise ValueError("No WAV format available for this video.")
            file_extension = 'wav'
        else:
            status_label.config(text="Invalid format.")
            return

        status_label.config(text="Downloading...")
        download_button.config(state=tk.DISABLED)

        progress_bar["value"] = 0
        progress_bar["maximum"] = 100

        thread = threading.Thread(target=download_video_thread, args=(video, video_title, file_extension, download_folder))
        thread.start()

    except Exception as e:
        status_label.config(text="Error: " + str(e))

def download_video_thread(video, video_title, file_extension, download_folder):
    try:
        filename = f"{video_title}.{file_extension}"
        video.download(output_path=download_folder, filename=filename)

        if file_extension == 'mp3':
            convert_to_mp3(video_title, download_folder, filename)

        status_label.config(text="Download completed.")
        download_button.config(state=tk.NORMAL)
    except Exception as e:
        status_label.config(text="Error: " + str(e))

def convert_to_mp3(video_title, download_folder, filename):
    current_filename = f"{download_folder}/{filename}"
    new_filename = f"{download_folder}/{video_title}.mp3"

    os.rename(current_filename, new_filename)

root = ThemedTk(theme="arc")
root.title("YouTube Video Downloader")
root.geometry("400x350")

# Set the path to your custom favicon file


# Set the custom favicon
root.wm_iconbitmap(default="C://Users/user/Documents/Abraar's Python Projects/YT Vid Downloader/favicon.ico")

url_label = ttk.Label(root, text="Enter YouTube Video URL:", font=("bold"))
url_label.pack(pady=10)

url_entry = ttk.Entry(root, width=50)
url_entry.pack()

format_label = ttk.Label(root, text="Select Download Format:", font=("bold"))
format_label.pack(pady=5)

format_var = tk.StringVar(root)
format_var.set('MP4')

format_menu = ttk.OptionMenu(root, format_var, *['MP4', 'MP3', 'MP4', 'WAV'])
format_menu.pack()

folder_label = ttk.Label(root, text="Select Download Folder:", font=("bold"))
folder_label.pack(pady=5)

folder_entry = ttk.Entry(root, width=50)
folder_entry.pack()

select_folder_button = ttk.Button(root, text="Select Folder", command=select_folder)
select_folder_button.pack(pady=5)

download_button = ttk.Button(root, text="Download", command=download_video)
download_button.pack(pady=10)

status_label = ttk.Label(root, text="")
status_label.pack()

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

root.mainloop()
