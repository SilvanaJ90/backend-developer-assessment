from .base_model import Base
from .user import User
from .messages import Message
from .engine.db_storage import DBStorage

# Inicializa el almacenamiento global
storage = DBStorage()
storage.reload()
