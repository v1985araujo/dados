from threading import RLock
import numpy as np, pandas as pd, matplotlib.pyplot as plt, streamlit as st

#   Notas históricas sobre os estados
notas = {1979: "A população do Mato Grosso do Sul está contida no Mato Grosso, pois no dia 11 de outubro de 1977, concretizou-se o desmembramento de Mato Grosso do Sul, que o presidente Ernesto Geisel elevou à categoria de estado em 1º de janeiro de 1979.",
         1988: "A população de Tocantins está contida em Goiás, pois o estado foi criado em 5 de outubro de 1988, após a promulgação da Constituição Cidadã.", 
}

#   Dados extraídos de: https://dados.al.gov.br/catalogo/datastore/dump/a77d4575-b225-444d-9e46-92362ae27b21
df = pd.read_csv('a77d4575-b225-444d-9e46-92362ae27b21.csv', 
                 sep = ',').replace('...', 0).astype({
                      'co_uf': np.int64, 'valor': np.int64}).drop('_id', axis = 1)

with st.sidebar:
    st.title('Opções do Gráfico')
    cor = st.color_picker('Escolha a cor', '#2A74B1')
    #  Pegando ocorrências distintas nos dados históricos (consideramos o período de 1970 até 2022)
    ano = st.selectbox('Escolha o ano', df['ano'].unique()) 
    for key, value in notas.items():
        if key >= ano:
            st.write(value)


#   Alterando o índice do DataFrame para corresponder as variações de ano e código UF, assim facilita a pesquisa por ano
df = df.set_index(['ano', 'co_uf'])

#   Pesquisar as Unidades Federativas na internet
estados = pd.read_html('https://www.oobj.com.br/bc/article/quais-os-c%C3%B3digos-de-cada-uf-no-brasil-465.html', 
                       encoding='UTF-8')
estados = estados[0].set_index('Código UF').sort_index(ascending = False)

#   Criar uma cópia das UFs em CSV
estados.to_csv('estados.csv', index = 'Código UF', sep = ',', encoding = 'utf-8')

#   Especifica-se o ascending mesmo no sort_index para não comprometer a informação
estados.sort_index(ascending = False)

st.markdown(f'### População de {ano} em milhões de habitantes')

#   Qual ano vai visualizar? Aquele que foi escolhido no selectbox
dados = df.loc[ano,].sort_index(ascending = False)

#   Copiando as Unidades Federativas para a plotagem
dados['uf'] = estados['UF'].values 
dados = dados[['valor', 'uf', 'no_uf']]
dados = dados[dados['valor'] > 0].sort_values('valor', ascending = False)
dados['valor'] = dados['valor'] / 1e6 # 10**6

#   Plotando o gráfico no 
c = st.container()
_lock = RLock() # Thread.yield() quando terminar o bloco?
with _lock:
    plt.style.use('_mpl-gallery')
    plt.figure(figsize = (10, 8), facecolor = '#AAA')
    plt.bar(edgecolor = '#aaa',
                facecolor = cor,
                data = dados,
                x = dados['uf'],
                width = .7,            
                height = dados['valor'])
    #plt.title(f'População por Estado em {ano}').set_fontweight('bold')
    plt.legend(['Milhão de habitantes'], 
                fontsize = 6, 
                title = 'População no Brasil', 
                title_fontsize = 7, 
                shadow = True).get_title().set_weight('bold')    
    c.pyplot(plt)

#c1, c2 = st.columns(2)
#c1.bar_chart(dados, x = 'uf', y = 'valor', color = cor, x_label = '', y_label = '', horizontal = True)
