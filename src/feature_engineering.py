import pandas as pd
import numpy as np

def create_target_variable(df, delay_threshold=15):
    """
    Cria a variável alvo binária (target) para o modelo de classificação.

    Um voo é considerado "atrasado" (1) se o `ARRIVAL_DELAY` for maior 
    ou igual ao `delay_threshold`. Caso contrário, (0).

    Args:
        df (pd.DataFrame): O DataFrame de voos (limpo).
        delay_threshold (int): O limite em minutos para considerar um voo atrasado.
                               O padrão da FAA é 15 minutos.

    Returns:
        pd.DataFrame: O DataFrame com a nova coluna 'IS_DELAYED'.
    """
    
    df_feat = df.copy()

    # Cria a coluna 'IS_DELAYED'
    # 1 se ARRIVAL_DELAY >= 15, 0 caso contrário
    df_feat['IS_DELAYED'] = (df_feat['ARRIVAL_DELAY'] >= delay_threshold).astype(int)

    print(f"Coluna 'IS_DELAYED' criada com threshold de {delay_threshold} minutos.")
    return df_feat

def engineer_time_features(df):
    """
    Cria features de tempo mais inteligentes a partir 
    das colunas de horário programado.
    """
    df_feat = df.copy()

    # 1. Converter SCHEDULED_DEPARTURE (HHMM) para formato de hora
    time_str = df_feat['SCHEDULED_DEPARTURE'].astype(str).str.zfill(4)
    time_str = time_str.replace('2400', '0000')
    hour_minute = pd.to_datetime(time_str, format='%H%M', errors='coerce').dt

    # 2. Criar a feature 'HOUR_OF_DAY' (0-23)
    df_feat['HOUR_OF_DAY'] = hour_minute.hour

    # 3. Criar 'PART_OF_DAY' (Manhã, Tarde, Noite, Madrugada)
    bins = [-1, 6, 12, 18, 24]
    labels = ['Madrugada', 'Manhã', 'Tarde', 'Noite']
    df_feat['PART_OF_DAY'] = pd.cut(df_feat['HOUR_OF_DAY'], bins=bins, labels=labels)

    # 4. TRATAMENTO DE NULOS (A CORREÇÃO)
    # Em vez de .dropna(), preenchemos os nulos.
    
    # Preenche 'PART_OF_DAY' nula com 'Desconhecido'
    df_feat['PART_OF_DAY'] = df_feat['PART_OF_DAY'].cat.add_categories('Desconhecido')
    df_feat['PART_OF_DAY'] = df_feat['PART_OF_DAY'].fillna('Desconhecido')
    
    # Preenche 'HOUR_OF_DAY' nula com -1
    df_feat['HOUR_OF_DAY'] = df_feat['HOUR_OF_DAY'].fillna(-1)

    print("Features 'HOUR_OF_DAY' e 'PART_OF_DAY' criadas (com tratamento de nulos).")
    return df_feat