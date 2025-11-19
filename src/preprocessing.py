import pandas as pd

def clean_flights(df):
    """
    Executa a limpeza principal no dataframe de voos.

    - Preenche nulos de motivos de atraso com 0.
    - Filtra apenas voos completados (não cancelados ou desviados).
    - Remove colunas desnecessárias.
    - Remove quaisquer linhas restantes com nulos.
    """
    # 1. Copiar para evitar aviso de SettingWithCopyWarning
    df_clean = df.copy()

    # 2. Tratar Grupo 2: Preencher motivos de atraso nulos com 0
    # (Baseado no dicionário de dados, incluímos todas as 5 colunas)
    delay_reason_cols = [
        'AIR_SYSTEM_DELAY', 
        'SECURITY_DELAY', 
        'AIRLINE_DELAY', 
        'LATE_AIRCRAFT_DELAY', 
        'WEATHER_DELAY'
    ]

    # Filtra a lista para incluir apenas colunas que existem no DataFrame
    existing_delay_cols = [col for col in delay_reason_cols if col in df_clean.columns]
    df_clean[existing_delay_cols] = df_clean[existing_delay_cols].fillna(0)

    # 3. Tratar Grupo 1: Filtrar apenas voos completados
    df_clean = df_clean[
        (df_clean['CANCELLED'] == 0) & (df_clean['DIVERTED'] == 0)
    ]

    # 4. Limpeza Final: Remover colunas de ID/texto que não usaremos
    #    e que continham nulos (TAIL_NUMBER, CANCELLATION_REASON)
    cols_to_drop = [
        'TAIL_NUMBER', 
        'CANCELLED', 
        'CANCELLATION_REASON', 
        'DIVERTED'
    ]

    # Filtra a lista para incluir apenas colunas que existem
    existing_cols_to_drop = [col for col in cols_to_drop if col in df_clean.columns]
    df_clean = df_clean.drop(columns=existing_cols_to_drop)

    # 5. Remove qualquer linha restante com nulos (ex: os 6 de SCHEDULED_TIME)
    df_clean = df_clean.dropna()

    print(f"Dataset limpo. De {len(df)} linhas para {len(df_clean)} linhas.")

    return df_clean