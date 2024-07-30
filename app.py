"""

Sistema de recomendação por meio de streamlit e compatibilade por cosseno
Autor: Luis Armando Quintanilla Villon

"""


import streamlit as st
from compatibilidade import vizinhos_compativeis
from front import grafico_compatibilidade, id_vizinhos


def config_inicial():
    """ 
    Configuração inicial
    """
    # Configurar a página para usar um layout mais amplo
    st.set_page_config(layout="wide")
    # Mostrar uma imagem grande no topo
    st.image('./img/apt-6.png', use_column_width=True)
    # Inserir um espaço vertical de 60px
    st.markdown(f'<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)


def input_resultado_compatibilidade():
    """
    Calcula o resultados de compatibiliadade utilizando o input fornecido
    """
    # Configurar o sidebar com inputs e um botão
    resultado = None
    with st.sidebar:
        st.header("Seleção de Proprietários")
        st.write("Quem está morando no apartamento atualmente? \n Escreva o ID dos proprietários:")
        proprietario1 = st.text_input("Proprietário 1")
        proprietario2 = st.text_input("Proprietário 2")
        proprietario3 = st.text_input("Proprietário 3")
        st.header("Seleção de futuros vizinhos")
        num_vizinhos = st.text_input("Quantos novos colegas ou vizinhos você deseja procurar?")
        if st.button('PESQUISE NOVOS VIZINHOS'):
            # VerifiCar se o número de colegas é um valor válido
            try:
                topn = int(num_vizinhos)
            except ValueError:
                st.error("Por gentileza, insira um número válido para o número de colegas.")
                topn = None
            
            # Obtendo IDs de proprietários usando a função 'id_vizinhos'
            id_proprietarios = id_vizinhos(proprietario1, proprietario2, proprietario3, topn)
            if id_proprietarios and topn is not None:
                # Chamando a função 'vizinhos_compativeis' com os parâmetros correspondentes
                resultado = vizinhos_compativeis(id_proprietarios, topn)
    return resultado


def print_resultado(resultado):
    """
    Imprime os resultados em duas colunas
    """
    # Verificar se 'resultado' contém uma mensagem de erro (string de texto)
    # Caso contrário, e se 'resultado' não for None, mostrar o gráfico de barras e a tabela
    if isinstance(resultado, str):
        st.error(resultado)    
    elif resultado is not None:
        st.markdown("## Resultados da Compatibilidade")
        st.markdown("---")
        st.write("Compatibilidade (%) com os vizinhos recomendados:")
        fig_grafico = grafico_compatibilidade(resultado[1])
        st.pyplot(fig_grafico)
        st.markdown("---")
  
    
def main() -> None:
    config_inicial()
    # Ingressar o input e encontrar o resultado para a compatibilidade
    resultado = input_resultado_compatibilidade()
    # Imprimir os resultados na aplicação
    print_resultado(resultado)


if __name__ == '__main__':
    main()
    