from django.shortcuts import render
from wStocks_main.models import Stock_Watcher15, Stock_Watcher30, Stock_Watcher60, wStockUser
from wStocks_main.tasks import send_email, get_to_data

def adicionar(req):
    if req.method == 'POST':
        if wStockUser.objects.count() == 1:
            email      = wStockUser.objects.all()[0].name
            ticker     = req.POST['ticker']
            buy_price  = req.POST['lower-limit']
            sell_price = req.POST['upper-limit']

            if req.POST['interval'] == '15':
                Stock_Watcher15.objects.create(email=email, ticker=ticker, buy_price=buy_price, sell_price=sell_price)
            elif req.POST['interval'] == '30':
                Stock_Watcher30.objects.create(email=email, ticker=ticker, buy_price=buy_price, sell_price=sell_price)
            elif req.POST['interval'] == '60':
                Stock_Watcher60.objects.create(email=email, ticker=ticker, buy_price=buy_price, sell_price=sell_price)
            else:
                return render(req, 'adicionar.html', {'user': True, 'non_created': True})

        else:
            return render(req, 'adicionar.html', {'user': False})

    return render(req, 'adicionar.html', {'user': True})

def entrar(req):
    if wStockUser.objects.count() == 1:
        return render(req, 'entrar.html', {'mode': False, 'username': wStockUser.objects.all()[0].name})
   
    elif req.method == 'POST':
            email = req.POST['email']
            name  = req.POST['name']
            wStockUser.objects.create(email=email,name=name)
            return render(req, 'entrar.html', {'mode': False, 'username': name})
    
    return render(req, 'entrar.html', {'mode': True})

def editar(req):
    if req.method == 'POST':
        if req.POST['time'] == '15':
            Stock_Watcher15.objects.filter(ticker=req.POST['ticker']).delete()
        elif req.POST['time'] == '30':
            Stock_Watcher30.objects.filter(ticker=req.POST['ticker']).delete()
        elif req.POST['time'] == '60':
            Stock_Watcher60.objects.filter(ticker=req.POST['ticker']).delete()


    th = {
        'stock_watcher_15': Stock_Watcher15.objects.all(),
        'stock_watcher_30': Stock_Watcher30.objects.all(),
        'stock_watcher_60': Stock_Watcher60.objects.all(),
    }

    return render(req, "editar.html", th)
    


#################
from apscheduler.schedulers.background import BackgroundScheduler

def create_checker(watcher):
    def checker():
        wstocks = watcher.objects.all()
        print(f'{watcher.__name__}')
        for stock in wstocks:
            do_some = stock.checkInterval()
            if do_some['opflag']:
                send_email(get_to_data(stock.email,stock.ticker, do_some['opcode']))
    return checker

scheduler = BackgroundScheduler()
scheduler.add_job(create_checker(Stock_Watcher15), 'interval', minutes=15)
scheduler.add_job(create_checker(Stock_Watcher30), 'interval', minutes=30)
scheduler.add_job(create_checker(Stock_Watcher60), 'interval', minutes=60)
scheduler.start()
