import Coffee
import threading
import unittest


class CoffeeTest(unittest.TestCase):
    def test_multithread(self):
        print('Testing multithreading')
        outlets = Coffee.load_machine("multithread.txt")
        thr = []
        for i in range(outlets):
            thr.append(threading.Thread(target=large_tester, args=([i])))
            thr[-1].start()
        for th in thr:
            th.join()

    def testraise(self):
        Coffee.load_machine("kk.txt")
        assert Coffee.dispense('hot_coffee') is True

        # if drink is not dispensed and low and miss both are None that means the beverage was not present
        dispensed, low, miss = Coffee.dispense('cold_drink')
        assert dispensed is False
        assert low is None
        assert miss is None

    def test_missing_item(self):
        Coffee.load_machine("kk.txt")
        assert Coffee.dispense('hot_coffee') is True
        dispensed, low, miss = Coffee.dispense('hot_coffee')
        assert dispensed is False
        assert low == ['hot_milk', 'sugar_syrup']  # low on hot milk, sugar_syrup
        dispensed, low, miss = Coffee.dispense('black_tea')
        assert dispensed is False
        assert low == ['sugar_syrup']  # low on hot milk

    def testrefill(self):
        Coffee.load_machine("kk.txt")
        assert Coffee.dispense('hot_coffee') is True

        dispensed, low, missing = Coffee.dispense('hot_coffee')
        assert dispensed is False
        assert low == ['hot_milk', 'sugar_syrup']  # low on hot milk, sugar_syrup
        for i in low:
            Coffee.change_quantity(i, 1000)

        assert Coffee.dispense('hot_coffee') is True

        dispensed, low, missing = Coffee.dispense('green_tea')
        assert dispensed is False
        assert missing == ['green_mixture']  # low on hot milk, sugar_syrup

        assert Coffee.fill_new_item(missing[0], 1000) is True
        assert Coffee.dispense('green_tea') is True

        assert Coffee.fill_new_item('hot_water', 1000) is False


def large_tester(outlet):
    print('Outlet ', outlet)
    Coffee.change_quantity('hot_milk', 1000)
    print('added hot milk by thread ', outlet)
    assert Coffee.dispense('hot_coffee') is True
    print('dispensed for ', outlet)
    assert Coffee.dispense('black_tea') is True
    print('dispensed for ', outlet)
    val = Coffee.fill_new_item('cold_drink', 1000)
    if val:
        print('Successfully added')
    else:
        print('Already present in list')

unittest.main()
