"""
Definizione completa delle carte del gioco "Consulenti di Felicità".

Contiene:
- carte rosse (problemi)
- carte verdi (risorse positive)
- carte gialle (fattori ambigui)
- ordini di visualizzazione
- utility per accedere a tutti i dati delle carte
"""

from copy import deepcopy

DIMENSIONS = ["E", "L", "B"]

DIMENSION_LABELS = {
    "E": "Equità",
    "L": "Libertà",
    "B": "Benessere",
}

BASE_SCORE = {
    "E": 5,
    "L": 5,
    "B": 5,
}

RED_CARDS = {
    "Stereotipi di genere": {
        "type": "red",
        "description": "Le persone vengono giudicate in base al loro genere, non per quello che sanno fare.",
        "E": -4,
        "L": -4,
        "B": -2,
        "image": "assets/cards/red/stereotipi_di_genere.png",
    },
    "Esclusione sociale": {
        "type": "red",
        "description": "Alcuni gruppi vengono lasciati fuori da opportunità, attività o decisioni.",
        "E": -4,
        "L": -2,
        "B": -4,
        "image": "assets/cards/red/esclusione_sociale.png",
    },
    "Pressione sociale": {
        "type": "red",
        "description": "Le persone si sentono obbligate a comportarsi in un certo modo per essere accettate.",
        "E": -2,
        "L": -5,
        "B": -3,
        "image": "assets/cards/red/pressione_sociale.png",
    },
    "Discriminazione nelle regole": {
        "type": "red",
        "description": "Le regole non sono uguali per tutti e favoriscono alcuni gruppi.",
        "E": -5,
        "L": -3,
        "B": -2,
        "image": "assets/cards/red/discriminazione_nelle_regole.png",
    },
}

GREEN_CARDS = {
    "Pari opportunità": {
        "type": "green",
        "description": "Tutti hanno le stesse possibilità di scegliere e riuscire.",
        "E": +3,
        "L": 0,
        "B": 0,
        "image": "assets/cards/green/pari_opportunita.png",
    },
    "Rispetto delle differenze": {
        "type": "green",
        "description": "Le diversità sono accettate e valorizzate.",
        "E": +2,
        "L": +1,
        "B": 0,
        "image": "assets/cards/green/rispetto_delle_differenze.png",
    },
    "Empatia": {
        "type": "green",
        "description": "Le persone cercano di capire come si sentono gli altri.",
        "E": +1,
        "L": 0,
        "B": +2,
        "image": "assets/cards/green/empatia.png",
    },
    "Ascolto": {
        "type": "green",
        "description": "Le opinioni di tutti vengono prese sul serio.",
        "E": 0,
        "L": +2,
        "B": +1,
        "image": "assets/cards/green/ascolto.png",
    },
    "Libertà di espressione": {
        "type": "green",
        "description": "Ognuno può dire ciò che pensa ed essere se stesso.",
        "E": 0,
        "L": +3,
        "B": 0,
        "image": "assets/cards/green/liberta_di_espressione.png",
    },
    "Educazione inclusiva": {
        "type": "green",
        "description": "La scuola insegna rispetto e pari diritti.",
        "E": +2,
        "L": +1,
        "B": 0,
        "image": "assets/cards/green/educazione_inclusiva.png",
    },
    "Cooperazione": {
        "type": "green",
        "description": "Le persone collaborano invece di competere sempre.",
        "E": +1,
        "L": 0,
        "B": +2,
        "image": "assets/cards/green/cooperazione.png",
    },
    "Supporto sociale": {
        "type": "green",
        "description": "Le persone si aiutano nei momenti difficili.",
        "E": +1,
        "L": 0,
        "B": +2,
        "image": "assets/cards/green/supporto_sociale.png",
    },
}

YELLOW_CARDS = {
    "Meritocrazia": {
        "type": "yellow",
        "description": "Chi si impegna di più ottiene di più.",
        "E": -1,
        "L": +2,
        "B": -1,
        "image": "assets/cards/yellow/meritocrazia.png",
    },
    "Tradizione": {
        "type": "yellow",
        "description": "Si seguono abitudini e ruoli tramandati nel tempo.",
        "E": 0,
        "L": -2,
        "B": +2,
        "image": "assets/cards/yellow/tradizione.png",
    },
    "Competizione": {
        "type": "yellow",
        "description": "Le persone competono per essere le migliori.",
        "E": -1,
        "L": 0,
        "B": +1,
        "image": "assets/cards/yellow/competizione.png",
    },
    "Sicurezza e controllo": {
        "type": "yellow",
        "description": "Ci sono molte regole per mantenere ordine e sicurezza.",
        "E": 0,
        "L": -3,
        "B": +3,
        "image": "assets/cards/yellow/sicurezza_e_controllo.png",
    },
    "Successo e performance": {
        "type": "yellow",
        "description": "Si dà valore ai risultati e ai traguardi.",
        "E": -1,
        "L": 0,
        "B": +1,
        "image": "assets/cards/yellow/successo_e_performance.png",
    },
    "Apparenza e immagine": {
        "type": "yellow",
        "description": "Conta molto come ci si presenta agli altri.",
        "E": -2,
        "L": +1,
        "B": +1,
        "image": "assets/cards/yellow/apparenza_e_immagine.png",
    },
    "Regole rigide": {
        "type": "yellow",
        "description": "Le regole sono molto precise e difficili da cambiare.",
        "E": +1,
        "L": -3,
        "B": +2,
        "image": "assets/cards/yellow/regole_rigide.png",
    },
    "Ruoli sociali tradizionali": {
        "type": "yellow",
        "description": "Uomini e donne hanno ruoli diversi e definiti.",
        "E": -2,
        "L": -1,
        "B": +3,
        "image": "assets/cards/yellow/ruoli_sociali_tradizionali.png",
    },
}

RED_ORDER = [
    "Stereotipi di genere",
    "Esclusione sociale",
    "Pressione sociale",
    "Discriminazione nelle regole",
]

GREEN_ORDER = [
    "Pari opportunità",
    "Rispetto delle differenze",
    "Empatia",
    "Ascolto",
    "Libertà di espressione",
    "Educazione inclusiva",
    "Cooperazione",
    "Supporto sociale",
]

YELLOW_ORDER = [
    "Meritocrazia",
    "Tradizione",
    "Competizione",
    "Sicurezza e controllo",
    "Successo e performance",
    "Apparenza e immagine",
    "Regole rigide",
    "Ruoli sociali tradizionali",
]

NON_RED_ORDER = [
    "Pari opportunità",
    "Rispetto delle differenze",
    "Empatia",
    "Ascolto",
    "Libertà di espressione",
    "Educazione inclusiva",
    "Cooperazione",
    "Supporto sociale",
    "Meritocrazia",
    "Tradizione",
    "Competizione",
    "Sicurezza e controllo",
    "Successo e performance",
    "Apparenza e immagine",
    "Regole rigide",
    "Ruoli sociali tradizionali",
]

ALL_CARDS = {}
ALL_CARDS.update(RED_CARDS)
ALL_CARDS.update(GREEN_CARDS)
ALL_CARDS.update(YELLOW_CARDS)


def get_card(card_name: str) -> dict:
    """Restituisce una copia dei dati della carta."""
    if card_name not in ALL_CARDS:
        raise KeyError(f"Carta non trovata: {card_name}")
    return deepcopy(ALL_CARDS[card_name])


def get_all_cards() -> dict:
    """Restituisce una copia dell'intero dizionario carte."""
    return deepcopy(ALL_CARDS)


def get_cards_by_type(card_type: str) -> dict:
    """Restituisce un sottoinsieme di carte per tipo: red, green, yellow."""
    if card_type == "red":
        return deepcopy(RED_CARDS)
    if card_type == "green":
        return deepcopy(GREEN_CARDS)
    if card_type == "yellow":
        return deepcopy(YELLOW_CARDS)
    raise ValueError("card_type deve essere 'red', 'green' o 'yellow'")


def get_card_type(card_name: str) -> str:
    """Restituisce il tipo della carta."""
    return ALL_CARDS[card_name]["type"]


def is_red(card_name: str) -> bool:
    return card_name in RED_CARDS


def is_green(card_name: str) -> bool:
    return card_name in GREEN_CARDS


def is_yellow(card_name: str) -> bool:
    return card_name in YELLOW_CARDS
