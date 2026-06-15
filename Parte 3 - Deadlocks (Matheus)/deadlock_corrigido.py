# Deadlock - versao corrigida
#
# A correcao e simples: as DUAS threads vao pegar os locks na MESMA
# ORDEM (primeiro LOCK_A, depois LOCK_B). Antes a Thread 2 pegava
# LOCK_B primeiro - então mudamos isso pra ela pegar LOCK_A primeiro, igual a thread1.
#
# Com essa regra, nao tem mais como dar deadlock: se uma thread quer
# o LOCK_B, ela precisa ter pego o LOCK_A antes. Entao nunca vai ter
# uma thread com LOCK_B esperando o LOCK_A (que e o que causava o
# ciclo antes).
#
# Isso quebra a condicao de "espera circular" do Coffman.

import threading
import time

LOCK_A = threading.Lock()
LOCK_B = threading.Lock()


def thread1():
    print("T1: pegando LOCK_A")
    LOCK_A.acquire()
    print("T1: peguei LOCK_A")

    time.sleep(0.05)

    print("T1: pegando LOCK_B")
    LOCK_B.acquire()
    print("T1: peguei LOCK_B")

    print("T1: terminei!")
    LOCK_B.release()
    LOCK_A.release()


def thread2():
    # antes era LOCK_B primeiro, agora seguimos a mesma ordem: A depois B
    print("T2: pegando LOCK_A")
    LOCK_A.acquire()
    print("T2: peguei LOCK_A")

    time.sleep(0.05)

    print("T2: pegando LOCK_B")
    LOCK_B.acquire()
    print("T2: peguei LOCK_B")

    print("T2: terminei!")
    LOCK_B.release()
    LOCK_A.release()


def main():
    print("=== Deadlock - versao corrigida (mesma ordem pras duas) ===\n")

    t1 = threading.Thread(target=thread1)
    t2 = threading.Thread(target=thread2)

    inicio = time.time()
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    fim = time.time()

    print(f"\nAs duas terminaram certinho em {fim - inicio:.2f}s")
    print("Sem deadlock!")


if __name__ == "__main__":
    main()
