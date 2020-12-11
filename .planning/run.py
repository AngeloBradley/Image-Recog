import logging
import threading
import time
import ai
import database
import new_file_detection


def start_database():
    pass

def start_ai():
    pass

def start_nfd():
    pass




if __name__ == '__main__':
    database_thread = threading.Thread(target=start_database)
    ai_thread = threading.Thread(target=start_ai)
    nfd_thread = threading.Thread(target=start_nfd)

    database_thread.start()
    ai_thread.start()
    nfd_thread.start()

    database_thread.join()
    ai_thread.join()
    nfd_thread.join()
