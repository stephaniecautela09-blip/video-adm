"""Monta o vídeo: gráficos → slides → narração (Piper TTS) → MP4 com legendas e capítulos.

Uso:
    python3 build.py              # tudo
    python3 build.py --slides     # só gera os slides (para revisar o visual)
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import wave

import graficos
import slides
from fala import normalizar
from roteiro import CENAS

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
BUILD = os.path.join(RAIZ, "build")
SAIDA = os.path.join(RAIZ, "saida")
VOZ = os.path.join(RAIZ, "voices", "pt_BR-faber-medium.onnx")
LENGTH_SCALE = 1.05        # >1 = fala mais devagar
PAUSA_ANTES, PAUSA_DEPOIS = 0.35, 0.75   # segundos de silêncio em volta de cada cena
PAUSA_CAPA = 1.2           # pausa extra depois de capas de bloco
SR = 22050


def gerar_slides():
    imgs = graficos.gerar(os.path.join(BUILD, "graficos"))
    pasta = os.path.join(BUILD, "slides")
    os.makedirs(pasta, exist_ok=True)
    paths = []
    for i, sc in enumerate(CENAS):
        sc = dict(sc)
        if sc["tipo"] == "grafico":
            sc["img"] = imgs[sc["img"]]
        p = os.path.join(pasta, f"{i:03d}.png")
        slides.render(sc, p)
        paths.append(p)
    return paths


def gerar_audio():
    from piper import PiperVoice, SynthesisConfig
    voz = PiperVoice.load(VOZ)
    cfg = SynthesisConfig(length_scale=LENGTH_SCALE)
    pasta = os.path.join(BUILD, "audio")
    os.makedirs(pasta, exist_ok=True)
    paths = []
    for i, sc in enumerate(CENAS):
        texto = normalizar(sc["narr"])
        h = hashlib.sha1(f"{texto}|{LENGTH_SCALE}".encode()).hexdigest()[:10]
        p = os.path.join(pasta, f"{i:03d}_{h}.wav")
        if not os.path.exists(p):
            with wave.open(p, "wb") as w:
                voz.synthesize_wav(texto, w, syn_config=cfg)
            print(f"  voz {i + 1}/{len(CENAS)}", flush=True)
        paths.append(p)
    return paths


def silencio(seg):
    return b"\x00\x00" * int(SR * seg)


def montar(slides_png, audios):
    os.makedirs(SAIDA, exist_ok=True)
    narr_wav = os.path.join(BUILD, "narracao.wav")
    tempos = []  # (inicio, fim_da_fala, fim_da_cena)
    t = 0.0
    with wave.open(narr_wav, "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(SR)
        for sc, a in zip(CENAS, audios):
            with wave.open(a) as w:
                assert w.getframerate() == SR
                fala = w.readframes(w.getnframes())
            depois = PAUSA_DEPOIS + (PAUSA_CAPA if sc["tipo"] in ("capa", "pegadinha") else 0)
            out.writeframes(silencio(PAUSA_ANTES) + fala + silencio(depois))
            dur_fala = len(fala) / 2 / SR
            ini = t
            t += PAUSA_ANTES + dur_fala + depois
            tempos.append((ini, ini + PAUSA_ANTES, ini + PAUSA_ANTES + dur_fala, t))

    # lista de imagens com duração (concat demuxer)
    lista = os.path.join(BUILD, "imagens.txt")
    with open(lista, "w") as f:
        for p, (ini, _, _, fim) in zip(slides_png, tempos):
            f.write(f"file '{p}'\nduration {fim - ini:.3f}\n")
        f.write(f"file '{slides_png[-1]}'\n")

    srt = os.path.join(SAIDA, "aula_adm_financeira.srt")
    escrever_srt(srt, tempos)
    meta = os.path.join(BUILD, "capitulos.txt")
    escrever_capitulos(meta, tempos, t)

    mp4 = os.path.join(SAIDA, "aula_adm_financeira.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-stats",
           "-f", "concat", "-safe", "0", "-i", lista,
           "-i", narr_wav, "-i", meta, "-map_metadata", "2", "-map", "0:v", "-map", "1:a",
           "-vf", "fps=12,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-tune", "stillimage",
           "-crf", "24", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "aac", "-b:a", "96k", "-ac", "1", "-movflags", "+faststart",
           "-shortest", mp4]
    subprocess.run(cmd, check=True)
    print(f"duração total: {t / 60:.1f} min → {mp4}")
    return mp4, t


def _ts(s):
    ms = int(round(s * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def escrever_srt(path, tempos):
    n = 1
    with open(path, "w") as f:
        for sc, (_, ini, fim, _) in zip(CENAS, tempos):
            frases = [x.strip() for x in re.split(r"(?<=[.!?:])\s+", sc["narr"]) if x.strip()]
            # junta frases curtas e divide longas em blocos de ~110 caracteres
            blocos = []
            for fr in frases:
                partes, atual = [], ""
                for pal in fr.split():
                    if len(atual) + len(pal) > 110:
                        partes.append(atual)
                        atual = pal
                    else:
                        atual = (atual + " " + pal).strip()
                partes.append(atual)
                blocos += partes
            total = sum(len(normalizar(b)) for b in blocos)
            t = ini
            for b in blocos:
                d = (fim - ini) * len(normalizar(b)) / total
                linhas = quebrar(b, 55)
                f.write(f"{n}\n{_ts(t)} --> {_ts(t + d)}\n{linhas}\n\n")
                t += d
                n += 1


def quebrar(txt, w):
    if len(txt) <= w:
        return txt
    meio = len(txt) // 2
    esq, dir_ = txt.rfind(" ", 0, meio + 10), txt.find(" ", meio - 10)
    corte = esq if esq > 0 else dir_
    return txt[:corte] + "\n" + txt[corte + 1:]


def escrever_capitulos(path, tempos, total):
    caps = []
    for sc, (ini, *_rest) in zip(CENAS, tempos):
        if sc["tipo"] == "capa":
            nome = slides.BLOCO_NOME[sc["bloco"]] if sc["bloco"] else ("Abertura" if ini == 0 else "Encerramento")
            caps.append((ini, nome))
    with open(path, "w") as f:
        f.write(";FFMETADATA1\ntitle=Administração Financeira — Revisão para a prova (Ross, 9ª ed.)\n")
        for i, (ini, nome) in enumerate(caps):
            fim = caps[i + 1][0] if i + 1 < len(caps) else total
            f.write(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(ini * 1000)}\nEND={int(fim * 1000)}\ntitle={nome}\n")
    with open(os.path.join(SAIDA, "capitulos.txt"), "w") as f:
        for ini, nome in caps:
            m, s = divmod(int(ini), 60)
            f.write(f"{m:02d}:{s:02d}  {nome}\n")


if __name__ == "__main__":
    png = gerar_slides()
    print(f"{len(png)} slides gerados")
    if "--slides" in sys.argv:
        sys.exit()
    wavs = gerar_audio()
    montar(png, wavs)
