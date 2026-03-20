# Relatório de Análise: Processamento Paralelo de Logs

**Nome:** Ana Júlia de Almeida Machado  
**Instituição:** Centro Universitário Unieuro  
**Curso:** Análise e Desenvolvimento de Sistemas  

## 1. Introdução
Este projeto analisa o ganho de desempenho ao paralelizar um processador de logs operacionais utilizando o modelo produtor-consumidor em Python.

## 2. Metodologia
O experimento consistiu em processar 1000 arquivos de log (cada um com 10.000 linhas) variando o número de processos trabalhadores (workers).

## 3. Resultados dos Testes
Os tempos foram medidos em uma máquina com as seguintes configurações:
- **Processos**: 2, 4, 8, 12.

| N° Processos | Tempo de Execução (s) | Speedup (Serial / Paralelo) |
|--------------|-----------------------|-----------------------------|
| 1 (Serial)   | 115.9621              | 1.0x                        |
| 2            | 61.5575               | 1.88x                       |
| 4            | 30.3854               | 3.81x                       |
| 8            | 18.8385               | 6.15x                       |
| 12           | 16.2395               |7.14x                        |

## 4. Análise e Conclusão
Escalabilidade Linear Inicial: Entre 2 e 4 processos, o ganho de desempenho foi quase linear (o tempo caiu praticamente pela metade a cada dobro de núcleos), indicando que o processamento é intensivo em CPU (CPU-bound) devido à simulação de carga pesada no código.

Ponto de Retorno Decrescente: Ao passar de 8 para 12 processos, a melhora no tempo foi menor (de 18.8s para 16.2s). Isso ocorre pois o overhead de criação de processos e a contenção no acesso ao disco para leitura dos arquivos começam a limitar o ganho de velocidade.

Conclusão: A implementação paralela reduziu o tempo total de execução de aproximadamente 2 minutos (serial) para apenas 16 segundos (12 processos), validando a eficiência do modelo produtor-consumidor para esta tarefa.
