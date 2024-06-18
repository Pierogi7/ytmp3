# YouTube to mp3


## Download video/audio from YouTube with ease

This is a simple project written in Python, it uses Pytube and ffmpeg
to download from YouTube.

* Download mp3
* Download mp4
* Download Playlist

## Table Of Contents
1.  [CLI Usage](#cli-usage)
2.  [Options](#Options)
3.  [Installation](#installation)
4.  [Script Like Usage](#script-like-usage)
5.  [Building](#building)
6.  [Known Issues](#known-issues)
7.  [Credits](#credits)
8.  [License](#license)
---

## CLI Usage
by default a single video is downloaded (Audio only) and converted to mp3 for convenience.
```
ytmp3 https://www.youtube.com/watch?v=zU9y354XAgM
```

## Options
You can pass command line options and flags to ytmp3.
| FLAGS               | USAGE                         | EXAMPLE |
|-----------------------|-------------------------------|---------|
| `-p`, `--playlist`    | Playlist mode                 | `ytmp3 <url> -p` |
| `-v`, `--video`       | Download videos as mp4        | `ytmp3 <url> -v` |


| OPTIONS                 | USAGE                         | EXAMPLE |
|-----------------------|-------------------------------|---------|
| `-r`, `--resolution RESOLUTION`  | Set desired resolution        | `ytmp3 <url> -r 1080p` |

## Installation
1. Click on releases and download ytmp3.zip, if you have ffmpeg installed already
you can get the noffmpmeg version.

2. Extract it anywhere you want.

3. Add it to your PATH variable so you can run it anywhere.

## Script like usage

1. Download the script file only (ytmp3.py).

2. You can use ytmp3 in your code like this.
```Python
from ytmp3 import Ytmp3

ytmp3 = Ytmp3()

ytmp3.run(url)
```

3. You can access the same options as with the CLI.
```Python
ytmp3.isAudioOnly = True
ytmp3.isPlaylist = True
ytmp3.videoQuality = "1080p"
```

4. You can disable status messages and errors being output to CLI and build
your own interface.
```Python
ytmp3 = Ytmp3(False) # Disable status and error messages

#Access the information and do what you want with it
msg = ytmp3.statusMessage
errLst = ytmp3.errorList
```

5. The run() function automatically checks the url provided and discriminates between
playlist downloads and single item downloads. You can access the relevant functions
manually if you do not want to use run(), just make sure to use check_url() or it
will throw an error if the user does not provide a valid YouTube link.
```Python
if ytmp3.check_url():
  ytmp3.download_video(url)
  #or
  ytmp3.playlist_download(url)
```

## Building
You can download the source code and build it yourself using pyinstaller.

1. Clone this repo or just download the file ytmp3.py
```
git clone https://github.com/Pierogi7/ytmp3.git
```
2. Make sure pytube and pyinstaller are installed.
```
pip install pytube
```
```
pip install pyinstaller
```
3. Navigate to the file location and run pyinstaller
```
pyinstaller -F ytmp3.py
```
4. Make sure FFMPEG is installed and included in PATH or in ./FFMPEG/FFMPEG.exe
```
https://ffmpeg.org/download.html
```
## Known Issues

* Age restricted videos cannot be downloaded
* FFMPEG can be quite slow when stitching 1080p videos
* Not tested outside of windows 10

## Credits

* pytube: https://github.com/pytube/pytube
* FFMPEG: https://ffmpeg.org

## License
MIT License

© Pierogi7 2024

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
