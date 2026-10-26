# WEARHOUSE — интернет-магазин одежды

Практические работы №1 «Создание первого проекта» и №2 «Базовый шаблон и включения». Автор: Шеронов Артём Владимирович.

Учебная витрина на Django: главная `/`, каталог `/catalog/`, «О нас» `/about/`. Общий header и footer наследуются из `base.html`. В каталоге шесть демонстрационных товаров и фильтр категорий. Покупка и оплата не входят в эту практическую работу. Иллюстрации одежды выполнены средствами CSS, внешние сервисы не требуются.

## Запуск Windows PowerShell

Требуется Python 3.10 или новее.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Открыть http://127.0.0.1:8000/. Активация окружения по желанию: `.\.venv\Scripts\Activate.ps1`. При ограничениях PowerShell можно использовать прямой путь к python.exe, как в примере.

## Проверка

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

`config/urls.py` подключает `shop/urls.py`. Представления находятся в `shop/views.py`, шаблоны — `shop/templates/shop/`. Все страницы наследуют `base.html`; шапка и подвал подключаются из `includes/header.html` и `includes/footer.html`. Единственный файл оформления — `shop/static/shop/styles.css`, весь JavaScript — `shop/static/shop/script.js` (кнопка «Наверх»). Встроенных CSS и JavaScript в шаблонах нет. Каталог хранится в списке Python, модель товаров на этом этапе не требуется. Сервер предназначен для локального учебного запуска.

Документация: https://docs.djangoproject.com/en/5.2/intro/tutorial01/
