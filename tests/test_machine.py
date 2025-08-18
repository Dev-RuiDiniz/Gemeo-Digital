import unittest
from twins.machine import Machine

class TestMachine(unittest.TestCase):
    def test_operate_returns_float(self):
        m = Machine("Test", 1, 2)
        t = m.operate()
        self.assertIsInstance(t, float)

    def test_average_time(self):
        m = Machine("Test", 1, 2)
        m.operate()
        avg = m.average_time()
        self.assertTrue(m.min_time <= avg <= m.max_time)

if __name__ == "__main__":
    unittest.main()
