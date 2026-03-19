"""
Componenti UI riusabili per il gioco "Consulenti di Felicità".
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


DIMENSION_NAMES = {
    "E": "Equità",
    "L": "Libertà",
    "B": "Benessere",
}


def section_title(title: str, caption: str | None = None) -> None:
    """Titolo di sezione uniforme."""
    st.markdown(f"## {title}")
    if caption:
        st.caption(caption)


def info_box(text: str) -> None:
    """Box informativo semplice."""
    st.info(text)


def warning_box(text: str) -> None:
    """Box warning semplice."""
    st.warning(text)


def success_box(text: str) -> None:
    """Box successo semplice."""
    st.success(text)


def render_card_summary(card_name: str, card_data: dict, show_scores: bool = True) -> None:
    """Mostra una carta in formato testuale compatto."""
    card_type = card_data.get("type", "")
    type_label = {
        "red": "🔴 Problema",
        "green": "🟢 Risorsa",
        "yellow": "🟡 Fattore ambiguo",
    }.get(card_type, "")

    with st.container(border=True):
        st.markdown(f"**{card_name}**")
        if type_label:
            st.caption(type_label)
        st.write(card_data.get("description", ""))

        if show_scores:
            cols = st.columns(3)
            cols[0].metric("Equità", card_data.get("E", 0))
            cols[1].metric("Libertà", card_data.get("L", 0))
            cols[2].metric("Benessere", card_data.get("B", 0))


def render_selected_cards_list(title: str, card_names: list[str]) -> None:
    """Mostra elenco sintetico carte selezionate."""
    st.markdown(f"### {title}")
    if not card_names:
        st.write("Nessuna carta selezionata.")
        return
    for card in card_names:
        st.write(f"- {card}")


def render_contribution_table(result: dict) -> None:
    """
    Mostra la tabella dei contributi:
    Base, problema, carte, combo, totale finale.
    """
    df = pd.DataFrame(result["contribution_rows"])

    def fmt_value(x):
        if isinstance(x, (int, float)):
            if x > 0:
                return f"+{int(x)}"
            return f"{int(x)}"
        return x

    styled_df = df.copy()
    for col in ["E", "L", "B"]:
        if col in styled_df.columns:
            styled_df[col] = styled_df[col].apply(fmt_value)

    st.dataframe(
        styled_df,
        hide_index=True,
        width="stretch",
    )


def render_score_bars(scores: dict) -> None:
    """
    Mostra istogramma delle 3 dimensioni finali su scala 0-5.
    """
    df = pd.DataFrame(
        {
            "Dimensione": ["Equità", "Libertà", "Benessere"],
            "Punteggio": [scores["E"], scores["L"], scores["B"]],
        }
    ).set_index("Dimensione")

    st.bar_chart(df, y="Punteggio")


def render_dimension_badges(scores: dict) -> None:
    """Mostra metriche compatte finali."""
    col1, col2, col3 = st.columns(3)
    col1.metric("Equità", f"{scores['E']}/5")
    col2.metric("Libertà", f"{scores['L']}/5")
    col3.metric("Benessere", f"{scores['B']}/5")


def render_emoji_result(total_score: int, emoji: str) -> None:
    """Mostra emoji finale e somma su 15."""
    st.markdown("### Indice finale della società")
    st.markdown(f"<div style='font-size: 4rem; text-align: center;'>{emoji}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='text-align: center; font-size: 1.2rem;'><strong>{total_score}/15</strong></p>",
        unsafe_allow_html=True,
    )


def interpret_scores(scores: dict) -> list[str]:
    """
    Genera un piccolo commento narrativo dai punteggi finali.
    Regole semplici e leggibili per la classe.
    """
    messages = []

    if scores["E"] <= 1:
        messages.append("In questa società ci sono forti disuguaglianze.")
    elif scores["E"] >= 4:
        messages.append("In questa società le opportunità sono distribuite in modo abbastanza equo.")

    if scores["L"] <= 1:
        messages.append("Molte persone non si sentono libere di essere se stesse.")
    elif scores["L"] >= 4:
        messages.append("Le persone hanno molto spazio per esprimersi e scegliere.")

    if scores["B"] <= 1:
        messages.append("Il clima sociale è pesante e molte persone stanno male.")
    elif scores["B"] >= 4:
        messages.append("La qualità della vita è alta e il clima sociale è abbastanza positivo.")

    if not messages:
        messages.append("Questa società ha elementi positivi, ma anche limiti importanti da discutere.")

    return messages


def render_interpretation_block(scores: dict) -> None:
    """Mostra il commento finale automatico."""
    messages = interpret_scores(scores)
    st.markdown("### Interpretazione")
    for msg in messages:
        st.write(f"- {msg}")


def render_result_panel(result: dict, group_label: str) -> None:
    """
    Pannello finale completo:
    tabella contributi, metriche, barre, emoji, interpretazione.
    """
    st.subheader(group_label)
    render_contribution_table(result)

    st.markdown("### Esiti sociali")
    render_dimension_badges(result["final_scores"])
    render_score_bars(result["final_scores"])
    render_emoji_result(result["total_score"], result["emoji"])
    render_interpretation_block(result["final_scores"])


def centered_button(label: str, key: str | None = None, use_container_width: bool = True) -> bool:
    """
    Bottone centrato visivamente usando 3 colonne.
    """
    left, center, right = st.columns([1, 2, 1])
    with center:
        return st.button(label, key=key, use_container_width=use_container_width)


def render_phase_header(step_title: str, instructions: str | None = None) -> None:
    """Header standard per le fasi."""
    st.header(step_title)
    if instructions:
        st.write(instructions)
