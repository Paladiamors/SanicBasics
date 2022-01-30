
from db.auth import *
from db.base import get_session


if __name__ == "__main__":
    from db.base import session_manager
    session_manager.createTables("local")
