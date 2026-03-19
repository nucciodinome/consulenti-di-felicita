import streamlit as st

from core.cards import (
    RED_ORDER,
    NON_RED_ORDER,
    RED_CARDS,
    GREEN_CARDS,
    YELLOW_CARDS,
)
from core.scoring import compute_society
from utils.session import (
    init_session_state,
    reset_game,
    next_phase,
    previous_phase,
    start_revision,
    finish_revision,
)
from utils.layout import (
    render_contribution_table,
    render_result_panel,
    render_phase_header,
    info_box,
    warning_box,
)
from utils.card_ui import (
    inject_card_ui_css,
    render_card_section,
    toggle_single_select,
    toggle_multi_select,
)

st.set_page_config(
    page_title="Consulenti di Felicità",
    layout="wide",
)

init_session_state()
inject_card_ui_css()

st.title("Consulenti di Felicità")
st.caption("Un gioco per immaginare società più giuste, libere e felici")


# =========================
# Helpers logici
# =========================

def get_blocked_red_cards_for_group2() -> list[str]:
    blocked = []
    if st.session_state["group1_selected_red"]:
        blocked.append(st.session_state["group1_selected_red"])
    return blocked


def get_blocked_nonred_cards_for_group2() -> list[str]:
    return list(st.session_state["group1_selected_nonred"])


def validate_full_selection(red_card: str | None, nonred_cards: list[str]) -> tuple[bool, str]:
    if red_card is None:
        return False, "Devi scegliere una carta rossa."

    if len(nonred_cards) != 4:
        return False, "Devi scegliere esattamente 4 carte non rosse."

    green_count = sum(1 for c in nonred_cards if c in GREEN_CARDS)
    yellow_count = sum(1 for c in nonred_cards if c in YELLOW_CARDS)

    if green_count < 2 or yellow_count < 2:
        return False, "Le 4 carte non rosse devono includere almeno 2 verdi e 2 gialle."

    return True, ""


def validate_solution_selection(solution_cards: list[str]) -> tuple[bool, str]:
    if len(solution_cards) != 3:
        return False, "Devi scegliere esattamente 3 carte soluzione."

    green_count = sum(1 for c in solution_cards if c in GREEN_CARDS)
    yellow_count = sum(1 for c in solution_cards if c in YELLOW_CARDS)

    if green_count < 1 or yellow_count < 1:
        return False, "Le 3 carte soluzione devono includere almeno 1 verde e 1 gialla."

    return True, ""


def clear_group_result(group_name: str) -> None:
    if group_name == "group1":
        st.session_state["group1_result"] = None
        st.session_state["group1_show_result"] = False
    elif group_name == "group2":
        st.session_state["group2_result"] = None
        st.session_state["group2_show_result"] = False


# =========================
# Sidebar
# =========================

with st.sidebar:
    st.markdown("### Controlli")
    st.write(f"**Fase corrente:** `{st.session_state['phase']}`")

    if st.button("🔄 Ricomincia da capo", use_container_width=True):
        reset_game()
        st.rerun()

    st.markdown("---")
    st.markdown("### Stato sintetico")

    st.write("**Gruppo 1**")
    st.write("Rossa:", st.session_state["group1_selected_red"])
    st.write("4 carte:", st.session_state["group1_selected_nonred"])
    st.write("Soluzioni:", st.session_state["group1_solution_cards"])

    st.write("**Gruppo 2**")
    st.write("Rossa:", st.session_state["group2_selected_red"])
    st.write("4 carte:", st.session_state["group2_selected_nonred"])
    st.write("Soluzioni:", st.session_state["group2_solution_cards"])


# =========================
# FASE 1 - Gruppo 1 sceglie tutto
# =========================

if st.session_state["phase"] == "group1_select_all":
    render_phase_header(
        "Fase 1 - Gruppo 1: scegli le carte",
        "Scegliete 1 carta rossa e 4 carte non rosse. Le 4 carte non rosse devono includere almeno 2 verdi e 2 gialle.",
    )
    info_box("In questa fase il Gruppo 1 costruisce il proprio set iniziale di 5 carte.")

    clicked_red = render_card_section(
        title="Carte rosse",
        card_names=RED_ORDER,
        cards_dict=RED_CARDS,
        selected_cards=[st.session_state["group1_selected_red"]] if st.session_state["group1_selected_red"] else [],
        blocked_cards=[],
        columns=4,
        key_prefix="g1_red",
        compact=True,
        counter_label="Carta rossa scelta",
        counter_selected=1 if st.session_state["group1_selected_red"] else 0,
        counter_max=1,
    )
    if clicked_red:
        st.session_state["group1_selected_red"] = toggle_single_select(
            st.session_state["group1_selected_red"],
            clicked_red,
        )
        clear_group_result("group1")
        st.rerun()

    nonred_cards_dict = {**GREEN_CARDS, **YELLOW_CARDS}

    clicked_nonred = render_card_section(
        title="Carte verdi e gialle",
        card_names=NON_RED_ORDER,
        cards_dict=nonred_cards_dict,
        selected_cards=st.session_state["group1_selected_nonred"],
        blocked_cards=[],
        columns=4,
        key_prefix="g1_nonred",
        compact=True,
        counter_label="Carte non rosse selezionate",
        counter_selected=len(st.session_state["group1_selected_nonred"]),
        counter_max=4,
    )
    if clicked_nonred:
        st.session_state["group1_selected_nonred"] = toggle_multi_select(
            st.session_state["group1_selected_nonred"],
            clicked_nonred,
            max_selections=4,
        )
        clear_group_result("group1")
        st.rerun()

    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("Salva Gruppo 1 e continua", use_container_width=True):
            is_valid, msg = validate_full_selection(
                st.session_state["group1_selected_red"],
                st.session_state["group1_selected_nonred"],
            )
            if not is_valid:
                st.error(msg)
            else:
                st.session_state["group1_solution_cards"] = []
                clear_group_result("group1")
                next_phase()
                st.rerun()


# =========================
# FASE 2 - Gruppo 2 sceglie tutto
# =========================

elif st.session_state["phase"] == "group2_select_all":
    render_phase_header(
        "Fase 2 - Gruppo 2: scegli le carte",
        "Scegliete 1 carta rossa e 4 carte non rosse. Le carte già prese dal Gruppo 1 non sono disponibili.",
    )
    warning_box("Le carte già scelte dal Gruppo 1 sono bloccate per il Gruppo 2.")

    blocked_red = get_blocked_red_cards_for_group2()
    blocked_nonred = get_blocked_nonred_cards_for_group2()

    clicked_red = render_card_section(
        title="Carte rosse",
        card_names=RED_ORDER,
        cards_dict=RED_CARDS,
        selected_cards=[st.session_state["group2_selected_red"]] if st.session_state["group2_selected_red"] else [],
        blocked_cards=blocked_red,
        columns=4,
        key_prefix="g2_red",
        compact=True,
        counter_label="Carta rossa scelta",
        counter_selected=1 if st.session_state["group2_selected_red"] else 0,
        counter_max=1,
    )
    if clicked_red and clicked_red not in blocked_red:
        st.session_state["group2_selected_red"] = toggle_single_select(
            st.session_state["group2_selected_red"],
            clicked_red,
        )
        clear_group_result("group2")
        st.rerun()

    nonred_cards_dict = {**GREEN_CARDS, **YELLOW_CARDS}

    clicked_nonred = render_card_section(
        title="Carte verdi e gialle",
        card_names=NON_RED_ORDER,
        cards_dict=nonred_cards_dict,
        selected_cards=st.session_state["group2_selected_nonred"],
        blocked_cards=blocked_nonred,
        columns=4,
        key_prefix="g2_nonred",
        compact=True,
        counter_label="Carte non rosse selezionate",
        counter_selected=len(st.session_state["group2_selected_nonred"]),
        counter_max=4,
    )
    if clicked_nonred and clicked_nonred not in blocked_nonred:
        st.session_state["group2_selected_nonred"] = toggle_multi_select(
            st.session_state["group2_selected_nonred"],
            clicked_nonred,
            max_selections=4,
        )
        clear_group_result("group2")
        st.rerun()

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("⬅️ Indietro", use_container_width=True):
            previous_phase()
            st.rerun()

    with col2:
        if st.button("Salva Gruppo 2 e continua", use_container_width=True):
            is_valid, msg = validate_full_selection(
                st.session_state["group2_selected_red"],
                st.session_state["group2_selected_nonred"],
            )
            if not is_valid:
                st.error(msg)
            else:
                st.session_state["group2_solution_cards"] = []
                clear_group_result("group2")
                next_phase()
                st.rerun()


# =========================
# FASE 3 - Problema Gruppo 1
# =========================

elif st.session_state["phase"] == "group1_problem":
    render_phase_header(
        "Fase 3 - Il problema del Gruppo 1",
        "Osservate il problema scelto e discutetene gli effetti iniziali sulla società.",
    )

    red_card = st.session_state["group1_selected_red"]
    red_data = RED_CARDS[red_card]

    st.subheader(red_card)
    if red_data.get("image"):
        st.image(red_data["image"], width=400)
    st.write(red_data["description"])

    st.markdown("### Impatto iniziale")
    st.write(f"- Equità: {red_data['E']}")
    st.write(f"- Libertà: {red_data['L']}")
    st.write(f"- Benessere: {red_data['B']}")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("⬅️ Indietro", use_container_width=True):
            previous_phase()
            st.rerun()

    with col2:
        if st.button("Continua", use_container_width=True):
            next_phase()
            st.rerun()


# =========================
# FASE 4 - Problema Gruppo 2
# =========================

elif st.session_state["phase"] == "group2_problem":
    render_phase_header(
        "Fase 4 - Il problema del Gruppo 2",
        "Osservate il problema scelto e discutetene gli effetti iniziali sulla società.",
    )

    red_card = st.session_state["group2_selected_red"]
    red_data = RED_CARDS[red_card]

    st.subheader(red_card)
    if red_data.get("image"):
        st.image(red_data["image"], width=400)
    st.write(red_data["description"])

    st.markdown("### Impatto iniziale")
    st.write(f"- Equità: {red_data['E']}")
    st.write(f"- Libertà: {red_data['L']}")
    st.write(f"- Benessere: {red_data['B']}")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("⬅️ Indietro", use_container_width=True):
            previous_phase()
            st.rerun()

    with col2:
        if st.button("Continua", use_container_width=True):
            next_phase()
            st.rerun()


# =========================
# FASE 5 - Soluzioni Gruppo 1
# =========================

elif st.session_state["phase"] == "group1_select_solutions":
    render_phase_header(
        "Fase 5 - Gruppo 1: scegliete le 3 carte soluzione",
        "Scegliete 3 carte tra le 4 non rosse già selezionate. Le 3 carte devono includere almeno 1 verde e 1 gialla.",
    )

    if st.session_state["revision_mode"] and st.session_state["revision_target_group"] == "group1":
        info_box("Modalità revisione attiva: il Gruppo 1 può modificare le sue 3 carte soluzione.")

    available_cards = st.session_state["group1_selected_nonred"]
    cards_dict = {name: ({**GREEN_CARDS, **YELLOW_CARDS}[name]) for name in available_cards}

    clicked_solution = render_card_section(
        title="Carte soluzione del Gruppo 1",
        card_names=available_cards,
        cards_dict=cards_dict,
        selected_cards=st.session_state["group1_solution_cards"],
        blocked_cards=[],
        columns=4,
        key_prefix="g1_sol",
        compact=True,
        counter_label="Soluzioni selezionate",
        counter_selected=len(st.session_state["group1_solution_cards"]),
        counter_max=3,
    )
    if clicked_solution:
        st.session_state["group1_solution_cards"] = toggle_multi_select(
            st.session_state["group1_solution_cards"],
            clicked_solution,
            max_selections=3,
        )
        clear_group_result("group1")
        st.rerun()

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("⬅️ Indietro", use_container_width=True):
            previous_phase()
            st.rerun()

    with col2:
        if st.button("Salva soluzioni Gruppo 1 e continua", use_container_width=True):
            is_valid, msg = validate_solution_selection(st.session_state["group1_solution_cards"])
            if not is_valid:
                st.error(msg)
            else:
                clear_group_result("group1")

                if st.session_state["revision_mode"] and st.session_state["revision_target_group"] == "group1":
                    finish_revision()
                    st.session_state["phase"] = "results"
                else:
                    next_phase()

                st.rerun()


# =========================
# FASE 6 - Soluzioni Gruppo 2
# =========================

elif st.session_state["phase"] == "group2_select_solutions":
    render_phase_header(
        "Fase 6 - Gruppo 2: scegliete le 3 carte soluzione",
        "Scegliete 3 carte tra le 4 non rosse già selezionate. Le 3 carte devono includere almeno 1 verde e 1 gialla.",
    )

    if st.session_state["revision_mode"] and st.session_state["revision_target_group"] == "group2":
        info_box("Modalità revisione attiva: il Gruppo 2 può modificare le sue 3 carte soluzione.")

    available_cards = st.session_state["group2_selected_nonred"]
    cards_dict = {name: ({**GREEN_CARDS, **YELLOW_CARDS}[name]) for name in available_cards}

    clicked_solution = render_card_section(
        title="Carte soluzione del Gruppo 2",
        card_names=available_cards,
        cards_dict=cards_dict,
        selected_cards=st.session_state["group2_solution_cards"],
        blocked_cards=[],
        columns=4,
        key_prefix="g2_sol",
        compact=True,
        counter_label="Soluzioni selezionate",
        counter_selected=len(st.session_state["group2_solution_cards"]),
        counter_max=3,
    )
    if clicked_solution:
        st.session_state["group2_solution_cards"] = toggle_multi_select(
            st.session_state["group2_solution_cards"],
            clicked_solution,
            max_selections=3,
        )
        clear_group_result("group2")
        st.rerun()

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("⬅️ Indietro", use_container_width=True):
            previous_phase()
            st.rerun()

    with col2:
        if st.button("Salva soluzioni Gruppo 2 e vai ai risultati", use_container_width=True):
            is_valid, msg = validate_solution_selection(st.session_state["group2_solution_cards"])
            if not is_valid:
                st.error(msg)
            else:
                clear_group_result("group2")

                if st.session_state["revision_mode"] and st.session_state["revision_target_group"] == "group2":
                    finish_revision()
                    st.session_state["phase"] = "results"
                else:
                    next_phase()

                st.rerun()


# =========================
# FASE 7 - RISULTATI
# =========================

elif st.session_state["phase"] == "results":
    render_phase_header(
        "Fase 7 - Esiti sociali finali",
        "Osservate prima come si costruisce il risultato. Poi premete il pulsante per mostrare grafico, emoji e interpretazione.",
    )

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Gruppo 1")

        if st.session_state["group1_result"] is None:
            try:
                st.session_state["group1_result"] = compute_society(
                    red_card=st.session_state["group1_selected_red"],
                    solution_cards=st.session_state["group1_solution_cards"],
                )
            except Exception as e:
                st.error(f"Errore nel calcolo del Gruppo 1: {e}")

        if st.session_state["group1_result"] is not None:
            render_contribution_table(st.session_state["group1_result"])

            if not st.session_state["group1_show_result"]:
                if st.button("Calcola esiti Gruppo 1", key="show_g1", use_container_width=True):
                    st.session_state["group1_show_result"] = True
                    st.rerun()
            else:
                render_result_panel(st.session_state["group1_result"], "Gruppo 1")

                if st.button("Rivedi le soluzioni del Gruppo 1", key="revise_g1", use_container_width=True):
                    start_revision("group1")
                    st.rerun()

    with col_right:
        st.subheader("Gruppo 2")

        if st.session_state["group2_result"] is None:
            try:
                st.session_state["group2_result"] = compute_society(
                    red_card=st.session_state["group2_selected_red"],
                    solution_cards=st.session_state["group2_solution_cards"],
                )
            except Exception as e:
                st.error(f"Errore nel calcolo del Gruppo 2: {e}")

        if st.session_state["group2_result"] is not None:
            render_contribution_table(st.session_state["group2_result"])

            if not st.session_state["group2_show_result"]:
                if st.button("Calcola esiti Gruppo 2", key="show_g2", use_container_width=True):
                    st.session_state["group2_show_result"] = True
                    st.rerun()
            else:
                render_result_panel(st.session_state["group2_result"], "Gruppo 2")

                if st.button("Rivedi le soluzioni del Gruppo 2", key="revise_g2", use_container_width=True):
                    start_revision("group2")
                    st.rerun()

    st.markdown("---")
    bottom_col1, bottom_col2 = st.columns([1, 1])

    with bottom_col1:
        if st.button("⬅️ Torna alla scelta soluzioni Gruppo 2", use_container_width=True):
            st.session_state["phase"] = "group2_select_solutions"
            st.rerun()

    with bottom_col2:
        if st.button("🔄 Nuova partita", use_container_width=True):
            reset_game()
            st.rerun()
