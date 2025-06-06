from PySide6.QtCore import QFile

def load_stylesheet(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Ошибка при загрузке стилей: {e}")
        return ""