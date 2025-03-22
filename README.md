# Sistema Preditivo de Manutenção para Refinaria de Petróleo

Este sistema foi desenvolvido para monitorar e otimizar as operações de manutenção de equipamentos em uma refinaria de petróleo. Ele utiliza aprendizado de máquina para prever falhas nos equipamentos e gerar recomendações de manutenção preventiva, melhorando a eficiência e a segurança da operação.

## Funcionalidades

### 1. **Carregamento e Processamento de Dados**
   - O sistema carrega dados operacionais, de manutenção e de falhas de equipamentos a partir de um arquivo Excel com três planilhas:
     - **Dados Operacionais**: Informações sobre o funcionamento dos equipamentos (temperatura, pressão, vibração, etc.).
     - **Dados de Manutenção**: Histórico das manutenções realizadas, incluindo peças substituídas e tipo de manutenção.
     - **Registros de Ocorrência**: Dados sobre falhas registradas, incluindo sintomas observados e causas identificadas.
   - Esses dados são combinados para criar um único conjunto de informações, onde cada linha representa uma entrada para um equipamento específico, com informações operacionais, de manutenção e de falhas.

### 2. **Pré-processamento de Dados**
   - Combina os dados das diferentes fontes com base no `Equipamento ID` e `Data`.
   - Cria novas variáveis úteis para a análise, como:
     - **Falha**: Indica se há um sintoma de falha registrado.
     - **Dias desde última manutenção**: Calcula a diferença de dias desde a última manutenção realizada.
     - **Horas de operação acumuladas**: Soma total das horas de operação de cada equipamento.
   - Preenche valores ausentes com informações padrão (por exemplo, "Nenhuma" para tipo de manutenção).

### 3. **Modelo Preditivo de Falha**
   - Utiliza um modelo de **Random Forest** para prever a probabilidade de falha de cada equipamento com base nas variáveis operacionais e de manutenção.
   - O modelo é treinado com 80% dos dados e testado com os 20% restantes, oferecendo uma avaliação de sua precisão.
   - As características analisadas pelo modelo incluem temperatura, pressão, vibração, dias desde a última manutenção e horas de operação acumuladas.

### 4. **Geração de Alertas e Recomendações**
   - O sistema gera alertas e recomendações de manutenção com base na probabilidade de falha calculada pelo modelo:
     - **Alertas Críticos**: Caso a probabilidade de falha seja superior a 70%, um alerta crítico é gerado, recomendando uma inspeção imediata.
     - **Recomendações de Manutenção Preventiva**: Para probabilidades entre 50% e 70%, o sistema sugere agendar manutenção preventiva nos próximos dias.
   - As recomendações incluem ações específicas, como a verificação de peças substituídas, inspeção de componentes críticos e monitoramento de variáveis como vibração e temperatura.

### 5. **Exibição de Resultados**
   - Os resultados são apresentados de forma clara e objetiva, exibindo os alertas críticos e as recomendações de manutenção para cada equipamento.
   - As informações incluem o **nome do equipamento**, **ID do equipamento**, a **probabilidade de falha** e as **ações recomendadas**, com prioridade de atendimento.

## Tecnologias Utilizadas
- **Pandas**: Para manipulação e análise de dados.
- **Scikit-learn**: Para modelagem preditiva utilizando o algoritmo Random Forest.
- **Excel**: Para importar e trabalhar com os dados das planilhas.

## Benefícios
- **Otimização de Manutenção**: Antecipação de falhas antes que ocorram, reduzindo o tempo de inatividade e aumentando a eficiência operacional.
- **Segurança**: A detecção precoce de falhas potencialmente críticas ajuda a evitar acidentes e danos aos equipamentos.
- **Eficiência Operacional**: Melhor alocação de recursos de manutenção, priorizando os equipamentos com maior risco de falha.

Este sistema pode ser uma ferramenta poderosa para refinar os processos de manutenção em uma refinaria de petróleo, promovendo maior segurança, redução de custos e aumento da vida útil dos equipamentos.

