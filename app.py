import streamlit as st
import random


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Quiz de Química",
    page_icon="🧪",
    layout="centered"
)


# ============================================================
# 35 REAÇÕES
# ============================================================

reacoes = [
    ("H₂O + CO₂", "H₂CO₃"),
    ("Zn + 2HCl", "ZnCl₂ + H₂"),
    ("H₂CO₃", "H₂O + CO₂"),
    ("Zn + CuSO₄", "ZnSO₄ + Cu"),
    ("NaOH + HCl", "NaCl + H₂O"),
    ("H₂SO₄ + CaCl₂", "CaSO₄ + 2HCl"),
    ("2Na + Cl₂", "2NaCl"),
    ("Na₂O + H₂O", "2NaOH"),
    ("2KClO₃", "2KCl + 3O₂"),
    ("2H₂O₂", "2H₂O + O₂"),
    ("2HCl + CaCO₃", "CaCl₂ + H₂O + CO₂"),
    ("Na₂CO₃", "Na₂O + CO₂"),
    ("2NaHCO₃", "Na₂CO₃ + H₂O + CO₂"),
    ("CaO + H₂O", "Ca(OH)₂"),
    ("CaCO₃", "CaO + CO₂"),
    ("NH₄OH", "NH₃ + H₂O"),
    ("NH₄NO₃", "N₂O + 2H₂O"),
    ("NaHCO₃ + HCl", "NaCl + H₂O + CO₂"),
    ("NaCl + AgNO₃", "NaNO₃ + AgCl"),
    ("H₂SO₄ + 2KCN", "2HCN + K₂SO₄"),
    ("2H₂ + O₂", "2H₂O"),
    ("2NaN₃", "2Na + 3N₂"),
    ("2Cu(NO₃)₂", "2CuO + 4NO₂ + O₂"),
    ("2AgCl", "2Ag + Cl₂"),
    ("Ba(OH)₂ + CO₂", "BaCO₃ + H₂O"),
    ("Fe₂O₃ + 2Al", "Al₂O₃ + 2Fe"),
    ("Ag₂O + C₆H₁₂O₆ (glicose)", "2Ag + C₆H₁₂O₇"),
    ("SO₂ + Br₂ + 2H₂O", "2HBr + H₂SO₄"),
    ("Cu + 4HNO₃", "Cu(NO₃)₂ + 2NO₂ + 2H₂O"),
    ("Ag + HCl", "não ocorre"),
    ("NaNO₃ + CuSO₄", "não ocorre"),
    ("AgNO₃ + Al(NO₃)₃", "não ocorre"),
    ("Cu + ZnCl₂", "não ocorre"),
    ("2SO₂ + O₂", "2SO₃"),
    ("4NH₃ + 5O₂", "4NO + 6H₂O"),
]


# ============================================================
# FUNÇÕES
# ============================================================

def normalizar(texto):
    """
    Deixa a resposta mais fácil de comparar.

    Aceita:
    H2O
    H₂O
    h2o
    H₂ O
    etc.
    """

    texto = texto.strip().lower()

    # Remove espaços
    texto = texto.replace(" ", "")

    # Aceita "não ocorre" e "nao ocorre"
    texto = texto.replace("nãoocorre", "naoocorre")

    # Converte números normais para subscritos
    conversao = str.maketrans(
        "0123456789",
        "₀₁₂₃₄₅₆₇₈₉"
    )

    texto = texto.translate(conversao)

    # Separa produtos pelo +
    partes = texto.split("+")

    # Ordena para permitir respostas em outra ordem
    partes = sorted(partes)

    return "+".join(partes)


def resposta_correta(resposta_usuario, resposta_certa):
    return normalizar(resposta_usuario) == normalizar(resposta_certa)


# ============================================================
# INICIALIZAÇÃO
# ============================================================

if "ordem" not in st.session_state:
    st.session_state.ordem = list(range(len(reacoes)))
    random.shuffle(st.session_state.ordem)

if "questao_atual" not in st.session_state:
    st.session_state.questao_atual = 0

if "respostas" not in st.session_state:
    st.session_state.respostas = {}

if "corretas" not in st.session_state:
    st.session_state.corretas = set()

if "resultado" not in st.session_state:
    st.session_state.resultado = {}

if "mostrar_resposta" not in st.session_state:
    st.session_state.mostrar_resposta = False


# ============================================================
# TÍTULO
# ============================================================

st.title("🧪 Quiz de Reações Químicas")

st.write("Complete os produtos de cada reação.")

st.divider()


# ============================================================
# INFORMAÇÕES
# ============================================================

total = len(reacoes)
numero = st.session_state.questao_atual
indice_real = st.session_state.ordem[numero]

reagentes, produtos = reacoes[indice_real]

pontuacao = len(st.session_state.corretas)

st.markdown(
    f"### Questão {numero + 1} de {total}"
)

st.progress((numero + 1) / total)

st.write(f"**Pontuação: {pontuacao} / {total}**")


# ============================================================
# REAÇÃO
# ============================================================

st.markdown("### Complete a reação:")

st.markdown(
    f"## {reagentes} → ?"
)


# ============================================================
# CAMPO DE RESPOSTA
# ============================================================

chave = f"resposta_{indice_real}"

if chave not in st.session_state:
    st.session_state[chave] = st.session_state.respostas.get(
        indice_real,
        ""
    )

resposta = st.text_input(
    "Digite os produtos:",
    key=chave,
    placeholder="Ex.: H₂O + CO₂"
)

st.session_state.respostas[indice_real] = resposta


# ============================================================
# BOTÕES PRINCIPAIS
# ============================================================

col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Verificar", use_container_width=True):

        if resposta.strip() == "":
            st.warning("Digite uma resposta primeiro!")

        else:
            if resposta_correta(resposta, produtos):
                st.session_state.corretas.add(indice_real)
                st.session_state.resultado[indice_real] = True
                st.success("🎉 Correto!")

            else:
                st.session_state.corretas.discard(indice_real)
                st.session_state.resultado[indice_real] = False
                st.error("❌ Incorreto!")


with col2:
    if st.button("👀 Ver resposta", use_container_width=True):
        st.session_state.mostrar_resposta = True


# ============================================================
# MOSTRAR RESPOSTA
# ============================================================

if st.session_state.mostrar_resposta:

    st.info(f"**Resposta:** {reagentes} → {produtos}")

    if st.button("Ocultar resposta", use_container_width=True):
        st.session_state.mostrar_resposta = False
        st.rerun()


# ============================================================
# RESULTADO DA QUESTÃO
# ============================================================

if indice_real in st.session_state.resultado:

    if st.session_state.resultado[indice_real]:
        st.success("✅ Você acertou esta questão.")

    else:
        st.error(
            f"❌ A resposta correta é: **{produtos}**"
        )


# ============================================================
# NAVEGAÇÃO
# ============================================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "⬅️ Anterior",
        use_container_width=True,
        disabled=(numero == 0)
    ):
        st.session_state.questao_atual -= 1
        st.session_state.mostrar_resposta = False
        st.rerun()


with col2:

    if st.button(
        "Próxima ➡️",
        use_container_width=True,
        disabled=(numero == total - 1)
    ):
        st.session_state.questao_atual += 1
        st.session_state.mostrar_resposta = False
        st.rerun()


# ============================================================
# BOTÕES EXTRAS
# ============================================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button("🧹 Limpar", use_container_width=True):

        if chave in st.session_state:
            st.session_state[chave] = ""

        st.session_state.respostas[indice_real] = ""
        st.session_state.resultado.pop(indice_real, None)
        st.session_state.corretas.discard(indice_real)

        st.rerun()


with col2:

    if st.button("🔀 Novo embaralhamento", use_container_width=True):

        st.session_state.ordem = list(range(len(reacoes)))
        random.shuffle(st.session_state.ordem)

        st.session_state.questao_atual = 0
        st.session_state.respostas = {}
        st.session_state.corretas = set()
        st.session_state.resultado = {}
        st.session_state.mostrar_resposta = False

        # Limpa respostas antigas
        for chave_antiga in list(st.session_state.keys()):
            if chave_antiga.startswith("resposta_"):
                del st.session_state[chave_antiga]

        st.rerun()


# ============================================================
# TODAS AS RESPOSTAS
# ============================================================

st.divider()

with st.expander("📚 Ver todas as respostas"):

    for i, (reag, prod) in enumerate(reacoes, start=1):

        st.write(
            f"**{i}.** {reag} → {prod}"
        )


# ============================================================
# FINAL
# ============================================================

if numero == total - 1:

    st.divider()

    st.markdown("### 🏆 Final do quiz")

    st.write(
        f"Você acertou **{pontuacao} de {total} questões**."
    )

    porcentagem = (pontuacao / total) * 100

    st.progress(pontuacao / total)

    st.write(f"**Aproveitamento: {porcentagem:.0f}%**")