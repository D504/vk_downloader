#!usr/bin/python

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


    def download_audio_all(self,
                           owner_id=None,
                           album_id=None,
                           through_albums=False,
                           offset=0,
                           count=6000,
                           q=None):
        """
            Сохраняет список аудиозаписей пользователя или сообщества.


        :param owner_id: Идентификатор владельца аудиозаписей
        :param album_id: Идентификатор альбома с аудиозаписями
        :param through_albums: Сохранять аудиозаписи находящиеся в альбомах
        :param offset: Смещение, необходимое для выборки определенного количества аудиозаписей. По умолчанию — 0
        :param count: Количество аудиозаписей, информацию о которых необходимо вернуть. Максимальное значение — 6000.
        """

        if through_albums:
            if owner_id:
                albums = self.session.audio.getAlbums(owner_id=owner_id)
                owner_dir = join(self.music_dir, str(owner_id))
                check_create_directory(owner_dir)
                count_album = 0
                print(u"All albums: {}".format(len(albums['items'])))
                for album in albums['items']:
                    album['title'] = re.sub(r"[^\w().-]", " ", album['title'])
                    dir = join(owner_dir, str(album['title']))

                    check_create_directory(dir)
                    count_album += 1
                    print(u"{0}) Start downloading album: {1}".format(count_album, album['title']))
                    audios = self.session.audio.get(owner_id=owner_id,
                                                    album_id=album['id'],
                                                    offset=offset,
                                                    count=count)

                    self.download_audios(audios, dir)
        else:

            dir = join(self.music_dir, str(album_id or owner_id))
            check_create_directory(dir)

            audios = self.session.audio.get(owner_id=owner_id, album_id=album_id)

            self.download_audios(audios, dir)


    def download_audio_api(self, dir=None, func="audio.get", **kwargs):
        self.download_audios(self.session(func, **kwargs), join(self.music_dir, dir))


    def download_audios(self, audios, dir=None):
        if not dir:
            dir = join(self.music_dir, "noname")
        check_create_directory(dir)
        count_audio = 0
        print(u"All audios: {0}".format(len(audios['items'])))
        for audio in audios['items']:
            if 'url' in audio and 'artist' in audio and 'title' in audio:
                count_audio += 1
                print(u"{0}) Start downloading audio: {1}".format(count_audio, (audio['title'], audio['artist'])))
                self.download_audio(audio['url'], audio['title'], audio['artist'], dir=dir)
                print("Downloading is ended")


    def download_audio(self, url=None, name=None, artists=None, force=False, *, dir):
        if name is not None and artists is not None and url is not None:
            filename = artists.strip() + '-' + name.strip()
            filename = re.sub(r"[^\w().-]", " ", filename)
            filepath = join(dir, filename[0:64]) + ".mp3"

            res = requests.get(url, stream=True)

            counter = 1
            if force:
                if exists(filepath):
                    name, ext = splitext(filepath)
                    filepath = name + " ({})".format(counter) + ext

                while exists(filepath):
                    counter += 1
                    name, ext = splitext(filepath)
                    filepath = name[:-4] + " ({})".format(counter) + ext
            else:
                if exists(filepath):
                    print("File '{}' exist".format(filepath))
                    return
            file = open(filepath, 'wb')
            file.write(res.content)
            file.close()


if __name__ == "__main__":
    # args = arg_parse()
    downloader = VK_downloader(vk.API('app_id', 'name', 'password'))
    downloader.download_audio_api( "Ludovico Einaudi", "audio.search", q="Ludovico Einaudi", count=300)
    # downloader.download_audio_all(owner_id = args.id)
    # album_id = args.aid,
    # through_albums=args.through_albums)