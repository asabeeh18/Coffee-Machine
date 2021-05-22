import Coffee
import threading

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


Coffee.take_input = mock_inp
test_parallel_dispensing()
