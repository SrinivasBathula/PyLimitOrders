from trading_framework.execution_client import ExecutionClient, ExecutionException
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.order_data = []
        self.ec = execution_client

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        for order in self.order_data:
            try:
                # if order type is sell and price is above 100
                if (order['order_type'] == 'sell' and price > order['limit']):
                    self.ec.sell(product_id, order['amount'])
                    self.order_data.remove(order)
                # if order type is buy and price is less than or equal to 100
                elif (order['order_type'] == 'buy' and price <= order['limit']):
                    self.ec.buy(product_id, order['amount'])
                    self.order_data.remove(order)
            except ExecutionException as e:
                print(str(e))

    def add_order(self, order_type: str, product_id: str, amount: int, limit: float):
        self.order_data.append({
            'order_type': order_type,
            'product_id': product_id,
            'amount': amount,
            'limit': limit
        })
