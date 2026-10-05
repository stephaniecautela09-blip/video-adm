"""Gráficos simples (matplotlib) no mesmo visual escuro dos slides."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

BG = "#18232e"
TXT = "#eceff4"
DIM = "#96a5b4"
Y, G, R, C = "#ffd166", "#06d6a0", "#ef476f", "#4cc9f0"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "axes.edgecolor": DIM, "axes.labelcolor": TXT, "xtick.color": TXT, "ytick.color": TXT,
    "text.color": TXT, "font.size": 17, "axes.titlesize": 20, "axes.grid": True,
    "grid.color": "#2e3f50", "grid.linewidth": 1, "font.family": "DejaVu Sans",
    "axes.spines.top": False, "axes.axisbelow": True, "axes.spines.right": False,
})


def br(v, casas=0):
    s = f"{v:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


FLUXOS = [35000, 40000, 45000, 30000]


def vpl(r):
    return sum(c / (1 + r) ** (i + 1) for i, c in enumerate(FLUXOS)) - 100000


def _save(fig, path):
    fig.savefig(path, dpi=110, bbox_inches="tight")
    plt.close(fig)


def selic_vpl(path):
    import numpy as np
    rs = np.linspace(0.04, 0.24, 200)
    fig, ax = plt.subplots(figsize=(10.5, 7))
    ax.plot(rs * 100, [vpl(r) / 1000 for r in rs], color=C, lw=4)
    ax.axhline(0, color=DIM, lw=1.5)
    for r, cor in [(0.10, G), (0.12, Y), (0.14, R)]:
        v = vpl(r)
        ax.plot(r * 100, v / 1000, "o", ms=14, color=cor)
        ax.annotate(f"{br(r*100)}% → VPL {br(v)}", (r * 100, v / 1000), xytext=(18, 12),
                    textcoords="offset points", color=cor, fontsize=17, fontweight="bold")
    ax.set_xlabel("Taxa de desconto (%)  ← Selic sobe →")
    ax.set_ylabel("VPL (R$ mil)")
    ax.set_title("Mesmo projeto, taxas diferentes")
    _save(fig, path)


def cascata(path):
    fig, ax = plt.subplots(figsize=(11, 7))
    etapas = [("FCO", 6454.20), ("− Gastos\nde capital", -7200), ("− ΔCCL", -680)]
    base = 0
    for i, (n, v) in enumerate(etapas):
        bot = base if v > 0 else base + v
        ax.bar(i, abs(v), bottom=bot, color=G if v > 0 else R, width=0.6)
        ax.text(i, base + v + (250 if v > 0 else -250), br(v, 2), ha="center",
                va="bottom" if v > 0 else "top", fontsize=17, fontweight="bold")
        base += v
    ax.bar(3, abs(base), bottom=base, color=Y, width=0.6)
    ax.text(3, base - 250, br(base, 2), ha="center", va="top", fontsize=17, fontweight="bold", color=Y)
    ax.axhline(0, color=DIM, lw=1.5)
    ax.set_xticks(range(4), [e[0] for e in etapas] + ["FC dos\nativos"])
    ax.set_ylim(-2600, 8000)
    ax.set_ylabel("R$")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: br(v)))
    ax.set_title("Dahlia: do FCO ao fluxo de caixa dos ativos")
    _save(fig, path)


def liquidez(path):
    fig, ax = plt.subplots(figsize=(10.5, 7))
    nomes = ["Corrente\nAC ÷ PC", "Seca\n(AC − Estoques) ÷ PC", "Imediata\nCaixa ÷ PC"]
    vals = [56260 / 43235, (56260 - 23084) / 43235, 5000 / 43235]
    bars = ax.bar(nomes, vals, color=[C, Y, R], width=0.6)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.03, br(v, 2), ha="center", fontsize=22, fontweight="bold")
    ax.axhline(1, color=DIM, ls="--", lw=1.5)
    ax.text(2.45, 1.02, "1,00", color=DIM, fontsize=15)
    ax.set_ylim(0, 1.5)
    ax.set_title("Marcos Golfe: do mais amplo ao mais restrito")
    _save(fig, path)


def perfil_vpl(path):
    import numpy as np
    rs = np.linspace(0.0, 0.26, 200)
    fig, ax = plt.subplots(figsize=(10.5, 7))
    ax.plot(rs * 100, [vpl(r) / 1000 for r in rs], color=C, lw=4)
    ax.axhline(0, color=DIM, lw=1.5)
    ax.plot(12, vpl(0.12) / 1000, "o", ms=14, color=G)
    ax.annotate("12% → VPL 14.233,41", (12, vpl(0.12) / 1000), xytext=(15, 10),
                textcoords="offset points", color=G, fontsize=17, fontweight="bold")
    ax.plot(18.64, 0, "o", ms=14, color=Y)
    ax.annotate("TIR = 18,64%\n(VPL = 0)", (18.64, 0), xytext=(-10, 30), textcoords="offset points",
                color=Y, fontsize=17, fontweight="bold")
    ax.set_xlabel("Taxa de desconto (%)")
    ax.set_ylabel("VPL (R$ mil)")
    ax.set_title("Perfil do VPL: a TIR é onde a curva cruza o zero")
    _save(fig, path)


def conflito(path):
    import numpy as np
    rs = np.linspace(0.0, 0.55, 200)
    fig, ax = plt.subplots(figsize=(10.5, 7))
    a = lambda r: 15000 / (1 + r) - 10000
    b = lambda r: 130000 / (1 + r) - 100000
    ax.plot(rs * 100, [a(r) / 1000 for r in rs], color=Y, lw=4, label="A: investe 10 mil (TIR 50%)")
    ax.plot(rs * 100, [b(r) / 1000 for r in rs], color=C, lw=4, label="B: investe 100 mil (TIR 30%)")
    ax.axhline(0, color=DIM, lw=1.5)
    ax.axvline(10, color=G, ls="--", lw=2)
    ax.text(10.8, 24, "taxa 10%", color=G, fontsize=17)
    ax.plot(10, a(0.1) / 1000, "o", ms=12, color=Y)
    ax.plot(10, b(0.1) / 1000, "o", ms=12, color=C)
    ax.annotate("VPL 18.182", (10, b(0.1) / 1000), xytext=(14, 2), textcoords="offset points", color=C, fontsize=16, fontweight="bold")
    ax.annotate("VPL 3.636", (10, a(0.1) / 1000), xytext=(14, -22), textcoords="offset points", color=Y, fontsize=16, fontweight="bold")
    ax.set_xlabel("Taxa de desconto (%)")
    ax.set_ylabel("VPL (R$ mil)")
    ax.legend(facecolor=BG, edgecolor=DIM, fontsize=15)
    ax.set_title("Projetos excludentes: TIR escolhe A, VPL escolhe B")
    _save(fig, path)


def cenarios(path):
    fig, ax = plt.subplots(figsize=(10.5, 7))
    nomes = ["Expansão\n(35%)", "Normal\n(50%)", "Retração\n(15%)"]
    vals = [35.0, 13.8, -20.2]
    bars = ax.bar(nomes, vals, color=[G, C, R], width=0.6)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + (1 if v > 0 else -1), br(v, 1) + "%", ha="center",
                va="bottom" if v > 0 else "top", fontsize=20, fontweight="bold")
    ax.axhline(16.12, color=Y, lw=3, ls="--")
    ax.text(2.35, 18.2, "E(R) = 16,12%", color=Y, fontsize=18, fontweight="bold", ha="right")
    ax.axhline(0, color=DIM, lw=1.5)
    ax.set_ylim(-28, 42)
    ax.set_ylabel("Retorno da carteira (%)")
    ax.set_title("Retorno da carteira em cada cenário (σ = 18,04%)")
    _save(fig, path)


def diversificacao(path):
    import numpy as np
    n = np.arange(1, 41)
    sis = 20
    tot = np.sqrt(sis ** 2 + 45 ** 2 / n)
    fig, ax = plt.subplots(figsize=(10.5, 7))
    ax.plot(n, tot, color=C, lw=4)
    ax.axhline(sis, color=Y, lw=3, ls="--")
    ax.fill_between(n, sis, tot, color=R, alpha=0.25)
    ax.fill_between(n, 0, sis, color=Y, alpha=0.12)
    ax.text(22, 31, "Não sistemático\n(some com a diversificação)", color=R, fontsize=17, fontweight="bold")
    ax.text(22, 9, "Sistemático (beta)\n(fica — é o que o mercado paga)", color=Y, fontsize=17, fontweight="bold")
    ax.set_xlabel("Número de ações na carteira")
    ax.set_ylabel("Risco da carteira, σ (%)")
    ax.set_ylim(0, 52)
    ax.set_title("Diversificar elimina só uma parte do risco")
    _save(fig, path)


def sml(path):
    import numpy as np
    rf, rm = 10.5, 16.5
    b = np.linspace(0, 2, 50)
    fig, ax = plt.subplots(figsize=(10.5, 7))
    ax.plot(b, rf + b * (rm - rf), color=C, lw=4, label="SML: E(R) = Rf + β(Rm − Rf)")
    ax.plot(0, rf, "o", ms=12, color=DIM)
    ax.annotate("Rf = 10,5%", (0, rf), xytext=(12, 6), textcoords="offset points", color=DIM, fontsize=16)
    ax.plot(1, rm, "o", ms=12, color=DIM)
    ax.annotate("Mercado (β = 1): 16,5%", (1, rm), xytext=(12, -30), textcoords="offset points", color=DIM, fontsize=16)
    ax.plot(1.15, 17.4, "o", ms=12, color=C)
    ax.plot(1.15, 18.0, "o", ms=16, color=G)
    ax.annotate("oferece 18%\nalfa = +0,6% → acima da SML\nsubvalorizada → COMPRAR", (1.15, 18.0),
                xytext=(-250, 30), textcoords="offset points", color=G, fontsize=16, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=G, lw=2))
    ax.annotate("exige 17,4%", (1.15, 17.4), xytext=(20, -22), textcoords="offset points", color=C, fontsize=16)
    ax.set_xlabel("Beta (β)")
    ax.set_ylabel("Retorno (%)")
    ax.set_xlim(-0.08, 2)
    ax.legend(loc="lower right", facecolor=BG, edgecolor=DIM, fontsize=15)
    ax.set_title("Linha do mercado de títulos (SML)")
    _save(fig, path)


def titulo(path):
    import numpy as np
    ytm = np.linspace(0.04, 0.14, 100)
    preco = lambda y: sum(80 / (1 + y) ** t for t in range(1, 11)) + 1000 / (1 + y) ** 10
    fig, ax = plt.subplots(figsize=(10.5, 7))
    ax.plot(ytm * 100, [preco(y) for y in ytm], color=C, lw=4)
    ax.axhline(1000, color=DIM, ls="--", lw=1.5)
    ax.text(4.1, 975, "valor de face 1.000", color=DIM, fontsize=15)
    for y, cor, txt in [(0.07, G, "7% → 1.070,24 (ágio)"), (0.08, DIM, "8% = cupom → 1.000"), (0.10, R, "10% → 877,11 (deságio)")]:
        ax.plot(y * 100, preco(y), "o", ms=13, color=cor)
        ax.annotate(txt, (y * 100, preco(y)), xytext=(16, 8), textcoords="offset points", color=cor, fontsize=17, fontweight="bold")
    ax.set_xlabel("Taxa de mercado / YTM (%)")
    ax.set_ylabel("Preço do título (R$)")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: br(v)))
    ax.set_title("Juros sobem → preço cai (cupom de 8%, 10 anos)")
    _save(fig, path)


def mm(path):
    fig, ax = plt.subplots(figsize=(10.5, 7))
    ax.bar(0, 281600 / 1000, color=C, width=0.55)
    ax.bar(1, 281600 / 1000, color=C, width=0.55)
    ax.bar(1, 32300 / 1000, bottom=281.6, color=G, width=0.55)
    ax.text(0, 290, "VU = 281.600", ha="center", fontsize=19, fontweight="bold")
    ax.text(1, 322, "VL = 313.900", ha="center", fontsize=19, fontweight="bold")
    ax.text(1, 297.75, "T × D = 32.300", ha="center", va="center", fontsize=15, fontweight="bold", color=BG)
    ax.set_xticks([0, 1], ["Sem dívida", "Com dívida de 95.000"])
    ax.set_ylim(0, 360)
    ax.set_ylabel("Valor da empresa (R$ mil)")
    ax.set_title("MM com impostos: VL = VU + T × D")
    _save(fig, path)


TODOS = {
    "selic_vpl": selic_vpl, "cascata": cascata, "liquidez": liquidez, "perfil_vpl": perfil_vpl,
    "conflito": conflito, "cenarios": cenarios, "diversificacao": diversificacao, "sml": sml,
    "titulo": titulo, "mm": mm,
}


def gerar(pasta):
    os.makedirs(pasta, exist_ok=True)
    out = {}
    for nome, fn in TODOS.items():
        p = os.path.join(pasta, nome + ".png")
        fn(p)
        out[nome] = p
    return out


if __name__ == "__main__":
    print(gerar("../build/graficos"))
