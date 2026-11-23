import streamlit as st

from detector import mascarar, restaurar

# Nome de cada tipo para mostrar na tabela
NOMES = {
    "CPF": "CPF",
    "CNPJ": "CNPJ",
    "EMAIL": "E-mail",
    "TELEFONE": "Telefone",
    "CARTAO": "Cartão",
}

# Exemplo com dados fictícios (CPF, CNPJ e cartão de teste, válidos só no cálculo)
EXEMPLO = (
    "Meu CPF é 111.444.777-35, meu e-mail é teste@exemplo.com e meu telefone "
    "é (11) 98765-4321. A empresa tem CNPJ 11.222.333/0001-81 e o cartão de "
    "teste é 4111 1111 1111 1111."
)

st.set_page_config(page_title="PrivaIA · Vitrine", page_icon=":material/shield_lock:")

st.title("PrivaIA")
st.markdown(
    "Antes de um texto ir para uma IA, o PrivaIA **encontra os dados pessoais "
    "e troca cada um por uma etiqueta**. A IA trabalha só com o texto protegido, "
    "e os dados reais são recolocados na resposta."
)
st.warning(
    "Use apenas dados fictícios. Esta página não envia nada para a IA "
    "e não guarda o que você digita.",
    title="Demonstração",
    icon=":material/info:",
)

texto = st.text_area(
    "Texto para proteger",
    value=EXEMPLO,
    height=130,
    key="texto",
)

if st.button("Proteger", type="primary", icon=":material/shield:", key="proteger"):
    mascarado, dados_por_marcador = mascarar(texto)

    if not dados_por_marcador:
        st.info("Nenhum dado pessoal encontrado neste texto.", icon=":material/search_off:")
        st.stop()

    st.subheader("1. O que a IA recebe")
    col_original, col_mascarado = st.columns(2)
    with col_original:
        st.caption("Texto original")
        st.code(texto, language=None, wrap_lines=True)
    with col_mascarado:
        st.caption("Texto protegido")
        st.code(mascarado, language=None, wrap_lines=True)

    st.subheader(f"2. Dados encontrados: {len(dados_por_marcador)}")
    linhas = []
    for marcador, dado in dados_por_marcador.items():
        tipo = marcador.strip("[]").rsplit("_", 1)[0]
        linhas.append({"Tipo": NOMES.get(tipo, tipo), "Etiqueta": marcador, "Dado original": dado})
    st.dataframe(linhas, hide_index=True, alt="Dados pessoais encontrados e suas etiquetas")
    st.caption("Este mapa fica só na empresa. A IA nunca o recebe.")

    st.subheader("3. A resposta volta com os dados reais")
    resposta_ia = "Recebido! Registrei os dados: " + ", ".join(dados_por_marcador) + "."
    col_ia, col_final = st.columns(2)
    with col_ia:
        st.caption("Resposta da IA (simulada)")
        st.code(resposta_ia, language=None, wrap_lines=True)
    with col_final:
        st.caption("Resposta final para quem perguntou")
        st.code(restaurar(resposta_ia, dados_por_marcador), language=None, wrap_lines=True)

st.divider()
st.caption(
    "Código no GitHub: [buenor877-ux/PrivaIA](https://github.com/buenor877-ux/PrivaIA) · "
    "Python · FastAPI · Gemini · SQLite · Docker Compose · n8n"
)
