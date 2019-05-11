"""
UMass ECE 241 - Advanced Programming
Project #1     Fall 2018
Song.py - Song class
"""

class Song:

    """
    Initial function for Song object.
    parse a given songRecord string to song object.
    For an example songRecord such as "0,Qing Yi Shi,Leon Lai,203.38893,5237536"
    It contains attributes (ID, title, artist, duration, trackID)
    """
    def __init__(self, songRecord):
        songparams = songRecord.split(",")
        self.ID = songparams[0]
        self.title = songparams[1]
        self.artist = songparams[2]
        self.duration = songparams[3]
        self.trackID = songparams[4]

    def toString(self):
        return "Title: " + self.title + ";  Artist: " + self.artist


# WRITE YOUR OWN TEST UNDER THAT IF YOU NEED
if __name__ == '__main__':

    sampleSongRecord = "0,Qing Yi Shi,Leon Lai,203.38893,5237536"
    sampleSong = Song(sampleSongRecord)
    print(sampleSong.toString())