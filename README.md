# WEARHOUSE — интернет-магазин одежды

Практические работы №1 «Создание первого проекта», №2 «Базовый шаблон и включения» и №3 «Подключение к базе данных». Автор: Шеронов Артём Владимирович.

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

`config/urls.py` подключает `shop/urls.py`. Представления находятся в `shop/views.py`, шаблоны — `shop/templates/shop/`. Все страницы наследуют `base.html`; шапка и подвал подключаются из `includes/header.html` и `includes/footer.html`. Единственный файл оформления — `shop/static/shop/styles.css`, весь JavaScript — `shop/static/shop/script.js` (кнопка «Наверх»). Встроенных CSS и JavaScript в шаблонах нет. Сервер предназначен для локального учебного запуска.

## База данных — работа №3

SQLite подключена в `config/settings.py`, файл `db.sqlite3` создаётся командой migrate. Миграция `0001_initial` создаёт пять основных таблиц и промежуточную таблицу размеров товаров; `0002_demo_data` заполняет демонстрационный каталог. Каталог и главная получают товары через ORM.

| Модель | Страница добавления и списка |
|---|---|
| Category | `/database/categories/` |
| Brand | `/database/brands/` |
| BrandProfile | `/database/profiles/` |
| Size | `/database/sizes/` |
| Product | `/database/products/` |

Связи: Brand—BrandProfile (OneToOneField), Category—Product и Brand—Product (ForeignKey), Product—Size (ManyToManyField). Для каждой таблицы есть отдельный HTML-шаблон, общая форма и список наследуются из `db/base_table.html`. Все пять ModelForm определены в `shop/forms.py`. Сохранение происходит только после `is_valid()`, формы содержат csrf_token, ошибки показываются рядом с полями. После успешного POST выполняется redirect, поэтому обновление страницы не повторяет сохранение.

Сначала добавляйте категории, бренды и размеры, затем профили и товары. Цена: 0.01–1000000 ₽, остаток: целое число 0–1000000, URL проверяется сервером, названия обязательны и не дублируются без учёта регистра, профиль у бренда только один. Размеры: XXS–XXXL из указанного в форме набора. Страницы предназначены для локальной учебной работы; перед публичным размещением необходимо ограничить доступ к операциям записи.

Чтобы воспроизвести записи со скриншотов отчёта после migrate, выполните `python manage.py loaddata practical3_demo`. Фикстура содержит только учебные данные: новый бренд URBAN, категорию «Свитшоты», размер XXL и товар «Свитшот Urban». Загружайте её в учебную базу сразу после миграций, до ввода собственных данных: записи с совпадающими ID заменяются содержимым фикстуры.

Документация: https://docs.djangoproject.com/en/5.2/intro/tutorial01/
