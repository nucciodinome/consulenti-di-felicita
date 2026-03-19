"""
Componenti UI per la visualizzazione e selezione delle carte.
Adattato per il gioco "Consulenti di Felicità".
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st
from PIL import Image


CARD_TYPE_STYLES = {
    "red": {
        "label": "Problema",
        "emoji": "🔴",
        "bg": "#fde2e2",
        "border": "#d9534f",
        "badge_bg": "#d9534f",
        "badge_fg": "#ffffff",
    },
    "green": {
        "label": "Risorsa",
        "emoji": "🟢",
        "bg": "#e6f4ea",
        "border": "#2e8b57",
        "badge_bg": "#2e8b57",
        "badge_fg": "#ffffff",
    },
    "yellow": {
        "label": "Fattore ambiguo",
        "emoji": "🟡",
        "bg": "#fff8db",
        "border": "#c9a227",
        "badge_bg": "#c9a227",
        "badge_fg": "#1f1f1f",
    },
}


def _safe_image_path(path: str) -> str | None:
    """Restituisce il path solo se il file esiste."""
    if not path:
        return None
    p = Path(path)
    return str(p) if p.exists() else None


@st.cache_data(show_spinner=False)
def load_card_image(path: str) -> Image.Image | None:
    """
    Carica e cachea un'immagine carta.
    Restituisce None se il file non esiste o non è leggibile.
    """
    safe_path = _safe_image_path(path)
    if safe_path is None:
        return None

    try:
        with Image.open(safe_path) as img:
            return img.copy()
    except Exception:
        return None


def inject_card_ui_css() -> None:
    """CSS globale leggero per migliorare la resa delle card."""
    st.markdown(
        """
        <style>
        .cdf-card-shell {
            border-radius: 18px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .cdf-card-title {
            font-size: 1rem;
            font-weight: 700;
            margin-top: 0.4rem;
            margin-bottom: 0.25rem;
            line-height: 1.2;
            min-height: 2.4em;
        }
        .cdf-card-badges {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            margin-bottom: 0.45rem;
        }
        .cdf-card-badge {
            display: inline-block;
            padding: 0.15rem 0.5rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .cdf-card-desc {
            font-size: 0.90rem;
            line-height: 1.25;
            min-height: 4.3em;
            margin-bottom: 0.4rem;
        }
        .cdf-missing-image {
            height: 160px;
            border-radius: 12px;
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #666;
            font-size: 0.95rem;
            border: 1px dashed #bbb;
            margin-bottom: 8px;
        }
        .cdf-counter {
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_selection_counter(label: str, selected_count: int, max_count: int) -> None:
    st.markdown(
        f"<div class='cdf-counter'>{label}: {selected_count}/{max_count}</div>",
        unsafe_allow_html=True,
    )


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
    img = load_card_image(card_data.get("image", ""))

    border_width = "4px" if selected else "2px"
    opacity = "0.45" if blocked else "1.0"
    shadow = "0 0 0 4px rgba(0, 123, 255, 0.18)" if selected else "0 1px 2px rgba(0,0,0,0.04)"

    st.markdown(
        f"""
        <div class="cdf-card-shell" style="
            border: {border_width} solid {style['border']};
            background: {style['bg']};
            opacity: {opacity};
            box-shadow: {shadow};
        ">
        """,
        unsafe_allow_html=True,
    )

    if img is not None:
        st.image(img, width="stretch")
    else:
        st.markdown(
            "<div class='cdf-missing-image'>immagine non trovata</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        f"<div class='cdf-card-title'>{card_name}</div>",
        unsafe_allow_html=True,
    )

    badges_html = [
        (
            f"<span class='cdf-card-badge' "
            f"style='background:{style['badge_bg']}; color:{style['badge_fg']};'>"
            f"{style['emoji']} {style['label']}</span>"
        )
    ]

    if selected:
        badges_html.append(
            "<span class='cdf-card-badge' style='background:#0d6efd; color:white;'>Selezionata</span>"
        )
    if blocked:
        badges_html.append(
            "<span class='cdf-card-badge' style='background:#6c757d; color:white;'>Bloccata</span>"
        )

    st.markdown(
        f"<div class='cdf-card-badges'>{''.join(badges_html)}</div>",
        unsafe_allow_html=True,
    )

    if not compact:
        st.markdown(
            f"<div class='cdf-card-desc'>{card_data.get('description', '')}</div>",
            unsafe_allow_html=True,
        )

    if show_scores:
        c1, c2, c3 = st.columns(3)
        c1.metric("E", card_data.get("E", 0))
        c2.metric("L", card_data.get("L", 0))
        c3.metric("B", card_data.get("B", 0))

    if blocked:
        button_label = "Non disponibile"
    elif selected:
        button_label = "Deseleziona"
    else:
        button_label = "Scegli"

    clicked = st.button(
        button_label,
        key=button_key,
        disabled=blocked,
        width="stretch",
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
    show_scores: bool = False,
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
        for col_idx in range(columns):
            with cols[col_idx]:
                if col_idx < len(row_cards):
                    card_name = row_cards[col_idx]
                    clicked = render_card_tile(
                        card_name=card_name,
                        card_data=cards_dict[card_name],
                        selected=card_name in selected_cards,
                        blocked=card_name in blocked_cards,
                        button_key=f"{key_prefix}_{row_idx}_{col_idx}_{card_name}",
                        compact=compact,
                        show_scores=show_scores,
                    )
                    if clicked:
                        clicked_card = card_name
                else:
                    st.empty()

    return clicked_card


def render_card_section(
    title: str,
    card_names: list[str],
    cards_dict: dict,
    selected_cards: list[str] | None = None,
    blocked_cards: list[str] | None = None,
    columns: int = 4,
    key_prefix: str = "section",
    compact: bool = False,
    show_scores: bool = False,
    counter_label: str | None = None,
    counter_selected: int | None = None,
    counter_max: int | None = None,
) -> str | None:
    """
    Sezione completa con titolo + contatore opzionale + griglia.
    """
    st.markdown(f"## {title}")

    if counter_label is not None and counter_selected is not None and counter_max is not None:
        render_selection_counter(counter_label, counter_selected, counter_max)

    return render_card_grid(
        card_names=card_names,
        cards_dict=cards_dict,
        selected_cards=selected_cards,
        blocked_cards=blocked_cards,
        columns=columns,
        key_prefix=key_prefix,
        compact=compact,
        show_scores=show_scores,
    )


def toggle_single_select(current_value: str | None, clicked_card: str) -> str:
    """
    Selezione singola.
    Se clicchi una carta già attiva, resta attiva.
    """
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
