"""

Desenho da estrurura do 'front' da app
Autor: Luis Armando Quintanilla Villon

"""


import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import streamlit as st


def grafico_compatibilidade(compatibilidade):
    """
    Função que gera o grafico de barras para a compatibilidad
    """
    compatibilidade = compatibilidade / 100  # Deve estar no intervalo [0, 1]
    print(compatibilidade)
    print(type(compatibilidade))
    # Criando o gráfico
    fig, ax = plt.subplots(figsize=(12, 4)) 
    sns.barplot(x=compatibilidade.index, y=compatibilidade.values, ax=ax, color='blue', edgecolor=None, order=compatibilidade.index)
    # sns.barplot(x=compatibilidade.index, y=compatibilidade.values, ax=ax, color='blue', edgecolor=None)
    sns.despine(top=True, right=True, left=True, bottom=False)
    ax.set_xlabel('ID do Proprietário', fontsize=10)
    ax.set_ylabel('Similaridade (%)', fontsize=10)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_yticklabels(['{:.1f}%'.format(y * 100) for y in ax.get_yticks()], fontsize=8)
    # Acrescentando rótulos de porcentagem acima de cada barra
    for p in ax.patches:
        height = p.get_height()
        ax.annotate('{:.1f}%'.format(height * 100),
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center',
                    xytext=(0, 5),
                    textcoords='offset points', fontsize=10, weight='bold')
    return(fig)


def tabela_compatibilidade(resultado):
    """
    Função que gera o tablea de vizinhos
    """
    # Mudando o nome do 'index' para VARIÁVEL
    resultado_0_with_index = resultado[0].reset_index()
    resultado_0_with_index.rename(columns={'index': 'VARIÁVEL'}, inplace=True)
    
    # Configurando a tabela com Plotly
    fig_table = go.Figure(data=[go.Table(
        columnwidth = [20] + [10] * (len(resultado_0_with_index.columns) - 1),
        header=dict(values=list(resultado_0_with_index.columns),
                    fill_color='paleturquoise',
                    align='left',
                    font_color='black',
                    font_size=14),
        cells=dict(values=[resultado_0_with_index[col] for col in resultado_0_with_index.columns],
                   fill_color='lavender',
                   font_color='black',
                   align='left'))
    ])
    
    # Configurando o tamanho do layout-tabela
    fig_table.update_layout(
        width=700, height=350,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return(fig_table)


def id_vizinhos(proprietario1, proprietario2, proprietario3, topn):
    """
    Função que gera uma lista dos vizinhos
    """
    # Gera uma lista com o ID dos proprietarios inseridos
    id_proprietarios = []
    for proprietario in [proprietario1, proprietario2, proprietario3]:
        try:
            if proprietario:
                id_proprietarios.append(int(proprietario))
        except ValueError:
            st.error(f"O ID do proprietario '{proprietario}' não é un número válido.")
            id_proprietarios = []
            break
    return(id_proprietarios)
