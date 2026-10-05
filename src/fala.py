"""Normalização do texto da narração para o TTS (Piper, pt-BR).

Converte números, porcentagens, siglas e símbolos em palavras, para que a voz
leia "6.454,20" como "seis mil quatrocentos e cinquenta e quatro vírgula vinte".
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


def extenso(n):
    if n < 1000:
        return _ate_mil(n)
    if n < 1_000_000:
        m, r = divmod(n, 1000)
        pref = "mil" if m == 1 else _ate_mil(m) + " mil"
        if r == 0:
            return pref
        sep = " e " if (r < 100 or r % 100 == 0) else " "
        return pref + sep + _ate_mil(r)
    mi, r = divmod(n, 1_000_000)
    pref = ("um milhão" if mi == 1 else _ate_mil(mi) + " milhões")
    if r == 0:
        return pref
    sep = " e " if (r < 100 or (r < 1000 and r % 100 == 0)) else " "
    return pref + sep + extenso(r)


def _numero(txt):
    inteiro, _, dec = txt.partition(",")
    s = extenso(int(inteiro.replace(".", "")))
    if dec:
        if dec.startswith("0"):
            # 0,05 -> zero vírgula zero cinco ; 0,0368 -> zero vírgula zero três seis oito
            s += " vírgula " + " ".join(UNI[int(ch)] for ch in dec)
        else:
            s += " vírgula " + extenso(int(dec))
    return s


SIGLAS = [
    (r"ΔCCL", "variação do cê cê éle"),
    (r"\bFCO\b", "éfe cê ó"),
    (r"\bCCL\b", "cê cê éle"),
    (r"\bVPL\b", "vê pê éle"),
    (r"\bTIR\b", "tír"),
    (r"\bIL\b", "í éle"),
    (r"\bROA\b", "érre ó á"),
    (r"\bROE\b", "érre ó é"),
    (r"\bCAPM\b", "cápem"),
    (r"\bCMPC\b", "cê eme pê cê"),
    (r"\bLAJIR\b", "lajír"),
    (r"\bSML\b", "ésse eme éle"),
    (r"\bVL\b", "vê éle"),
    (r"\bVU\b", "vê u"),
    (r"\bRf\b", "érre éfe"),
    (r"\bRm\b", "érre eme"),
    (r"\bRe\b", "érre é"),
    (r"\bRd\b", "érre dê"),
    (r"\bRa\b", "érre á"),
    (r"\bD1\b", "dê um"),
    (r"\bD0\b", "dê zero"),
    (r"\bHP 12C\b", "agá pê doze cê"),
    (r"\bB3\b", "bê três"),
    (r"\bf (?=REG|IRR|NPV|FIN)", "éfe "),
    (r"\bg CF\b", "gê cê éfe"),
    (r"\bIRR\b", "í érre érre"),
    (r"\bNPV\b", "ene pê vê"),
    (r"\bCF\b", "cê éfe"),
    (r"\bCHS\b", "cê agá ésse"),
    (r"\bPMT\b", "pê eme tê"),
    (r"\bFV\b", "éfe vê"),
    (r"\bPV\b", "pê vê"),
    (r"\bREG\b", "érre é gê"),
    (r"\bFIN\b", "éfe í ene"),
    (r"\bMM\b", "Modigliani-Miller"),
    (r"\bCVM\b", "cê vê eme"),
    (r"\bS/A\b", "ésse á"),
    (r"\bESG\b", "ê ésse gê"),
    (r"\bPIB\b", "píbi"),
    (r"\bIPO\b", "í pê ó"),
    (r"\bD/E\b", "dívida sobre patrimônio"),
    (r"\bE\(R\)", "retorno esperado"),
    (r"\bDu Pont\b", "Du Pónt"),
    (r"\bstock options\b", "stóqui ópichons"),
    (r"\btakeover\b", "têikôver"),
    (r"\bpayback\b", "peibéqui"),
    (r"\bPayback\b", "Peibéqui"),
    (r"\bpaybacks\b", "peibéquis"),
    (r"\bSelic\b", "Selíqui"),
    (r"\bGordon\b", "Górdon"),
    (r"\bIbovespa\b", "Ibovéspa"),
    (r"\bbeta\b", "bêta"),
    (r"\bBeta\b", "Bêta"),
    (r"\bdo Ross\b", "do Róss"),
    (r"\bRoss\b", "Róss"),
]


def normalizar(t):
    for pad, sub in SIGLAS:
        t = re.sub(pad, sub, t)
    t = t.replace("−", " menos ").replace("×", " vezes ").replace("÷", " dividido por ")
    t = t.replace("=", " igual a ").replace("→", ", ")
    t = re.sub(r"(\d)\s*%", r"\1 por cento", t)
    t = re.sub(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?", lambda m: _numero(m.group()), t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


if __name__ == "__main__":
    for x in ["O FCO é 6.454,20.", "TIR de 18,64% e VPL de 14.233,41.", "0,05 e 0,0368",
              "ROE = 18,91%", "1.000.000 e 2.026", "100 e 1.100 e 1.230"]:
        print(normalizar(x))
