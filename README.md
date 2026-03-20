# Relatório de Experimento: Paralelização de Avaliador de Logs

**Estudante:** Ana Júlia de Almeida Machado 
**Instituição:** Centro Universitário Unieuro 
**Curso:** Tecnologia em Análise e Desenvolvimento de Sistemas 
---

## 1. Descrição do Problema

* **Objetivo do programa:** O programa visa processar grandes volumes de arquivos de log para extrair métricas consolidadas (contagem de linhas, palavras, caracteres e termos específicos como "erro", "warning" e "info").
* **Volume de dados:** Foram processados **1.000 arquivos**, totalizando **10.000.000 de linhas** de log.
* **Algoritmo utilizado:** Foi implementado o modelo **Produtor-Consumidor** com buffer limitado (fila de tarefas). Um processo produtor mapeia os arquivos e os coloca em uma `JoinableQueue`, enquanto processos consumidores competem para processar cada arquivo.
* **Complexidade aproximada:** O algoritmo possui complexidade linear $O(n \times m)$, onde $n$ é o número de arquivos e $m$ o número de linhas por arquivo, uma vez que cada linha é lida e decomposta uma única vez.
* **Objetivo da paralelização:** Reduzir o tempo de resposta do sistema, que originalmente operava de forma serial, aproveitando a arquitetura multi-core da CPU para processar múltiplos arquivos simultaneamente.

---

## 2. Ambiente Experimental

| Item | Descrição |
| :--- | :--- |
| **Processador** | Intel Core i5 (ou equivalente conforme hardware do laboratório) |
| **Número de núcleos** | 4 núcleos físicos / 8 threads (estimado) |
| **Memória RAM** | 8 GB / 16 GB |
| **Sistema Operacional** | [cite_start]Windows 10/11 (Ambiente MINGW64) [cite: 1] |
| **Linguagem utilizada** | [cite_start]Python 3.x [cite: 1] |
| **Biblioteca de paralelização** | [cite_start]`multiprocessing` [cite: 1] |
| **Compilador / Versão** | Python 3.12.x |

---

## 3. Metodologia de Testes

* [cite_start]**Medição do tempo:** O tempo foi medido utilizando a biblioteca `time` do Python, capturando o intervalo exato entre o início da alimentação da fila e o encerramento do processamento de todos os itens (`tarefas.join()`)[cite: 1].
* [cite_start]**Entrada:** Pasta `log2` contendo 1.000 arquivos gerados artificialmente[cite: 1].
* [cite_start]**Execuções:** Foram realizadas múltiplas execuções para cada configuração de processos (2, 4, 8 e 12) para garantir a consistência dos dados[cite: 1].
* [cite_start]**Condições de execução:** Máquina de laboratório acadêmico, com carga de sistema variável, simulando um ambiente de uso real[cite: 1].

---

## 4. Resultados Experimentais

[cite_start]Tempos médios obtidos durante a execução do script `avaliadorparalelo.py`[cite: 1]:

| Nº Processos | Tempo de Execução (s) |
| :--- | :--- |
| **1 (Serial)** | 115.96 |
| **2** | 61.55 |
| **4** | 30.38 |
| **8** | 18.83 |
| **12** | 16.23 |

---

## 5. Cálculo de Speedup e Eficiência

As métricas foram calculadas com base nas fórmulas:
* **Speedup:** $S(p) = \frac{T(1)}{T(p)}$
* **Eficiência:** $E(p) = \frac{S(p)}{p}$

---

## 6. Tabela de Resultados

| Processos | Tempo (s) | Speedup | Eficiência |
| :--- | :--- | :--- | :--- |
| **1** | 115.96 | 1.00 | 1.00 |
| **2** | 61.55 | 1.88 | 0.94 |
| **4** | 30.38 | 3.81 | 0.95 |
| **8** | 18.83 | 6.15 | 0.76 |
| **12** | 16.23 | 7.14 | 0.59 |

---

## 7. Gráfico de Tempo de Execução

```text
Tempo (s)
 ^
 | * (115.96)
 |
 |       * (61.55)
 |
 |             * (30.38)
 |                   * (18.83)
 |                         * (16.23)
 +-----------------------------------> Processos
   1     2     4     8     12
```

## 8. Gráfico de Speedup

```text
Speedup
 ^                                  / (Ideal)
 |                                /
 |                        * (7.14)
 |                  * (6.15)
 |            * (3.81)
 |      * (1.88)
 | * (1.0)
 +-----------------------------------> Processos
   1     2     4     8     12
```

## 9. Gráfico de Eficiência

```text
Eficiência
 ^
 | * (1.0)  * (0.95)
 |    * (0.94)
 |             
 |                  * (0.76)
 |                         * (0.59)
 +-----------------------------------> Processos
   1     2     4     8     12
```

---

## 10. Análise dos Resultados

* [cite_start]**Escalabilidade:** A aplicação apresentou excelente escalabilidade até 4 processos, onde a eficiência se manteve acima de 90%[cite: 1].
* [cite_start]**Ponto de Queda de Eficiência:** A eficiência começou a cair significativamente ao passar de 8 processos (0.76 para 0.59)[cite: 1]. [cite_start]Isso indica que o número de processos (12) ultrapassou o número de núcleos físicos disponíveis na máquina utilizada[cite: 1].
* [cite_start]**Overhead de Paralelização:** Houve overhead perceptível na comunicação entre processos e na disputa pelo acesso ao disco (I/O) para leitura simultânea de múltiplos arquivos[cite: 1].
* **Gargalos:** O principal gargalo é o I/O de disco. [cite_start]Embora a CPU processe as strings rapidamente, a velocidade de leitura do sistema de arquivos limita o ganho de desempenho em altas contagens de processos[cite: 1].

---

## 11. Conclusão

[cite_start]O paralelismo trouxe um ganho de desempenho substancial, reduzindo o tempo de processamento de aproximadamente 2 minutos para apenas 16 segundos[cite: 1]. [cite_start]O melhor custo-benefício (equilíbrio entre tempo e uso de recursos) foi observado com **4 processos**, onde a eficiência foi máxima[cite: 1]. [cite_start]A implementação escala bem, mas é limitada pelo hardware físico (número de núcleos) e pela velocidade de entrada de dados (disco)[cite: 1]. [cite_start]Como melhoria, sugere-se o uso de leitura assíncrona ou o processamento de arquivos em lotes (*batch*) para reduzir a troca de contexto[cite: 1].

