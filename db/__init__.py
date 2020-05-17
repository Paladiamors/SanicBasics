
from db.appTables import *
from db.base import getSession, sessionManager


if __name__ == "__main__":
    
    sessionManager.createTables("local")