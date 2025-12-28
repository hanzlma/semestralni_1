import unittest as u
from .card_tests import CardTests
from .player_tests import PlayerTests
from .runner_tests import RunnerTests


def get_tests(testClass):
    return [testClass(entry) for entry in u.TestLoader().getTestCaseNames(testClass)]


def suite():
    suite = u.TestSuite()
    suite.addTests(get_tests(CardTests))
    suite.addTests(get_tests(PlayerTests))
    suite.addTests(get_tests(RunnerTests))
    return suite


if __name__ == "__main__":
    runner = u.TextTestRunner(verbosity=0)
    runner.run(suite())
