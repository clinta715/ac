import os
import random
import sys
import argparse
import subprocess

class Song:
    def __init__(self, filename, full_path):
        self.filename = filename
        self.full_path = full_path
        parts = os.path.splitext(filename)[0].split(' - ', 1)
        self.artist = parts[0] if len(parts) > 1 else "Unknown Artist"
        self.title = parts[1] if len(parts) > 1 else parts[0]

    def __str__(self):
        return f"{self.title} by {self.artist}"

class Playlist:
    def __init__(self, name, songs):
        self.name = name
        self.songs = songs

    def shuffle(self):
        random.shuffle(self.songs)

    def display(self):
        print(f"\n{'='*60}")
        print(f"  ♫ Playlist: {self.name} ♫  ".center(60))
        print(f"{'='*60}")
        for i, song in enumerate(self.songs, 1):
            print(f"  [{i:02d}] {song}")
        print(f"{'='*60}")

def get_songs_from_folder(folder_path):
    songs = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp3'):
            full_path = os.path.join(folder_path, filename)
            songs.append(Song(filename, full_path))
    return songs

def combine_songs_streaming(playlist, output_file):
    ffmpeg_command = ['ffmpeg', '-y']
    
    for song in playlist.songs:
        ffmpeg_command.extend(['-i', song.full_path])
    
    filter_complex = ''
    for i in range(len(playlist.songs)):
        filter_complex += f'[{i}:0]'
    filter_complex += f"concat=n={len(playlist.songs)}:v=0:a=1[outa]"
    
    ffmpeg_command.extend(['-filter_complex', filter_complex])
    ffmpeg_command.extend(['-map', '[outa]', output_file])
    
    try:
        subprocess.run(ffmpeg_command, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error combining audio: {e.stderr.decode()}")
        sys.exit(1)

def print_title():
    print(r"""
 _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ 
|     |  |  |   __|     |     |   __|_   _| __  |   __|   __|
| | | |  |  |__   |-   -| | | |   __| | | |    -|   __|__   |
|_|_|_|_____|_____|_____|_|_|_|_____| |_| |__|__|_____|_____|
                                                             
 _____ _____ _____ _____ _____ _____ _____ _____ 
|     |   | |   | |   __|  _  |   __| __  |     |
| | | | | | | | | |   __|     |  |  |    -|  |  |
|_|_|_|_|___|_|___|_____|__|__|_____|__|__|_____|
    """)

def print_menu():
    print("\n" + "+"*60)
    print("  Options:".center(60))
    print("+"*60)
    print("  [1] Accept playlist and create combined WAV")
    print("  [2] Reshuffle playlist")
    print("  [3] Quit")
    print("+"*60)

def main(folder_path, output_file):
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        sys.exit(1)

    songs = get_songs_from_folder(folder_path)
    if not songs:
        print(f"No MP3 files found in '{folder_path}'. Exiting.")
        sys.exit(1)

    playlist = Playlist("Auto-generated Playlist", songs)

    print_title()

    while True:
        playlist.display()
        print_menu()

        choice = input("Enter your choice [1-3]: ")

        if choice == '1':
            print("\n" + "*"*60)
            print("  Playlist accepted. Creating combined WAV file...  ".center(60))
            print("*"*60)
            combine_songs_streaming(playlist, output_file)
            print("\n" + "🎉"*20)
            print(f"  Combined WAV file created: {output_file}  ".center(60))
            print("  Enjoy your music!  ".center(60))
            print("🎉"*20)
            break
        elif choice == '2':
            playlist.shuffle()
            print("\n" + "🔀"*20)
            print("  Playlist reshuffled!  ".center(60))
            print("🔀"*20)
        elif choice == '3':
            print("\n" + "👋"*20)
            print("  Quitting without creating combined WAV. Goodbye!  ".center(60))
            print("👋"*20)
            break
        else:
            print("\n" + "❌"*20)
            print("  Invalid choice. Please try again.  ".center(60))
            print("❌"*20)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Music Playlist Manager and Streaming Combiner")
    parser.add_argument("folder", help="Path to the folder containing MP3 files")
    parser.add_argument("output", help="Path for the output combined WAV file")
    args = parser.parse_args()

    main(args.folder, args.output)
