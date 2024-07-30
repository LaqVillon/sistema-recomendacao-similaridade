"""

Desenho da estrurura do 'front' da app
Autor: Luis Armando Quintanilla Villon

"""


import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


def grafico_compatibilidade(compatibilidade):
    """
    Função que gera o gráfico de barras para a compatibilidade
    """
    compatibilidade = compatibilidade / 100  # Deve estar no intervalo [0, 1]
    
    # Criando o gráfico
    fig, ax = plt.subplots(figsize=(14, 6)) 
    sns.set(style="whitegrid")
    palette = sns.color_palette("Blues_r", len(compatibilidade))
    sns.barplot(x=compatibilidade.index, 
                y=compatibilidade.values, 
                ax=ax, palette=palette, 
                edgecolor=None, order=compatibilidade.index)
    sns.despine(top=True, right=True, left=True, bottom=False)
    ax.set_xlabel('ID do Proprietário', fontsize=12, weight='bold')
    ax.set_ylabel('Similaridade (%)', fontsize=12, weight='bold')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)
    ax.set_yticklabels(['{:.1f}%'.format(y * 100) for y in ax.get_yticks()], fontsize=10)
    
    # Acrescentando rótulos de porcentagem acima de cada barra
    for p in ax.patches:
        height = p.get_height()
        ax.annotate('{:.1f}%'.format(height * 100),
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center',
                    xytext=(0, 8),
                    textcoords='offset points', fontsize=10, weight='bold', color='black')
    
    # Título do gráfico
    ax.set_title('Compatibilidade com os Vizinhos Recomendados', fontsize=14, weight='bold')
    
    return fig


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
