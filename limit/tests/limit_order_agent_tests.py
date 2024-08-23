from trading_framework.execution_client import ExecutionException
from limit.limit_order_agent import LimitOrderAgent
import unittest

class MockExecutionClient:
    def __init__(self):
        self.order_data = []

    def sell(self, product_id: str, amount: int):
        if amount <= 0:
            raise ExecutionException("Amount should be positive")
        self.order_data.append(('sell', product_id, amount))

    def buy(self, product_id: str, amount: int):
        if amount <= 0:
            raise ExecutionException("Amount should be positive")
        self.order_data.append(('buy', product_id, amount))

class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self) -> None:
        self.ec = MockExecutionClient()
        self.limit_order_agent = LimitOrderAgent(self.ec)

    def test_buy_order(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 100)
        self.assertEqual(len(self.limit_order_agent.order_data), 1)
        self.assertEqual(self.limit_order_agent.order_data[0]['order_type'], 'buy')
        self.assertEqual(self.limit_order_agent.order_data[0]['product_id'], 'IBM')
        self.assertEqual(self.limit_order_agent.order_data[0]['amount'], 1000)
        self.assertEqual(self.limit_order_agent.order_data[0]['limit'], 100)

    def test_sell_order(self):
        self.limit_order_agent.add_order('sell', 'IBM', 1000, 100)
        self.assertEqual(len(self.limit_order_agent.order_data), 1)
        self.assertEqual(self.limit_order_agent.order_data[0]['order_type'], 'sell')
        self.assertEqual(self.limit_order_agent.order_data[0]['product_id'], 'IBM')
        self.assertEqual(self.limit_order_agent.order_data[0]['amount'], 1000)
        self.assertEqual(self.limit_order_agent.order_data[0]['limit'], 100)

    def test_execute_order_type_buy(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 100)
        self.limit_order_agent.on_price_tick('IBM', 100)
        self.assertEqual(len(self.limit_order_agent.order_data), 0)
        self.assertEqual(len(self.ec.order_data), 1)
        self.assertEqual(self.ec.order_data[0], ('buy', 'IBM', 1000))

    def test_execute_order_type_sell(self):
        self.limit_order_agent.add_order('sell', 'IBM', 1000, 110)
        self.limit_order_agent.on_price_tick('IBM', 110)
        self.assertEqual(len(self.limit_order_agent.order_data), 1)
        self.assertEqual(len(self.ec.order_data), 0)
        self.assertEqual(self.ec.order_data, [])

    def test_no_order_when_price_not_met(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 100)
        self.limit_order_agent.on_price_tick('IBM', 101)
        self.assertEqual(len(self.limit_order_agent.order_data), 1)
        self.assertEqual(len(self.ec.order_data), 0)

    def test_exception_handling(self):
        self.limit_order_agent.add_order('buy', 'IBM', -1000, 100)
        self.limit_order_agent.on_price_tick('IBM', 99)
        self.assertEqual(len(self.limit_order_agent.order_data), 1)
        with self.assertRaises(ExecutionException) as context:
            self.assertEqual(len(self.ec.order_data), 0)
        breakpoint()

if __name__ == '__main__':
    unittest.main()
