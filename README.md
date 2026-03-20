# Relatório de Desempenho: Avaliador de Logs Paralelo

Este projeto apresenta a evolução de um sistema de análise de logs de uma execução serial para uma arquitetura paralela, utilizando o modelo **Produtor-Consumidor** com buffer limitado. A solução foi desenvolvida em Python para otimizar o processamento de grandes volumes de dados operacionais.

## 1. Descrição do Problema

* **Objetivo do programa:** O programa visa processar grandes volumes de arquivos de log para extrair métricas consolidadas (contagem de linhas, palavras, caracteres e termos específicos como "erro", "warning" e "info").
* **Volume de dados:** Foram processados **1.000 arquivos**, totalizando **10.000.000 de linhas** de log.
* **Algoritmo utilizado:** Foi implementado o modelo **Produtor-Consumidor** com buffer limitado. Um processo produtor mapeia os arquivos e os coloca em uma fila (`JoinableQueue`), enquanto processos consumidores competem para processar cada arquivo.
* **Complexidade aproximada:** O algoritmo possui complexidade linear $O(n \times m)$, onde $n$ é o número de arquivos e $m$ o número de linhas por arquivo.
* **Objetivo da paralelização:** Reduzir o tempo de resposta do sistema aproveitando a arquitetura multi-core da CPU para processar múltiplos arquivos simultaneamente.

## 2. Ambiente Experimental

| Item | Descrição |
| :--- | :--- |
| **Processador** | Intel Core i5 (Ambiente de Laboratório) |
| **Número de núcleos** | 4 núcleos físicos / 8 threads (estimado) |
| **Memória RAM** | 8 GB / 16 GB |
| **Sistema Operacional** | Windows 10/11 (Ambiente MINGW64) |
| **Linguagem utilizada** | Python 3.x |
| **Biblioteca de paralelização** | `multiprocessing` |
| **Compilador / Versão** | Python 3.12.x |

## 3. Metodologia de Testes

* **Medição do tempo:** O tempo foi medido utilizando a biblioteca `time`, capturando o intervalo entre o início da alimentação da fila e o encerramento do processamento (`tarefas.join()`).
* **Entrada:** Pasta `log2` contendo 1.000 arquivos gerados artificialmente.
* **Configurações testadas:** Foram realizados testes com 1 (serial), 2, 4, 8 e 12 processos.
* **Condições de execução:** Máquina de laboratório com carga de sistema variável, simulando um ambiente de uso real.

## 4. Resultados Experimentais

| Nº Processos | Tempo de Execução (s) |
| :--- | :--- |
| **1 (Serial)** | 115.96 |
| **2** | 61.55 |
| **4** | 30.38 |
| **8** | 18.83 |
| **12** | 16.23 |

## 5. Cálculo de Speedup e Eficiência

As métricas foram calculadas com base nas fórmulas:
* **Speedup:** $S(p) = T(1) / T(p)$
* **Eficiência:** $E(p) = S(p) / p$

## 6. Tabela de Resultados Consolidados

| Processos | Tempo (s) | Speedup | Eficiência |
| :--- | :--- | :--- | :--- |
| **1** | 115.96 | 1.00 | 1.00 |
| **2** | 61.55 | 1.88 | 0.94 |
| **4** | 30.38 | 3.81 | 0.95 |
| **8** | 18.83 | 6.15 | 0.76 |
| **12** | 16.23 | 7.14 | 0.59 |

## 7. Análise dos Resultados

* **Escalabilidade:** A aplicação apresentou excelente escalabilidade até 4 processos, mantendo eficiência próxima de 1.0.
* **Ponto de Queda de Eficiência:** A eficiência caiu significativamente ao ultrapassar 8 processos (de 0.76 para 0.59). Isso ocorre porque o número de processos (12) excedeu o número de núcleos físicos da máquina.
* **Overhead e Gargalos:** Houve overhead na comunicação entre processos e na disputa pelo acesso ao disco (I/O). A velocidade de leitura do sistema de arquivos é o principal limitador em altas contagens de paralelismo.

## 8. Conclusão

O paralelismo trouxe um ganho de desempenho substancial, reduzindo o tempo de processamento em aproximadamente **86%**. O melhor equilíbrio entre tempo e recursos foi observado com **4 processos**. A implementação escala bem, sendo limitada apenas pelos limites físicos de hardware (núcleos e I/O).

---
