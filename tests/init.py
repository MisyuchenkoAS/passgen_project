import os
import sys    # Поиск модулей

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)   # Список путей, где Python ищет модули при импорте
