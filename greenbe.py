import streamlit as st
import requests
def mostrar():
    #Título
    st.title("GreenBe - Produtos naturais")

    #Campos
    codigo_produto = st.text_input("Código do produto")
    nome_produto = st.text_input("Nome do Produto")
    valor_produto = st.number_input("Valor do produto",min_value=0.0,format="%.2f")
    quantidade_produto = st.number_input("Quantidade do produto",min_value=0,step=1)
    categoria_produto = st.selectbox("Categoria do produto",["Alimentos","Bebidas","Suplementos","Outros"])
    descricao_produto = st.text_area("Descrição do produto")
    data_da_compra = st.date_input("Data da compra")
    data_compra = data_da_compra.strftime("%d/%m/%Y")
    total = valor_produto*quantidade_produto

    cep = st.text_input("Digite seu cep (Somente números)")
    numero_loja = st.text_input("Número da loja")

    endereco=""
    cidade = ""
    estado = ""

    if cep and len(cep)==8 and cep.isdigit():
        try:
            response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            data = response.json()
            if "erro" not in data:
                logradouro = data.get("logradouro","")
                bairro = data.get("bairro","")
                endereco = f"{logradouro} - {bairro}" if bairro else logradouro
                cidade = data.get("localidade","")
                estado = data.get("uf","")
                st.success("Endereço encontrado com sucesso!")
            else:
                st.error("CEP não encontrado")
        except Exception as e:
            st.error(f"Erro ao consultar o CEP: {e}")
    elif cep and (len(cep)!=8 or not cep.isdigit()):
        st.warning("Digite um CEP válido com 8 números")

    endereco = st.text_input("Endereço (rua/avenida/bairro)",value=endereco)
    cidade = st.text_input("Cidade",value = cidade)
    estado = st.text_input("estado",value = estado)

    #Salvar as informações
    if st.button("Adicionar produto"):
        if not codigo_produto or not nome_produto:
            st.warning("Preencha todos os campos obrigatórios")
        else:
            with open("produtos.txt",'a') as arquivo:
                arquivo.write(f"Código: {codigo_produto}\n")
                arquivo.write(f"Nome: {nome_produto}\n")
                arquivo.write(f"Valor: {valor_produto:.2f}\n")
                arquivo.write(f"Quantidade: {quantidade_produto}\n")
                arquivo.write(f"Categoria: {categoria_produto}\n")
                arquivo.write(f"Descrição: {descricao_produto}\n")
                arquivo.write(f"Total: {total:.2f}\n")
                arquivo.write(f"Data: {data_compra}\n")
                arquivo.write(f"CEP: {cep}\n")
                arquivo.write(f"Número: {numero_loja}\n")
                arquivo.write(f"Endereço: {endereco}\n")
                arquivo.write(f"Cidade: {cidade}\n")
                arquivo.write(f"Estado: {estado}\n")
                arquivo.write("="*40+"\n")
