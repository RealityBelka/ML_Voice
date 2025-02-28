import os
from AudioParams import AudioParams


def audio_process(ap, audio_file, example_numerals=None):

    flag = False  # True, если проверка пройдена успешно

    audio_wav = audio_file .replace(audio_file[-3:], "wav")

    if not os.path.exists(audio_wav):
        ap.convert_to_wav(audio_file, audio_wav)

    '''1-2'''
    noise_level = ap.analyze_audio_quality(audio_wav)
    if noise_level == "тихо":
        return flag, "Говорите громче или переместитесь в более тихое место"
    if noise_level == "громко":
        return flag, "Говорите тише или отодвиньте телефон от лица"

    recognized_text = ap.text_recognition(audio_wav)

    '''3'''
    language = ap.check_language(recognized_text)
    if language != "ru":
        return flag, "Произносите указанные цифры на русском языке"

    only_numerals = ap.only_numerals(recognized_text)

    '''4'''
    if only_numerals:
        recognized_text = ap.replace_word_numerals(recognized_text.split())
    else:
        return flag, "Произносите только указанные на экране цифры"

    '''5'''
    check_single_speaker = ap.check_single_speaker(audio_wav)
    if not check_single_speaker:
        return flag, "Посторонние шумы. Переместитесь в более тихое место"

    recognized_numerals = [int(x) for x in recognized_text]
    print(recognized_numerals)
    if example_numerals is not None and recognized_numerals != example_numerals:
        return flag, "Произносите только указанные на экране цифры"

    flag = True

    return flag, None


def main():
    ap = AudioParams()

    # Пример получаемых файлов: аудиозапись и массив показанных чисел
    audio_file = "audio_samples/wav/samara.ogg"
    example_numerals = [1, 1, 1, 1, 2, 3]

    ok, message = audio_process(ap, audio_file, example_numerals)

    return {"ok": ok, "message": message}


if __name__ == "__main__":
    result = main()
    print(result)
