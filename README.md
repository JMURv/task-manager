### Hexlet tests and linter status:
[![Actions Status](https://github.com/JMURv/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/JMURv/python-project-52/actions)
[![linter-and-test](https://github.com/JMURv/python-project-52/actions/workflows/linter-and-test.yml/badge.svg)](https://github.com/JMURv/python-project-52/actions/workflows/linter-and-test.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/d391d5ad05b78ef79a11/maintainability)](https://codeclimate.com/github/JMURv/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d391d5ad05b78ef79a11/test_coverage)](https://codeclimate.com/github/JMURv/python-project-52/test_coverage)
___
# Менеджер задач
[Веб-приложение](https://task-manager.home.jmurv.site/) для управления задачами. Можно сказать, похоже на упрощенный аналог jira. Идеально подойдёт для небольших команд или, может, использования локально.
Бэкэнд написан на Django и его внутренних CBV's, а фронтенд - на Bootstrap. Использована база данных PostgreSQL.

### Что реализовано в этом проекте?
- CRUD операции для каждой из сущностей: пользователи, статусы, метки, задачи.
- Система регистрации и аутентификации пользователей.
- Локализация RU | EN
- Фильтрация задач при помощи django-filter.
- Неавторизованные пользователи не могут взаимодействовать ни с одной сущностью, кроме просмотра спика пользователей. Также реализован запрет на удаление задачи не её автором, удаление меток и статусов, если они привязаны к задаче.
- Система трекинга ошибок через Rollbar
- Рабочий пример можно увидеть по [ссылке](https://task-manager.home.jmurv.site/)

### Как установить?
1. Настройте ваши переменные окружения: `cp .env.sample .env` и отредактируйте необходимые поля.
2. `git clone https://github.com/JMURv/python-project-52.git`
3. `make ready`
4. Через секунду приложение доступно на localhost
