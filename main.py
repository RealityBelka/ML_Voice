import os
from AudioParams import AudioParams


def audio_process(ap, audio_file, example_numerals=None):

    flag = False  # True, если проверка пройдена успешно

    audio_wav = audio_file.replace(audio_file[-3:], "wav")

    if not os.path.exists(audio_wav):
        ap.convert_to_wav(audio_file, audio_wav)

    noise_level = ap.analyze_audio_quality(audio_wav)
    # print("1-2) noise_level: ", noise_level)
    if noise_level == "тихо":
        return flag, "Говорите громче или переместитесь в более тихое место"
    if noise_level == "громко":
        return flag, "Говорите тише или отодвиньте телефон от лица"

    recognized_text = ap.text_recognition(audio_wav)

    language = ap.check_language(recognized_text)
    # print("3) language: ", language)
    if language != "ru":
        return flag, "Произносите указанные цифры на русском языке"

    only_numerals = ap.only_numerals(recognized_text)
    # print("4) only_numerals: ", only_numerals)
    if not only_numerals:
        return flag, "Произносите только указанные на экране цифры"

    check_single_speaker = ap.check_single_speaker(audio_wav)
    # print("5) check_single_speaker: ", check_single_speaker)
    if not check_single_speaker:
        return flag, "Посторонние шумы. Переместитесь в более тихое место"

    recognized_numerals = [int(x) for x in recognized_text.split()]

    if example_numerals is not None and recognized_numerals != example_numerals:
        return flag, "Произносите только указанные на экране цифры"

    flag = True

    return flag, None


def main():
    ap = AudioParams()

    # Пример получаемых файлов: аудиозапись и массив показанных чисел
    audio_file = "audio_samples/ogg/overload_3.ogg"
    example_numerals = [1, 2, 3, 4, 8, 8]

    ok, message = audio_process(ap, audio_file, example_numerals)

    return {"ok": ok, "message": message}


if __name__ == "__main__":
    result = main()
    print(result)
