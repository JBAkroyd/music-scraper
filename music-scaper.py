from unicodedata import name
from numpy import equal
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from multiprocessing import Process

class SongData:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

    def __eq__(self, other: 'SongData'):
        if isinstance(other, SongData):
            return self.title == other.title and self.artist == other.artist
        return False
    
    def Print(self):
        print(f"Title:\t{self.title}\t\t\t\tArtist:\t{self.artist}")

def list_songs(song_list):
    for x in song_list:
        x.Print()
    print("---")

# def append_song(song, song_list):
#     if song not in song_list:
#         song_list.append(song)
#     else:
#         print(f"{song} is a duplicate!")
    


def monitor_songs(song_list):
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    url = "https://www.therock.net.nz/home.html"
    driver = webdriver.Firefox(options=firefox_options)
    driver.get(url)
    current_song = SongData("", "")
    while True:
        music_player = driver.find_element(by=By.CLASS_NAME, value='c-NavPlayer-playing')
        music_player_text = music_player.text.split('\n')
        song = SongData(music_player_text[0], music_player_text[1])
        if current_song != song:
            current_song = song
            # move the append to a thread instead of in this method to improve performance
            # p1 = Process(target=append_song, args=(current_song, song_list,))
            # p1.start()
            # p1.join()
            if current_song not in song_list:
                song_list.append(current_song)
            else:
                print(f"{current_song} is a duplicate!")
            p2 = Process(target=list_songs, args=(song_list,))
            p2.start()
            p2.join()

if __name__ == '__main__':
    song_list = []
    monitor_songs(song_list)
