from __future__ import annotations

import re

def reorder_nombre(value: str | None) -> str | None:

    if value is None:
        return None
    
    text = str(value).strip()

    if not text:
        return text
    
    if "," not in text:
        return text
    
    apellido, nombre = text.split(",", 1)
    apellido = " ".join(apellido.strip().split())
    nombre = " ".join(nombre.strip().split())

    if not nombre or not apellido:
        return text
    
    return f"{nombre} {apellido}"

def format_rut(value: str | int | None) -> str | int | None:
    if value is None:
        return None

    original = value
    text = str(value).strip().upper()

    if not text:
        return original

    clean = re.sub(r"[^0-9K]", "", text)

    # 7 u 8 dígitos de cuerpo + 1 dígito verificador
    if not re.fullmatch(r"\d{7,8}[0-9K]", clean):
        return original

    cuerpo = clean[:-1]
    dv = clean[-1]

    cuerpo_formateado = f"{int(cuerpo):,}".replace(",", ".")

    return f"{cuerpo_formateado}-{dv}"

def expand_fuente(value: str | None) -> str | None:
    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return value

    mapping = {
        "GX": "Gendex (GX)",
        "TW": "TWAIN (TW)",
    }

    return mapping.get(text.upper(), value)
    
