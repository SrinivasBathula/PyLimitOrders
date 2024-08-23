import unittest

suite = unittest.TestLoader().loadTestsFromName('limit.tests.limit_order_agent_tests.LimitOrderAgentTest')
unittest.TextTestRunner().run(suite)
