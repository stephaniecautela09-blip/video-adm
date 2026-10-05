"""Monta o vídeo: narração (Piper) → cenas (Manim) → áudio sincronizado → MP4 com capítulos e legendas.

Uso (no venv com manim e piper-tts):
    python build.py               # tudo, 1920x1080
    python build.py --rapido      # 854x480, para revisar
    python build.py Cena04        # renderiza só essa cena e remonta o vídeo
"""
import json
import os
import re
import subprocess
import sys
import wave
from concurrent.futures import ThreadPoolExecutor

import numpy as np

import audio
from fala import normalizar

AQUI = audio.AQUI
SAIDA = os.path.join(audio.RAIZ, "saida")
MEDIA = os.path.join(audio.BUILD, "media")
NOME = "aula_contabilidade_avancada_ii"
CENAS = [f"Cena{int(c[0][1:]):02d}" for c in audio.CENAS]


def render(cena, rapido):
    res = "854,480" if rapido else "1920,1080"
    cmd = [sys.executable, "-m", "manim", "-r", res, "--fps", "30", "--media_dir", MEDIA,
           "--progress_bar", "none", "-v", "WARNING", os.path.join(AQUI, "cenas.py"), cena]
    subprocess.run(cmd, check=True, cwd=AQUI)
    print(f"  {cena} pronta", flush=True)


def video_da_cena(cena, rapido):
    pasta = "480p30" if rapido else "1080p30"
    return os.path.join(MEDIA, "videos", "cenas", pasta, f"{cena}.mp4")


def duracao_video(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                          "csv=p=0", p], capture_output=True, text=True, check=True).stdout
    return float(out)


def ler_wav(p):
    with wave.open(p) as w:
        assert w.getframerate() == audio.SR and w.getsampwidth() == 2
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)


def montar(rapido):
    os.makedirs(SAIDA, exist_ok=True)
    trilha, lista, legendas, caps = [], [], [], []
    t0 = 0.0
    for cena, (cid, titulo, _) in zip(CENAS, audio.CENAS):
        info = json.load(open(os.path.join(audio.BUILD, "tempos", f"{cid}.json")))
        mp4 = video_da_cena(cena, rapido)
        dv = duracao_video(mp4)
        assert abs(dv - info["duracao"]) < 0.1, f"{cena}: vídeo {dv:.2f}s × relógio {info['duracao']:.2f}s"
        buf = np.zeros(int(round(dv * audio.SR)), dtype=np.int32)
        for b in info["batidas"]:
            x = ler_wav(b["wav"])
            i = int(round(b["inicio"] * audio.SR))
            n = min(len(x), len(buf) - i)
            buf[i:i + n] += x[:n]
            legendas.append((t0 + b["inicio"], b["dur"], audio.TEXTOS[b["chave"]]))
        trilha.append(np.clip(buf, -32768, 32767).astype(np.int16))
        lista.append(mp4)
        caps.append((t0, f"{int(cid[1:])}. {titulo}"))
        t0 += dv

    wav = os.path.join(audio.BUILD, "narracao.wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(audio.SR)
        w.writeframes(np.concatenate(trilha).tobytes())

    concat = os.path.join(audio.BUILD, "cenas.txt")
    with open(concat, "w") as f:
        f.writelines(f"file '{p}'\n" for p in lista)
    meta = os.path.join(audio.BUILD, "capitulos.ffmeta")
    with open(meta, "w") as f:
        f.write(";FFMETADATA1\ntitle=Contabilidade Avançada II — revisão para a Aval 1\n")
        for k, (ini, nome) in enumerate(caps):
            fim = caps[k + 1][0] if k + 1 < len(caps) else t0
            f.write(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(ini * 1000)}\nEND={int(fim * 1000)}\ntitle={nome}\n")
    with open(os.path.join(SAIDA, "capitulos_contabilidade.txt"), "w") as f:
        for ini, nome in caps:
            m, s = divmod(int(ini), 60)
            f.write(f"{m:02d}:{s:02d}  {nome}\n")
    escrever_srt(os.path.join(SAIDA, f"{NOME}.srt"), legendas)

    mp4 = os.path.join(SAIDA, f"{NOME}.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-stats",
           "-f", "concat", "-safe", "0", "-i", concat, "-i", wav, "-i", meta,
           "-map_metadata", "2", "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "26", "-tune", "animation",
           "-pix_fmt", "yuv420p",
           "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "aac", "-b:a", "96k",
           "-ac", "1", "-movflags", "+faststart", mp4]
    subprocess.run(cmd, check=True)
    print(f"duração total: {t0 / 60:.1f} min → {mp4}")


def _ts(s):
    ms = int(round(s * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def escrever_srt(path, legendas):
    """Divide a fala de cada batida em blocos de ~90 caracteres, com tempo proporcional ao texto."""
    n = 1
    with open(path, "w") as f:
        for ini, dur, texto in legendas:
            blocos, atual = [], ""
            for frase in re.split(r"(?<=[.!?:])\s+", texto):
                for pal in frase.split():
                    if atual and len(atual) + len(pal) > 90:
                        blocos.append(atual)
                        atual = pal
                    else:
                        atual = (atual + " " + pal).strip()
                if len(atual) > 40:
                    blocos.append(atual)
                    atual = ""
            if atual:
                blocos.append(atual)
            total = sum(len(normalizar(b)) for b in blocos)
            t = ini
            for b in blocos:
                d = dur * len(normalizar(b)) / total
                f.write(f"{n}\n{_ts(t)} --> {_ts(t + d)}\n{quebrar(b, 48)}\n\n")
                t += d
                n += 1


def quebrar(txt, w):
    if len(txt) <= w:
        return txt
    meio = len(txt) // 2
    esq, dir_ = txt.rfind(" ", 0, meio + 8), txt.find(" ", meio - 8)
    corte = esq if esq > 0 else dir_
    return txt[:corte] + "\n" + txt[corte + 1:]


if __name__ == "__main__":
    rapido = "--rapido" in sys.argv
    pedidas = [a for a in sys.argv[1:] if a.startswith("Cena")] or CENAS
    print("narração…")
    audio.gerar()
    print(f"render ({len(pedidas)} cenas)…")
    with ThreadPoolExecutor(max_workers=4) as ex:
        list(ex.map(lambda c: render(c, rapido), pedidas))
    print("montagem…")
    montar(rapido)
