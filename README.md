# ToDo Приложение

Простое приложение для управления задачами, написанное на Python с использованием PySide6.

## Структура проекта

```
src/
├── ui/
│   ├── components/     # Компоненты интерфейса
│   ├── dialogs/       # Диалоговые окна
│   ├── styles/        # Стили приложения
│   └── main_window.py # Основное окно приложения
├── utils/             # Утилиты
└── main.py           # Точка входа
```

## Установка

1. Клонируйте репозиторий
2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск

```bash
python src/main.py
```

## Функциональность

- Создание задач с названием, датой выполнения, приоритетом, описанием и подзадачами
- Просмотр списка задач
- Редактирование задач
- Современный и удобный интерфейс
