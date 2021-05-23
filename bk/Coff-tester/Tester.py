import Coffee

def mock_inp():
    print("1")
    return 1

Coffee.take_input = mock_inp
Coffee.initmachine("kk.txt")