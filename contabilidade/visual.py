"""Peças visuais e a cena-base com sincronia de narração.

A cena-base (`Aula`) controla o tempo: `self.fala(chave)` começa uma batida do roteiro; a
duração dela é a do WAV gerado pelo Piper. Durante a batida, `self.em("trecho", anims)`
espera até o momento aproximado em que a voz diz aquele trecho e só então anima. Assim cada
número aparece na tela quando é falado. O tempo de cada batida fica registrado em
build/contabilidade/tempos/<cena>.json para o build montar o áudio e as legendas.
"""
import json
import os
import re

from manim import *  # noqa: F401,F403

import audio
from fala import normalizar

FPS = 30
FONTE = "DejaVu Sans"
BG = "#18232e"
PAINEL = "#22313f"
LINHA = "#3a4d60"
TXT = "#eceff4"
DIM = "#96a5b4"
AMA = "#ffd166"   # destaque / números-chave
VER = "#06d6a0"   # ativo, confere, certo
VERM = "#ef476f"  # passivo, erro, alerta
AZUL = "#4cc9f0"  # contabilidade / conceitos
ROXO = "#b39ddb"

PAUSA = 0.35  # silêncio depois de cada batida

ETAPAS = ["O que é", "Por que existe", "Como identificar", "Exemplo", "Na prova"]


def q(t):
    """Arredonda para um número inteiro de quadros (evita deriva entre áudio e vídeo)."""
    return max(1, round(t * FPS)) / FPS


def T(s, size=30, color=TXT, weight=NORMAL, **kw):
    return Text(s, font=FONTE, font_size=size, color=color, weight=weight, **kw)


def Tb(s, ponto, alinhar=None, x_borda=None, **kw):
    """Texto alinhado pela linha de base: posiciona uma cópia com um "|" na frente (que tem
    sempre a mesma altura) e encaixa o texto real nela, para que "Lucro líquido" e "LAIR"
    fiquem na mesma linha."""
    t = T(s, **kw)
    ref = T("|" + s, **kw)
    ref.shift(ponto - ref.get_center())
    t.shift(ref.submobjects[1].get_center() - t.submobjects[0].get_center())
    if alinhar is None:
        t.set_x(ponto[0])
    else:
        t.align_to(np.array([x_borda, 0, 0]), alinhar)
    return t


def quebra(s, n):
    """Quebra um texto em linhas de até n caracteres."""
    if "\n" in s:
        return "\n".join(quebra(x, n) for x in s.split("\n"))
    linhas, atual = [], ""
    for p in s.split():
        if atual and len(atual) + 1 + len(p) > n:
            linhas.append(atual)
            atual = p
        else:
            atual = (atual + " " + p).strip()
    linhas.append(atual)
    return "\n".join(linhas)


def P(s, n=60, size=28, color=TXT, **kw):
    """Parágrafo com quebra automática."""
    return T(quebra(s, n), size=size, color=color, line_spacing=0.9, **kw)


def caixa(m, cor=AZUL, buff=0.25, fill=PAINEL, op=1.0, raio=0.12):
    r = SurroundingRectangle(m, color=cor, buff=buff, corner_radius=raio, stroke_width=2.5)
    r.set_fill(fill, opacity=op)
    return VGroup(r, m)


def cartao(titulo, corpo, cor=AZUL, larg=4.0, n=28, size=24, alt=None, rodape=None):
    """Cartão com título colorido, texto e (opcional) rodapé; o conteúdo encolhe para caber."""
    livre = larg - 0.45

    def cabe(fazer, s, n0):
        """Quebra o texto em linhas cada vez mais curtas até caber na largura do cartão."""
        k = n0
        m = fazer(quebra(s, k))
        while m.width > livre and k > 10:
            k -= 2
            m = fazer(quebra(s, k))
        return m

    t = cabe(lambda s: T(s, size=size + 4, color=cor, weight=BOLD, line_spacing=0.85), titulo,
             max(len(titulo), 10))
    c = cabe(lambda s: T(s, size=size, color=TXT, line_spacing=0.9), corpo, n)
    g = VGroup(t, c)
    if rodape:
        g.add(T(rodape, size=size - 2, color=cor))
    g.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    if g.width > larg - 0.45:
        g.scale_to_fit_width(larg - 0.45)
    h = max(alt or 0, g.height + 0.5)
    r = RoundedRectangle(width=larg, height=h, corner_radius=0.12, color=cor, stroke_width=2.5)
    r.set_fill(PAINEL, opacity=1)
    g.move_to(r).align_to(r, LEFT).shift(RIGHT * 0.22)
    g.align_to(r, UP).shift(DOWN * 0.25)
    if rodape:
        g[2].align_to(r, DOWN).shift(UP * 0.22)
    return VGroup(r, *g)


def pilula(s, cor, size=22):
    t = T(s, size=size, color=BG, weight=BOLD)
    r = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.22, corner_radius=0.15,
                         stroke_width=0).set_fill(cor, 1)
    t.move_to(r)
    return VGroup(r, t)


class Grade(VGroup):
    """Tabela construída célula por célula.

    rotulos: textos da 1ª coluna (um por linha); colunas: cabeçalhos das demais colunas.
    As células começam vazias; `valor(i, j, s)` cria o texto da célula (i = linha, j = coluna,
    a partir de 0) já posicionado, para ser animado pela cena.
    """

    def __init__(self, rotulos, colunas, larg_rot=5.2, larg_col=2.3, alt=0.46, size=24,
                 cab_rot="", alinhar_valores=RIGHT, larg_cols=None, alts=None, n_rot=40):
        super().__init__()
        self.size = size
        self.n, self.m = len(rotulos), len(colunas)
        self.larg_cols = larg_cols or [larg_col] * self.m
        self.alts = alts or [alt] * self.n
        self.alt_cab = alt
        self.larg_rot = larg_rot
        self.alinhar = alinhar_valores
        largura = larg_rot + sum(self.larg_cols)
        altura = self.alt_cab + sum(self.alts)
        self.x0, self.y0 = -largura / 2, altura / 2
        self.largura, self.altura = largura, altura

        self.cab = VGroup()
        if cab_rot:
            self.cab.add(T(cab_rot, size=size, color=DIM).move_to(self._centro(-1, -1))
                         .align_to(self._borda_esq(-1), LEFT))
        for j, c in enumerate(colunas):
            self.cab.add(T(c, size=size, color=AZUL, weight=BOLD).move_to(self._centro(-1, j)))
        self.rot = VGroup(*[
            Tb(quebra(r, n_rot), self._centro(i, -1), LEFT, self.x0 + 0.12, size=size,
               color=TXT, line_spacing=0.8)
            for i, r in enumerate(rotulos)])
        self.linhas = VGroup()
        y = self.y0 - self.alt_cab
        self.linhas.add(Line([self.x0, y, 0], [self.x0 + largura, y, 0], color=DIM, stroke_width=2))
        for i in range(self.n - 1):
            y -= self.alts[i]
            self.linhas.add(Line([self.x0, y, 0], [self.x0 + largura, y, 0], color=LINHA,
                                 stroke_width=1))
        self.add(self.linhas, self.cab, self.rot)
        self.vals = {}

    def _x(self, j):
        if j < 0:
            return self.x0 + self.larg_rot / 2
        return self.x0 + self.larg_rot + sum(self.larg_cols[:j]) + self.larg_cols[j] / 2

    def _y(self, i):
        if i < 0:
            return self.y0 - self.alt_cab / 2
        return self.y0 - self.alt_cab - sum(self.alts[:i]) - self.alts[i] / 2

    def _centro(self, i, j):
        return np.array([self._x(j), self._y(i), 0]) + self.get_center() * 0

    def _borda_esq(self, i):
        return Dot(np.array([self.x0 + 0.12, self._y(i), 0]))

    # posições reais (depois de mover a grade)
    def ponto(self, i, j):
        desloc = self.linhas[0].get_start() - np.array([self.x0, self.y0 - self.alt_cab, 0])
        return np.array([self._x(j), self._y(i), 0]) + desloc

    def celula_ret(self, i, j, cor=AMA):
        w = self.larg_rot if j < 0 else self.larg_cols[j]
        r = Rectangle(width=w - 0.06, height=self.alts[i] - 0.04, color=cor, stroke_width=3)
        return r.move_to(self.ponto(i, j))

    def linha_ret(self, i, cor=AMA):
        r = Rectangle(width=self.largura, height=self.alts[i] - 0.02, color=cor, stroke_width=3)
        return r.move_to(self.ponto(i, -1)).align_to(self.linhas[0], LEFT)

    def valor(self, i, j, s, cor=TXT, size=None, weight=NORMAL, n=None):
        s = quebra(s, n) if n else s
        p = self.ponto(i, j)
        w = self.larg_cols[j]
        borda = {RIGHT.tobytes(): p[0] + w / 2 - 0.15, LEFT.tobytes(): p[0] - w / 2 + 0.15}
        al = None if self.alinhar is None else self.alinhar
        t = Tb(s, p, al, borda.get(al.tobytes()) if al is not None else None,
               size=size or self.size, color=cor, weight=weight, line_spacing=0.8)
        self.vals[(i, j)] = t
        return t


def lancamento(linhas, titulo=None, cor=AZUL, size=26, larg=11.5):
    """Lançamento contábil. linhas = [("D", "conta", "valor"), ("C", ...)]."""
    rows = VGroup()
    for dc, conta, v in linhas:
        c = VERM if dc == "C" else VER
        a = T(dc, size=size, color=c, weight=BOLD)
        b = T(conta, size=size)
        val = T(v, size=size, color=AMA)
        rows.add(VGroup(a, b, val))
    larg = max(larg, max(r[1].width + r[2].width for r in rows) + 2.6)
    for k, r in enumerate(rows):
        r[0].move_to([-larg / 2 + 0.5, -k * 0.62, 0])
        r[1].next_to(r[0], RIGHT, buff=0.35 + (0.5 if r[0].text == "C" else 0))
        r[2].move_to([larg / 2 - 0.4, -k * 0.62, 0]).align_to([larg / 2 - 0.3, 0, 0], RIGHT)
    g = VGroup(rows)
    if titulo:
        t = T(titulo, size=size - 2, color=cor, weight=BOLD).next_to(rows, UP, buff=0.3)
        t.align_to(rows, LEFT)
        g.add(t)
    r = RoundedRectangle(width=larg, height=g.height + 0.5, corner_radius=0.12, color=cor,
                         stroke_width=2).set_fill(PAINEL, 1).move_to(g)
    r.stretch_to_fit_width(larg).set_x(0)
    return VGroup(r, g)


class Aula(Scene):
    CENA = "c0"

    def setup(self):
        self.camera.background_color = BG
        self.T = 0.0          # relógio próprio, em quadros inteiros
        self.fim_batida = 0.0
        self.log = []
        self.chaves = [k for c in audio.CENAS if c[0] == self.CENA for k in c[2]]
        self.prox = 0
        self.titulo_atual = None
        self.faixa = None

    # ---- tempo ---------------------------------------------------------------------------
    def play(self, *anims, run_time=None, **kw):
        # Scene.wait() também passa por aqui (com uma animação Wait que já traz run_time)
        if run_time is None:
            rts = [a.run_time for a in anims if isinstance(a, Animation)]
            run_time = max(rts) if rts else 0.8
        rt = q(run_time)
        super().play(*anims, run_time=rt, **kw)
        self.T += rt

    def wait(self, t=1.0, **kw):
        if t < 1 / FPS:
            return
        super().wait(q(t), **kw)

    def fala(self, chave):
        """Encerra a batida anterior e começa a próxima do roteiro."""
        self.fecha()
        esperada = self.chaves[self.prox] if self.prox < len(self.chaves) else None
        assert chave == esperada, f"{self.CENA}: esperava [{esperada}], veio [{chave}]"
        self.prox += 1
        dur = audio.duracao(chave)
        self.log.append({"chave": chave, "inicio": self.T, "dur": dur,
                         "wav": audio.caminho(chave)})
        self.batida = {"ini": self.T, "dur": dur, "texto": audio.TEXTOS[chave], "pos": 0}
        self.fim_batida = self.T + dur + PAUSA

    def fecha(self):
        self.wait(self.fim_batida - self.T)

    def resto(self):
        return max(0.0, self.fim_batida - PAUSA - self.T)

    def instante(self, trecho):
        """Momento (s) em que a voz termina de dizer `trecho` na batida atual."""
        b = self.batida
        i = b["texto"].find(trecho, b["pos"])
        assert i >= 0, f"trecho {trecho!r} não encontrado em: {b['texto'][b['pos']:]!r}"
        fim = i + len(trecho)
        b["pos"] = i + 1   # o próximo trecho pode se sobrepor a este, mas não vir antes

        def peso(s):
            n = normalizar(s)
            return len(n) + 6 * len(re.findall(r"[.!?:]", s)) + 3 * len(re.findall(r"[,;]", s))
        frac = peso(b["texto"][:fim]) / max(1, peso(b["texto"]))
        return b["ini"] + frac * b["dur"]

    def em(self, trecho, *anims, rt=0.6, antes=0.25):
        """Toca `anims` quando a narração chegar em `trecho`."""
        alvo = self.instante(trecho) - antes
        self.wait(alvo - self.T)
        if anims:
            self.play(*anims, run_time=rt)

    def ao_longo(self, anims, rt=0.6):
        """Distribui as animações ao longo do que falta da batida."""
        n = len(anims)
        folga = max(0, self.resto() - n * rt) / (n + 1)
        for a in anims:
            self.wait(folga)
            self.play(a, run_time=rt)

    def tear_down(self):
        self.fecha()
        self.wait(0.6)
        assert self.prox == len(self.chaves), \
            f"{self.CENA}: faltou narrar {self.chaves[self.prox:]}"
        pasta = os.path.join(audio.BUILD, "tempos")
        os.makedirs(pasta, exist_ok=True)
        with open(os.path.join(pasta, f"{self.CENA}.json"), "w") as f:
            json.dump({"duracao": self.T, "batidas": self.log}, f, indent=1)
        super().tear_down()

    # ---- peças de tela ---------------------------------------------------------------------
    def abertura(self, numero, titulo, sub=""):
        n = T(f"Cena {numero}", size=30, color=AMA)
        t = T(titulo, size=50, weight=BOLD)
        if t.width > 12.5:
            t.scale_to_fit_width(12.5)
        g = VGroup(n, t)
        if sub:
            g.add(T(sub, size=30, color=DIM))
        g.arrange(DOWN, buff=0.35)
        barra = Line(LEFT * 3, RIGHT * 3, color=AMA, stroke_width=4).next_to(g, DOWN, buff=0.4)
        self.play(FadeIn(g, shift=UP * 0.3), Create(barra), run_time=1.0)
        return VGroup(g, barra)

    def cabecalho(self, s, cor=AZUL):
        t = T(s, size=30, color=cor, weight=BOLD)
        if t.width > 13.3:
            t.scale_to_fit_width(13.3)
        t.to_corner(UL, buff=0.35)
        lin = Line(LEFT, RIGHT, color=cor, stroke_width=2).set_width(t.width).next_to(
            t, DOWN, buff=0.08).align_to(t, LEFT)
        novo = VGroup(t, lin)
        if self.titulo_atual is None:
            self.play(FadeIn(novo, shift=RIGHT * 0.3), run_time=0.5)
        else:
            self.play(ReplacementTransform(self.titulo_atual, novo), run_time=0.5)
        self.titulo_atual = novo
        return novo

    def faixa_etapas(self):
        ps = VGroup(*[pilula(e, DIM, size=18) for e in ETAPAS]).arrange(RIGHT, buff=0.12)
        ps.to_corner(UR, buff=0.3)
        for p in ps:
            p[0].set_fill(PAINEL, 1)
            p[1].set_color(DIM)
        self.faixa = ps
        self.faixa_ativa = None
        return ps

    def etapa(self, k):
        """Acende a etapa k (0..4) da faixa O que é → … → Na prova."""
        if self.faixa is None:
            return
        anims = []
        for i, p in enumerate(self.faixa):
            on = i == k
            anims += [p[0].animate.set_fill(AMA if on else PAINEL, 1),
                      p[1].animate.set_color(BG if on else DIM)]
        self.play(*anims, run_time=0.35)

    def limpa(self, *manter, rt=0.5):
        keep = set(manter) | {self.titulo_atual, self.faixa}
        sai = [m for m in self.mobjects if m not in keep]
        if sai:
            self.play(*[FadeOut(m) for m in sai], run_time=rt)

    def conta(self, s, cor=AMA, y=-3.55, size=28):
        """Mostra a conta da vez na barra de baixo (substitui a anterior)."""
        t = T(s, size=size, color=cor)
        t.move_to([0, y, 0])
        if t.width > 13.4:
            t.scale_to_fit_width(13.4)
        anims = [FadeIn(t, shift=UP * 0.15)]
        if getattr(self, "_conta", None) is not None:
            anims.append(FadeOut(self._conta))
        self._conta = t
        return anims

    def sem_conta(self):
        if getattr(self, "_conta", None) is not None:
            c, self._conta = self._conta, None
            return [FadeOut(c)]
        return []

    def escreve(self, g, i, j, s, cor=TXT, **kw):
        """Animação de uma célula: o número aparece com um piscar amarelo em volta."""
        v = g.valor(i, j, s, cor=cor, **kw)
        r = g.celula_ret(i, j)
        return Succession(AnimationGroup(FadeIn(v, scale=1.3), Create(r)), FadeOut(r),
                          lag_ratio=1.0)

    def destaque(self, g, celulas, cor=AMA):
        rs = VGroup(*[g.celula_ret(i, j, cor) for i, j in celulas])
        return rs

    def rotulo(self, g, i, rt=0.4):
        self.play(FadeIn(g.rot[i], shift=RIGHT * 0.2), run_time=rt)

    def linha(self, g, i, itens, rot=True):
        """Mostra o rótulo da linha i e escreve as células no momento em que são faladas.

        itens: (trecho, j, texto[, cor]); com j=None, `texto` vai para a barra de conta."""
        if rot:
            self.rotulo(g, i)
        for it in itens:
            trecho, j, s = it[:3]
            cor = it[3] if len(it) > 3 else TXT
            if j is None:
                self.em(trecho, *self.conta(s, cor=cor if len(it) > 3 else AMA))
            else:
                self.em(trecho, self.escreve(g, i, j, s, cor))

    def dados(self, s, size=21):
        """Linha com os dados do enunciado, logo abaixo do cabeçalho."""
        t = T(s, size=size, color=DIM)
        if t.width > 13.4:
            t.scale_to_fit_width(13.4)
        t.next_to(self.titulo_atual, DOWN, buff=0.16).align_to(self.titulo_atual, LEFT)
        return t

    def tira_faixa(self):
        if self.faixa is not None:
            self.play(FadeOut(self.faixa), run_time=0.3)
            self.faixa = None

    def separador(self, g, i, cor=AMA):
        """Linha mais forte embaixo da linha i da grade (ex.: fim da DRE, começo da apuração)."""
        y = g.ponto(i, -1)[1] - g.alts[i] / 2
        x0, x1 = g.linhas[0].get_start()[0], g.linhas[0].get_end()[0]
        return Line([x0, y, 0], [x1, y, 0], color=cor, stroke_width=3)

    def varias(self, g, i, js, vals, cor=TXT, lag=0.35):
        """Escreve várias células da linha i, uma depois da outra."""
        return LaggedStart(*[self.escreve(g, i, j, v, cor) for j, v in zip(js, vals)],
                           lag_ratio=lag)

    def enunciado(self, s, n=62, size=27, y=0.2):
        c = caixa(P(s, n=n, size=size), cor=DIM, buff=0.3)
        c.move_to([0, y, 0])
        return c
