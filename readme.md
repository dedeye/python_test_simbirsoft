# Тестовое задание на Python
Репозиторий на github: https://github.com/dedeye/python_test_simbirsoft

## Описание:
Данное приложение реализовывает функционал небольшого веб-сервиса, который, используя внешние веб-сервисы, по запросу возвращает случайную фотографию собаки, кота или лисы, предварительно обработав фотографию на сервере. 

## Функции:

### Запрос /animal/cat
Возвращает случайную фотографию кошки, обработанную фильтром SMOOTH_MORE

### Запрос /animal/dog
Возвращает случайную фотографию собаки, обработанную фильтром SMOOTH_MORE

### Запрос /animal/fox
Возвращает случайную фотографию лисы, обработанную фильтром SMOOTH_MORE

### Запрос /history
Возвращает историю запросов animal постранично в формате html (по умолчанию) или json
Для получения поределенной стронице добавьте аргумент page (/history?page=2)
Для получения данных в формате json укажеите аргумент output=json (/history?output=json)

### Запрос /history/static/<uuid>
Возвращает ранее обработканную картинку с указанным uuid
Для того, чтобы узнать uuid нужной картинки, можно возпользоваться запросом /history

### Журнал ошибок
Журнал ошибок сохраняется в файлы app.log (app.log.1 и так далее) в директории программы

## Запуск приложения:
Для запуска приложения требуется python3.7.3 (работа с другими версиями не тестировалась)

1) перейдите в папку с приложением
2) создайте виртуальное окружение python удобным вам способом
    например 'python3 -m venv my_env'
3) активируйте виртуальное окружение
    например 'source my_env/bin/activate'
4) установите пакет в виртуальном окружении
    'pip install -e .'
5) Отредактируйте файл конфигурации config.txt по вашим нуждам. Описание файла представлено в блоке Конфигурация приложения
6) При первом запуске требуется создать базу данных. Для этого запустите скрипт animals/create_db.py из виртуального окружения
    'python3 animals/create_db.py'
    Пропустите этот шаг, если у вас уже есть подходящая база данных
7) Запустите программу скриптом animals/runserver.py
    'python3 animals/runserver.py'

## Конфигурация приложения
Некоторые параметры приложения доступны для редактирования в файле config.txt

request_timeout:    максимальное время ожидания ответа от сторонних сервисов
img_folder:         путь к директории для соранения обаботанных изображений
db_file:            используемая база данных
logging:            включение/отключение логирования

