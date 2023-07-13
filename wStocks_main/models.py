from wStocks_main.tasks import get_stock_price
from django.db import models

class Stock_Watcher(models.Model):
    email      = models.EmailField(max_length=150)
    ticker     = models.CharField(max_length=6)
    buy_price  = models.FloatField()
    sell_price = models.FloatField()

    def getStockPrice(self) -> float:
        return get_stock_price(self.ticker)

    def getBuyPrice(self) -> float:
        return self.buy_price
    
    def getSellPrice(self) -> float:
        return self.sell_price
    
    def checkInterval(self) -> dict:
        now_price = self.getStockPrice()

        print(now_price)
        print(self.buy_price)

        return {
            'opflag': self.getBuyPrice() > now_price or self.getSellPrice() < now_price,
            'opcode': self.getBuyPrice() > now_price
        }

class Stock_Watcher15(Stock_Watcher):
    pass

class Stock_Watcher30(Stock_Watcher):
    pass

class Stock_Watcher60(Stock_Watcher):
    pass

class wStockUser(models.Model):
    name  = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)



