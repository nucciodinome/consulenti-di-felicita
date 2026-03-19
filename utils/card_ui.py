"""
Componenti UI per la visualizzazione e selezione delle carte.
"""

from __future__ import annotations

from pathlib import Path
import streamlit as st


CARD_TYPE_STYLES = {
    "red": {
        "label": "Problema",
        "emoji": "🔴",
        "bg": "#fde2e2",
        "border": "#d9534f",
    },
    "green": {
        "label": "Risorsa",
        "emoji": "🟢",
        "bg": "#e6f4ea",
        "border": "#2e8b57",
    },
    "yellow": {
        "label": "Fattore ambiguo",
        "emoji": "🟡",
        "bg": "#fff8db",
        "border": "#c9a227",
    },
}


def _safe_image(path: str) -> str | None:
    """Restituisce il path solo se il file esiste."""
    if not path:
        return None
    p = Path(path)
    return str(p) if p.exists() else None


def render_card_tile(
    card_name: str,
    card_data: dict,
    selected: bool = False,
    blocked: bool = False,
    button_key: str | None = None,
    show_scores: bool = False,
    compact: bool = False,
) -> bool:
    """
    Renderizza una singola carta con immagine e bottone.
    Ritorna True se il bottone è stato cliccato.
    """
    card_type = card_data.get("type", "")
    style = CARD_TYPE_STYLES.get(card_type, CARD_TYPE_STYLES["yellow"])
    image_path = _safe_image(card_data.get("image", ""))

    border_width = "4px" if selected else "2px"
    opacity = "0.45" if blocked else "1.0"
    outline = "box-shadow: 0 0 0 4px rgba(0, 123, 255, 0.25);" if selected else ""

    container_style = f"""
        border: {border_width} solid {style['border']};
        border-radius: 16px;
        padding: 10px;
        background: {style['bg']};
        opacity: {opacity};
        min-height: 100%;
        {outline}
    """

    with st.container():
        st.markdown(f"<div style='{container_style}'>", unsafe_allow_html=True)

        if image_path:
            st.image(image_path, use_container_width=True)
        else:
            st.markdown(
                f"""
                <div style="
                    height: 170px;
                    border-radius: 12px;
                    background: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #666;
                    font-size: 0.95rem;
                    border: 1px dashed #bbb;
                ">
                    immagine non trovata
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(f"**{card_name}**")
        st.caption(f"{style['emoji']} {style['label']}")

        if not compact:
            st.write(card_data.get("description", ""))

        if show_scores:
            c1, c2, c3 = st.columns(3)
            c1.metric("E", card_data.get("E", 0))
            c2.metric("L", card_data.get("L", 0))
            c3.metric("B", card_data.get("B", 0))

        button_label = "Selezionata" if selected else "Scegli"
        if blocked:
            button_label = "Non disponibile"

        clicked = st.button(
            button_label,
            key=button_key,
            disabled=blocked,
            use_container_width=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    return clicked


def render_card_grid(
    card_names: list[str],
    cards_dict: dict,
    selected_cards: list[str] | None = None,
    blocked_cards: list[str] | None = None,
    columns: int = 4,
    key_prefix: str = "grid",
    compact: bool = False,
) -> str | None:
    """
    Renderizza una griglia di carte.
    Se una carta viene cliccata, restituisce il nome della carta cliccata.
    """
    selected_cards = selected_cards or []
    blocked_cards = blocked_cards or []

    clicked_card = None
    rows = [card_names[i:i + columns] for i in range(0, len(card_names), columns)]

    for row_idx, row_cards in enumerate(rows):
        cols = st.columns(columns)
        for col_idx, card_name in enumerate(row_cards):
            with cols[col_idx]:
                clicked = render_card_tile(
                    card_name=card_name,
                    card_data=cards_dict[card_name],
                    selected=card_name in selected_cards,
                    blocked=card_name in blocked_cards,
                    button_key=f"{key_prefix}_{row_idx}_{col_idx}_{card_name}",
                    compact=compact,
                )
                if clicked:
                    clicked_card = card_name

    return clicked_card


def toggle_single_select(current_value: str | None, clicked_card: str) -> str:
    """Selezione singola. Se clicchi una carta già attiva, resta attiva."""
    return clicked_card if clicked_card else current_value


def toggle_multi_select(
    current_values: list[str],
    clicked_card: str,
    max_selections: int,
) -> list[str]:
    """
    Toggle multi-select.
    - se la carta è già selezionata, la deseleziona
    - se non è selezionata e c'è spazio, la aggiunge
    - se non c'è spazio, non fa nulla
    """
    values = list(current_values)

    if clicked_card in values:
        values.remove(clicked_card)
        return values

    if len(values) < max_selections:
        values.append(clicked_card)

    return values
