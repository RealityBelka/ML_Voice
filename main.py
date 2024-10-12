import os
from AudioParams import AudioParams


def process(audio_file, ap):

    audio_wav = audio_file.replace(audio_file[-3:], "wav")

    if not os.path.exists(audio_wav):
        ap.convert_to_wav(audio_file, audio_wav)

    noise_level = ap.analyze_audio_quality(audio_wav)
    # print("1-2) noise_level: ", noise_level)
    if noise_level == "тихо":
        return "Говорите громче или переместитесь в более тихое место"
    if noise_level == "громко":
        return "Говорите тише или отодвиньте телефон от лица"

    recognized_text = ap.text_recognition(audio_wav)

    language = ap.check_language(recognized_text)
    # print("3) language: ", language)
    if language != "ru":
        return "Произносите указанные цифры на русском языке"

    only_numerals = ap.only_numerals(recognized_text)
    # print("4) only_numerals: ", only_numerals)
    if not only_numerals:
        return "Произносите только указанные на экране цифры"

    check_single_speaker = ap.check_single_speaker(audio_wav)
    # print("5) check_single_speaker: ", check_single_speaker)
    if not check_single_speaker:
        return "Посторонние шумы. Переместитесь в более тихое место"

    # print(recognized_text)

    return "Запись прошла проверку успешно."


def main():
    ap = AudioParams()

    audio_file = "audio_samples/ogg/normal_1.ogg"

    message = process(audio_file, ap)

    print(message)


if __name__ == "__main__":
    main()
