import time
from unicodedata import name
from numpy import equal
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from multiprocessing import Process

class SongData:
    def __init__(self, title: str, artist: str):
        self.title = title.lower()
        self.artist = artist.lower()

    def __eq__(self, other: 'SongData'):
        if isinstance(other, SongData):
            return self.title == other.title and self.artist == other.artist
        return False
    
    def Print(self):
        print(f"Title: {self.title} Artist: {self.artist}")

def list_songs():
    for x in song_list:
        x.Print()
    print("---")

# appends a song to the song_list
def append_song(song: SongData):
    if song not in song_list:
        song_list.append(song)
    else:
        print(f"Title: {song.title} Artist: {song.artist} is a duplicate!")
    

def monitor_songs(driver):
    music_player = driver.find_element(by=By.CLASS_NAME, value='c-NavPlayer-playing')
    music_player_text = music_player.text.split('\n')
    song = SongData(music_player_text[0], music_player_text[1])
    current_song = song_list[-1] if len(song_list) > 0 else SongData("","")
    if current_song != song:
        current_song = song
        append_song(current_song)

if __name__ == '__main__':
    global song_list
    song_list = []
    # configure web driver to scrape javascript webpage
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    url = "https://www.therock.net.nz/home.html"
    driver = webdriver.Firefox(options=firefox_options)
    driver.get(url)
    while True:
        monitor_songs(driver)
        list_songs()
        time.sleep(10)
