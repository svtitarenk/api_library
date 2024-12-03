#### api_library  
REST API для управления библиотекой. API предоставляет возможность для управления книгами, авторами и пользователями, а также для отслеживания выдачи книг пользователям. Для реализации API используется Django Rest Framework (DRF)

Запуск проекта:
```cmd
docker-compose up -d --build
```

##### Детали по проекту:

1. Приложение обеспечивает аутентификацию и авторизацию пользователей с использованием **JWT токенов**
	1. Авторизация осуществляется через метод POST на endpoint `users/register/` и login `users/login/`
	2. Acsess token должен быть добавлен в Headers запроса по `key`=`Authorization`, `Value`=`Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXV...`

2. Приложение позволяет управлять книгами и авторами. Управление книгами, авторами и движениями книг доступно только авторизованным пользователям по JWT acsess token
	1. **Управление книгами через endpoint `books` через `ViewSet`**:
	    - Создание, редактирование и удаление книг.
	    - Получение списка всех книг.
	    - Поиск книг по различным критериям (название, автор, жанр и т.д.).
	    - взаимодействие с книгами через endpoint: `http://127.0.0.1:8000/books/` (GET, PATCH, DELETE)
		    - * книги можно добавлять сразу с автором, для этого нужно передать словарь автора, например 
			```json
					"author":{
						"name": "Михаил Лермонтов",
						"birth_date": "1814-10-15",
						"biography": "Поэт, драматург и прозаик, художник."
					}
			```
	    - Владелец книги присваивается в зависимости от того, кто ее создал.
	    - Список книг отражает также рейтинг (`"average_rating": 5.0`), который формируется пользователями, которые уже вернули книгу в библиотеку, что позволит ориентировать по популярности.
	1. **Управление авторами через endpoint `authors` через `ViewSet`**:
	    - Создание, редактирование и удаление авторов.
	    - Получение списка всех авторов.
	    - взаимодействие с авторами через endpoint: `http://127.0.0.1:8000/authors/` (GET, PATCH, DELETE)
	2. **Управление пользователями через endpoint `users` через `generic`**:
	    - Регистрация и авторизация пользователей (register, login).
	    - Получение информации о пользователях через метод GET. Список пользователей доступен только пользователям, входящим группу `Moderators`. Добавление в группу через админ панель `admin`.
	    - У пользователя отражаются дополнительные поля 
		    - total_books_taken - сколько книг было взято
		    - total_days_held_books - сколько дней находились на руках книги
	1. **Выдача книг через endpoint `book-issues` через `ViewSet`**:
	    - Запись информации о выдаче книги пользователю.
		    - минимальные поля для заполнения:
		    ```json
				{
				    "book": 6,
				    "user": 1
				}
			```
	    - Запись о сдаче книги обратно в библиотеку. Рейтинг опционально
		    ```json
			{
				"return_date": "2024-12-02",
				"rating": 4
			}
			```
	    - Отслеживание статуса возврата книги (is_returned). `GET` запрос на endpoint `book-usses`
3. Документация API по проекту [redoc](http://127.0.0.1:8000/redoc) или [swagger](http://127.0.0.1:8000/swagger/)
4. Код соответствует стандартам PEP8. Проверено Flake8
5. `README.md` содержит описание структуры, инструкцию по установке и запуску проекта
6. Запуск проекта
```cmd
docker-compose up -d --build
```
7. После сборки должны появиться контейнеры:
	1. Контейнеры
		1. **postgres_db**
		2. **django_app**
8. Проверка работоспособности
	1. Проверить [документацию](http://localhost:8000/redoc/)
	2. Проверить запросы через postman
9. Регистрация [/users/register/](http://localhost:8000/users/register/)
	Передать параметры raw in JSON
	```json
	{
		"email": "test_user1@yandex.ru",
		"password": "admin"
	}
	```
	Ответ должен прийти следующего вида:
	```json
	{
		"id": 1,
		"email": "test_user1@yandex.ru",
		"total_books_taken": 0,
		"total_days_held_books": 0,
		"date_joined": "2024-12-03T10:29:55.400305Z",
		"groups": [],
		"is_staff": false,
		"last_login": null,
		"is_superuser": false,
		"is_active": true,
		"phone": null,
		"tg_nick": null
	}
	```

10. Логин [/users/login/](http://localhost:8000/users/login/)
	передать аналогичные параметры как /users/register/
	```json
	{
		"email": "test_user1@yandex.ru",
		"password": "admin"
	}
	```
	Ответ придет вида:
	```json
	{
		"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMzMwODUwMywiaWF0IjoxNzMzMjIyMTAzLCJqdGkiOiIzODI1YTExN2E5NDg0MWNhOTg4MDg0OGY5ODVjMWRjOCIsInVzZXJfaWQiOjF9.Ac6H0LjNQRbq3EUHwRdcJooLvQPz3zpUcC2xQ2Ge9pc",
		"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzMzA4NTAzLCJpYXQiOjE3MzMyMjIxMDMsImp0aSI6IjJhMTRhNDZiOTgzMTRmNDA4ZmQ2MDM3Y2M3N2Q0ZWMwIiwidXNlcl9pZCI6MX0.UC4phtaMVzjnI_pWg6rM9cOYqIo9RIbU0ciidjPU6sk"
	}
	```
11. Далее работа с [книгами](http://127.0.0.1:8000/books), [авторами] и [забрать/сдать книги](http://127.0.0.1:8000/book-issues/)
		Авторизация через `Headers`, не забудьте добавить `access token` как значение `Bearer <access token>`



### Следующие реализации и улучшения
1. Реализовать фильтрацию или сортировку по рейтингу
2. Добавить аватар книги
3. Добавление сортировки по популярности книги
4. Разрешенный срок, на который можно взять книгу, уведомление пользователя за несколько дней до истечения на почту. 
5. Добавление инфо о том, на сколько книга интересна читателям, по полю, сколько раз ее взяли и какой рейтинг.
6. Реализовать Web интерфейс или Telegram-бота для работы с библиотекой.