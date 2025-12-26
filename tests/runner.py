import unittest as u
from .card_tests import Cards

suite = u.TestLoader().loadTestsFromTestCase(Cards)
runner = u.TextTestRunner(verbosity=0)
result = runner.run(suite)
print(f"Tests run: {result.testsRun}")
