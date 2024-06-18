from pytube import YouTube
from pytube import Playlist
from pytube.exceptions import RegexMatchError
from pytube.exceptions import VideoUnavailable

import os
import sys
import subprocess
import argparse


class Ytmp3:

    def __init__(self, cliOut=True):
        self.cliOut = cliOut # Set to False for no command line output
        self.isAudioOnly = True
        self.isPlaylist = True
        self.videoQuality = ""
        self.statusMessage = "Idle"
        self.errorList = []

    #prints status messages to console
    def print_status(self):
        if self.cliOut: print(self.statusMessage)

    #prints list of errors from playlist mode
    def print_errors(self):
        #if command line output is enabled
        if self.cliOut:
            #and playlist mode was used
            if ytmp3.isPlaylist:
                #and errors occurred
                if ytmp3.errorList:
                    #header
                    print("\nErrors:")
                    #contents
                    for error in ytmp3.errorList:
                        print(error)
                    #end space
                    print("\n")

    #function for adding prefix to file names
    def addPrefix(self, fileName, prefix):
        #adding prefix
        newfileName = prefix+fileName
        #renaming file on system
        try:
            #this can fail if a file with this name already exists
            os.rename(fileName, newfileName)
        except:
            #remove existing file
            os.remove(newfileName)
            #reattempt
            os.rename(fileName, newfileName)

        return newfileName

    #Used to check if a given url is a valid YouTube link
    def check_url(self, url):
        try:
            checkUrl = YouTube(url)
            return True

        except RegexMatchError:
            return False

    #gets the filename of downloaded video
    def get_file_name(self, path):
        pathList = path.split("\\")
        fileName = pathList[len(pathList)-1]
        return fileName

    #Selects resolution for video download
    def select_resolution(self, Yt):
        #Grab applicable streams
        out = Yt.streams.filter(adaptive=True, file_extension="mp4").order_by("resolution")

        #if resolution spcified
        if self.videoQuality:
            #gets correct stream for specified resolution
            for stream in out:
                if self.videoQuality in str(stream):
                    return stream
        else:
            #returns highest available resolution video stream if none specified
            return (out.last())

    #runs ffmpeg command
    def run_ffmpeg(self, command):
        try:
            #attemp to run ffmpeg
            subprocess.run(command)
        except:
            #attempt to run ffmpeg bundled with ytmp3
            command = command+'./'
            subprocess.run(command)

    #Converts an mp4 to an mp3
    def convert_to_mp3(self, fileName):
        #Remove file extension
        sep = fileName.split(".")
        #Append .mp3
        outputFile = (sep[0]+".mp3")

        #Construct ffmpeg command
        command = ('ffmpeg/ffmpeg.exe -y -loglevel quiet -i "'+fileName+'" "'+outputFile+'"')
        #run ffmpeg
        self.run_ffmpeg(command)

        #Delete mp4 file
        os.remove(fileName)

    def stitch_audio_video(self, audio, video, output):
        #Construct ffmpeg command
        command = ('ffmpeg/ffmpeg.exe -y -loglevel quiet -i "'+audio+'" -i "'+video+'" "'+output+'"')
        #run ffmpeg
        self.run_ffmpeg(command)

        #delete mp4 files
        os.remove(audio)
        os.remove(video)

    #Downloads one video, returns true on success and false on failure
    def download_video(self, url, itemCount=1):
        #updating status
        self.statusMessage = ("\nitem "+str(itemCount)+": Downloading..")
        self.print_status()
        #catching unavailable videos
        try:
            Yt = YouTube(url)
        except VideoUnavailable:
            self.statusMessage = "Download failed: Video unavailable"
            self.print_status()
            return False

        #catching age restricted videos
        try:
            #Select highest quality audio stream
            Stream = Yt.streams.get_audio_only()
        except:
            self.statusMessage = "Download failed: Video is age restricted"
            self.print_status()
            return False

        #attempt download
        try:
            fileName = self.get_file_name(Stream.download())
            #doing this to preserve the original file name for stitching
            fileNameAudio = fileName

        except:
            self.statusMessage = ("Download failed: Audio stream")
            self.print_status()
            return False

        #Convert to mp3 for audio only downloads
        if self.isAudioOnly:
            self.statusMessage = "Converting to mp3"
            self.print_status()

            self.convert_to_mp3(fileNameAudio)

            #updating status
            self.statusMessage = ("Done")
            self.print_status()
            return True

        #Downloading audio and video streams
        else:
            #Since the audio and video files will have the same name
            #we need to rename one to prevent it being overwritten(both mp4)
            fileNameAudio = self.addPrefix(fileNameAudio, "aud")

            try:
                #Select the correct itag based on resolution choice
                Stream = self.select_resolution(Yt)
                #Attempt to download video at selected resolution
                fileNameVideo = self.get_file_name(Stream.download())

            except AttributeError:
                #User entered resolution that is not available for the video
                self.statusMessage = ("resolution unavailable, check video settings on youtube")
                self.print_status()
                return False

            #ffmpeg cannot output a file with the same name as input file
            #need to rename it also
            fileNameVideo = self.addPrefix(fileNameVideo, "vid")

            self.statusMessage = "stitching.."
            self.print_status()
            #stitch video and audio together
            self.stitch_audio_video(fileNameAudio, fileNameVideo, fileName)

            #updating status
            self.statusMessage = ("Done")
            self.print_status()
            return True

    #Downloads whole playlist
    def playlist_download(self, url):
        P = Playlist(url)
        itemCount = 1

        #Download all videos in playlist
        for vid in P.video_urls:

            #attempt download
            if not self.download_video(vid, itemCount):
                #every failure is apended to the error list
                self.errorList.append("Item "+str(itemCount)+": "+self.statusMessage)

            itemCount+=1

    #Run the program
    def run(self, url):

        #reset success flag
        downloadSuccess = False
        #Reset error list
        self.errorList=[]
        #Check input url is valid YouTube url
        if self.check_url(url):

            #Detect if the url for the video provided by the user is part of a playlist
            if "list" in url and self.isPlaylist:
                self.playlist_download(url)
            else:
                downloadSuccess = self.download_video(url)
        else:
            self.statusMessage = "Invalid Url"
            self.print_status()

        #Printing errors list
        self.print_errors()

        #End message
        self.statusMessage = "Downloads complete"
        self.print_status()


#CLI
if __name__ == "__main__":
    #overriding error func to display help message
    class HelpfulArgParse(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            self.print_help()
            sys.exit(2)

    # Initialize parser
    parser = HelpfulArgParse()

    #Required arguments
    parser.add_argument('url', action='store', help = "url for youtube video")

    # Optinal arguments
    parser.add_argument('-v', '--video', action='store_true', help = 'mp4 mode')
    parser.add_argument('-p', '--playlist', action='store_true', help = 'playlist mode')
    parser.add_argument('-r', '--resolution', action='store', help = 'desired resolution for video (eg 1080p)')

    # Read arguments from command line
    args = parser.parse_args()

    #Pass args to ytmp3
    ytmp3 = Ytmp3()
    ytmp3.isPlaylist = args.playlist
    ytmp3.isAudioOnly = not args.video
    ytmp3.videoQuality = args.resolution

    #Run ytmp3
    ytmp3.run(args.url)

    #Cleanup
    del ytmp3
