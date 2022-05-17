from selenium import webdriver #criar o navegado
from selenium.webdriver.common.keys import Keys #Permiter clicar teclas no teclador
from selenium.webdriver.common.by import By #Localizar elementos (os itens de um site)
import pandas as pd
import numpy


navegador = webdriver.Chrome()

#1 - Entrar no google
navegador.get('https://www.google.com/')

#2 - Pesquisar a cotação do dolar
navegador.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('cotação do dolar')
navegador.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
#3 - Pegar a cotação do dolar
cotacao_dolar = navegador.find_element(By.XPATH,'//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')
#4 - Pegar a cotação do euro
navegador.get('https://www.google.com/')
navegador.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('cotação do euro')
navegador.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
cotacao_euro = navegador.find_element(By.XPATH,'//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')
#5 - Pegar a cotação do ouro
navegador.get('https://www.melhorcambio.com/ouro-hoje')
cotacao_ouro = navegador.find_element(By.XPATH,'//*[@id="comercial"]').get_attribute('value')
cotacao_ouro = cotacao_ouro.replace(',','.') #trocar a virgula pelo ponto
#6 - Atuaçozar a minha abse de dados com as novas cotações
tabela = pd.read_excel('Produtos.xlsx')
#Atualizar a cotação de acordo com a moeda correspondente
#Dolar
tabela.loc[tabela['Moeda'] == 'Dólar',"Cotação"] = float(cotacao_dolar)
#Euro
tabela.loc[tabela['Moeda'] == 'Euro',"Cotação"] = float(cotacao_euro)
#Ouro
tabela.loc[tabela['Moeda'] == 'Ouro',"Cotação"] = float(cotacao_ouro)

#atualiar preço de compra = preco original * cotação
tabela['Preço de Compra'] = tabela['Preço Original'] * tabela['Cotação']
#atualizar preço de venda = preço de compra * margem
tabela['Preço de Venda'] = tabela['Preço de Compra'] * tabela['Margem']

#Para criar uma tabela Depoid do = é só colocar a somar que você quer
#tabela['Preço de Venda Atualizado'] = tabela['Preço de Compra'] * tabela['Margem']

#Exporta a nova base de preço atualizado
tabela.to_excel('tabela Atualizada.xlsx', index=False)
