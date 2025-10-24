

# 🌱 GreenBe Dashboard
Visão geral

O GreenBe Dashboard é um aplicativo interativo desenvolvido com Streamlit e Plotly, que centraliza o controle e a análise de produtos naturais.
O sistema permite o cadastro de produtos, visualização de dados de vendas e análise de desempenho por categoria, tornando o processo de gestão mais dinâmico e visual.

Funcionalidades principais

Cadastro de produtos com informações como nome, valor, quantidade, categoria e localização.

Consulta automática de CEP usando a API pública do ViaCEP.

Visualização interativa de dados com gráficos de pizza, dispersão, barras e linha.

Geolocalização de vendas com integração ao Geopy para exibir um mapa dinâmico dos registros.

Armazenamento local de dados em arquivo .txt e conversão automática para DataFrame do Pandas.

Tecnologias utilizadas
Tecnologia	Função
Python	Linguagem base
Streamlit	Criação da interface web
Plotly Express	Visualização de dados
Pandas	Manipulação de dados
Geopy	Geocodificação de endereços
Requests	Consumo da API ViaCEP
