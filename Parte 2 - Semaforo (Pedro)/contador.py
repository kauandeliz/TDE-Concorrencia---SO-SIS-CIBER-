import threading
import time

T = 8     # numero de threads
M = 2000  # incrementos por thread



def main():
    esperado = T * M
    print(f"Threads: {T}, incrementos por thread: {M}")
    print(f"Valor esperado = {T} x {M} = {esperado}\n")


if __name__ == "__main__":
    main()