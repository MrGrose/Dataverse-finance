# Dataverse - платформа образовательных курсов.
Данный проект автоматизирует работу с образовательными потоками, преподавателями, менеджерами, контрактами и начислениями вознаграждений для авторов и ведущих образовательных курсов.
Система позволяет вести учет преподавателей, менеджеров, образовательных потоков, заключать контракты, рассчитывать вознаграждения и фиксировать выплаты.

## Функциональность
### Модели
1. `Person`: Хранит информацию о преподавателях, которые могут быть авторами или ведущими курсов.
    - username: Имя преподавателя.
    - contact_email: Контактный email.
    - contact_phone: Контактный телефон.

2. `Manager`: Сотрудник, ответственный за оформление контрактов и начислений.
    - manager: Имя менеджера.

3. `Education_Thread`: Хранит информацию о курсах/потоках, по которым заключаются контракты.
    - name: Название потока (курса).
    - started_at: Дата начала потока.
    - ended_at: Дата окончания потока.
    - type_course: Тип курса (regular, bootcamp, workshop, indi).
    - articul: Артикул потока (генерируется автоматически).

4. `Author`: вязывает преподавателя с образовательным потоком и фиксирует условия авторского вознаграждения.
    - uthor: Преподаватель (Person).
    - thead: Образовательные потоки (Education_Thread).
    - revenue: Ожидаемый оборот/прибыль.
    - reward_percent: Процент вознаграждения.
    - reward_type: Тип награды (оборот/прибыль).
    - currency: Валюта (RUB/USD).

5. `Presenter`: Связывает преподавателя с потоком и фиксирует условия почасовой оплаты.
    - presenter: Преподаватель (Person).
    - thead: Образовательные потоки (Education_Thread).
    - estimate: Прогнозное количество часов.
    - hourly_rate: Ставка за час.
    - currency: Валюта (RUB/USD).

6. `Contract`: Документирует условия сотрудничества с авторами и ведущими по конкретным образовательным потокам.
    - contract_number: Уникальный номер контракта.
    - authors: Авторы (Author).
    - presenters: Ведущие (Presenter).
    - created_at: Дата создания.
    - started_at: Дата запуска контракта.
    - ended_at: Дата окончания контракта.
    - created_by: Менеджер, создавший контракт.
    - responsible_manager: Ответственный менеджер.
    - comment_manager: Комментарий менеджера.

7. `Accrual`: Фиксирует начисления по контракту, автоматически рассчитывает сумму
    - contract_type: Тип контракта (author/presenter).
    - contract: Контракт (Contract).
    - accrual_flags: Флаг начисления (схлопнутое, корректировка, нефинансовое).
    - accrual_status: Статус начисления (ожидание, проверено).
    - payed: Факт оплаты.
    - created_by: Менеджер, создавший начисление.
    - updated_by: Менеджер, изменивший начисление.
    - comment_manager: Комментарий менеджера.
    - hours_worked: Фактические часы (для ведущих).
    - real_revenue: Фактический оборот/выручка (для авторов).
    - calculation_formula: JSON с формулой расчета и исходными данными.

## Требования
- Python 3.12+
- Django 5

## Установка
1. Клонировать репозиторий:
    ```bash
    git clone <URL репозитория>
    cd <имя директории>
    ```
2. Установить зависимости:
    ```bash
    pip install -r requirements.txt
    ```
3. Создать файл .env в корне проекта со следующими переменнами:
    - [SECRET_KEY](https://docs.djangoproject.com/en/5.2/ref/settings/#secret-key) = секретный ключ для криптографической подписи, должен быть уникальным и непредсказуемым.
    - [DEBUG](https://docs.djangoproject.com/en/5.2/ref/settings/#debug) = булево значение (True или False), включающее или отключающее режим отладки.
    - [ALLOWED_HOSTS](https://docs.djangoproject.com/en/5.2/ref/settings/#allowed-hosts) = список разрешённых доменов/хостов, разделённых запятыми.

4. Настройте проект Django, указав необходимые параметры в файле settings.py.
    ```bash
        LANGUAGE_CODE = 'ru'
        TIME_ZONE = 'Europe/Moscow'
        USE_I18N = True
        USE_TZ = True
        INSTALLED_APPS = [
            ....
        'app_name',
        'app_name',
        'app_name',
        ]
        SECRET_KEY = env.str('SECRET_KEY')
        DEBUG = env.bool('DEBUG', default=False)
        ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
    ```
5. Создайте базу данных и примените миграции, создайте админ пользователя, запуск сервера:
    ```bash
        python manage.py makemigrations
        python manage.py migrate
        python manage.py createsuperuser
        python manage.py runserver
    ```