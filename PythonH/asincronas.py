import time
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

def super_task(a):
    time.sleep(3)
    logging.info(f"Terminamos la tarea compleja con valores {a}" )

executor = ThreadPoolExecutor(max_workers=1)

executor.submit(super_task, 1)
executor.submit(super_task, 2)
