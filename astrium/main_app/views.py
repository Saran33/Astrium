from django.shortcuts import render
from yahoo_fin.stock_info import *
from django.http import HttpResponse
from collections import defaultdict
import time
import queue
from threading import Thread
from asgiref.sync import sync_to_async

# from .dtools import get_single_tkr, get_multi_tkr, indexed_vals, ext_str_lst, calc_endpoint
# from .sqlalch import all_tickers
# from pwe.av import get_av_live, av_search
from .apis.utilsAPI import list_all_tickers, get_ticker
from .apis.nom import list_nomics_coins


# Create your views here.

# def securitySearcher(request):
#     keywords = request.GET.getlist('keywords')
#     security_search = av_search(keywords)
#     return render(request, 'main_app/securityselector.html', {"security_search": security_search})

def SecuritySelector(request):
    # security_selector = tickers_ftse100()
    # security_selector = tickers_sp500()
    # security_selector = request.GET.getlist('keywords')
    # security_selector = all_tickers()
    # security_selector = {'AAPL': 'Apple Inc.', 'TSLA': 'Tesla'}
    stocks = {'AAPL': 'Apple Inc.', 'TSLA': 'Tesla'}
    # security_selector = list_all_tickers()
    security_selector = list_nomics_coins(attributes=['id', 'name'])
    print(security_selector)
    return render(request, 'main_app/securityselector.html', {"securityselector": security_selector})


@sync_to_async
def checkAuthenticated(request):
    if not request.user.is_authenticated:
        return False
    else:
        return True

async def SecurityTracker(request):
    is_logged_in = await checkAuthenticated(request)
    if not is_logged_in:
        return HttpResponse("Login First")
    securityselector = request.GET.getlist('securityselector')
    print('securityselector')
    data = {}
    # data = defaultdict()
    # available_securities = tickers_sp500()
    # available_securities = all_tickers()
    available_securities = list_all_tickers()
    for i in securityselector:
        # available_securities = av_search(i)
        if i in available_securities:
            pass
        else:
            return HttpResponse("Error")

    n_threads = len(securityselector)
    thread_list = []
    que = queue.Queue()
    start = time.time()
    # for i in securityselector:
    #     result = get_quote_table(i)
    #     if result:
    #         data[f'{i}'] = result
    for i in range(n_threads):
        thread = Thread(target=lambda q, arg1: q.put(
            # {securityselector[i]: get_quote_table(arg1)}), args=(que, securityselector[i]))
            # {securityselector[i]: get_av_live(arg1)}), args=(que, securityselector[i]))
            {securityselector[i]: get_ticker(arg1, stocks=False)}), args=(que, securityselector[i]))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        if result:
            data.update(result)
            # for key, value in result.items():
            #     data[f'{key}'] = value
    end = time.time()
    speed = end - start
    print("TIME TAKEN:", speed)

    # for key, value in data.items():
    #     print(key, value)
    print(data)
    return render(request, 'main_app/securitytracker.html', {'data': data, 'room_name': 'track'})


# def SecurityTracker(request):
#     details = get_quote_table('AAPL')
#     print(details)
#     return render(request, 'main_app/securitytracker.html')

# def SecurityTracker(request):
#     securityselector = request.GET.getlist('securityselector')
#     print('securityselector')
#     data = {}
#     available_securities = tickers_sp500()
#     for i in securityselector:
#         if i in available_securities:
#             pass
#         else:
#             return HttpResponse("Error")
#     for i in securityselector:
#         details = get_quote_table(i)
#         data.update(details)

#     print(data)
#     return render(request, 'main_app/securitytracker.html')

# def SecurityTracker(request):
#     securityselector = request.GET.getlist('securityselector')
#     print('securityselector')
#     # data = {}
#     data = defaultdict()
#     available_securities = tickers_sp500()
#     for i in securityselector:
#         if i in available_securities:
#             pass
#         else:
#             return HttpResponse("Error")
#     for i in securityselector:
#         details = get_quote_table(i)
#         data[f'{i}'] = details

#     for key, value in data.items():
#         print(key, value)
#     return render(request, 'main_app/securitytracker.html')
