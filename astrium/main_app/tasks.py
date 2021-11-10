from celery import shared_task
from yahoo_fin.stock_info import *
from threading import Thread
import queue


@shared_task(bind=True)
def update_security(self, securityselector):
    data = {}
    available_securities = tickers_sp500()
    for i in securityselector:
        if i in available_securities:
            pass
        else:
            securityselector.remove(i)

    n_threads = len(securityselector)
    thread_list = []
    que = queue.Queue()

    for i in range(n_threads):
        thread = Thread(target=lambda q, arg1: q.put(
            {securityselector[i]: get_quote_table(arg1)}), args=(que, securityselector[i]))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        if result:
            data.update(result)

    return 'Done'
