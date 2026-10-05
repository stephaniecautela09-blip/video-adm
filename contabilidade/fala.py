"""Normalização do texto da narração para o TTS (Piper, pt-BR).

Converte números, porcentagens, siglas e símbolos em palavras, para que a voz
leia "R$ 193.600" como "cento e noventa e três mil e seiscentos reais" e
"CSLL" como "cê ésse éle éle".
"""
import re

UNI = ["zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove",
       "dez", "onze", "doze", "treze", "catorze", "quinze", "dezesseis", "dezessete",
       "dezoito", "dezenove"]
DEZ = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta",
       "oitenta", "noventa"]
CEM = ["", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos", "seiscentos",
       "setecentos", "oitocentos", "novecentos"]


def _ate_mil(n):
    if n < 20:
        return UNI[n]
    if n < 100:
        d, u = divmod(n, 10)
        return DEZ[d] + ("" if u == 0 else " e " + UNI[u])
    if n == 100:
        return "cem"
    c, r = divmod(n, 100)
    return CEM[c] + ("" if r == 0 else " e " + _ate_mil(r))


def _usa_e(r):
    """Português usa "e" antes do último grupo quando ele é "redondo"."""
    return r < 100 or r % 100 == 0 and r < 1000


def extenso(n):
    if n < 1000:
        return _ate_mil(n)
    if n < 1_000_000:
        m, r = divmod(n, 1000)
        pref = "mil" if m == 1 else _ate_mil(m) + " mil"
        if r == 0:
            return pref
        return pref + (" e " if _usa_e(r) else " ") + _ate_mil(r)
    mi, r = divmod(n, 1_000_000)
    pref = "um milhão" if mi == 1 else _ate_mil(mi) + " milhões"
    if r == 0:
        return pref
    # 1.200.000 -> "um milhão e duzentos mil"
    redondo = r % 1000 == 0 and _usa_e(r // 1000)
    return pref + (" e " if redondo or _usa_e(r) else " ") + extenso(r)


def _numero(txt):
    inteiro, _, dec = txt.partition(",")
    s = extenso(int(inteiro.replace(".", "")))
    if dec:
        s += " vírgula " + extenso(int(dec))
    return s


SIGLAS = [
    (r"\bOCPC 09\b", "ó cê pê cê zero nove"),
    (r"\bOCPC\b", "ó cê pê cê"),
    (r"\bICPC\b", "í cê pê cê"),
    (r"\bCPC\b", "cê pê cê"),
    (r"\bCPCs\b", "cê pê cês"),
    (r"\bIFRS S1\b", "í éfe érre ésse ésse um"),
    (r"\bIFRS S2\b", "í éfe érre ésse ésse dois"),
    (r"\bS1\b", "ésse um"),
    (r"\bS2\b", "ésse dois"),
    (r"\bIFRS\b", "í éfe érre ésse"),
    (r"\bIFRIC\b", "ífric"),
    (r"\bSIC\b", "ésse í cê"),
    (r"\bIASB\b", "í á ésse bê"),
    (r"\bIASC\b", "í á ésse cê"),
    (r"\bISSB\b", "í ésse ésse bê"),
    (r"\bIAS\b", "í á ésse"),
    (r"\bIOSCO\b", "iósco"),
    (r"\bFASB\b", "fázbi"),
    (r"\bBR GAAP\b", "bê érre gápi"),
    (r"\bUS GAAP\b", "u ésse gápi"),
    (r"\bGAAP\b", "gápi"),
    (r"\bESG\b", "ê ésse gê"),
    (r"\bLAIR\b", "láir"),
    (r"\bCSLL\b", "cê ésse éle éle"),
    (r"\bIR\b", "í érre"),
    (r"\bPECLD\b", "pê é cê éle dê"),
    (r"\bORA\b", "ó érre á"),
    (r"\bPBA\b", "pê bê á"),
    (r"\bDRE\b", "dê érre é"),
    (r"\bROI\b", "érre ó í"),
    (r"\bSARs\b", "sárs"),
    (r"\bDaimler-Benz\b", "Dáimler Bénz"),
    (r"\bcode law\b", "côud ló"),
    (r"\bcommon law\b", "cómon ló"),
    (r"\btrue and fair view\b", "trú end fér viú"),
    (r"\bvesting\b", "vésting"),
    (r"\bgoodwill\b", "gudúiu"),
    (r"\bIlírio\b", "Ilírio"),
]


def normalizar(t):
    for pad, sub in SIGLAS:
        t = re.sub(pad, sub, t)
    t = re.sub(r"R\$\s*(\d[\d.]*(?:,\d+)?)", r"\1 reais", t)
    t = t.replace("−", " menos ").replace("×", " vezes ").replace("÷", " dividido por ")
    t = t.replace("=", " igual a ").replace("→", ", ")
    t = re.sub(r"(\d)\s*%", r"\1 por cento", t)
    t = re.sub(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?", lambda m: _numero(m.group()), t)
    t = re.sub(r"(milhão|milhões) reais", r"\1 de reais", t)
    t = t.replace("“", "").replace("”", "").replace('"', "")
    t = re.sub(r"\s+", " ", t)
    return t.strip()


if __name__ == "__main__":
    for x in ["R$ 1.000.000 e 1.200.000 e 193.600", "19.040 e 24.480 e 3.400", "34% do LAIR",
              "IR e CSLL, OCPC 09, IFRS S1", "Lei 12.973 de 2014, artigo 33", "1973 e 2000",
              "102.000 e 1.250.000 e 2.300.000"]:
        print(normalizar(x))
