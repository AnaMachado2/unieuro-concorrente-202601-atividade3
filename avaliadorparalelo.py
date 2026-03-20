import os
import time
from multiprocessing import Process, JoinableQueue, Queue, cpu_count

# Reutiliza sua lógica de processamento de arquivo
def processar_arquivo(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.readlines()

    total_linhas = len(conteudo)
    total_palavras = 0
    total_caracteres = 0
    contagem = {"erro": 0, "warning": 0, "info": 0}

    for linha in conteudo:
        palavras = linha.split()
        total_palavras += len(palavras)
        total_caracteres += len(linha)
        for p in palavras:
            if p in contagem:
                contagem[p] += 1
        
        # Simulação de carga de CPU (conforme seu original)
        for _ in range(1000):
            pass

    return {
        "linhas": total_linhas,
        "palavras": total_palavras,
        "caracteres": total_caracteres,
        "contagem": contagem
    }

# Função do Consumidor
def worker(tarefas, resultados):
    while True:
        caminho = tarefas.get()
        if caminho is None: # Sinal de parada (Poison Pill)
            tarefas.task_done()
            break
        resultado = processar_arquivo(caminho)
        resultados.put(resultado)
        tarefas.task_done()

def executar_paralelo(pasta, num_processos):
    tarefas = JoinableQueue(maxsize=20) # Buffer limitado
    resultados_fila = Queue()
    
    # Inicia os processos consumidores
    consumidores = []
    for _ in range(num_processos):
        p = Process(target=worker, args=(tarefas, resultados_fila))
        p.start()
        consumidores.append(p)

    inicio = time.time()

    # Produtor: Adiciona arquivos na fila
    arquivos = [os.path.join(pasta, a) for a in os.listdir(pasta)]
    for arq in arquivos:
        tarefas.put(arq)

    # Adiciona sinal de parada para cada consumidor
    for _ in range(num_processos):
        tarefas.put(None)

    tarefas.join() # Aguarda processamento de todos os itens
    fim = time.time()

    # Coleta e consolida resultados
    resultados_lista = []
    while not resultados_fila.empty():
        resultados_lista.append(resultados_fila.get())

    tempo_total = fim - inicio
    return tempo_total, resultados_lista

if __name__ == "__main__":
    pasta_alvo = "log2"
    processos_teste = [2, 4, 8, 12]
    
    print(f"Iniciando testes na pasta: {pasta_alvo}")
    
    for n in processos_teste:
        print(f"\n--- Executando com {n} processos ---")
        tempo, res_parciais = executar_paralelo(pasta_alvo, n)
        print(f"Tempo total: {tempo:.4f} segundos")

        
