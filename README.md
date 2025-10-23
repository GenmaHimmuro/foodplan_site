# foodplan_site
Сайт с автоматизированным планированием питания и покупок, с рецептами.


Скачайте код:
```sh
git clone https://github.com/GenmaHimmuro/foodplan_site.git
```

Перейдите в каталог проекта:
```sh
cd foodplan_site
```

[Установите Python версию 3.12.8](https://www.python.org/downloads/release/python-3128). Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии. 

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv .venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

Определите переменные окружения:
```sh
SECRET_KEY = ваш SECRET_KEY
DEBUG = True (для продакшена)
CSRF_COOKIE_SECURE = False (для продакшена)
```

Создайте файл базы данных SQLite и отмигрируйте её следующей командой:

```sh
python manage.py migrate
```

Запустите сервер:

```sh
python manage.py runserver
```

