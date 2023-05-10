import vlc
import glob
import time
import os 

base_folder = '/home/group5/Desktop/mmlab/Control-Bluetooth-Devices-by-Gesture-Recognition/music'
song_name = os.listdir(base_folder)
song_name = sorted(song_name)
playlist = glob.glob(base_folder + "/" + "*.mp3")
playlist = sorted(playlist)

def set_uri(uri):
    media_player.set_mrl(uri)

# 暫停
def pause():
    media_player.pause()

# 恢復
def resume():
    media_player.set_pause(0)
    
# 停止
def stop():
    media_player.stop()
    
# 釋放資源
def release():
    return media_player.release()

# 獲取當前音量（0~100）
def get_volume():
    return media_player.audio_get_volume()

# 設置音量（0~100）
def set_volume(volume):
    return media_player.audio_set_volume(volume)

def next_song(index):
    index += 1
    return index
def previous_song(index):
    index -= 1
    return index
    
inst = vlc.Instance('--no-xlib --quiet ') 
media_player = vlc.MediaPlayer()
set_uri(playlist[10])

media_player.play()
time.sleep(0.1)
idx = 10

set_volume(50)
while True:
    time.sleep(30.0)
    stop()

    idx = previous_song(idx)
    set_uri(playlist[idx])
    media_player.play()
    print(song_name[idx])

    
    
    