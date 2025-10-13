import streamlit as st
import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim
import time

def mostrar():
    
    st.title("📊 Dashboard - GreenBe")


    # -------------------- FUNÇÃO DE CARREGAMENTO --------------------
    def carregar_dados(arquivo):
        try:
            with open(arquivo, 'r', encoding='utf-8') as file:
                linhas = file.readlines()

            produtos = []
            produto = {}

            for linha in linhas:
                linha = linha.strip()
                linha_lower = linha.lower()

                if linha_lower.startswith("código:"):
                    produto["Código"] = linha.split(":", 1)[1].strip()
                elif linha_lower.startswith("nome:"):
                    produto["Nome"] = linha.split(":", 1)[1].strip()
                elif linha_lower.startswith("valor:"):
                    valor = linha.split(":", 1)[1].strip().replace(',', '.')
                    produto["Valor"] = float(valor) if valor else None
                elif linha_lower.startswith("quantidade:"):
                    qtd = linha.split(":", 1)[1].strip()
                    produto["Quantidade"] = int(qtd) if qtd else None
                elif linha_lower.startswith("categoria:"):
                    produto["Categoria"] = linha.split(":", 1)[1].strip()
                elif linha_lower.startswith("descrição:"):
                    produto["Descrição"] = linha.split(":", 1)[1].strip()
                elif linha_lower.startswith("total:"):
                    total = linha.split(":", 1)[1].strip().replace(',', '.')
                    produto["Total"] = float(total) if total else None
                elif linha_lower.startswith("data:"):
                    produto["Data"] = linha.split(":", 1)[1].strip()
                elif linha_lower.startswith("cep:"):
                    produto["CEP"] = linha.split(":", 1)[1].strip()
                elif linha_lower.startswith("número:"):
                    produto["Número"] = linha.split(":", 1)[1].strip()
                elif linha_lower.startswith("endereço:"):
                    produto["Endereço"] = linha.split(":", 1)[1].strip()
                elif linha_lower.startswith("cidade:"):
                    produto["Cidade"] = linha.split(":", 1)[1].strip()
                elif linha_lower.startswith("estado:"):
                    produto["Estado"] = linha.split(":", 1)[1].strip()
                elif linha_lower.startswith("="):
                    if produto:
                        produtos.append(produto)
                        produto = {}

            # Garante que o último item seja salvo mesmo sem linha de separação
            if produto:
                produtos.append(produto)

            df = pd.DataFrame(produtos)

            # Garante que a coluna Data exista
            
            df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
            
            return df

        except FileNotFoundError:
            st.error("❌ Arquivo não encontrado.")
            return pd.DataFrame()
        except Exception as e:
            st.error(f"⚠️ Erro ao carregar os dados: {e}")
            return pd.DataFrame()


    # -------------------- EXECUÇÃO PRINCIPAL --------------------
    df = carregar_dados("produtos2.txt")

    if not df.empty:
        st.header("📋 Tabela com os dados")
        st.dataframe(df)
        

        # Gráfico de pizza por categoria
        if "Categoria" in df.columns and "Total" in df.columns:
            df_categoria = df.groupby("Categoria")["Total"].sum().reset_index()
            graf_pizza = px.pie(
                df_categoria,
                names="Categoria",
                values="Total",
                title="Participação no valor total por categoria",
                color_discrete_sequence=["#a8329b", "#a87132", "#090854", "#540808"]
            )
            st.plotly_chart(graf_pizza)
        else:
            st.warning("⚠️ Colunas 'Categoria' ou 'Total' não encontradas.")

        # Gráfico de dispersão Valor x Quantidade
        if "Valor" in df.columns and "Quantidade" in df.columns:
            graf_disp = px.scatter(
                df,
                x="Valor",
                y="Quantidade",
                color="Categoria" if "Categoria" in df.columns else None,
                hover_data=["Nome"] if "Nome" in df.columns else None,
                title="Correlação entre preço e quantidade"
            )
            st.plotly_chart(graf_disp)

        # Top 5 produtos mais caros
        if "Valor" in df.columns:
            top5 = df.sort_values(by="Valor", ascending=False).head(5)
            graf_bar = px.bar(
                top5,
                x="Nome" if "Nome" in df.columns else "Código",
                y="Valor",
                color="Categoria" if "Categoria" in df.columns else None,
                title="Top 5 produtos mais caros"
            )
            st.plotly_chart(graf_bar)

        # Total vendido por data
        if "Data" in df.columns and "Total" in df.columns:
            df_data = df.groupby("Data")["Total"].sum().reset_index()
            graf_linha = px.line(
                df_data,
                x="Data",
                y="Total",
                markers=True,
                title="Total vendido por data"
            )
            st.plotly_chart(graf_linha)

        # Geolocalização
        geolocalizacao = Nominatim(user_agent='raizac_dashboard')

        def obter_coordenadas(row):
            try:
                endereco = f"{row.get('Endereço', '')}, {row.get('Número', '')}, {row.get('Cidade', '')}, {row.get('Estado', '')}, Brasil"
                localizacao = geolocalizacao.geocode(endereco, timeout=10)
                if localizacao:
                    return pd.Series({'lat': localizacao.latitude, 'lon': localizacao.longitude})
            except Exception as e:
                print(f"Erro ao geocodificar {endereco}: {e}")
            return pd.Series({'lat': None, 'lon': None})

        if 'lat' not in df.columns or 'lon' not in df.columns:
            with st.spinner("🗺️ Obtendo coordenadas dos endereços..."):
                coords = df.apply(obter_coordenadas, axis=1)
                df['lat'] = coords['lat']
                df['lon'] = coords['lon']
                time.sleep(1)

        mapa_df = df.dropna(subset=['lat', 'lon'])
        if not mapa_df.empty:
            st.success("✅ Mapa gerado com sucesso!")
            st.map(mapa_df[['lat', 'lon']])
        else:
            st.warning("⚠️ Nenhum endereço válido para exibir no mapa.")

    else:
        st.warning("📭 Nenhum dado cadastrado encontrado.")
