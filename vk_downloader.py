__author__ = 'zabidon'

import vk
import re
import time
import requests
from os.path import exists, isfile, join, splitext, curdir
from os import mkdir, remove
from arg_parse import arg_parse

def check_create_directory(path):
    if exists(path) and isfile(path):
        remove(path)
    if not exists(path):
        mkdir(path)

class VK_downloader(object):
    def __init__(self, session):
        self.session = session
        self.download_dir = join(curdir, "download")
        self.music_dir = join(self.download_dir, "music")

        for directory in [self.download_dir, self.music_dir]:
            check_create_directory(directory)

    def download_audio_all(self, owner_id=None, album_id=None, through_albums=False):
        if through_albums:
            if owner_id:
                albums = self.session.audio.getAlbums(owner_id=owner_id)
                owner_dir = join(self.music_dir, str(owner_id))
                check_create_directory(owner_dir)
                for album in albums['items']:
                    dir = join(owner_dir, str(album['id']))
                    check_create_directory(dir)

                    audios = self.session.audio.get(owner_id=owner_id, album_id=album['id'])

                    self.download_audios(audios, dir)
        else:

            dir = join(self.music_dir, str(album_id or owner_id))
            check_create_directory(dir)

            audios = self.session.audio.get(owner_id=owner_id, album_id=album_id)

            self.download_audios(audios, dir)

    def download_audios(self, audios, dir=None):
        if not dir:
            dir = join(self.music_dir, "noname")
        check_create_directory(dir)
        for audio in audios['items']:
            if 'url' in audio and 'artist' in audio and 'title' in audio:
                self.download_audio(audio['url'], audio['title'], audio['artist'], dir=dir)

    def download_audio(self, url=None, name=None, artists=None, *, dir):
        if name is not None and artists is not None and url is not None:
            filename = artists.strip() + '-' + name.strip()
            filename = re.sub(r"[^\w().-]", "_", filename)
            filepath = join(dir, filename[0:64]) + ".mp3"

            res = requests.get(url, stream=True)

            counter = 1
            if exists(filepath) and isfile(filepath):
                name, ext = splitext(filepath)
                filepath = name + " ({})".format(counter) + ext

            while exists(filepath) and isfile(filepath):
                counter += 1
                name, ext = splitext(filepath)
                filepath = name[:-4] + " ({})".format(counter) + ext

            print(u"Start download audio: {}".format(filepath))

            file = open(filepath, 'wb')
            file.write(res.content)
            file.close()

            print("Downloading is ended")


if __name__ == "__main__":
    # args = arg_parse()
    downloader = VK_downloader(vk.API('', '', ''))
    downloader.download_audio_all(19202619)
    # downloader.download_audio_all(owner_id = args.id,
    #                               album_id = args.aid,
    #                               through_albums=args.through_albums)