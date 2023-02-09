import argparse
import textwrap
from dataclasses import dataclass

from ttanalyzer.analyzer import VoiceAnalyzer
from ttanalyzer.reader import FileReader
from ttanalyzer.scrapper import TikTokScraper
from ttanalyzer.writer import JSONFileWriter


@dataclass(frozen=True)
class InputConfig:
    model: str
    input_path: str
    output_path: str
    hashtag: str
    user: str
    max_videos: int
    transcribe: bool


class ArgsHandler:
    NAME = 'TikTok Analyzer'
    DESC = f'''
    TikTok Analyzer - crawling and analyzing TikTok videos.
    '''

    SPEECH_TO_TXT_DESC = 'Enable speech to text on sound files located in the input path'
    INPUT_PATH = 'Input path to directory with mp3 files for speech to text.'
    OUTPUT_PATH = 'Path to directory where crawler will write all files (audio, video, transcriptions).'
    MODEL_DESC = 'Name of ML model'
    MAX_VIDEOS_DESC = 'Max number of videos to crawl'
    HASHTAG_DESC = 'Enable crawling videos by hashtag'
    USER_DESC = 'Enable crawling user\'s video'
    TRANSCRIBE_DESC = 'Flag enabling speech to text analysis.'

    def __init__(self):
        parser = argparse.ArgumentParser(description=textwrap.dedent(self.DESC), add_help=True,
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('--input-path', metavar='input_path', type=str, help=self.INPUT_PATH)
        parser.add_argument('--output-path', metavar='output_path', type=str, help=self.OUTPUT_PATH)
        parser.add_argument('--model', metavar='model', type=str, help=self.MODEL_DESC, default='base')
        parser.add_argument('--transcribe', action='store_true', help=self.TRANSCRIBE_DESC)
        parser.add_argument('--hashtag', metavar='hashtag', type=str, help=self.HASHTAG_DESC)
        parser.add_argument('--user', metavar='user', type=str, help=self.USER_DESC)
        parser.add_argument('--max-videos', metavar='max_videos', type=int, help=self.MAX_VIDEOS_DESC)
        self._parser = parser

    def parse(self):
        args = self._parser.parse_args()
        return InputConfig(args.model,
                           args.input_path,
                           args.output_path,
                           args.hashtag,
                           args.user,
                           args.max_videos,
                           args.transcribe)


if __name__ == '__main__':
    config = ArgsHandler().parse()

    if config.hashtag is not None and config.output_path is not None:
        TikTokScraper.by_hashtag(config.hashtag, config.output_path, video_limit=config.max_videos)
    if config.user is not None and config.output_path is not None:
        TikTokScraper.by_user(config.user, config.output_path, video_limit=config.max_videos)
    if config.transcribe and config.input_path is not None and config.output_path is not None:
        voice_analyzer = VoiceAnalyzer(config.model)
        results = FileReader.read(config.input_path, lambda path: voice_analyzer.transcribe(path))
        JSONFileWriter.write(results, config.output_path)
