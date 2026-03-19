"""
Gestione dello stato di sessione per il gioco "Consulenti di Felicità".
"""

import streamlit as st

PHASES = [
    "group1_select_all",
    "group2_select_all",
    "group1_problem",
    "group2_problem",
    "group1_select_solutions",
    "group2_select_solutions",
    "results",
]

DEFAULT_STATE = {
    "phase": "group1_select_all",

    # Gruppo 1
    "group1_selected_red": None,
    "group1_selected_nonred": [],
    "group1_solution_cards": [],
    "group1_result": None,
    "group1_show_result": False,

    # Gruppo 2
    "group2_selected_red": None,
    "group2_selected_nonred": [],
    "group2_solution_cards": [],
    "group2_result": None,
    "group2_show_result": False,

    # Revisione
    "revision_mode": False,
    "revision_target_group": None,
}


def init_session_state() -> None:
    """Inizializza le chiavi principali della sessione."""
    for key, value in DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_game() -> None:
    """Reset completo del gioco."""
    for key, value in DEFAULT_STATE.items():
        st.session_state[key] = value


def reset_results_only() -> None:
    """Azzera solo i risultati calcolati, mantenendo le carte scelte."""
    st.session_state["group1_result"] = None
    st.session_state["group2_result"] = None
    st.session_state["group1_show_result"] = False
    st.session_state["group2_show_result"] = False


def set_phase(phase: str) -> None:
    """Imposta direttamente la fase corrente."""
    if phase not in PHASES:
        raise ValueError(f"Fase non valida: {phase}")
    st.session_state["phase"] = phase


def next_phase() -> None:
    """Passa alla fase successiva."""
    current = st.session_state["phase"]
    idx = PHASES.index(current)
    if idx < len(PHASES) - 1:
        st.session_state["phase"] = PHASES[idx + 1]


def previous_phase() -> None:
    """Torna alla fase precedente."""
    current = st.session_state["phase"]
    idx = PHASES.index(current)
    if idx > 0:
        st.session_state["phase"] = PHASES[idx - 1]


def start_revision(group_name: str) -> None:
    """
    Avvia la revisione per un gruppo.
    Riporta il gioco alla fase di scelta soluzioni del gruppo selezionato.
    """
    if group_name not in ["group1", "group2"]:
        raise ValueError("group_name deve essere 'group1' o 'group2'")

    st.session_state["revision_mode"] = True
    st.session_state["revision_target_group"] = group_name

    if group_name == "group1":
        st.session_state["group1_show_result"] = False
        st.session_state["group1_result"] = None
        st.session_state["phase"] = "group1_select_solutions"
    else:
        st.session_state["group2_show_result"] = False
        st.session_state["group2_result"] = None
        st.session_state["phase"] = "group2_select_solutions"


def finish_revision() -> None:
    """Chiude lo stato revisione."""
    st.session_state["revision_mode"] = False
    st.session_state["revision_target_group"] = None


def get_group_state(group_name: str) -> dict:
    """Restituisce i dati principali del gruppo richiesto."""
    if group_name == "group1":
        return {
            "selected_red": st.session_state["group1_selected_red"],
            "selected_nonred": st.session_state["group1_selected_nonred"],
            "solution_cards": st.session_state["group1_solution_cards"],
            "result": st.session_state["group1_result"],
            "show_result": st.session_state["group1_show_result"],
        }
    if group_name == "group2":
        return {
            "selected_red": st.session_state["group2_selected_red"],
            "selected_nonred": st.session_state["group2_selected_nonred"],
            "solution_cards": st.session_state["group2_solution_cards"],
            "result": st.session_state["group2_result"],
            "show_result": st.session_state["group2_show_result"],
        }
    raise ValueError("group_name deve essere 'group1' o 'group2'")
