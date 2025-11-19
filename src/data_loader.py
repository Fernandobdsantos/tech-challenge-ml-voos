import pandas as pd

def load_datasets(base_path='data/'):
    """
    Carrega os três datasets principais do projeto.

    Args:
        base_path (str): Caminho para a pasta que contém os CSVs.

    Returns:
        tuple: (df_flights, df_airlines, df_airports)
    """
    try:
        path_flights = f"{base_path}flights.csv"
        path_airlines = f"{base_path}airlines.csv"
        path_airports = f"{base_path}airports.csv"

        df_flights = pd.read_csv(path_flights)
        df_airlines = pd.read_csv(path_airlines)
        df_airports = pd.read_csv(path_airports)

        print("Datasets carregados com sucesso!")
        return df_flights, df_airlines, df_airports

    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado. Verifique o caminho: {e}")
        return None, None, None