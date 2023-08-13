import connection as cn
import random

def chooseAction(stateIndex, epsilon, qTable, actions):
    if random.uniform(0, 1) <= epsilon: 
        # Ação aleatória
        return actions[random.randint(0, 2)]
    else:                               
        # Melhor ação
        return actions[qTable[stateIndex].index(max(qTable[stateIndex]))]

# Inicialização
alpha = 0.3                                 # Taxa de aprendizado: Quanto o agente aprende com novas ações
gamma = 0.9                                 # Fator de desconto: Quanto o agente valoriza recompensas futuras
epsilon = 0.1                               # Aleatoriedade: Chance de escolher uma ação ao acaso
actions = ["left", "right", "jump"]         # Três ações possíveis
qTable = []                                 # Cria qTable
for i in range(96): qTable.append([0,0,0])  # Preenche de zeros
state = 0                                   # Começa na plataforma 0
reward = 0                                  # Prêmio

s = cn.connect(2037) # Conecta ao jogo

for i in range(1000): # Serão feitos mil episódios partindo de diferentes plataformas escolhidas manualmente ao longo da execução
    while reward != 300:
        # Armazena o último estado
        previousState = state
        # Escolhe melhor ação, ou com chance epsilon de ser aleatória, e armazena seu index
        action = chooseAction(state, epsilon, qTable, actions)
        actionIndex = actions.index(action)
        # Envia ação para o jogo e recebe estado e recompensa resultantes
        state, reward = cn.get_state_reward(s, action)
        print(f"{state}\t{reward}\t{i}")
        # Converte state de binário para inteiro
        state = int(state, 2)
        # Calcula utilidade do último estado
        qTable[previousState][actionIndex] += alpha * (reward + gamma * max(qTable[state]) - qTable[previousState][actionIndex])
    reward = 0

# Salva qTable em resultado.txt
with open("resultado.txt", 'w') as f:
        for row in qTable:
            s = " ".join(map(str, row))
            f.write(s+'\n')
