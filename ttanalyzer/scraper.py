from urllib.error import HTTPError

from tiktokapipy.async_api import TikTokAPI
import urllib.request as req


class TikTokScraper:

    @staticmethod
    def _grab(url, content_type, output_file):
        try:
            req.urlretrieve(url, output_file)
            print(f'{content_type} downloaded.')
            return True
        except HTTPError as e:
            print(f"Error with downloading {content_type} {url} ({e.code})")
            return False

    @staticmethod
    def by_hashtag(hashtag, output_dir, music=True, video=True, video_limit=None):
        print(f'Downloading videos by hashtag {hashtag}...')
        with TikTokAPI() as api:
            videos_wrapper = api.challenge(hashtag, video_limit=video_limit)
            TikTokScraper._grab_all_videos(videos_wrapper, output_dir, music, video)
        print('Done.')

    @staticmethod
    def by_user(user, output_dir, music=True, video=True, video_limit=None):
        print(f'Downloading videos by user {user}...')
        with TikTokAPI() as api:
            videos_obj = api.user(user, video_limit=video_limit)
            TikTokScraper._grab_all_videos(videos_obj, output_dir, music, video)
        print('Done.')

    @staticmethod
    def _grab_all_videos(videos_wrapper, output_dir, music=True, video=True):
        for video_el in videos_wrapper.videos:
            print(f"User: {video_el.author}; ID: {video_el.id}")
            if music:
                TikTokScraper._grab(video_el.music.play_url, 'video\'s sound', f'{output_dir}/{video_el.author}_{video_el.id}.mp3')
            if video:
                TikTokScraper._grab(video_el.video.download_addr, 'video',
                                    f'{output_dir}/{video_el.author}_{video_el.id}.{video_el.video.format}')
            print('----------------------------')