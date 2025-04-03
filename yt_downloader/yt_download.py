import yt_dlp

URL = input("Enter your URL: ")
destination = "/path/to/Downloads/folder"

try:
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best[ext=webm]/best',  
        'outtmpl': f'{destination}/%(title)s.%(ext)s',
        'noplaylist': True, 
        'merge_output_format': None,  
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])
    
    print(f"Downloaded to {destination}.")
except Exception as e:
    print(f"An error occurred: {e}")
