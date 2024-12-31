from tkinter import *
import yt_dlp
from PIL import Image, ImageTk
import threading

#function to download video
def download_video():
    video_url = url_entry.get()
    path_url = path_entry.get()

    if not video_url:
        error_msg.pack()
        return

    #function to display the progress in GUI
    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
            download_button.config(text=f"Downloading: {percent:.2f}%", bg="white", fg="black")
            sr.update_idletasks()

    def download_thread():
        ydl_opts = {
            'outtmpl': f'{path_url}/%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
            'format': 'best',
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=True)
                title = info_dict.get('title', 'No title available')
                view_count = info_dict.get('view_count', 'No view count available')
                duration = info_dict.get('duration', 'No duration available')
                uploader = info_dict.get('uploader', 'No uploader available')
                upload_date = info_dict.get('upload_date', 'No upload_date available')

            download_button.config(text="Download Complete!", bg="green", fg="white")
            progress_label.config(text=f"Title: {title}\nViews: {view_count}\nUploaded by: {uploader}\nUploaded on: {upload_date[6:]}/{upload_date[4:6]}/{upload_date[:4]}\nDuration: {duration} sec", fg="white",height=6)
            progress_label.pack()
        except Exception as e:
            download_button.config(text="Error", bg="red", fg="white")
            progress_label.config(text=f"Error: {str(e)}", fg="red")
            progress_label.pack()

    download_button.config(text="Starting download...", bg="white", fg="black")
    threading.Thread(target=download_thread, daemon=True).start()

#Create main frame
sr = Tk()
sr.configure(background="black") 
sr.title("Video Downloader GUI") 
sr.iconbitmap("D:/Sathya/Python/utube_b&w.ico")  
sr.geometry("800x450")
sr.configure(bg="black")
Label(sr, text="VIDEO DOWNLOADER",font="Algerian", bg="black", fg="white").pack(pady=5)

# Input fields
Label(sr, text="Enter local PATH for download:", bg="black", fg="white").pack(pady=5)
path_entry = Entry(sr, width=50)
path_entry.pack(pady=5)

Label(sr, text="Enter YouTube Video URL:",bg="black", fg="white").pack(pady=5)
url_entry = Entry(sr, width=50)
url_entry.pack(pady=5)

error_msg = Label(sr, text="Error! Please enter a valid URL.", fg="red", font=("Arial", 12), bg="black")

# Download button
download_button = Button(sr, text="Download", command=download_video, bg="white", fg="black")
download_button.pack(pady=10)

progress_label = Label(sr, text="", font=("Arial Rounded MT Bold", 13), bg="black", fg="black")
progress_label.pack(pady=10)

#loop in main frame
sr.mainloop()
