import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def load_data_from_excel(file_path):
    operational_data = pd.read_excel(file_path, sheet_name='Dados Operacionais')
    maintenance_data = pd.read_excel(file_path, sheet_name='Dados de Manutenção')
    failures_records = pd.read_excel(file_path, sheet_name='Registros de Ocorrência')
    return operational_data, maintenance_data, failures_records

# Função para pré-processamento de dados
def preprocess_data(operational_df, maintenance_df, failures_df):
    df = operational_df.merge(maintenance_df, on=['Equipamento ID', 'Data'], how='left')
    df = df.merge(failures_df, on=['Equipamento ID', 'Data'], how='left')
    df['Falha'] = df['Sintoma Observado'].notnull().astype(int)
    df['Dias desde última manutenção'] = df.groupby('Equipamento ID')['Data'].diff().dt.days
    df['Horas Operação Acumuladas'] = df.groupby('Equipamento ID')['Horas de Operação'].cumsum()
    df.fillna({'Tipo de Manutenção': 'Nenhuma', 'Peças Substituídas': 'Nenhuma'}, inplace=True)
    return df

def train_predictive_model(df):
    features = ['Temperatura (°C)', 'Pressão (bar)', 'Vibração (mm/s)', 'Dias desde última manutenção', 'Horas Operação Acumuladas']
    target = 'Falha'
    
    X = df[features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(class_weight='balanced', random_state=42)
    model.fit(X_train, y_train)
    
    return model

# Gerar alertas e recomendações
def generate_recommendations(df, model, features):
    alerts = []
    recommendations = []
    
    latest_data = df.groupby('Equipamento ID').last().reset_index()
    
    for _, row in latest_data.iterrows():
        X_latest_df = pd.DataFrame(row[features].values.reshape(1, -1), columns=features)
        
        prob_failure = model.predict_proba(X_latest_df)[0][1]
        
        equipamento_nome = row['Equipamento']
        
        if prob_failure > 0.7:
            alerts.append(f"ALERTA CRÍTICO: {equipamento_nome} (ID: {row['Equipamento ID']})\n  - Probabilidade de falha: {prob_failure:.0%}\n")
            recommendations.append(f"[ALTA] {equipamento_nome} (ID: {row['Equipamento ID']}): Realizar inspeção imediata nas próximas 24h.")
        elif prob_failure > 0.5:
            recommendations.append(f"[MÉDIA] {equipamento_nome} (ID: {row['Equipamento ID']}): Agendar manutenção preventiva nas próximas 72h.")
    
    return alerts, recommendations


def run_scan():

    file_path = 'Dados.xlsx'
    
    # Carregar e processar os dados
    operational_df, maintenance_df, failures_df = load_data_from_excel(file_path)
    processed_df = preprocess_data(operational_df, maintenance_df, failures_df)
    
    # Treinar o modelo
    model = train_predictive_model(processed_df)
    
    # Gerar alertas e recomendações
    features = ['Temperatura (°C)', 'Pressão (bar)', 'Vibração (mm/s)', 'Dias desde última manutenção', 'Horas Operação Acumuladas']
    alerts, recommendations = generate_recommendations(processed_df, model, features)
    
    # Exibir os alertas e recomendações
    alert_text.delete(1.0, tk.END) 
    rec_text.delete(1.0, tk.END)    
    
    alert_text.insert(tk.END, "\n".join(alerts))  # Exibe os alertas
    rec_text.insert(tk.END, "\n".join(recommendations))  # Exibe as recomendações

# Configuração da interface gráfica com Tkinter
root = tk.Tk()
root.title("Sistema de Manutenção Preditiva")
root.geometry("600x600")

# Botão
scan_button = tk.Button(root, text="FAZER VARREDURA DOS EQUIPAMENTOS", command=run_scan, height=2, width=40)
scan_button.pack(pady=20)

alert_label = tk.Label(root, text="ALERTAS CRÍTICOS:")
alert_label.pack()
alert_text = scrolledtext.ScrolledText(root, width=70, height=10)
alert_text.pack(pady=10)

rec_label = tk.Label(root, text="RECOMENDAÇÕES DE MANUTENÇÃO:")
rec_label.pack()
rec_text = scrolledtext.ScrolledText(root, width=70, height=10)
rec_text.pack(pady=10)

root.mainloop()
