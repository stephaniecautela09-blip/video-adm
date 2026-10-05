"""Lê o roteiro.md e gera um WAV por batida com o Piper (com cache por hash do texto).

Uso:  python audio.py      # gera o que faltar e mostra a duração de cada cena
"""
import hashlib
import os
import re
import wave

from fala import normalizar

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
BUILD = os.path.join(RAIZ, "build", "contabilidade")
PASTA_AUDIO = os.path.join(BUILD, "audio")
VOZ = os.path.join(RAIZ, "voices", "pt_BR-faber-medium.onnx")
LENGTH_SCALE = 1.05   # >1 = fala mais devagar
SR = 22050


def ler_roteiro(path=os.path.join(AQUI, "roteiro.md")):
    """Devolve (cenas, textos): cenas = [(id, titulo, [chaves])], textos = {chave: texto}."""
    cenas, textos, chave = [], {}, None
    for linha in open(path, encoding="utf-8"):
        linha = linha.rstrip("\n")
        m = re.match(r"# Cena (\d+) — (.+)", linha)
        if m:
            cenas.append((f"c{m.group(1)}", m.group(2).strip(), []))
            chave = None
            continue
        m = re.fullmatch(r"\[(\w+)\]", linha.strip())
        if m:
            chave = m.group(1)
            assert chave not in textos, f"chave repetida: {chave}"
            textos[chave] = ""
            cenas[-1][2].append(chave)
            continue
        if chave and linha.strip() and not linha.startswith(">"):
            textos[chave] = (textos[chave] + " " + linha.strip()).strip()
    return cenas, textos


CENAS, TEXTOS = ler_roteiro()


def caminho(chave):
    texto = normalizar(TEXTOS[chave])
    h = hashlib.sha1(f"{texto}|{LENGTH_SCALE}".encode()).hexdigest()[:10]
    return os.path.join(PASTA_AUDIO, f"{chave}_{h}.wav")


def duracao(chave):
    with wave.open(caminho(chave)) as w:
        return w.getnframes() / w.getframerate()


def gerar():
    from piper import PiperVoice, SynthesisConfig
    os.makedirs(PASTA_AUDIO, exist_ok=True)
    faltam = [k for k in TEXTOS if not os.path.exists(caminho(k))]
    if faltam:
        voz = PiperVoice.load(VOZ)
        cfg = SynthesisConfig(length_scale=LENGTH_SCALE)
        for i, k in enumerate(faltam):
            p = caminho(k)
            with wave.open(p + ".tmp", "wb") as w:
                voz.synthesize_wav(normalizar(TEXTOS[k]), w, syn_config=cfg)
            os.replace(p + ".tmp", p)
            print(f"  voz {i + 1}/{len(faltam)}: {k}", flush=True)


if __name__ == "__main__":
    gerar()
    total = 0
    for cid, titulo, chaves in CENAS:
        d = sum(duracao(k) for k in chaves)
        total += d
        print(f"{cid}  {d / 60:5.1f} min  {len(chaves):3d} batidas  {titulo}")
    print(f"fala total: {total / 60:.1f} min")
