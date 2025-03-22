import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def load_data_from_excel(file_path):
    operational_data = pd.read_excel(file_path, sheet_name='Dados Operacionais')
    maintenance_data = pd.read_excel(file_path, sheet_name='Dados de Manutenção')
    failures_records = pd.read_excel(file_path, sheet_name='Registros de Ocorrência')
    
    return operational_data, maintenance_data, failures_records


# Pré-processamento de dados
def preprocess_data(operational_df, maintenance_df, failures_df):
    df = operational_df.merge(maintenance_df, on=['Equipamento ID', 'Data'], how='left')
    df = df.merge(failures_df, on=['Equipamento ID', 'Data'], how='left')
    
    # Engenharia de features
    df['Falha'] = df['Sintoma Observado'].notnull().astype(int)
    df['Dias desde última manutenção'] = df.groupby('Equipamento ID')['Data'].diff().dt.days
    df['Horas Operação Acumuladas'] = df.groupby('Equipamento ID')['Horas de Operação'].cumsum()
    df.fillna({'Tipo de Manutenção': 'Nenhuma', 'Peças Substituídas': 'Nenhuma'}, inplace=True)
    return df


# Treinar modelo preditivo
def train_predictive_model(df):
    features = ['Temperatura (°C)', 'Pressão (bar)', 'Vibração (mm/s)',
                'Dias desde última manutenção', 'Horas Operação Acumuladas']
    target = 'Falha'
    
    X = df[features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(class_weight='balanced', random_state=42)
    model.fit(X_train, y_train)
    
    # print("Avaliação do Modelo:")
    # print(classification_report(y_test, model.predict(X_test)))
    return model


# Gerar recomendações e alertas
def generate_recommendations(df, model):
    alerts = []
    recommendations = []
    
    # Analisar últimos 7 dias para cada equipamento
    latest_data = df.groupby('Equipamento ID').last().reset_index()
    
    for _, row in latest_data.iterrows():
        X_latest_df = pd.DataFrame(row[features].values.reshape(1, -1), columns=features)
        
        prob_failure = model.predict_proba(X_latest_df)[0][1]

        equipamento_nome = row['Equipamento'] 
        
        if prob_failure > 0.7:
            alerts.append({
                'Equipamento ID': row['Equipamento ID'],
                'Nome do Equipamento': equipamento_nome,
                'Probabilidade Falha': f"{prob_failure:.0%}",
                'Alertas': [
                    f"Probabilidade crítica de falha ({prob_failure:.0%})",
                    f"Sintoma esperado: {row['Sintoma Observado'] or 'Desconhecido'}"
                ]
            })
            
            maintenance_rec = {
                'Equipamento ID': row['Equipamento ID'],
                'Nome do Equipamento': equipamento_nome, 
                'Ações Recomendadas': [
                    f"Realizar inspeção imediata nas próximas 24h",
                    f"Verificar {row['Peças Substituídas']}",
                    f"Monitorar {row['Causa da Falha']}"
                ],
                'Prioridade': 'Alta'
            }
            recommendations.append(maintenance_rec)
            
        elif prob_failure > 0.5:
            recommendations.append({
                'Equipamento ID': row['Equipamento ID'],
                'Nome do Equipamento': equipamento_nome,
                'Ações Recomendadas': [
                    f"Agendar manutenção preventiva nas próximas 72h",
                    f"Verificar tendência de vibração: {row['Vibração (mm/s)']:.1f} mm/s"
                ],
                'Prioridade': 'Média'
            })
    
    return alerts, recommendations



if __name__ == "__main__":
    # 1. Gerar e processar dados
    file_path = 'Dados.xlsx'
    operational_df, maintenance_df, failures_df = load_data_from_excel(file_path)
    processed_df = preprocess_data(operational_df, maintenance_df, failures_df)
    
    # 2. Treinar modelo
    model = train_predictive_model(processed_df)
    
    # 3. Gerar alertas e recomendações
    features = ['Temperatura (°C)', 'Pressão (bar)', 'Vibração (mm/s)',
                'Dias desde última manutenção', 'Horas Operação Acumuladas']
    alerts, recommendations = generate_recommendations(processed_df, model)
    
   # Exibir resultados
    print("\nALERTAS CRÍTICOS:")
    for alert in alerts:
        print(f"\n[!] ALERTA: {alert['Nome do Equipamento']} (Equipamento ID {alert['Equipamento ID']})")
        for msg in alert['Alertas']:
            print(f"  - {msg}")

    print("\nRECOMENDAÇÕES DE MANUTENÇÃO:")
    for rec in recommendations:
        print(f"\n[{rec['Prioridade']}] {rec['Nome do Equipamento']} (Equipamento ID {rec['Equipamento ID']}):")
        for action in rec['Ações Recomendadas']:
            print(f"  • {action}")

