import re
import librosa
import webrtcvad
import numpy as np
from langdetect import detect
import speech_recognition as sr
from pydub import AudioSegment


class AudioParams:
    def __init__(self):
        self.number_words = {
            "ноль": '0', "один": '1', "раз": '1', "два": '2', "три": '3', "четыре": '4',
            "пять": '5', "шесть": '6', "семь": '7', "восемь": '8', "девять": '9',
            "десять": '10'
        }

    def convert_to_wav(self, input_file, output_file):
        """Преобразует аудиофайл из AAC (или другого) в WAV.
        Args:
            input_file: путь к входному файлу (AAC или др.)
            output_file: путь для сохранения выходного файла WAV
        """
        try:
            filetype = input_file[-3:]

            # Загружаем аудиофайл AAC
            audio = AudioSegment.from_file(input_file, format=filetype)

            # Экспортируем аудиофайл в формате WAV
            audio.export(output_file, format="wav")
            print(f"Файл успешно преобразован в {output_file}")

        except Exception as e:
            print(f"Ошибка при преобразовании: {e}")

    def analyze_audio_quality(self, audio_file, threshold_quite=0.1, threshold_overload=0.99):
        """
        Определение уровня шума и наличия перегрузки.

        :param audio_file: Путь к аудиофайлу
        :param threshold_quite: Порог тихого звучания (чем больше значение, тем тише порог)
        :param threshold_overload: Порог перегрузки (чем больше значение, тем громче порог)
        :return: Уровень шума (тихо, громко, норм)
        """
        y, _ = librosa.load(audio_file, sr=16000)

        # Расчет отношения сигнал/шум
        signal_energy = np.mean(y ** 2)
        noise_energy = np.var(y)

        snr = 1000 * np.log10(signal_energy / noise_energy)
        overload = np.max(np.abs(y)) >= threshold_overload

        if snr > threshold_quite:
            return "тихо"
        if overload:
            return "громко"
        return "норм"

    def replace_non_alphanumeric(self, text):
        """
        Заменяет все символы в строке, которые не являются буквами (латинскими или русскими) или цифрами, на пробелы.

        :param text: исходный текст
        :return: текст с замененными символами
        """
        return re.sub(r"[^a-zA-Zа-яА-ЯёЁ0-9]", ' ', text)

    def replace_word_numerals(self, text):
        new_text = []
        for word in text:
            if word.isdigit():
                new_text.append(word)
            else:
                new_text.append(self.number_words[word])
        return new_text

    def text_recognition(self, audio_file):
        """Производит распознавание текста из аудио."""
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="ru_RU")
            # wh = WhisperHuggingface(audio)  # Вторая версия, на выбор
            # text = wh.process()
            clean_text = self.replace_non_alphanumeric(text)
            return clean_text
        except:
            return None

    def check_language(self, transcription):
        """Проверяет язык записи"""
        try:
            lang = detect(transcription)
            return lang
        except:
            lang = "ru" if transcription else None
        return lang

    def only_numerals(self, input_string):
        """Проверяет, содержит ли строка только числа (словесные или символы)"""

        words = input_string.lower().split()

        for word in words:
            if word.isdigit() or word in self.number_words:
                continue
            else:
                return False
        return True

    def get_vad_segments(self, audio_path, sample_rate=16000, frame_duration=30):
        """
        Возвращает список активных (с голосом) и неактивных (тихих) сегментов в аудио.

        :param audio_path: Путь к аудиофайлу
        :param sample_rate: Частота дискретизации (должна быть 8000, 16000, 32000 или 48000)
        :param frame_duration: Длительность кадра в миллисекундах (10, 20 или 30 мс)
        :return: Сегменты активных и неактивных участков
        """
        vad = webrtcvad.Vad(2)  # Агрессивность VAD (0-3)

        y, _ = librosa.load(audio_path, sr=sample_rate)

        y = (y * 32768).astype(np.int16)

        frame_length = int(sample_rate * frame_duration / 1000)

        frames = [y[i:i + frame_length] for i in range(0, len(y), frame_length)]

        segments = {
            "active": [],
            "non_active": []
        }

        for frame in frames:
            if len(frame) != frame_length:
                continue

            is_speech = vad.is_speech(frame.tobytes(), sample_rate)

            if is_speech:
                segments["active"].append(frame)
            else:
                segments["non_active"].append(frame)

        return segments

    def analyze_silence(self, segments):
        """
        Анализирует неактивные (тихие) участки аудиозаписи.

        :param segments: Сегменты аудио (результат функции get_vad_segments)
        :return: Дисперсия для неактивных сегментов
        """
        non_active_segments = segments["non_active"]

        variances = [np.var(segment) for segment in non_active_segments]

        avg_variance = np.mean(variances) if variances else 0

        return avg_variance

    def check_single_speaker(self, audio_file, silence_threshold=5000):
        """
        Проверяет уровень шума (дисперсию) на тихих участках аудио.

        :param audio_file: Путь к аудиофайлу
        :param silence_threshold: Порог для определения шума в тихих сегментах
        :return: True, если запись проходит проверку на шум, иначе False
        """
        try:
            segments = self.get_vad_segments(audio_file)

            avg_variance = self.analyze_silence(segments)

            # print(f"Средняя дисперсия на тихих участках: {avg_variance}")

            if avg_variance > silence_threshold:
                return False
            else:
                return True
        except Exception:
            return False
