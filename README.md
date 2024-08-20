Проект мониторинга веб-сайтов
Данный проект написан на языке программирования Python. Это многопоточное приложение для отслеживания ответов от URL-адресов. Если ответ не 200 (успешный), то приложение отправляет уведомление пользователю по электронной почте и в Telegram.

Это приложение будет полезно для мониторинга работы сайтов, обнаружения ошибок и повышения производительности. Приложение содержит Docker-образ, поэтому его можно запускать на любой другой машине с установленными зависимостями.

Запуск приложения
Для запуска приложения необходимо:

1.Скачать проект на свой ПК.  
2.Запустить файл main.py в среде разработки, например PyCharm.  
3.Открыть браузер, создать монитор и ввести URL-адрес, который должен отслеживаться. Также можно установить время ожидания ответа для потока.  

Архитектура приложения  
1.Директория crud:
- monitor.py - получение мониторов из базы данных и удаление мониторов.
- request.py - получение запросов, привязанных к монитору, из базы данных.
  
2.Директория model: 
-base.py - родительский класс для сохранения таблиц в базе данных.
- monitor.py - создание, сохранение, обновление и представление объекта монитора для пользователя.
- request.py - создание, сохранение и представление объекта запроса для пользователя.
  
3. Директория router:
- monitor.py - обработка запросов от пользователя на создание, удаление, обновление и просмотр мониторов.
- Dockerfile - образ, на основе которого будет создан контейнер приложения.
- app_factory.py - создание приложения.
- database.py - создание генератора асинхронных сессий.
- executingRequests.py - запуск процесса отслеживания URL-адресов мониторами.
- main.py - запуск приложения.
- requirements.txt - описание использованных библиотек и модулей.
- sending_notification.py - отправка сообщений в Telegram-бот.
