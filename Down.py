import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError
from PIL import ImageTk, Image
import requests
import io

def fetch_video_details():
    url = url_entry.get().strip()
    try:
        # Clean and validate URL
        clean_url = url.split('&')[0]
        yt = YouTube(clean_url)

        # Set video info
        title_label.config(text=f"Title: {yt.title}")
        stream = yt.streams.get_highest_resolution()
        size = round(stream.filesize / (1024 * 1024), 2)
        size_label.config(text=f"Size: {size} MB")

        # Load thumbnail
        response = requests.get(yt.thumbnail_url)
        img_data = response.content
        img = Image.open(io.BytesIO(img_data)).resize((300, 180))
        thumbnail_img = ImageTk.PhotoImage(img)
        thumbnail_label.config(image=thumbnail_img)
        thumbnail_label.image = thumbnail_img

    except VideoUnavailable:
        messagebox.showerror("Error", "Video is unavailable or removed.")
    except RegexMatchError:
        messagebox.showerror("Error", "Invalid YouTube URL.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch video info:\n{e}")

def download_video():
    url = url_entry.get().strip()
    try:
        clean_url = url.split('&')[0]
        yt = YouTube(clean_url)
        stream = yt.streams.get_highest_resolution()

        folder_selected = filedialog.askdirectory()
        if not folder_selected:
            return

        stream.download(output_path=folder_selected)
        messagebox.showinfo("Success", "Video downloaded successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Download failed:\n{e}")

# GUI Setup
root = tk.Tk()
root.title("🎥 YouTube Video Downloader")
root.geometry("500x550")
root.configure(bg="#1e1e2f")

title = tk.Label(root, text="YouTube Video Downloader", font=("Helvetica", 16, "bold"), fg="white", bg="#1e1e2f")
title.pack(pady=10)

url_entry = tk.Entry(root, width=50, font=("Arial", 12))
url_entry.pack(pady=10)
url_entry.insert(0, "Paste YouTube video URL here...")

fetch_button = tk.Button(root, text="Fetch Video Info", font=("Arial", 12), command=fetch_video_details, bg="#6c5ce7", fg="white")
fetch_button.pack(pady=5)

thumbnail_label = tk.Label(root, bg="#1e1e2f")
thumbnail_label.pack(pady=10)

title_label = tk.Label(root, text="Title: ", font=("Arial", 12), fg="white", bg="#1e1e2f")
title_label.pack()

size_label = tk.Label(root, text="Size: ", font=("Arial", 12), fg="white", bg="#1e1e2f")
size_label.pack()

download_button = tk.Button(root, text="Download Video", font=("Arial", 12), command=download_video, bg="#00b894", fg="white")
download_button.pack(pady=20)

root.mainloop()
def fetch_video_details():
    url = url_entry.get().strip()
    try:
        # Clean and validate URL
        clean_url = url.split('&')[0]
        yt = YouTube(clean_url)

        # Set video info
        title_label.config(text=f"Title: {yt.title}")
        stream = yt.streams.get_highest_resolution()
        size = round(stream.filesize / (1024 * 1024), 2)
        size_label.config(text=f"Size: {size} MB")

        # Load thumbnail (check if thumbnail_url exists and is valid)
        thumbnail_url = yt.thumbnail_url
        if thumbnail_url:
            response = requests.get(thumbnail_url)
            if response.status_code == 200:
                img_data = response.content
                img = Image.open(io.BytesIO(img_data)).resize((300, 180))
                thumbnail_img = ImageTk.PhotoImage(img)
                thumbnail_label.config(image=thumbnail_img)
                thumbnail_label.image = thumbnail_img
            else:
                thumbnail_label.config(image='', text="Thumbnail not available")
        else:
            thumbnail_label.config(image='', text="Thumbnail not available")

    except VideoUnavailable:
        messagebox.showerror("Error", "Video is unavailable or removed.")
    except RegexMatchError:
        messagebox.showerror("Error", "Invalid YouTube URL.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch video info:\n{e}")


