
# Проект 8-го спринта API для YaTube
###### @Яндекс Практикум
***



## О проекте
Разработка полноценного API для проекта YaTube

## Использованные технологии
Основа проекта
Python 3.9.13
Django 3.2.16
Django Rest Famework 3.12.4


Полный перечень использованных библиотек и модулей можно посмотреть в файле `requirements.txt`**
***




## Структура проекта
<details>
  <summary style="font-size:250%;">Проект имеет следующую структуру</summary>
  <p>

  `yatube_api/` - основная директория проекта с приложениями _api_ и _posts_.


  `manage.py` - основной файл для управления проектом.


  `README.md` - файл с документацией.


  `tests/` - директория с тестами.


  `postman_collection/` - директория с тестами HTTP запросов к API для программы Postman.

</p>
</details>

## Установка и запуск проекта

<details>
  <summary><b<strong>Установка и запуск</strong></b></summary>

### Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке:
  ```bash
  git clone https://github.com/xVismar/api_final_yatube.git
  ```

  ```bash
  cd api_final_yatube
  ```

2. Создать и активировать виртуальное окружение:
  ```bash
  python -m venv venv
  ```
  ```bash
  . venv/Scripts/activate
  ```

3. Обновить установщик Python и установить зависимости из файла requirements.txt:
  ```bash
  python -m pip install --upgrade pip
  ```
  ```bash
  pip install -r requirements.txt
  ```

4. Выполнить миграции:
  ```bash
  python ./yatube_api/manage.py migrate
  ```

5. Запустить проект:
  ```bash
  python ./yatube_api/manage.py runserver
  ```
</p>
</details>

***
<br></br>

## Примеры запросов и тестирование

<details>
<summary><b><strong>Примеры запросов к API</strong></b></summary>

### Получение списка постов:
```api/v1/posts/```

**Ответ:**
```json
{
    "count": 123,
    "next": "http://api.example.org/accounts/?offset=400&limit=100",
    "previous": "http://api.example.org/accounts/?offset=200&limit=100",
    "results": [
        {
            "id": 0,
            "author": "string",
            "text": "string",
            "pub_date": "2021-10-14T20:41:29.648Z",
            "image": "string",
            "group": 0
        }
    ]
}
```

### Получение комментария к посту:
```/api/v1/posts/{post_id}/comments/{id}/```

**Ответ:**
```json
{
    "id": 0,
    "author": "string",
    "text": "string",
    "created": "2019-08-24T14:15:22Z",
    "post": 0
}
```
</p>
</details>


<details>
<summary><b><strong>Тестирование</strong></b></summary>

# Тестирование

Для тестирования проекта используется `pytest`.



## Установка

Для начала, убедитесь, что у вас установлен `pytest`.

Вы можете установить его с помощью `pip`:

```bash
pip install pytest
```



## Структура тестов
В проекте тесты организованы в папке `tests`.

В ней находятся следующие файлы и директории:

`conftest.py` - Этот файл содержит общие настройки и фикстуры для тестов.
`test_jwt.py` - Тесты для проверки JWT аутентификации.
`test_group.py` - Тесты для проверки функционала групп.
`test_follow.py` -  Тесты для проверки функционала подписок.



## Запуск тестов
Для запуска всех тестов выполните команду:
```
pytest
```



Вы также можете запустить тесты в определенном файле:
```
pytest tests/test_jwt.py
```


Или запустить конкретный тест в файле:
```
pytest tests/test_jwt.py::TestJWT::test_jwt_create__valid_request_data
```



## Фикстуры
Фикстуры определены в файле `tests/conftest.py` и других файлах в папке `fixtures`.

Они помогают подготовить данные и окружение для тестов.

### Пример фикстуры:
```
@pytest.fixture
def user(db):
    return UserFactory.create()
```

## Примеры тестов

### Тестирование JWT
Файл `tests/test_jwt.py` содержит тесты для проверки JWT аутентификации.

### Пример теста:
```
@pytest.mark.django_db(transaction=True)
class TestJWT:
    url_create = '/api/v1/jwt/create/'

    def test_jwt_create__valid_request_data(self, client, user):
        response = client.post(self.url_create, data={'username': user.username, 'password': 'password'})
        assert response.status_code == HTTPStatus.OK, 'Проверьте, что при правильных данных возвращается статус 200.'
```


### Тестирование групп
Файл `tests/test_group.py` содержит тесты для проверки функционала групп.


### Пример теста:
```
@pytest.mark.django_db(transaction=True)
class TestGroupAPI:
    group_url = '/api/v1/groups/'

    def test_group_list_not_auth(self, client, group_1):
        response = client.get(self.group_url)
        assert response.status_code == HTTPStatus.OK, 'Проверьте, что GET-запрос неавторизованного пользователя возвращает статус 200.'
```



## Тестирование подписок
Файл `tests/test_follow.py` содержит тесты для проверки функционала подписок.


## Пример теста:
```
@pytest.mark.django_db(transaction=True)
class TestFollowAPI:
    url = '/api/v1/follow/'

    def test_follow_not_auth(self, client, follow_1, follow_2):
        response = client.get(self.url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, 'Проверьте, что GET-запрос неавторизованного пользователя возвращает статус 401.'
```


### Полезные команды
`pytest -v` - Запуск тестов с подробным выводом.
`pytest --maxfail=1` - Остановить выполнение после первого проваленного теста.
`pytest --tb=short` - Сокращенный вывод трассировки.

</p>
</details>



<details>
  <summary><b><strong>Тестирование работы запросов к API через Postman</strong></b></summary>
  <p>

## Postman-коллекция для проверки API
Проект содержит Postman-коллекцию - набор заранее подготовленных запросов для проверки работы API через программу Postman.

## Загрузка коллекции в Postman:
  1. Запустите Postman.
  2. В левом верхнем углу нажмите `File` -> `Import`.
  3. Во всплывающем окне будет предложено перетащить в него файл с коллекцией либо выбрать файл через окно файлового менеджера. Загрузите файл `postman_collection.json` в Postman.

   </p>
</details>
<br></br>

***

**Автор** - Алексеев Алексей (Vismar)
_Студент 11-когорты бэкенд-факультета Яндекс Практикум_
**Курс** - Python-разработчик буткемп
27/08/2024 - Сдача первой рабочей версии проекта.
