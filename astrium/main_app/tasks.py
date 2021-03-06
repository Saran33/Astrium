from celery import shared_task
from yahoo_fin.stock_info import *
from threading import Thread
import queue
from channels.layers import get_channel_layer
import asyncio
import simplejson as json

# from .sqlalch import all_tickers
# from pwe.av import get_av_live, av_search
from .apis.utilsAPI import list_all_tickers, get_ticker
from .apis.nom import list_nomics_coins

@shared_task(bind=True)
def update_security(self, securityselector):
    data = {}
    # available_securities = tickers_sp500()
    # available_securities = all_tickers()
    available_securities = list_all_tickers()
    for i in securityselector:
        # available_securities = av_search(i)
        if i in available_securities:
            pass
        else:
            securityselector.remove(i)

    n_threads = len(securityselector)
    thread_list = []
    que = queue.Queue()

    for i in range(n_threads):
        # thread = Thread(target=lambda q, arg1: q.put(
            # {securityselector[i]: get_quote_table(arg1)}), args=(que, securityselector[i]))
        thread = Thread(target=lambda q, arg1: q.put({securityselector[i]: json.loads(
            # json.dumps(get_quote_table(arg1), ignore_nan=True))}), args=(que, securityselector[i]))
            # json.dumps(get_av_live(arg1), ignore_nan=True))}), args=(que, securityselector[i]))
            json.dumps(get_ticker(arg1, stocks=False), ignore_nan=True))}), args=(que, securityselector[i]))

        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        if result:
            data.update(result)

    # send data to group
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)  # inside of thread

    # Allocate task to loop
    loop.run_until_complete(channel_layer.group_send("security_track", {
        'type': 'send_security_update',
        'message': data,  # Currently in dict format, need to convert it to JSON dump
    }))

    return 'Done'
