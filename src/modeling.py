import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

def create_preprocessing_pipeline(numeric_features, categorical_features):
    """
    Cria um ColumnTransformer para aplicar pré-processamento 
    diferenciado em colunas numéricas e categóricas.

    Args:
        numeric_features (list): Lista de nomes das colunas numéricas.
        categorical_features (list): Lista de nomes das colunas categóricas.

    Returns:
        sklearn.compose.ColumnTransformer: O objeto ColumnTransformer.
    """

    # Pipeline para features numéricas:
    # Apenas aplica o StandardScaler (padroniza média=0, desvio=1)
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])

    # Pipeline para features categóricas:
    # Aplica OneHotEncoder (transforma 'AA', 'JFK' em colunas 0/1)
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
        # handle_unknown='ignore' é crucial: se o teste tiver um 
        # aeroporto que não vimos no treino, ele apenas ignora.
    ])

    # Combina os dois transformadores usando ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='passthrough' # Mantém colunas não especificadas (se houver)
    )

    print("Pipeline de pré-processamento (ColumnTransformer) criado com sucesso.")
    return preprocessor