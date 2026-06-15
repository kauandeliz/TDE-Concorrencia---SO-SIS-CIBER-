# Deadlock - versao que trava
#
# Temos 2 threads e 2 locks (LOCK_A e LOCK_B).
#
# Thread 1: pega LOCK_A, espera um pouco, tenta pegar LOCK_B
# Thread 2: pega LOCK_B, espera um pouco, tenta pegar LOCK_A
#
# Depois de pegar o primeiro lock cada uma, as duas vao ficar
# esperando o lock que a OUTRA esta segurando. Ninguem solta nada,
# entao trava pra sempre. Isso e deadlock.
#
# As 4 condicoes do Coffman acontecem aqui:
# 1) Exclusao mutua -> cada Lock so pode ser de uma thread por vez
# 2) Manter e esperar -> cada thread fica com seu lock esperando o outro
# 3) Sem preempcao -> nao da pra "roubar" o lock da outra thread
# 4) Espera circular -> T1 espera T2, e T2 espera T1 (ciclo)

import threading
import time

LOCK_A = threading.Lock()
LOCK_B = threading.Lock()


def thread1():
   print("T1: pegando LOCK_A")
    LOCK_A.acquire()
    print("T1: peguei LOCK_A")

    time.sleep(0.05)

    print("T1: tentando pegar LOCK_B (vai travar aqui)")
    LOCK_B.acquire()
    print("T1: peguei LOCK_B")

    print("T1: terminei!")
    LOCK_B.release()
    LOCK_A.release()


def thread2():
    print("T2: pegando LOCK_B")
    LOCK_B.acquire()
    print("T2: peguei LOCK_B")

    time.sleep(0.05)

    print("T2: tentando pegar LOCK_A (vai travar aqui)")
    LOCK_A.acquire()
    print("T2: peguei LOCK_A")

    print("T2: terminei!")
    LOCK_A.release()
    LOCK_B.release()


def main():
    print("=== Deadlock - versao que trava ===\n")

    t1 = threading.Thread(target=thread1)
    t2 = threading.Thread(target=thread2)

    t1.start()
    t2.start()

    # espera 3 segundos pra ver se termina
    t1.join(timeout=3)
    t2.join(timeout=3)

    if t1.is_alive() or t2.is_alive():
        print("\n!!! DEADLOCK !!!")
        print("As threads ainda estao vivas e travadas:")
        if t1.is_alive():
            print("- Thread 1 esta presa esperando LOCK_B")
        if t2.is_alive():
            print("- Thread 2 esta presa esperando LOCK_A")
        print("\nT1 tem o LOCK_A e quer o LOCK_B (que T2 tem)")
        print("T2 tem o LOCK_B e quer o LOCK_A (que T1 tem)")
        print("Ninguem larga o que tem -> espera circular -> DEADLOCK")
        print("\nEncerrando o programa (ele nao terminaria sozinho).")
        import os
        os._exit(0)
    else:
        print("\nAs duas threads terminaram normal (nao deveria acontecer aqui)")


if __name__ == "__main__":
    main()