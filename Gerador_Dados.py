import pandas as pd
import random

def gerar_datas(inicio, fim):
    return pd.date_range(inicio, fim, freq='D')

# Equipamentos possíveis
equipamentos_nome = [
    'Bomba Centrífuga',
    'Compressor de Gás',
    'Trocador de Calor',
    'Turbina a Vapor',
    'Válvula de Controle',
    'Sistema de Refrigeração',
    'Desgastador de Partículas',
    'Forno de Craqueamento Catalítico',
    'Refinador de Hidrogênio',
    'Unidade de Destilação a Vácuo'
]

def gerar_equipamentos():
    equipamentos = []
    for i in range(1, 51):
        nome = equipamentos_nome[(i - 1) % len(equipamentos_nome)] 
        equipamentos.append({'ID': i, 'Nome': nome})
    return equipamentos


# Gerar dados operacionais
def gerar_dados_operacionais(equipamentos):
    dados = []
    for data in gerar_datas('2024-01-01', '2024-06-01'):
        equipamento = random.choice(equipamentos)
        temperatura = round(random.uniform(70, 130), 2)
        pressao = round(random.uniform(8, 16), 2)
        vibracao = round(random.uniform(1, 3), 2)
        horas_operacao = random.randint(16, 24)
        consumo_energia = random.randint(300, 500)
        dados.append([data, equipamento['ID'], equipamento['Nome'], temperatura, pressao, vibracao, horas_operacao, consumo_energia])
    return pd.DataFrame(dados, columns=['Data', 'Equipamento ID', 'Equipamento', 'Temperatura (°C)', 'Pressão (bar)', 'Vibração (mm/s)', 'Horas de Operação', 'Consumo Energético (kWh)'])

# Gerar dados de manutenção
def gerar_dados_manutencao(equipamentos):
    tipos_manutencao = ['Preventiva', 'Corretiva']
    pecas_substituidas = ['Rolamento', 'Válvula', 'Filtro', 'Trocador de calor', 'Compressor']
    causas_falhas = ['Desgaste natural', 'Falha elétrica', 'Vazamento', 'Problema mecânico', 'N/A']
    dados = []
    for data in gerar_datas('2024-01-01', '2024-12-31'):
        equipamento = random.choice(equipamentos)
        tipo = random.choice(tipos_manutencao)
        pecas = random.sample(pecas_substituidas, k=random.randint(1, 3))
        causa = random.choice(causas_falhas)
        dados.append([data, equipamento['ID'], equipamento['Nome'], tipo, ', '.join(pecas), causa])
    return pd.DataFrame(dados, columns=['Data', 'Equipamento ID', 'Equipamento', 'Tipo de Manutenção', 'Peças Substituídas', 'Causa da Falha'])


# Gerar dados de registros de ocorrência
def gerar_dados_ocorrencia(equipamentos):
    pecas = ['Rolamento', 'Filtro de óleo', 'Válvula de pressão', 'Trocador de calor', 'Válvula de controle de fluxo']
    sintomas = ['Vibração acima do normal', 'Perda de pressão', 'Falta de pressão', 'Vazamento de fluido', 'Anomalia no fluxo de óleo', 'Parou de funcionar']
    dados = []
    for data in gerar_datas('2024-01-01', '2024-12-31'):
        equipamento = random.choice(equipamentos)
        peca = random.choice(pecas)
        sintoma = random.choice(sintomas)
        
        # A classe 1 representa falha, se o sintoma for "Parou de funcionar", a classe será 1
        classe_falha = 1 if sintoma == 'Parou de funcionar' else 0
        
        dados.append([data, equipamento['ID'], equipamento['Nome'], peca, sintoma, classe_falha])
    
    return pd.DataFrame(dados, columns=['Data', 'Equipamento ID', 'Equipamento', 'Peça', 'Sintoma Observado', 'Classe Falha'])

# Gerar a lista de equipamentos
equipamentos = gerar_equipamentos()

# Gerar os dados
dados_operacionais = gerar_dados_operacionais(equipamentos)
dados_manutencao = gerar_dados_manutencao(equipamentos)
dados_ocorrencia = gerar_dados_ocorrencia(equipamentos)

print(dados_operacionais.head())
print(dados_manutencao.head())
print(dados_ocorrencia.head())

# Salvar
with pd.ExcelWriter('Dados.xlsx') as writer:
    dados_operacionais.to_excel(writer, sheet_name='Dados Operacionais', index=False)
    dados_manutencao.to_excel(writer, sheet_name='Dados de Manutenção', index=False)
    dados_ocorrencia.to_excel(writer, sheet_name='Registros de Ocorrência', index=False)