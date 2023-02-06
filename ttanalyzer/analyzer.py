import whisper


class VoiceAnalyzer:

    def __init__(self, model_name):
        self.model = whisper.load_model(model_name)

    def transcribe(self, path):
        r = self.model.transcribe(path)
        print(f'Text: {r["text"]}')
        return r