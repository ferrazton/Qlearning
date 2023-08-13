import connection as cn
import random

def chooseAction(stateIndex, epsilon, qTable, actions):
    if random.uniform(0, 1) <= epsilon: 
        # Ação aleatória
        return actions[random.randint(0, 2)]
    else:                               
        # Melhor ação
        bestActionReward = max(qTable[stateIndex])
        return actions[qTable[stateIndex].index(bestActionReward)]

# Inicialização
alpha = 0.3                             # Taxa de aprendizado
gamma = 0.9                             # Fator de desconto
epsilon = 0.1                           # Aleatoriedade
actions = ["left", "right", "jump"]     # Três ações possíveis
qTable = []                             # Cria qTable
for i in range(96):                     # Preenche de zeros
    qTable.append([0,0,0])
state = 0                               # Começa na plataforma 0
reward = 0                              # Prêmio

s = cn.connect(2037) # Conecta ao jogo

for i in range(1000): # Mil episódios
    while reward != 300:
        # Armazena o último estado
        previousState = state
        # Escolhe melhor ação, mas com chance epsilon de ser aleatória, e armazena seu index
        action = chooseAction(state, epsilon, qTable, actions)
        actionIndex = actions.index(action)
        # Envia ação para o jogo e recebe estado e recompensa encontrados
        state, reward = cn.get_state_reward(s, action)
        print(f"{state}\t{reward}\t{i}")
        # Converta para inteiro
        state = int(state, 2)

        qTable[previousState][actionIndex] += alpha * (reward + gamma * max(qTable[state]) - qTable[previousState][actionIndex])
    reward = 0

# Salva qTable em resultado.txt
with open("resultado.txt", 'w') as f:
        for row in qTable:
            s = " ".join(map(str, row))
            f.write(s+'\n')