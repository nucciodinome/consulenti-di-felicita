"""
Motore di calcolo del gioco.

Funzioni principali:
- clamp_score
- get_emoji
- yellow_matrix_combo
- compute_society
"""

from itertools import combinations
from typing import Any

from core.cards import (
    ALL_CARDS,
    BASE_SCORE,
    GREEN_CARDS,
    RED_CARDS,
    YELLOW_CARDS,
)
from core.combos import (
    EXTRA_COMBOS,
    YELLOW_COMBO_B,
    YELLOW_COMBO_E,
    YELLOW_COMBO_L,
    YELLOW_INDEX,
)


def clamp_score(value: int) -> int:
    """Limita il punteggio finale della singola dimensione tra 0 e 5."""
    return max(0, min(5, value))


def get_emoji(total_score: int) -> str:
    """
    Mappa la somma finale 0-15 a un'emoji.
    """
    if total_score <= 3:
        return "😞"
    if total_score <= 6:
        return "🙁"
    if total_score <= 9:
        return "😐"
    if total_score <= 12:
        return "🙂"
    if total_score <= 14:
        return "😀"
    return "🤩"


def yellow_matrix_combo(card_a: str, card_b: str) -> dict[str, Any]:
    """
    Restituisce l'effetto combo tra due carte gialle.
    Le matrici sono simmetriche, quindi basta leggere [i][j].
    """
    i = YELLOW_INDEX[card_a]
    j = YELLOW_INDEX[card_b]
    return {
        "E": YELLOW_COMBO_E[i][j],
        "L": YELLOW_COMBO_L[i][j],
        "B": YELLOW_COMBO_B[i][j],
        "label": f"{card_a} + {card_b}",
    }


def validate_solution_cards(solution_cards: list[str]) -> None:
    """
    Verifica che le carte soluzione siano esattamente 3
    e che includano almeno una verde e una gialla.
    """
    if len(solution_cards) != 3:
        raise ValueError("Servono esattamente 3 carte soluzione.")

    green_count = sum(1 for c in solution_cards if c in GREEN_CARDS)
    yellow_count = sum(1 for c in solution_cards if c in YELLOW_CARDS)

    if green_count < 1 or yellow_count < 1:
        raise ValueError(
            "Tra le 3 carte soluzione deve esserci almeno 1 carta verde e almeno 1 carta gialla."
        )

    unknown_cards = [c for c in solution_cards if c not in ALL_CARDS]
    if unknown_cards:
        raise ValueError(f"Carte soluzione non valide: {unknown_cards}")


def compute_society(red_card: str, solution_cards: list[str]) -> dict[str, Any]:
    """
    Calcola gli esiti finali della società.

    Parametri:
    - red_card: nome di una carta rossa
    - solution_cards: lista di 3 carte tra verdi e gialle

    Restituisce:
    - final_scores: dict con E, L, B
    - total_score: int (0-15)
    - emoji: str
    - contribution_rows: lista di righe per la tabella finale
    """
    if red_card not in RED_CARDS:
        raise ValueError("La carta rossa non è valida.")

    validate_solution_cards(solution_cards)

    running_scores = BASE_SCORE.copy()
    contribution_rows: list[dict[str, Any]] = []

    contribution_rows.append({
        "Voce": "Base",
        "E": BASE_SCORE["E"],
        "L": BASE_SCORE["L"],
        "B": BASE_SCORE["B"],
    })

    # Carta rossa
    red = RED_CARDS[red_card]
    running_scores["E"] += red["E"]
    running_scores["L"] += red["L"]
    running_scores["B"] += red["B"]

    contribution_rows.append({
        "Voce": f"Problema: {red_card}",
        "E": red["E"],
        "L": red["L"],
        "B": red["B"],
    })

    # Carte soluzione
    for card in solution_cards:
        data = ALL_CARDS[card]
        running_scores["E"] += data["E"]
        running_scores["L"] += data["L"]
        running_scores["B"] += data["B"]

        contribution_rows.append({
            "Voce": f"Carta: {card}",
            "E": data["E"],
            "L": data["L"],
            "B": data["B"],
        })

    # Combo
    combo_rows: list[dict[str, Any]] = []
    for card_a, card_b in combinations(solution_cards, 2):
        pair = tuple(sorted((card_a, card_b)))

        # Gialla + gialla
        if card_a in YELLOW_CARDS and card_b in YELLOW_CARDS:
            combo = yellow_matrix_combo(card_a, card_b)
            if combo["E"] != 0 or combo["L"] != 0 or combo["B"] != 0:
                running_scores["E"] += combo["E"]
                running_scores["L"] += combo["L"]
                running_scores["B"] += combo["B"]

                combo_rows.append({
                    "Voce": f"Combo: {combo['label']}",
                    "E": combo["E"],
                    "L": combo["L"],
                    "B": combo["B"],
                })

        # Verde + verde oppure verde + gialla
        elif pair in EXTRA_COMBOS:
            combo = EXTRA_COMBOS[pair]
            if combo["E"] != 0 or combo["L"] != 0 or combo["B"] != 0:
                running_scores["E"] += combo["E"]
                running_scores["L"] += combo["L"]
                running_scores["B"] += combo["B"]

                combo_rows.append({
                    "Voce": f"Combo: {combo['label']}",
                    "E": combo["E"],
                    "L": combo["L"],
                    "B": combo["B"],
                })

    contribution_rows.extend(combo_rows)

    final_scores = {
        "E": clamp_score(running_scores["E"]),
        "L": clamp_score(running_scores["L"]),
        "B": clamp_score(running_scores["B"]),
    }

    total_score = final_scores["E"] + final_scores["L"] + final_scores["B"]
    emoji = get_emoji(total_score)

    contribution_rows.append({
        "Voce": "Totale finale",
        "E": final_scores["E"],
        "L": final_scores["L"],
        "B": final_scores["B"],
    })

    return {
        "final_scores": final_scores,
        "total_score": total_score,
        "emoji": emoji,
        "contribution_rows": contribution_rows,
    }
