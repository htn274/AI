from forward import main as main_forward
from backward import main as main_backward
from resolution import main as main_resolution

if __name__ == "__main__":
    filename = input("Enter file input of knowledge base: ")

    try:
        choice = int(input("0. Exit\n1. Forward\n2. Backward\n3. Resolution\nWhich do you want to choose? "))
        if choice == 0: exit(0)
        if choice == 1:
            main_forward(filename)
        if choice == 2:
            main_backward(filename)
        if choice == 3:
            main_resolution(filename)
    except:
        pass
