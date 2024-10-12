# ML_Voice

---

Проверка аудиозаписи происходит по следующим признакам:

 - signal_noise — отношение сигнал-шум;
 - overload_border — перегрузка аудиозаписи;
 - russian_language — наличие не русского языка;
 - single_voice — наличие больше одного голоса;
 - only_numbers — проверка наличия иных слов (не цифр от 0 до 9).

## Установка и запуск
1) Установите зависимости:
```pip install -r requirements.txt```
2) Скачайте и установите библиотеку FFMPEG (рекомендуется full-release build): https://ffmpeg.org/download.html
3) Распакуйте скачанный архив и добавьте каталог в PATH, запустив данную команду в cmd от имени администратора:
```setx /m PATH "C:\ffmpeg\bin;%PATH%"```, где вместо 'C:\ffmpeg\\' - ваш путь к каталогу
4) Модуль готов к использованию:
   - принимает аудиозапись **audio_file** и массив чисел **example_numerals**, которые пользователь должен был произносить;
   - возвращает состояние проверки записи **status** и сообщение об ошибке **message**.
   - Пример использования:
   ```python
   from AudioParams import AudioParams
   
   ap = AudioParams()

   audio_file = "path_to_audio.wav"
   example_numerals = [1, 2, 3, 4]

   status, message = process_audio(ap, audio_file, example_numerals)
   print(f"ok: {status}, message: {message}")
   ```
   
## Результаты

- status: возвращает True или False в зависимости от того, прошла ли запись проверку.
- message: возвращает строку с описанием ошибки, если запись не прошла проверку.


## Используемые библиотеки:

Все подключаемые пакеты, используемые в проекте, имеют лицензии, позволяющие использовать их программное обеспечение в коммерческих продуктах, с необходимостью указания авторства. 

А именно:

 - Librosa: https://librosa.org/ (ISC)
 - Webrtcvad: https://libraries.io/pypi/webrtcvad (MIT)
 - Langdetect: https://libraries.io/pypi/langdetect (MIT)
 - SpeechRecognition: https://pypi.org/project/SpeechRecognition/ (BSD) 
 - PyDub: https://github.com/jiaaro/pydub (MIT)
 - PyTorch: https://pypi.org/project/torch/ (BSD)
 - Transformers: https://pypi.org/project/transformers/ (Apache 2.0)
