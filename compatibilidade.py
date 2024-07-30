"""

Implementação do algoritmo de similaridade por cosseno para encontrar a similaridade entre proprietários
Autor: Luis Armando Quintanilla Villon

"""


import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def dados_preprocesados():
    """
    Função que carga e pre-processa os dados
    """
    df = pd.read_csv('dataset/dataset_proprietarios.csv', index_col = 'id')
    
    # One Hot Encoding
    encoder = OneHotEncoder(sparse_output=False)
    df_encoded = encoder.fit_transform(df)
        
    # Calcule a matriz de similaridade usando o produto escalar e define o intervalo
    matriz_s = np.dot(df_encoded, df_encoded.T)
    rango_min = -100
    rango_max = 100
    min_original = np.min(matriz_s)
    max_original = np.max(matriz_s)
    
    # Normalizando a matriz ([0,100]) e passando para um objeto pandas
    matriz_s_normalizada = ((matriz_s - min_original) / (max_original - min_original)) * (rango_max - rango_min) + rango_min    
    df_similaridade = pd.DataFrame(matriz_s_normalizada,
        index = df.index,
        columns = df.index)
    return df, df_similaridade
    

def vizinhos_compativeis(id_proprietarios, topn):
    """ 
    BÚSQUEDA DE PROPRIETAROS COMPATIVEIS

    Input:
        * id_proprietarios: Deve ser uma lista de IDs
        * topn: número de proprietários compatíveis para buscar

    Output:
        Lista com 2 elementos.
        Elemento 0: Features dos proprietarios compatibles
        Elemento 1: A similaridade em número
    """
    # Preparando os dados
    df, df_similaridade = dados_preprocesados()
    
    # Verificar se todos os ID de inquilinos estão na matriz de similaridade
    for id_proprietario in id_proprietarios:
        if id_proprietario not in df_similaridade.index:
            return 'Al menos uno de los inquilinos no encontrado'

    # Obter as linhas correspondientes aos proprietarios inseridos
    linhas_proprietarios = df_similaridade.loc[id_proprietarios]
    
    # Calcular a similaridade media entre os proprietarios
    similitude_media = linhas_proprietarios.mean(axis=0)
    
    # Ordenamento dos proprietarios de acordo com a similaridade média
    proprietarios_similares = similitude_media.sort_values(ascending=False)

    # Excluir os proprietarios iniciai
    proprietarios_similares = proprietarios_similares.drop(id_proprietarios)

    # Calcular os proprietarios com más similaridade média
    topn_proprietarios = proprietarios_similares.head(topn)
    
    # Obter os registros dos proprietarios similares
    registros_similares = df.loc[topn_proprietarios.index]
    
    # Obter os registros dos proprietarios procurados
    registros_buscados = df.loc[id_proprietarios]

    # Concatenar os registros buscados com os registros similares
    resultado = pd.concat([registros_buscados.T, registros_similares.T], axis=1)

    # Criar un objeto panda series
    similitude_series = pd.Series(data=topn_proprietarios.values, index=topn_proprietarios.index, name='Similitud')
    return(resultado, similitude_series)
