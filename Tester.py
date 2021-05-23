import Coffee
import threading
import unittest

threads = {}
i = 0
ips = []


def mock_inp():
    global i
    global threads
    x = threading.get_ident()
    if x in threads:
        pass
    else:
        threads[x] = i
        i += 1
    v = ips[threads[x]].pop(0)
    print('thread ', threads[x], ' test_selection: ', v)
    return v
    # return 1


def test_parallel_dispensing():
    global ips
    ips = [[1, 1, 1, 'kill_thread'], [1, 1, 1, 'kill_thread'], [1, 1, 1, 'kill_thread']]
    Coffee.initmachine("kk.txt")
    print('Test Finished')


def APItester():
    Coffee.load_machine("kk.txt")
    assert Coffee.dispense('hot_coffee') == True
    assertRaises(ValueError, Coffee.dispense, 'cool')


class raiseTest(unittest.TestCase):
    def testraise(self):
        Coffee.load_machine("kk.txt")
        assert Coffee.dispense('hot_coffee') == True
        dispensed, low, miss = Coffee.dispense(
            'cold_drink')  # if drink is not dispensed and low and miss both are None that means the beverage was not present
        assert dispensed == False
        assert low == None
        assert miss == None

    def test_missing_item(self):
        Coffee.load_machine("kk.txt")
        assert Coffee.dispense('hot_coffee') == True
        dispensed, low, miss = Coffee.dispense('hot_coffee')
        assert dispensed == False
        assert low == ['hot_milk', 'sugar_syrup']  # low on hot milk, sugar_syrup
        dispensed, low, miss = Coffee.dispense('black_tea')
        assert dispensed == False
        assert low == ['sugar_syrup']  # low on hot milk

    def testrefill(self):
        Coffee.load_machine("kk.txt")
        assert Coffee.dispense('hot_coffee') == True

        dispensed, low, missing = Coffee.dispense('hot_coffee')
        assert dispensed == False
        assert low == ['hot_milk', 'sugar_syrup']  # low on hot milk, sugar_syrup
        for i in low:
            Coffee.change_quantity(i, 1000)

        assert Coffee.dispense('hot_coffee') == True

        dispensed, low, missing = Coffee.dispense('green_tea')
        assert dispensed == False
        assert missing == ['green_mixture']  # low on hot milk, sugar_syrup

        Coffee.fill_new_item(missing[0], 1000)
        assert Coffee.dispense('green_tea') == True

    def test_multithread(self):
        print('Testing multithreading')
        outlets=Coffee.load_machine("kk.txt")
        thr=[]
        for i in range(outlets):
            thr.append(threading.Thread(target=large_tester, args=([i])))
            thr[-1].start()
        for th in thr:
            th.join()

def large_tester(outlet):
    print('Outlet ', outlet)
    Coffee.change_quantity('hot_milk', 1000)
    print('added hot milk by thread ', outlet)
    assert Coffee.dispense('hot_coffee') == True
    print('dispensed for ',outlet)

# Coffee.take_input = mock_inp
# test_parallel_dispensing()
# APItester()
unittest.main()
