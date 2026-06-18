# TDE - Concorrencia: Filosofos, Semaforos e Deadlock

VIDEO NO YOUTUBE: https://youtu.be/8kKp3YjBw4g

## Integrantes do grupo

- Kauan de Moraes de Liz 
- Pedro Henrique Rebechi 
- Matheus Henrique Martins 

## Linguagem usada

Python 3. Nao usamos nenhuma biblioteca
externa, so o que ja vem com o Python (`threading`, `time`, `random`).

## Como rodar


```bash
# Parte 1
python3 parte1-filosofos/filosofos_naive.py
python3 parte1-filosofos/filosofos_corrigido.py

# Parte 2
python3 parte2-semaforo/contador.py

# Parte 3
python3 parte3-deadlock/deadlock_travado.py
python3 parte3-deadlock/deadlock_corrigido.py
```

A versao "naive" da parte 1 e a "travado" da parte 3 vao mostrar um
monte de mensagens e depois travar de propósito (deadlock), mas o
programa detecta isso e se encerra sozinho depois de alguns segundos.

---

## Parte 1 - Jantar dos Filosofos

### O que e o problema

Tem 5 filosofos numa mesa redonda. Cada um fica alternando entre
pensar e comer. Para comer, precisa dos 2 garfos do lado (esquerdo e
direito), mas os garfos sao compartilhados com os vizinhos.

### Por que da deadlock (versao ingenua)

Cada filosofo tenta pegar primeiro o garfo da esquerda e depois o da
direita. Se todos pegarem o garfo da esquerda ao mesmo tempo (que e o
que forcamos no codigo com uma Barrier), ninguem consegue pegar o garfo
do vizinho porque ele esta na mao do vizinho. Todo mundo fica esperando
pra sempre.

As 4 condicoes do Coffman que rolam aqui:

1. **Exclusao mutua** - cada garfo (Lock) so pode ser usado por um
   filosofo de cada vez
2. **Manter e esperar** - o filosofo fica com o garfo da esquerda
   enquanto espera o da direita
3. **Sem preempcao** - nao tem como tirar o garfo de quem ja esta
   segurando
4. **Espera circular** - o filosofo 0 espera o garfo do 1, o 1 espera
   o do 2, e assim vai até o ultimo esperar o do primeiro, fechando o
   ciclo

### Como resolvemos

Demos um numero pra cada garfo (0 a 4). Cada filosofo sempre pega
primeiro o garfo de **numero menor** e depois o de **numero maior**,
nao importa se esse for o garfo da esquerda ou da direita dele.

Isso resolve porque quebra a **espera circular**: como todo mundo
respeita a mesma ordem (0 antes de 1, 1 antes de 2...), nunca vai
formar um ciclo de espera. Sempre vai ter algum filosofo que consegue
pegar os dois garfos e comer, liberando espaco pros outros.

### Sobre nao deixar ninguem com fome

Achamos que isso ficou ok porque:
- O `Lock` do Python ja meio que respeita quem chegou primeiro na fila
  de espera
- Cada filosofo "pensa" por um tempo aleatorio entre uma refeicao e
  outra, entao ninguem fica sempre "na frente" dos outros

No teste que fizemos, todos os 5 filosofos conseguiram comer
exatamente 5 vezes cada, então parece que ta justo.

### Pseudocodigo (versao corrigida)

```
garfos numerados de 0 a 4
garfo i fica entre o filosofo i e o filosofo (i+1)

para cada filosofo i:
  esquerda = i
  direita = (i+1) % 5

  primeiro = o menor entre esquerda e direita
  segundo  = o maior entre esquerda e direita

  repetir:
    pensar
    pegar garfo "primeiro"
    pegar garfo "segundo"
    comer
    soltar garfo "segundo"
    soltar garfo "primeiro"
```

### Print da execucao (versao naive - deu deadlock)

```
Filosofo 0: peguei o garfo 0
Filosofo 1: peguei o garfo 1
Filosofo 2: peguei o garfo 2
Filosofo 3: peguei o garfo 3
Filosofo 4: peguei o garfo 4
Filosofo 0: agora vou tentar o garfo 1 (direita)... vai travar
Filosofo 1: agora vou tentar o garfo 2 (direita)... vai travar
Filosofo 2: agora vou tentar o garfo 3 (direita)... vai travar
Filosofo 3: agora vou tentar o garfo 4 (direita)... vai travar
Filosofo 4: agora vou tentar o garfo 0 (direita)... vai travar

!!! DEADLOCK !!!
5 filosofos travados, ninguem consegue comer.
Cada um esta com o garfo da esquerda e esperando o da direita,
que ta na mao do vizinho. Isso e espera circular -> deadlock.
```

### Print da execucao (versao corrigida)

```
Demorou 1.51 segundos
Filosofo 0 comeu 5 vezes
Filosofo 1 comeu 5 vezes
Filosofo 2 comeu 5 vezes
Filosofo 3 comeu 5 vezes
Filosofo 4 comeu 5 vezes

Ninguem travou, todo mundo conseguiu comer. Deu certo!
```

---

## Parte 2 - Contador com threads e semaforo

### O problema

Varias threads (8) vao incrementar o mesmo contador (200.000 vezes cada).
O esperado e que o valor final seja 8 x 200.000 = 1.600.000.

`contador = contador + 1` parece uma coisa simples, mas na verdade sao
3 passos no processador: ler o valor na memoria, somar 1 localmente, escrever de volta. Se duas threads fazem isso ao mesmo tempo, elas podem ler o mesmo valor antigo e uma sobrescrever a outra, perdendo o incremento.

### Ajuste de parametros e o GIL

No Python, por conta do GIL, operacoes simples de CPU tendem a rodar de forma quase atomica sem alternância de threads a tempo de causar o erro facilmente. Para simular a corrida de forma consistente em loops rápidos, inserimos um `time.sleep(0)` a cada 100 iterações (logo apos ler a variavel e antes de salvar o valor modificado). Isso forca a troca de contexto de forma controlada. Ao ceder a CPU de forma intervalada (a cada 100 loops), conseguimos demonstrar a perda massiva de incrementos de forma muito rapida e eficiente.

### Como o semaforo resolve

O semaforo funciona como uma exclusao mutua, ele garante que so uma thread por vez entre na secao de codigo critica (leitura, sleep a cada 100 loops e escrita). Se outra thread tenta entrar, fica bloqueada aguardando a liberação.

### Tabela com 3 execucoes de cada versao

T = 8 threads, M = 200.000 incrementos por thread, esperado = 1.600.000. Ambas as versoes executam com ceder cpu/sleep condicional a cada 100 iterações no loop para garantir uma comparacao justa de tempo.

| Versao        | Tentativa | Esperado | Obtido | Tempo   |
|---------------|-----------|----------|--------|---------|
| Sem semaforo  | 1         | 1600000  | 200000 | 0.149s  |
| Sem semaforo  | 2         | 1600000  | 316500 | 0.147s  |
| Sem semaforo  | 3         | 1600000  | 382100 | 0.149s  |
| Com semaforo  | 1         | 1600000  | 1600000| 1.727s  |
| Com semaforo  | 2         | 1600000  | 1600000| 1.686s  |
| Com semaforo  | 3         | 1600000  | 1600000| 1.681s  |

### Discussao

- **Perda de incrementos:** Sem sincronizacao, a troca de threads ocorre apos uma thread ler o valor antigo, mas antes de salvar o valor incrementado. Outras threads tambem leem o mesmo valor desatualizado, resultando em sobreposicao de escrita e perda de incrementos.
- **Corretude com semaforo:** O semaforo bloqueia o acesso concorrente a variavel compartilhada, permitindo que apenas uma thread manipule o contador por vez e garanta o valor correto.
- **Trade-off de Throughput:** A versao com semaforo é bem mais lenta porque o semaforo adiciona overhead para adquirir/liberar a trava e obriga a execucao sequencial (serializacao) da secao critica pelas threads, diminuindo o throughput geral do programa em troca da corretude.
- **Justica (Fairness):** Em Java, a classe `Semaphore` permite configurar a ordenacao FIFO na fila de espera (justiça). Em Python, o `threading.Semaphore` depende do agendamento de threads do sistema operacional e nao da garantias de justica estrita, mas para esse experimento o impacto e desprezivel.
- **Visibilidade e Ordenacao:** Em Java, a sincronizacao segue a regra de *happens-before* entre `release()` e o depois `acquire()`. Em Python, as operacoes de lock no modulo `threading` implementam barreiras de memoria de baixo nivel que forcam a CPU a atualizar os caches de memoria, assegurando que o novo valor do contador escrito por uma thread seja visivel para as proximas threads que entrarem na secao critica.

---

## Parte 3 - Deadlock

O que e o problema

Deadlock acontece quando duas ou mais threads ficam bloqueadas para sempre porque cada uma esta esperando por um recurso que esta sendo segurado por outra thread.

No nosso exemplo, usamos 2 threads (T1 e T2) e 2 locks (LOCK_A e LOCK_B).

Na versao que trava:

A Thread 1 pega o LOCK_A e depois tenta pegar o LOCK_B.
A Thread 2 pega o LOCK_B e depois tenta pegar o LOCK_A.

Depois que cada thread pega o primeiro lock, ambas ficam esperando pelo lock que a outra esta segurando. Como nenhuma consegue continuar para liberar o recurso que possui, o programa fica travado indefinidamente.

As 4 condicoes do Coffman que acontecem aqui

Exclusao mutua - cada lock so pode ser utilizado por uma thread por vez.
Manter e esperar - cada thread continua segurando um lock enquanto espera pelo outro.
Sem preempcao - um lock nao pode ser retirado a forca da thread que o possui.
Espera circular - T1 espera um recurso que esta com T2, enquanto T2 espera um recurso que esta com T1.

Como resolvemos

A solucao adotada foi fazer as duas threads adquirirem os locks na mesma ordem.

Antes:

T1 -> LOCK_A -> LOCK_B

T2 -> LOCK_B -> LOCK_A

Depois:

T1 -> LOCK_A -> LOCK_B

T2 -> LOCK_A -> LOCK_B

Com essa regra, uma thread pode precisar esperar pela outra, mas nao existe mais a possibilidade de formar um ciclo de espera. Assim, eliminamos a condicao de espera circular e impedimos a ocorrencia do deadlock.

Pseudocodigo (versao que trava)

Thread 1:
pegar LOCK_A
pegar LOCK_B

Thread 2:
pegar LOCK_B
pegar LOCK_A

Resultado:
T1 espera T2
T2 espera T1
DEADLOCK

Pseudocodigo (versao corrigida)

Thread 1:
pegar LOCK_A
pegar LOCK_B

Thread 2:
pegar LOCK_A
pegar LOCK_B

Resultado:
uma thread espera a outra terminar
nao existe espera circular
sem deadlock

Print da execucao (versao travada)

=== Deadlock - versao que trava ===

T1: pegando LOCK_A
T2: pegando LOCK_B
T1: tentando pegar LOCK_B
T2: tentando pegar LOCK_A

!!! DEADLOCK !!!
As threads ainda estao vivas e travadas.

T1 tem o LOCK_A e quer o LOCK_B.
T2 tem o LOCK_B e quer o LOCK_A.

Ninguem larga o recurso que possui, formando uma espera circular.

Print da execucao (versao corrigida)

=== Deadlock - versao corrigida (mesma ordem pras duas) ===

T1: pegando LOCK_A
T1: peguei LOCK_A

T2: pegando LOCK_A

T1: pegando LOCK_B
T1: peguei LOCK_B
T1: terminei!

T2: peguei LOCK_A
T2: pegando LOCK_B
T2: peguei LOCK_B
T2: terminei!

As duas terminaram corretamente.
Sem deadlock.
