"""
Definizione delle combo tra carte.

Contiene:
- matrici 8x8 per le combo tra carte gialle
- combo extra per coppie verdi-verdi e verdi-gialle
"""

from core.cards import YELLOW_ORDER

YELLOW_INDEX = {name: i for i, name in enumerate(YELLOW_ORDER)}

# Matrice combo gialle: Equità
YELLOW_COMBO_E = [
    # M   T   C   S   SP  A   R   RS
    [ 0, -1, -1,  0, -2, -2,  0, -2],  # Meritocrazia
    [-1,  0,  0,  0,  0, -1, -1, -2],  # Tradizione
    [-1,  0,  0,  0, -1, -1,  0, -1],  # Competizione
    [ 0,  0,  0,  0,  0, -1, -1, -2],  # Sicurezza e controllo
    [-2,  0, -1,  0,  0, -2,  0, -2],  # Successo e performance
    [-2, -1, -1, -1, -2,  0,  0, -2],  # Apparenza e immagine
    [ 0, -1,  0, -1,  0,  0,  0, -2],  # Regole rigide
    [-2, -2, -1, -2, -2, -2, -2,  0],  # Ruoli sociali tradizionali
]

# Matrice combo gialle: Libertà
YELLOW_COMBO_L = [
    # M   T   C   S   SP  A   R   RS
    [ 0, -1,  0,  0,  0,  0,  0, -1],  # Meritocrazia
    [-1,  0,  0, -1,  0,  0, -2, -2],  # Tradizione
    [ 0,  0,  0,  0,  0,  0,  0, -1],  # Competizione
    [ 0, -1,  0,  0,  0,  0, -2, -2],  # Sicurezza e controllo
    [ 0,  0,  0,  0,  0,  0,  0, -1],  # Successo e performance
    [ 0,  0,  0,  0,  0,  0, -1, -1],  # Apparenza e immagine
    [ 0, -2,  0, -2,  0, -1,  0, -2],  # Regole rigide
    [-1, -2, -1, -2, -1, -1, -2,  0],  # Ruoli sociali tradizionali
]

# Matrice combo gialle: Benessere
YELLOW_COMBO_B = [
    # M   T   C   S   SP  A   R   RS
    [ 0,  0, -1,  0, -1, -1,  0, -1],  # Meritocrazia
    [ 0,  0,  0, +1,  0,  0,  0, +1],  # Tradizione
    [-1,  0,  0,  0, +1, -1,  0, -1],  # Competizione
    [ 0, +1,  0,  0,  0,  0, +1, +1],  # Sicurezza e controllo
    [-1,  0, +1,  0,  0, -1,  0, -1],  # Successo e performance
    [-1,  0, -1,  0, -1,  0,  0, -1],  # Apparenza e immagine
    [ 0,  0,  0, +1,  0,  0,  0,  0],  # Regole rigide
    [-1, +1, -1, +1, -1, -1,  0,  0],  # Ruoli sociali tradizionali
]

EXTRA_COMBOS = {
    tuple(sorted(("Empatia", "Ascolto"))): {
        "E": 0, "L": 0, "B": +2,
        "label": "Empatia + Ascolto"
    },
    tuple(sorted(("Pari opportunità", "Educazione inclusiva"))): {
        "E": +3, "L": 0, "B": 0,
        "label": "Pari opportunità + Educazione inclusiva"
    },
    tuple(sorted(("Cooperazione", "Supporto sociale"))): {
        "E": 0, "L": 0, "B": +2,
        "label": "Cooperazione + Supporto sociale"
    },
    tuple(sorted(("Rispetto delle differenze", "Libertà di espressione"))): {
        "E": +1, "L": +2, "B": 0,
        "label": "Rispetto delle differenze + Libertà di espressione"
    },
    tuple(sorted(("Ascolto", "Supporto sociale"))): {
        "E": 0, "L": +1, "B": +1,
        "label": "Ascolto + Supporto sociale"
    },
    tuple(sorted(("Meritocrazia", "Pari opportunità"))): {
        "E": +2, "L": 0, "B": 0,
        "label": "Meritocrazia + Pari opportunità"
    },
    tuple(sorted(("Tradizione", "Rispetto delle differenze"))): {
        "E": +1, "L": +1, "B": 0,
        "label": "Tradizione + Rispetto delle differenze"
    },
    tuple(sorted(("Sicurezza e controllo", "Libertà di espressione"))): {
        "E": 0, "L": -2, "B": 0,
        "label": "Sicurezza e controllo + Libertà di espressione"
    },
    tuple(sorted(("Regole rigide", "Educazione inclusiva"))): {
        "E": 0, "L": -1, "B": 0,
        "label": "Regole rigide + Educazione inclusiva"
    },
    tuple(sorted(("Apparenza e immagine", "Rispetto delle differenze"))): {
        "E": +1, "L": 0, "B": 0,
        "label": "Apparenza e immagine + Rispetto delle differenze"
    },
    tuple(sorted(("Competizione", "Cooperazione"))): {
        "E": 0, "L": 0, "B": -1,
        "label": "Competizione + Cooperazione"
    },
    tuple(sorted(("Successo e performance", "Empatia"))): {
        "E": 0, "L": 0, "B": -1,
        "label": "Successo e performance + Empatia"
    },
}
