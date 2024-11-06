"""
    Raspagem de Dados de Produtos
        ...
        O programa Raspagem de Dados de Produtos tem como objetivo extrair dados de sites e plataformas de e-commerce.
        
        Recomenda-se o uso em operações de raspagem de dados para cotação de preços.
"""

"""
    Para a execução do programa, serão importadas bibliotecas.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import math


print("\nPrograma de Raspagem de Dados\n")


"""
    O navegador faz uso de configurações do Webdriver, ChromeDriverManager e Service.
        ...
        Ao abrir o navegador, a janela será maximizada automaticamente.
        Para acessar uma determinada página, deve-se inserir a url completa como argumento.
"""
navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
navegador.maximize_window()
navegador.get('') # Inserir a url para acessar uma determinada página.


"""
    Raspagem dos produtos.
        ...
        Para a extração dos dados por página, o programa busca a quantidade de produtos.
"""
qtde_itens = navegador.find_element(By.ELEMENTO, 'CONTAGEM DE PRODUTOS').text
numeros = re.findall(r'\d+', qtde_itens)

if numeros:
    resultado = ''.join(numeros)
    print(f"Total de produtos: {resultado}")
else:
    print("O texto não possui caracteres numéricos.")


"""
    Cálculo de páginas.
        ...
        Para o cálculo de páginas, o programa faz a divisão do total de produtos anunciados pelo total de produtos por página.
        O resultado será o total de páginas.
"""
ultima_pagina = math.ceil(int(resultado) / 20)
print(f"Total de páginas: {ultima_pagina}")


"""
    Dicionário.
        ...
        Para o armazenamento dos dados extraídos, será gerado um dicionário.
"""
dic_produtos = {"Produto": [], "Preço": []}


"""
    Raspagem de dados por página.
        ...
        Para cada página, será extraído os dados de cada produto anunciado.

"""
for i in range(1, ultima_pagina + 1):
    url_pagina = f'' # Inserir a url da primeira página de produtos; na url, inserir {i} no lugar do valor referente ao número da página.
    navegador.get(url_pagina)

    WebDriverWait(navegador, 4).until(EC.presence_of_element_located((By.ELEMENTO, 'PRODUTO')))
    produtos = navegador.find_elements(By.ELEMENTO, 'PRODUTO')

    if produtos:
        for produto in produtos:
            WebDriverWait(navegador, 4).until(EC.presence_of_element_located((By.ELEMENTO, 'NOME DO PRODUTO')))
            nome_produto = produto.find_element(By.ELEMENTO, 'NOME DO PRODUTO').text

            WebDriverWait(navegador, 4).until(EC.presence_of_element_located((By.ELEMENTO, 'PREÇO DO PRODUTO')))
            preco_produto = produto.find_element(By.ELEMENTO, 'PREÇO DO PRODUTO').text

            dic_produtos["Produto"].append(nome_produto)  
            dic_produtos["Preço"].append(preco_produto)

            print(nome_produto, preco_produto)


"""
    Tabela.
        ...
        Após o fim da extração dos dados de todos os produtos, será gerado um arquivo CSV.
"""
df = pd.DataFrame(dic_produtos)
df.to_csv(r'DIRETÓRIO PARA O ENVIO DO ARQUIVO GERADO', encoding='utf-8-sig', sep=';', index=False)


"""
    Encerrar o programa manualmente.
"""
input("Aperte 'Enter' para finalizar.")