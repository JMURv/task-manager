### Hexlet tests and linter status:
[![Actions Status](https://github.com/JMURv/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/JMURv/python-project-52/actions)
[![linter-and-test](https://github.com/JMURv/python-project-52/actions/workflows/linter-and-test.yml/badge.svg)](https://github.com/JMURv/python-project-52/actions/workflows/linter-and-test.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/d391d5ad05b78ef79a11/maintainability)](https://codeclimate.com/github/JMURv/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d391d5ad05b78ef79a11/test_coverage)](https://codeclimate.com/github/JMURv/python-project-52/test_coverage)
___
# Менеджер задач
Веб-приложения для управления задачами. Можно сказать, похоже на упрощенный аналог jira. Идеально подойдёт для небольших команд или, может, использования локально.
Бэкэнд написан на Django и его внутренних CBV's, а фронтенд - на Bootstrap. Использована база данных PostgreSQL.

### Что реализовано в этом проекте?
- CRUD операции для каждой из сущностей: пользователи, статусы, метки, задачи.
- Система регистрации и аутентификации пользователей.
- Локализация RU | EN
- Фильтрация задачи при помощи django-filter.
- Неавторизованные пользователи не могут взаимодействовать ни с одной сущностью, кроме просмотра спика пользователей. Также реализован запрет на удаление задачи не её автором, удаление меток и статусов, если они привязаны к задаче.

### Как установить?
1. `git clone https://github.com/JMURv/python-project-52.git`
2. `make ready`
3. Через секунду приложение доступно на localhost