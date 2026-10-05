"""Renderiza cada cena do roteiro como uma imagem 1920x1080 (estilo quadro)."""
import re
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_M = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

BG = (24, 35, 46)
PANEL = (33, 48, 62)
LINE = (62, 82, 100)
TXT = (236, 240, 244)
DIM = (150, 165, 180)
COR = {
    "y": (255, 209, 102),   # amarelo giz: destaque
    "g": (6, 214, 160),     # verde: resultado / aceitar
    "r": (239, 71, 111),    # vermelho: pegadinha / rejeitar
    "c": (76, 201, 240),    # azul: fórmula
    "w": TXT,
    "d": DIM,
}
BLOCO_COR = {0: (120, 140, 160), 1: (76, 201, 240), 2: (6, 214, 160), 3: (255, 209, 102),
             4: (239, 130, 90), 5: (180, 140, 250), 6: (239, 71, 111)}
BLOCO_NOME = {0: "Abertura", 1: "Bloco 1 · Introdução", 2: "Bloco 2 · Fluxo de caixa e indicadores",
              3: "Bloco 3 · Crescimento e avaliação de projetos", 4: "Bloco 4 · Risco, retorno e CAPM",
              5: "Bloco 5 · Custo de capital e estrutura", 6: "Bloco 6 · Resumo final"}

_cache = {}


def F(size, bold=False, mono=False):
    k = (size, bold, mono)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(FONT_M if mono else (FONT_B if bold else FONT), size)
    return _cache[k]


TAG = re.compile(r"\[(y|g|r|c|d|b)\](.*?)\[/\1\]")


def parse(text, base="w"):
    """'Texto [y]destaque[/y]' -> [(palavra, cor, negrito)]"""
    for a, b in (("D1", "D₁"), ("D0", "D₀"), ("P0", "P₀")):
        text = re.sub(rf"\b{a}\b", b, text)
    out, pos = [], 0
    for m in TAG.finditer(text):
        out += [(w, base, False) for w in text[pos:m.start()].split(" ") if w != ""]
        tag = m.group(1)
        cor, bold = (base, True) if tag == "b" else (tag, True)
        out += [(w, cor, bold) for w in m.group(2).split(" ") if w != ""]
        pos = m.end()
    out += [(w, base, False) for w in text[pos:].split(" ") if w != ""]
    return out


def rich(d, x, y, text, size, maxw, base="w", line_h=None, bold_all=False, mono=False, center=False):
    """Escreve texto com marcações de cor e quebra de linha. Retorna o y final."""
    line_h = line_h or int(size * 1.32)
    words = parse(text, base)
    lines, cur, curw = [], [], 0
    sp = d.textlength(" ", font=F(size))
    for w, c, b in words:
        f = F(size, b or bold_all, mono)
        ww = d.textlength(w, font=f)
        gruda = bool(cur) and w[0] in ".,:;!?)"
        if cur and not gruda and curw + sp + ww > maxw:
            lines.append((cur, curw))
            cur, curw = [], 0
        cur.append((w, c, b, ww, gruda))
        curw += (sp if len(cur) > 1 and not gruda else 0) + ww
    if cur:
        lines.append((cur, curw))
    for ln, lw in lines:
        xx = x + (maxw - lw) / 2 if center else x
        for j, (w, c, b, ww, gruda) in enumerate(ln):
            if gruda and j:
                xx -= sp
            d.text((xx, y), w, font=F(size, b or bold_all, mono), fill=COR[c])
            xx += ww + sp
        y += line_h
    return y


def measure(d, text, size, maxw, line_h=None):
    img = Image.new("RGB", (10, 10))
    return rich(ImageDraw.Draw(img), 0, 0, text, size, maxw, line_h=line_h)


def frame(sc):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    b = sc.get("bloco", 0)
    cor = BLOCO_COR[b]
    d.rectangle([0, 0, W, 8], fill=cor)
    d.text((70, 30), BLOCO_NOME[b], font=F(28, True), fill=cor)
    rt = "Adm. Financeira · Ross 9ª ed. · Revisão para a prova"
    d.text((W - 70 - d.textlength(rt, font=F(24)), 33), rt, font=F(24), fill=DIM)
    if sc.get("titulo"):
        ts = 54
        while d.textlength(sc["titulo"], font=F(ts, True)) > W - 140 and ts > 30:
            ts -= 2
        d.text((70, 82 + (54 - ts) // 2), sc["titulo"], font=F(ts, True), fill=TXT)
        d.line([70, 160, W - 70, 160], fill=LINE, width=2)
    return img, d


def box(d, xy, fill=PANEL, outline=None, w=3, r=18):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=w)


# ---------------------------------------------------------------- layouts

def capa(sc):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    cor = BLOCO_COR[sc.get("bloco", 0)]
    d.rectangle([0, 0, 24, H], fill=cor)
    if sc.get("kicker"):
        d.text((140, 300), sc["kicker"], font=F(44, True), fill=cor)
    y = rich(d, 140, 380, sc["titulo"], 92, W - 280, bold_all=True)
    if sc.get("sub"):
        y = rich(d, 140, y + 30, sc["sub"], 42, W - 280, base="d")
    if sc.get("tempo"):
        d.text((140, H - 150), sc["tempo"], font=F(32), fill=DIM)
    return img


def lista(sc):
    img, d = frame(sc)
    itens = sc["itens"]
    n = sc.get("reveal", len(itens))
    y = 200
    size = sc.get("size", 42)
    numerada = sc.get("numerada", False)
    first = sc.get("num_ini", 1)
    for i, it in enumerate(itens[:n]):
        atual = "reveal" in sc and i == n - 1
        mark = f"{first + i}." if numerada else "•"
        markc = COR["y"] if atual else COR["c"]
        d.text((90, y), mark, font=F(size, True), fill=markc)
        y = rich(d, 90 + (80 if numerada else 50), y, it, size, W - 260 - (30 if numerada else 0),
                 base="w") + int(size * 0.45)
    if sc.get("formula") and n >= sc.get("formula_em", 0):
        fy = max(y + 20, H - 230)
        box(d, [90, fy, W - 90, fy + 150], outline=COR["c"])
        rich(d, 120, fy + 45, sc["formula"], 46, W - 240, center=True, mono=False)
    return img


def calc(sc):
    img, d = frame(sc)
    dados = sc.get("dados", [])
    passos = sc["passos"]
    n = sc.get("reveal", len(passos))
    lx = 70
    if dados:
        lw = sc.get("dados_w", 560)
        box(d, [lx, 190, lx + lw, H - 60])
        d.text((lx + 30, 210), sc.get("dados_titulo", "Dados"), font=F(34, True), fill=COR["c"])
        y = 270
        for it in dados:
            y = rich(d, lx + 30, y, it, sc.get("dados_size", 35), lw - 60) + 12
        rx = lx + lw + 40
    else:
        rx = 90
    rw = W - rx - 80
    d.text((rx, 200), sc.get("passos_titulo", "Passo a passo"), font=F(34, True), fill=COR["c"])
    y = 260
    size = sc.get("size", 38)
    for i, p in enumerate(passos[:n]):
        atual = i == n - 1
        if atual:
            h = measure(d, p, size, rw - 40) + 10
            box(d, [rx - 10, y - 8, rx + rw, y + h], fill=(48, 64, 80), outline=None, r=10)
        y = rich(d, rx + 10, y, p, size, rw - 40, base="w" if atual else "d") + int(size * 0.55)
    if sc.get("resultado") and n >= len(passos):
        h = measure(d, sc["resultado"], 36, rw - 60)
        ry = H - 60 - h - 56
        box(d, [rx - 10, ry, rx + rw, H - 60], fill=(20, 60, 52), outline=COR["g"])
        rich(d, rx + 20, ry + 26, sc["resultado"], 36, rw - 60)
    return img


def tabela(sc):
    img, d = frame(sc)
    cab, linhas = sc["cab"], sc["linhas"]
    n = sc.get("reveal", len(linhas))
    cols = sc.get("cols") or [1] * len(cab)
    tot = sum(cols)
    x0, x1 = 90, W - 90
    widths = [(x1 - x0) * c / tot for c in cols]
    size = int(sc.get("size", 34) * 1.2)
    rh = sc.get("rh", int(size * 2.0))
    y = sc.get("y0", 200)
    d.rounded_rectangle([x0, y, x1, y + rh], radius=10, fill=(45, 70, 92))
    xx = x0
    for c, w in zip(cab, widths):
        rich(d, xx + 18, y + (rh - size) // 2 - 4, c, size, w - 30, bold_all=True, base="c")
        xx += w
    y += rh
    hl = set(sc.get("hl", []))
    for i, ln in enumerate(linhas[:n]):
        fill = (52, 70, 86) if (i in hl or ("reveal" in sc and i == n - 1)) else (PANEL if i % 2 == 0 else BG)
        hrow = max(rh, max(measure(d, str(c), size, w - 30) for c, w in zip(ln, widths)) + 24)
        d.rectangle([x0, y, x1, y + hrow], fill=fill)
        xx = x0
        for c, w in zip(ln, widths):
            rich(d, xx + 18, y + 14, str(c), size, w - 30)
            xx += w
        y += hrow
    d.line([x0, y, x1, y], fill=LINE, width=2)
    y += 30
    for nt in sc.get("notas", []):
        y = rich(d, 90, y, nt, sc.get("nota_size", 38), W - 180) + 12
    return img


def grafico(sc):
    img, d = frame(sc)
    g = Image.open(sc["img"]).convert("RGB")
    notas = sc.get("notas", [])
    gw = 1150 if notas else 1600
    gh = int(g.height * gw / g.width)
    if gh > 860:
        gh = 860
        gw = int(g.width * gh / g.height)
    g = g.resize((gw, gh), Image.LANCZOS)
    gx = 70 if notas else (W - gw) // 2
    img.paste(g, (gx, 190))
    if notas:
        x = gx + gw + 50
        y = 220
        for nt in notas:
            y = rich(d, x, y, nt, sc.get("nota_size", 36), W - x - 70) + 26
    return img


def pegadinha(sc):
    img, d = frame(sc)
    box(d, [140, 250, W - 140, H - 160], fill=(58, 30, 42), outline=COR["r"], w=6, r=30)
    d.text((200, 300), "⚠  PEGADINHA DO BLOCO", font=F(50, True), fill=COR["r"])
    rich(d, 200, 420, sc["texto"], 54, W - 400, line_h=78)
    return img


LAYOUT = {"capa": capa, "lista": lista, "calc": calc, "tabela": tabela, "grafico": grafico,
          "pegadinha": pegadinha}


def render(sc, path):
    LAYOUT[sc["tipo"]](sc).save(path)
