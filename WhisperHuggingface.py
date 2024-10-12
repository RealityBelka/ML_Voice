import os
import torch
import librosa
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
from functools import lru_cache


class WhisperHuggingface:
    def __init__(self, audio_path):
        self.model_path = "./whisper-large-v3"
        self.model_id = "openai/whisper-large-v3"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.audio_path = audio_path

    @lru_cache(maxsize=1)
    def load_model(self):
        return AutoModelForSpeechSeq2Seq.from_pretrained(self.model_path).to(self.device)

    @lru_cache(maxsize=1)
    def load_processor(self, path):
        return AutoProcessor.from_pretrained(path)

    @property
    def process(self):
        print("process")
        if not os.path.exists(self.model_path):
            print("Модель не найдена локально. Загружаем с Hugging Face...")
            model = AutoModelForSpeechSeq2Seq.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                low_cpu_mem_usage=True,
                use_safetensors=True
            )
            model.save_pretrained(self.model_path)
            processor = self.load_processor(self.model_id)
            processor.save_pretrained(self.model_path)
            model.to(self.device)
        else:
            print("Модель найдена локально. Загружаем из локальных файлов...")
            model = self.load_model()
            processor = self.load_processor(self.model_path)
        print("Модель загружена и передана на девайс.")

        audio_path = "audio_samples/multilang_3.ogg"
        audio, sampling_rate = librosa.load(audio_path, sr=16000)
        # Убираем тишину
        audio_trimmed, _ = librosa.effects.trim(audio)

        inputs = processor(audio_trimmed, sampling_rate=sampling_rate, return_tensors="pt").to(self.device)

        # Cast input features to the same data type as the model's weights
        inputs.input_features = inputs.input_features.type(model.parameters().__next__().dtype)

        with torch.no_grad():
            generated_ids = model.generate(inputs.input_features, max_new_tokens=100)
            transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        print("process")

        return transcription

    # print("Распознанный текст:", process)
