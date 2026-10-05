"""Cenas do vídeo (Manim Community). Cada classe é uma cena numerada do roteiro.md.

Render de uma cena (o build.py faz todas):
    manim -r 1920,1080 --fps 30 cenas.py Cena04
"""
from visual import *  # noqa: F401,F403


def tomada(tipo, cor):
    """Ícone de tomada (analogia de padronização/harmonização/convergência)."""
    if tipo == 0:
        corpo = Circle(radius=0.42)
        furos = VGroup(Dot(LEFT * 0.15, radius=0.06), Dot(RIGHT * 0.15, radius=0.06))
    elif tipo == 1:
        corpo = RoundedRectangle(width=0.84, height=0.84, corner_radius=0.15)
        furos = VGroup(Rectangle(width=0.06, height=0.26).shift(LEFT * 0.16),
                       Rectangle(width=0.06, height=0.26).shift(RIGHT * 0.16))
    else:
        corpo = RegularPolygon(6).scale(0.46)
        furos = VGroup(Dot(LEFT * 0.17 + DOWN * 0.08, radius=0.06),
                       Dot(RIGHT * 0.17 + DOWN * 0.08, radius=0.06), Dot(UP * 0.16, radius=0.06))
    corpo.set_stroke(cor, 3).set_fill(PAINEL, 1)
    furos.set_fill(cor, 1).set_stroke(cor, 1)
    return VGroup(corpo, furos)


def formula(partes, size=32):
    """Fórmula em três linhas: [resultado =] / [a × b ×] / [(fração)]. partes = 7 pedaços (texto, cor)."""
    ts = [T(p.strip(), size=size, color=c) for p, c in partes]
    l1 = VGroup(ts[0], ts[1]).arrange(RIGHT, buff=0.2)
    l2 = VGroup(*ts[2:6]).arrange(RIGHT, buff=0.2)
    l3 = ts[6]
    g = VGroup(l1, l2, l3).arrange(DOWN, buff=0.18)
    return VGroup(*ts).move_to(g)


class Cena01(Aula):
    CENA = "c1"

    def construct(self):
        self.fala("c1_ola")
        t1 = T("Contabilidade Avançada II", size=58, weight=BOLD)
        t2 = T("Revisão para a Aval 1", size=40, color=AMA)
        t3 = T("UFG · Ciências Contábeis · Prof. Ilirio José Rech", size=26, color=DIM)
        capa = VGroup(t1, t2, t3).arrange(DOWN, buff=0.35)
        barra = Line(LEFT * 3.5, RIGHT * 3.5, color=AMA, stroke_width=4).next_to(capa, DOWN, buff=0.4)
        self.play(FadeIn(capa, shift=UP * 0.3), Create(barra), run_time=1.2)
        self.em("sozinha", rt=0.1)
        meta = T("entender cada conceito  +  fazer as contas sozinha", size=30, color=VER)
        meta.next_to(barra, DOWN, buff=0.5)
        self.play(FadeIn(meta, shift=UP * 0.2))

        self.fala("c1_mapa")
        self.play(FadeOut(VGroup(capa, barra, meta)), run_time=0.5)
        self.cabecalho("Mapa da prova")
        dados = [("Unidade 1", "Internacionalização das normas contábeis e ESG", "OCPC 09", AZUL),
                 ("Unidade 2", "Tributos sobre o lucro", "CPC 32", AMA),
                 ("Unidade 3", "Pagamento baseado em ações  ·  Benefícios a empregados",
                  "CPC 10  ·  CPC 33", VER)]
        cards = VGroup()
        for nome, tema, norma, cor in dados:
            cards.add(cartao(nome, tema, cor=cor, larg=4.2, n=22, size=24, alt=2.8, rodape=norma))
        cards.arrange(RIGHT, buff=0.3).shift(UP * 0.5)
        for (nome, *_), c in zip(dados, cards):
            self.em(nome, FadeIn(c, shift=UP * 0.3))

        self.fala("c1_tipo")
        tipos = [("teoria", AZUL), ("teoria + cálculo", AMA), ("cálculo (PBA) + teoria (CPC 33)", VER)]
        trechos = ["só teoria", "teoria e cálculo", "são só teoria"]
        pils = VGroup()
        for (s, cor), c in zip(tipos, cards):
            p = pilula(s, cor, size=20).next_to(c, DOWN, buff=0.3)
            pils.add(p)
        for tr, p in zip(trechos, pils):
            self.em(tr, FadeIn(p, scale=1.2))

        self.fala("c1_metodo")
        self.play(FadeOut(VGroup(cards, pils)), run_time=0.5)
        faixa = VGroup(*[pilula(e, DIM, size=26) for e in ETAPAS]).arrange(RIGHT, buff=0.25)
        setas = VGroup(*[Arrow(faixa[i].get_right(), faixa[i + 1].get_left(), buff=0.03,
                               stroke_width=3, color=DIM, max_tip_length_to_length_ratio=0.5)
                         for i in range(4)])
        for p in faixa:
            p[0].set_fill(PAINEL, 1)
            p[1].set_color(DIM)
        self.play(FadeIn(faixa), FadeIn(setas), run_time=0.6)
        for tr, p in zip(["o que é", "por que existe", "como se identifica", "um exemplo",
                          "na prova"], faixa):
            self.em(tr, p[0].animate.set_fill(AMA, 1), p[1].animate.set_color(BG), rt=0.4)

        self.fala("c1_metodo2")
        nota = caixa(P('"Na prova" = o que você precisa saber responder. O material não traz '
                       'questões teóricas do professor.', n=52, size=28), cor=AMA)
        nota.next_to(faixa, DOWN, buff=0.9)
        self.em("na prova", FadeIn(nota, shift=UP * 0.2))

        self.fala("c1_avisos")
        self.play(FadeOut(VGroup(faixa, setas, nota)), run_time=0.5)
        self.cabecalho("3 avisos", cor=AMA)
        avisos = [
            ("1. Questões de treino", "As questões resolvidas foram elaboradas para treino, no "
             "estilo das listas. Não são do professor."),
            ("2. PBA e imposto", "Tratamento fiscal do PBA: Lei 12.973/14, art. 33, como "
             "diferença temporária. Confirme se o professor adota o mesmo critério."),
            ("3. Data da prova", "Confirme a data da prova com o professor."),
        ]
        acs = VGroup(*[cartao("⚠ " + a, b, cor=AMA, larg=4.2, n=24, size=22, alt=3.3)
                       for a, b in avisos]).arrange(RIGHT, buff=0.3).shift(DOWN * 0.2)
        self.em("Primeiro", FadeIn(acs[0], shift=UP * 0.3))
        self.fala("c1_avisos2")
        self.em("Segundo", FadeIn(acs[1], shift=UP * 0.3))
        self.fala("c1_avisos3")
        self.em("Terceiro", FadeIn(acs[2], shift=UP * 0.3))


class Cena02(Aula):
    CENA = "c2"

    def construct(self):
        self.fala("c2_intro")
        ab = self.abertura(2, "Unidade 1", "Internacionalização das normas contábeis e ESG")
        self.em("Primeiro", FadeOut(ab))
        self.cabecalho("Duas palavras antes de começar")
        d1 = cartao("Norma contábil", "a regra que diz como a empresa registra e apresenta os "
                    "seus números", larg=6.2, n=34, size=26, alt=2.6)
        d2 = cartao("Comparabilidade", "poder colocar duas empresas lado a lado e comparar os "
                    "números delas de forma justa", larg=6.2, n=34, size=26, alt=2.6, cor=VER)
        VGroup(d1, d2).arrange(RIGHT, buff=0.4)
        self.em("Norma contábil", FadeIn(d1, shift=UP * 0.2))
        self.em("comparabilidade", FadeIn(d2, shift=UP * 0.2))

        # --- o problema da comparabilidade
        self.fala("c2_prob_oque")
        self.limpa()
        self.cabecalho("O problema: cada país, suas normas")
        self.add(self.faixa_etapas().to_edge(DOWN, buff=0.25))
        self.etapa(0)
        f = caixa(T("mesma empresa  →  lucros diferentes conforme o país", size=32), cor=AMA)
        f.shift(UP * 1.9)
        self.em("próprias normas contábeis", FadeIn(f, shift=DOWN * 0.2))

        self.fala("c2_prob_daimler")
        self.etapa(3)
        emp = caixa(T("Daimler-Benz", size=32, weight=BOLD), cor=AZUL).shift(UP * 0.4 + LEFT * 3.3)
        al = caixa(T("Normas alemãs → LUCRO", size=26, color=VER), cor=VER)
        am = caixa(T("Normas americanas → PREJUÍZO", size=26, color=VERM), cor=VERM)
        VGroup(al, am).arrange(DOWN, buff=0.3).next_to(emp, RIGHT, buff=1.2)
        a1 = Arrow(emp.get_right(), al.get_left(), color=DIM, buff=0.1)
        a2 = Arrow(emp.get_right(), am.get_left(), color=DIM, buff=0.1)
        self.em("A Daimler-Benz", FadeIn(emp))
        self.em("normas alemãs", GrowArrow(a1), FadeIn(al))
        self.em("normas americanas", GrowArrow(a2), FadeIn(am))
        daimler = VGroup(emp, al, am, a1, a2)

        self.fala("c2_prob_sadia")
        self.play(daimler.animate.scale(0.75).shift(UP * 0.35), run_time=0.5)
        sad = caixa(T("Sadia", size=30, weight=BOLD), cor=AZUL)
        br = caixa(T("BR GAAP: uma margem", size=24), cor=DIM)
        us = caixa(T("US GAAP: outra margem", size=24), cor=DIM)
        linha_s = VGroup(sad, br, T("≠", size=40, color=AMA), us).arrange(RIGHT, buff=0.35)
        linha_s.shift(DOWN * 1.6)
        gaap = T("GAAP = conjunto de princípios contábeis aceitos num país", size=22, color=DIM)
        gaap.next_to(linha_s, DOWN, buff=0.25)
        self.em("A Sadia", FadeIn(sad))
        self.em("BR GAAP", FadeIn(br))
        self.em("US GAAP", FadeIn(linha_s[2]), FadeIn(us))
        self.em("GAAP é a sigla", FadeIn(gaap))

        self.fala("c2_prob_porque")
        self.etapa(1)
        self.play(FadeOut(VGroup(daimler, linha_s, gaap)), run_time=0.5)
        cres = caixa(P("Comércio e mercado de capitais cresceram → o investidor estrangeiro não "
                       "conseguia comparar empresas", n=48, size=28), cor=AZUL).shift(UP * 0.4)
        self.em("mercado de capitais", FadeIn(cres, shift=UP * 0.2))
        r1 = caixa(T("preço em reais", size=26), cor=VER)
        r2 = caixa(T("preço numa moeda desconhecida", size=26), cor=VERM)
        regua = VGroup(r1, T("?", size=40, color=AMA), r2).arrange(RIGHT, buff=0.5)
        regua.next_to(cres, DOWN, buff=0.6)
        self.em("Pense em comparar", FadeIn(regua, shift=UP * 0.2))
        sem = T("sem a mesma régua, não dá", size=26, color=AMA).next_to(regua, DOWN, buff=0.3)
        self.em("Sem a mesma régua", FadeIn(sem))

        self.fala("c2_prob_solucao")
        self.play(FadeOut(VGroup(regua, sem)), run_time=0.4)
        ifrs = caixa(T("IFRS: um conjunto único de normas", size=34, color=VER, weight=BOLD),
                     cor=VER).next_to(cres, DOWN, buff=0.5)
        self.em("as IFRS", FadeIn(ifrs, scale=1.1))
        self.etapa(4)
        prova = T("Na prova: motivo = comparabilidade · exemplos: Daimler-Benz e Sadia",
                  size=26, color=AMA).next_to(ifrs, DOWN, buff=0.5)
        self.em("Na prova", FadeIn(prova))

        # --- code law x common law
        self.fala("c2_law_oque")
        self.limpa()
        self.cabecalho("Code law × common law")
        self.etapa(0)
        rot = ["O que é", "Quem faz a norma", "Usuário principal", "Estilo", "Ideia central",
               "Países"]
        g = Grade(rot, ["Code law", "Common law"], larg_rot=3.0, larg_cols=[5.0, 5.0],
                  alts=[0.85, 0.62, 0.62, 0.62, 0.85, 0.85], alt=0.6, size=22,
                  alinhar_valores=LEFT)
        g.move_to(UP * 0.35)
        self.play(FadeIn(g.linhas), FadeIn(g.cab), run_time=0.6)
        cel = [
            ("Direito codificado: a lei diz tudo", "Direito baseado em costumes e princípios"),
            ("O governo, por lei", "Organismos privados (ex.: FASB)"),
            ("Credor (e o Fisco)", "Investidor"),
            ("Baseado em regras", "Baseado em princípios"),
            ("Conservadorismo, “imagem fiel” à lei", "Essência sobre a forma, true and fair view"),
            ("Brasil (antes), Alemanha, França, Itália", "EUA, Inglaterra, Canadá, Austrália"),
        ]
        chaves = [("c2_law_oque", "No code law", "No common law"),
                  ("c2_law_quem", "No code law", "No common law"),
                  ("c2_law_usuario", "No code law", "No common law"),
                  ("c2_law_estilo", "Code law", "Common law"),
                  ("c2_law_ideia", "No code law", "No common law"),
                  ("c2_law_paises", "Code law", "Common law")]
        for i, ((k, tr1, tr2), (a, b)) in enumerate(zip(chaves, cel)):
            if i:
                self.fala(k)
            self.rotulo(g, i)
            self.em(tr1, self.escreve(g, i, 0, a, n=31), rt=0.5)
            self.em(tr2, self.escreve(g, i, 1, b, n=31), rt=0.5)
            if k == "c2_law_ideia":
                ess = T("essência sobre a forma = registrar o que a operação realmente é",
                        size=22, color=AMA).to_edge(DOWN, buff=1.0)
                self.em("Essência sobre a forma quer dizer", FadeIn(ess))
        self.fala("c2_law_ident")
        self.play(FadeOut(ess), run_time=0.3)
        self.etapa(2)
        col1 = Rectangle(width=5.0, height=g.altura, color=AZUL, stroke_width=4).move_to(
            g.ponto(0, 0)).align_to(g.linhas[0], UP).shift(UP * g.alt_cab)
        col2 = col1.copy().set_color(VER).move_to(g.ponto(0, 1)).align_to(col1, UP)
        self.em("é code law", Create(col1))
        self.em("é common law", Create(col2))
        self.em("Daimler-Benz", Indicate(g.vals[(5, 0)], color=AMA, scale_factor=1.1),
                Indicate(g.vals[(5, 1)], color=AMA, scale_factor=1.1), rt=1.2)

        self.fala("c2_law_prova")
        self.etapa(4)
        prob = caixa(T("Problema do code law: a lei é difícil de mudar e não acompanha os negócios",
                       size=24, color=VERM), cor=VERM).to_edge(DOWN, buff=0.85)
        self.play(FadeOut(col1), FadeOut(col2), FadeIn(prob, shift=UP * 0.2), run_time=0.6)

        # --- padronização, harmonização, convergência
        self.fala("c2_phc_intro")
        self.limpa()
        self.cabecalho("Padronização · harmonização · convergência")
        self.etapa(0)
        nomes = ["Padronização", "Harmonização", "Convergência"]
        cores = [AZUL, AMA, VER]
        ys = [1.8, 0.0, -1.8]
        tits = VGroup(*[T(n, size=30, color=c, weight=BOLD).move_to([-4.8, y, 0])
                        for n, c, y in zip(nomes, cores, ys)])
        dica = T("analogia: as tomadas elétricas de vários países", size=26, color=DIM)
        dica.move_to(UP * 2.9 + RIGHT * 2.5)
        self.em("tomadas elétricas", FadeIn(dica))

        self.fala("c2_pad")
        pad = VGroup(*[tomada(0, AZUL) for _ in range(3)]).arrange(RIGHT, buff=0.6)
        pad.move_to([-0.6, ys[0], 0])
        tx_pad = T("mesma regra, sem flexibilidade", size=22, color=DIM).next_to(pad, RIGHT, 0.5)
        self.em("Padronização", FadeIn(tits[0]))
        self.em("sem flexibilidade", FadeIn(pad, lag_ratio=0.3), FadeIn(tx_pad), rt=0.8)

        self.fala("c2_harm")
        har = VGroup(*[tomada(k, AMA) for k in range(3)]).arrange(RIGHT, buff=0.6)
        har.move_to([-0.6, ys[1], 0])
        adapt = VGroup(*[T("⇄", size=30, color=AMA).move_to((har[k].get_right() + har[k + 1].get_left()) / 2)
                         for k in range(2)])
        tx_har = T("cada um com a sua, reconciliável", size=22, color=DIM).next_to(har, RIGHT, 0.5)
        self.em("Harmonização", FadeIn(tits[1]))
        self.em("particularidades", FadeIn(har, lag_ratio=0.3))
        self.em("adaptador", FadeIn(adapt), FadeIn(tx_har))

        self.fala("c2_conv")
        conv = VGroup(*[tomada(k, VER) for k in range(3)]).arrange(RIGHT, buff=0.6)
        conv.move_to([-0.6, ys[2], 0])
        ref = tomada(2, AMA).scale(0.8)
        ref_t = VGroup(ref, T("referencial", size=20, color=AMA)).arrange(DOWN, buff=0.1)
        ref_t.move_to([4.6, ys[2], 0])
        self.em("Convergência", FadeIn(tits[2]), FadeIn(conv))
        self.em("mesmo referencial", FadeIn(ref_t))
        alvo = VGroup(*[tomada(2, VER).move_to(c) for c in conv])
        self.em("modelo de referência", *[Transform(conv[k], alvo[k]) for k in range(3)], rt=1.5)
        iasb = pilula("adotado pelo IASB a partir de 2000", VER, size=20).next_to(conv, DOWN, 0.3)
        self.em("a partir de 2000", FadeIn(iasb))

        self.fala("c2_phc_prova")
        self.etapa(4)
        res = VGroup(T("sem flexibilidade", size=24, color=AZUL),
                     T("mantém diferenças, reconcilia", size=24, color=AMA),
                     T("reduz diferenças → referencial comum", size=24, color=VER))
        for r, linha_ in zip(res, [pad, har, conv]):
            r.next_to(linha_, RIGHT, buff=0.6)
        self.play(FadeOut(VGroup(tx_pad, tx_har, ref_t)), run_time=0.3)
        for tr, r in zip(["padronização não tem", "Harmonização mantém", "Convergência reduz"], res):
            self.em(tr, FadeIn(r, shift=LEFT * 0.2))

        # --- linha do tempo
        self.fala("c2_tl_intro")
        self.limpa()
        self.cabecalho("Linha do tempo")
        self.etapa(3)
        eixo = Line(LEFT * 6.4, RIGHT * 6.4, color=DIM, stroke_width=4).shift(UP * 1.2)
        self.play(Create(eixo), run_time=0.8)
        marcos = [
            ("1973", "criação do IASC (antecessor do IASB)"),
            ("2000", "IASC vira IASB (ONG); IOSCO recomenda as IAS"),
            ("2005", "União Europeia: IAS obrigatórias nas consolidadas"),
            ("2007", "Lei 11.638/07: convergência, Fisco separado, essência sobre a forma"),
            ("2010", "normas do CPC baseadas nas IFRS entram em vigor"),
        ]
        xs = [-5.4, -2.7, 0, 2.7, 5.4]
        for k, ((ano, txt), x) in enumerate(zip(marcos, xs)):
            chave = ["c2_tl_1973", "c2_tl_2000", "c2_tl_2005", "c2_tl_2007", "c2_tl_2010"][k]
            self.fala(chave)
            ponto = Dot([x, 1.2, 0], radius=0.12, color=AMA)
            a = T(ano, size=34, color=AMA, weight=BOLD).next_to(ponto, UP, buff=0.25)
            d = P(txt, n=17, size=21).next_to(ponto, DOWN, buff=0.35)
            self.play(FadeIn(ponto, scale=2), FadeIn(a, shift=DOWN * 0.2), run_time=0.5)
            self.play(FadeIn(d, shift=UP * 0.1), run_time=0.5)
            if ano == "2000":
                iosco = T("IOSCO = organização internacional dos reguladores de mercados de valores",
                          size=20, color=DIM).to_edge(DOWN, buff=1.0)
                self.em("a IOSCO", FadeIn(iosco))
            if ano == "2005":
                self.play(FadeOut(iosco), run_time=0.3)
                cons = T("consolidadas = empresa-mãe + controladas, como se fossem uma só",
                         size=20, color=DIM).to_edge(DOWN, buff=1.0)
                self.em("Demonstrações consolidadas são", FadeIn(cons))
            if ano == "2007":
                self.play(FadeOut(cons), run_time=0.3)
                elo = caixa(T("separar o Fisco → diferenças contabilidade × Fisco → Unidade 2",
                              size=22, color=AMA), cor=AMA, buff=0.15).to_edge(DOWN, buff=0.95)
                self.em("Guarde a separação do Fisco", FadeIn(elo, shift=UP * 0.2))
        self.fala("c2_tl_prova")
        self.etapa(4)
        self.play(FadeOut(elo), run_time=0.3)
        mem = T("73 IASC · 2000 IASB · 2005 Europa · 2007 lei brasileira · 2010 CPCs em vigor",
                size=24, color=AMA).to_edge(DOWN, buff=1.0)
        self.play(FadeIn(mem, shift=UP * 0.2), run_time=0.6)

        # --- CPC, ICPC, OCPC
        self.fala("c2_cpc_oque")
        self.limpa()
        self.cabecalho("CPC × ICPC × OCPC")
        self.etapa(0)
        dados = [("CPC — Pronunciamento", "A norma em si. Define reconhecimento (quando registrar), "
                  "mensuração (por quanto) e divulgação (o que mostrar).", "≈ IAS / IFRS", AZUL,
                  "regra do jogo"),
                 ("ICPC — Interpretação", "Esclarece dúvidas de um CPC, para evitar interpretações "
                  "diferentes.", "≈ IFRIC / SIC", AMA, "árbitro esclarecendo"),
                 ("OCPC — Orientação", "Guia prático de aplicação. Não é norma nova.",
                  "ex.: OCPC 09", VER, "manual de dicas")]
        cs = VGroup()
        for tit, corpo, eq, cor, _ in dados:
            cs.add(cartao(tit, corpo, cor=cor, larg=4.25, n=24, size=22, alt=3.6, rodape=eq))
        cs.arrange(RIGHT, buff=0.25).shift(UP * 0.5)
        sub = T("CPC = Comitê de Pronunciamentos Contábeis: emite três tipos de documento",
                size=24, color=DIM).next_to(cs, UP, buff=0.3)
        self.em("Comitê de Pronunciamentos Contábeis", FadeIn(sub))
        self.fala("c2_cpc_cpc")
        self.em("Pronunciamento", FadeIn(cs[0][:3], shift=UP * 0.2))
        self.em("Equivale", FadeIn(cs[0][3]))
        self.fala("c2_cpc_icpc")
        self.em("Interpretação", FadeIn(cs[1][:3], shift=UP * 0.2))
        self.em("Equivale", FadeIn(cs[1][3]))
        self.fala("c2_cpc_ocpc")
        self.em("Orientação", FadeIn(cs[2][:3], shift=UP * 0.2))
        self.em("Não é norma nova", FadeIn(cs[2][3]))
        ana = VGroup(*[pilula(d[4], d[3], size=20).next_to(c, DOWN, buff=0.25)
                       for d, c in zip(dados, cs)])
        for tr, p in zip(["regra do jogo", "árbitro", "manual de dicas"], ana):
            self.em(tr, FadeIn(p, scale=1.2))
        self.fala("c2_cpc_prova")
        self.etapa(2)
        for tr, c in zip(["? CPC", "? ICPC", "? OCPC"], cs):
            self.em(tr, Indicate(c[0], color=AMA, scale_factor=1.04))
        self.em("é uma orientação", Indicate(cs[2][3], color=AMA, scale_factor=1.3), rt=1.0)

        # --- IASB, ISSB, ESG, Relato Integrado
        self.fala("c2_iasb")
        self.limpa()
        self.cabecalho("Quem emite as normas internacionais")
        self.etapa(0)
        cm = caixa(T("Conselho de Monitoramento", size=24), cor=DIM)
        fu = caixa(T("Fundação IFRS", size=26, weight=BOLD), cor=AZUL)
        ia = caixa(T("IASB → IFRS (normas contábeis)", size=26, color=AZUL), cor=AZUL)
        pilha = VGroup(cm, fu, ia).arrange(DOWN, buff=0.7).shift(LEFT * 3.4 + UP * 0.3)
        s1 = Arrow(cm.get_bottom(), fu.get_top(), buff=0.05, color=DIM)
        s2 = Arrow(fu.get_bottom(), ia.get_top(), buff=0.05, color=DIM)
        sup = T("supervisiona", size=20, color=DIM).next_to(s1, RIGHT, buff=0.15)
        self.em("O IASB emite", FadeIn(ia))
        self.em("Fundação IFRS", FadeIn(fu), GrowArrow(s2))
        self.em("Conselho de Monitoramento", FadeIn(cm), GrowArrow(s1), FadeIn(sup))

        self.fala("c2_issb")
        issb = cartao("ISSB → sustentabilidade", "IFRS S1: requisitos gerais\nIFRS S2: clima\n"
                      "Foco: o investidor", cor=VER, larg=5.4, n=40, size=24)
        issb.shift(RIGHT * 3.3 + UP * 0.9)
        self.em("O ISSB", FadeIn(issb[:2]))
        self.em("IFRS S1", FadeIn(issb[2], shift=UP * 0.1))

        self.fala("c2_esg")
        esg = VGroup(*[VGroup(T(l, size=44, color=c, weight=BOLD), T(w, size=22))
                       .arrange(DOWN, buff=0.1) for l, w, c in
                       [("E", "ambiental", VER), ("S", "social", AMA), ("G", "governança", AZUL)]])
        esg.arrange(RIGHT, buff=0.6).next_to(issb, DOWN, buff=0.45)
        self.em("ESG significa", FadeIn(esg, lag_ratio=0.3), rt=1.0)
        alem = T("riscos e impactos além dos números financeiros", size=22, color=AMA)
        alem.next_to(esg, DOWN, buff=0.3)
        self.em("além dos números financeiros", FadeIn(alem))
        self.etapa(1)

        self.fala("c2_ri")
        self.limpa()
        self.cabecalho("Relato Integrado (OCPC 09)")
        self.etapa(0)
        centro = caixa(P("como a empresa cria valor", n=14, size=26, color=AMA), cor=AMA)
        caps = ["Financeiro", "Manufaturado", "Intelectual", "Humano", "Social e de\nrelacionamento",
                "Natural"]
        dicas = ["dinheiro", "máquinas", "conhecimento", "pessoas", "relações", "natureza"]
        cores6 = [AMA, AZUL, ROXO, VER, VERM, VER]
        circ = VGroup()
        for k, (cname, cor) in enumerate(zip(caps, cores6)):
            ang = PI / 2 - k * TAU / 6
            pos = np.array([np.cos(ang) * 3.7, np.sin(ang) * 2.0 + 0.1, 0])
            cc = Circle(radius=0.85, color=cor, stroke_width=3).set_fill(PAINEL, 1).move_to(pos)
            tt = T(cname, size=19, color=cor).move_to(pos)
            if tt.width > 1.5:
                tt.scale_to_fit_width(1.5)
            circ.add(VGroup(cc, tt))
        centro.move_to([0, 0.1, 0])
        self.em("cria valor", FadeIn(centro))
        tr6 = ["Financeiro", "manufaturado", "intelectual", "humano", "social e de relacionamento",
               "natural"]
        for tr, c in zip(tr6, circ):
            self.em(tr, FadeIn(c, scale=0.7), rt=0.4)
        self.fala("c2_ri_dica")
        self.etapa(4)
        dts = VGroup(*[T(d, size=20, color=DIM).next_to(c, DOWN, buff=0.05) for d, c in zip(dicas, circ)])
        for d, tr in zip(dts, dicas):
            self.em(tr, FadeIn(d), rt=0.3)


class Cena03(Aula):
    CENA = "c3"

    def construct(self):
        self.fala("c3_intro")
        ab = self.abertura(3, "Unidade 2 — Tributos sobre o lucro", "CPC 32: os conceitos")
        self.em("vamos devagar", FadeOut(ab))
        self.cabecalho("Os impostos sobre o lucro")
        ir = cartao("IR", "imposto de renda", larg=4.0, size=28, alt=1.7)
        cs = cartao("CSLL", "contribuição social sobre o lucro líquido", larg=6.0, n=30, size=28,
                    alt=1.7, cor=VER)
        VGroup(ir, cs).arrange(RIGHT, buff=0.4).shift(UP * 1.4)
        self.em("imposto de renda", FadeIn(ir, shift=UP * 0.2))
        self.em("lucro líquido", FadeIn(cs, shift=UP * 0.2))
        al = caixa(T("IR + CSLL = 34%  (questões de treino)", size=32, color=AMA), cor=AMA)
        al.next_to(VGroup(ir, cs), DOWN, buff=0.5)
        self.em("34%", FadeIn(al, scale=1.1))

        self.fala("c3_lair")
        la = cartao("LAIR", "lucro antes do imposto de renda: o lucro da contabilidade",
                    larg=6.0, n=30, size=26, alt=2.0, cor=AZUL)
        lr = cartao("Lucro real", "o lucro pelas regras do Fisco: base do imposto a pagar",
                    larg=6.0, n=30, size=26, alt=2.0, cor=VERM)
        VGroup(la, lr).arrange(RIGHT, buff=0.4).next_to(al, DOWN, buff=0.45)
        self.em("LAIR é", FadeIn(la, shift=UP * 0.2))
        self.em("lucro real", FadeIn(lr, shift=UP * 0.2))

        self.fala("c3_porque")
        self.limpa()
        self.cabecalho("Por que existe o CPC 32")
        self.add(self.faixa_etapas().to_edge(DOWN, buff=0.25))
        self.etapa(1)
        cont = caixa(T("Contabilidade\nsegue o CPC", size=30, color=AZUL), cor=AZUL).shift(LEFT * 3.5 + UP * 1.2)
        fis = caixa(T("Fisco\nsegue a lei fiscal", size=30, color=VERM), cor=VERM).shift(RIGHT * 3.5 + UP * 1.2)
        self.em("A contabilidade segue o CPC", FadeIn(cont))
        self.em("a lei fiscal", FadeIn(fis))
        d1 = T("mesma despesa, anos diferentes", size=26, color=AMA).shift(DOWN * 0.4)
        d2 = T("despesa que o Fisco não aceita", size=26, color=AMA).shift(DOWN * 1.2)
        self.em("anos diferentes", FadeIn(d1, shift=UP * 0.2))
        self.em("não aceita uma despesa", FadeIn(d2, shift=UP * 0.2))
        mid = T("≠", size=60, color=AMA).move_to(UP * 1.2)
        self.play(FadeIn(mid), run_time=0.4)

        self.fala("c3_corrente")
        self.limpa()
        self.cabecalho("Corrente × diferido")
        self.etapa(0)
        co = cartao("Tributo corrente", "o IR/CSLL que a empresa realmente paga (ou recupera) "
                    "sobre o lucro fiscal do período", cor=AMA, larg=6.1, n=32, size=26, alt=2.6)
        di = cartao("Tributo diferido", "o IR/CSLL que será pago ou recuperado em anos futuros, "
                    "por diferenças entre contabilidade e Fisco", cor=AZUL, larg=6.1, n=32,
                    size=26, alt=2.6)
        VGroup(co, di).arrange(RIGHT, buff=0.35).shift(UP * 1.55)
        self.em("Tributo corrente", FadeIn(co, shift=UP * 0.2))
        hoje = pilula("a conta de hoje", AMA).next_to(co, DOWN, buff=0.25)
        self.em("a conta de hoje", FadeIn(hoje))
        self.fala("c3_diferido")
        self.em("Tributo diferido", FadeIn(di, shift=UP * 0.2))
        dep = pilula("a conta que fica para depois", AZUL).next_to(di, DOWN, buff=0.25)
        self.em("fica para depois", FadeIn(dep))

        self.fala("c3_base")
        base = cartao("Base fiscal", "o valor que o Fisco reconhece para um ativo ou passivo",
                      cor=VER, larg=12.5, n=70, size=26)
        base.next_to(VGroup(hoje, dep), DOWN, buff=0.3)
        self.em("Base fiscal", FadeIn(base, shift=UP * 0.2))
        ex = T("máquina já deduzida: base fiscal = 0   ·   contabilidade: valor contábil maior",
               size=22, color=AMA).next_to(base, DOWN, buff=0.22)
        self.em("Essa é a base fiscal", FadeIn(ex))
        self.em("valor contábil", Indicate(ex, color=AMA, scale_factor=1.04))

        self.fala("c3_perm")
        self.limpa()
        self.cabecalho("Permanente × temporária")
        pe = cartao("Diferença permanente", "despesa que o Fisco nunca aceita, ou receita que "
                    "nunca tributa. Ex.: multas, equivalência patrimonial.", cor=VERM, larg=6.1,
                    n=32, size=25, alt=2.9)
        te = cartao("Diferença temporária", "contabilidade e Fisco reconhecem o mesmo valor, mas "
                    "em anos diferentes. Uma hora se anula.", cor=VER, larg=6.1, n=32, size=25,
                    alt=2.9)
        VGroup(pe, te).arrange(RIGHT, buff=0.35).shift(UP * 1.25)
        self.em("Diferença permanente", FadeIn(pe, shift=UP * 0.2))
        eq = T("equivalência patrimonial = resultado da participação em outra empresa", size=21,
               color=DIM).next_to(VGroup(pe, te), DOWN, buff=0.95)
        self.em("participação que tem em outra empresa", FadeIn(eq))
        n1 = pilula("NÃO gera diferido", VERM, size=24).next_to(pe, DOWN, buff=0.3)
        self.em("não gera diferido", FadeIn(n1, scale=1.2))
        self.fala("c3_temp")
        self.em("Diferença temporária", FadeIn(te, shift=UP * 0.2))
        n2 = pilula("GERA diferido", VER, size=24).next_to(te, DOWN, buff=0.3)
        self.em("gera diferido", FadeIn(n2, scale=1.2))

        self.fala("c3_ident")
        self.etapa(2)
        self.play(FadeOut(eq), run_time=0.3)
        per = caixa(T("Um dia o Fisco vai aceitar isso?", size=28, color=AMA), cor=AMA, buff=0.15)
        per.move_to(DOWN * 1.35)
        self.em("um dia o Fisco vai aceitar isso", FadeIn(per, shift=UP * 0.2))
        r1 = T("“nunca” → permanente", size=24, color=VERM)
        r2 = T("“sim, em outro ano” → temporária", size=24, color=VER)
        r1.move_to([pe.get_x(), -2.3, 0])
        r2.move_to([te.get_x(), -2.3, 0])
        self.em("é permanente", FadeIn(r1))
        self.em("é temporária", FadeIn(r2))

        # --- ativo x passivo diferido
        self.fala("c3_logica")
        self.limpa()
        self.cabecalho("Quando nasce passivo e quando nasce ativo diferido")
        self.etapa(1)
        cab = VGroup(T("Hoje", size=28, color=DIM), T("Futuro", size=28, color=DIM))
        cab[0].move_to([1.0, 2.3, 0])
        cab[1].move_to([4.2, 2.3, 0])
        self.play(FadeIn(cab), run_time=0.4)
        l1 = T("Fisco deixa deduzir ANTES", size=26).move_to([-3.6, 1.2, 0])
        h1 = T("pago menos ↓", size=28, color=VER).move_to([1.0, 1.2, 0])
        f1 = T("pago mais ↑", size=28, color=VERM).move_to([4.2, 1.2, 0])
        p1 = caixa(T("PASSIVO fiscal diferido: dívida com o Fisco que fica para depois", size=26,
                     color=VERM), cor=VERM, buff=0.18).move_to([0, 0.25, 0])
        self.em("deduzir antes da contabilidade", FadeIn(l1))
        self.em("hoje pago menos imposto", FadeIn(h1))
        self.em("vou pagar mais", FadeIn(f1))
        self.em("passivo fiscal diferido", FadeIn(p1, shift=UP * 0.2))
        self.fala("c3_logica2")
        l2 = T("Fisco só deixa deduzir DEPOIS", size=26).move_to([-3.6, -1.2, 0])
        h2 = T("pago mais ↑", size=28, color=VERM).move_to([1.0, -1.2, 0])
        f2 = T("recupero ↓", size=28, color=VER).move_to([4.2, -1.2, 0])
        p2 = caixa(T("ATIVO fiscal diferido: crédito que vou receber do Fisco no futuro", size=26,
                     color=VER), cor=VER, buff=0.18).move_to([0, -2.15, 0])
        self.em("deduzir depois", FadeIn(l2))
        self.em("hoje pago mais imposto", FadeIn(h2))
        self.em("recupero", FadeIn(f2))
        self.em("ativo fiscal diferido", FadeIn(p2, shift=UP * 0.2))

        # --- quadro das 5 situações
        self.fala("c3_tab_intro")
        self.limpa()
        self.cabecalho("As 5 situações")
        self.etapa(2)
        rot = ["Ativo com valor contábil maior que a base fiscal",
               "Ativo com valor contábil menor que a base fiscal",
               "Passivo com valor contábil maior que a base fiscal",
               "Passivo com valor contábil menor que a base fiscal",
               "Prejuízo fiscal a compensar"]
        g = Grade(rot, ["Diferença temporária", "Nasce"], larg_rot=7.3, larg_cols=[3.0, 3.4],
                  alt=0.62, size=22, alinhar_valores=None, n_rot=70)
        g.move_to(UP * 0.55)
        self.play(FadeIn(g.linhas), FadeIn(g.cab), run_time=0.5)
        defs = VGroup(T("tributável = imposto a mais no futuro", size=22, color=VERM),
                      T("dedutível = imposto a menos no futuro", size=22, color=VER)
                      ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=1.0)
        self.em("tributável", FadeIn(defs[0]))
        self.em("dedutível", FadeIn(defs[1]))
        linhas = [("c3_tab1", "Tributável", "Passivo fiscal diferido", "A diferença é tributável",
                   "nasce passivo fiscal diferido"),
                  ("c3_tab2", "Dedutível", "Ativo fiscal diferido", "Diferença dedutível",
                   "nasce ativo fiscal diferido"),
                  ("c3_tab3", "Dedutível", "Ativo fiscal diferido", "Dedutível", "nasce ativo"),
                  ("c3_tab4", "Tributável", "Passivo fiscal diferido", "Tributável", "nasce passivo"),
                  ("c3_tab5", "Dedutível", "Ativo fiscal diferido", "dedutível", "gera ativo")]
        for i, (k, dt, nasce, tr1, tr2) in enumerate(linhas):
            self.fala(k)
            self.rotulo(g, i)
            if k == "c3_tab5":
                pf = T("prejuízo fiscal = lucro real negativo", size=22, color=DIM)
                pf.to_edge(DOWN, buff=1.0)
                self.em("dá negativo", FadeOut(tag1), FadeIn(pf))
            self.em(tr1, self.escreve(g, i, 0, dt, VERM if dt == "Tributável" else VER))
            self.em(tr2, self.escreve(g, i, 1, nasce, VERM if "Passivo" in nasce else VER))
            if k == "c3_tab1":
                self.em("depreciação acelerada", FadeOut(defs), rt=0.3)
                tag1 = T("ex.: depreciação acelerada → passivo", size=22, color=AMA)
                tag1.to_edge(DOWN, buff=1.0)
                self.play(FadeIn(tag1), run_time=0.4)

        self.fala("c3_tab_dica")
        self.etapa(4)
        at = T("atalho: ativo e passivo se comportam ao contrário", size=24, color=AMA)
        at.to_edge(DOWN, buff=1.0)
        self.em("ao contrário", FadeOut(pf), FadeIn(at))
        exs = T("depreciação acelerada → passivo   ·   PECLD e provisões → ativo", size=24,
                color=AMA).to_edge(DOWN, buff=1.0)
        self.em("PECLD e provisões geram ativo", FadeOut(at), FadeIn(exs))
        self.em("custam nota", Indicate(exs, color=VERM, scale_factor=1.05), rt=1.0)

        # --- regras do CPC 32
        self.fala("c3_regras")
        self.limpa()
        self.cabecalho("As 4 regras do CPC 32")
        self.etapa(0)
        regras = [("1. Ativo diferido", "só se for provável haver lucro tributável futuro para usá-lo"),
                  ("2. Alíquota", "vigente ou já aprovada (34% IR + CSLL). Sem ajuste a valor "
                   "presente no diferido."),
                  ("3. ORA / PL", "item registrado em ORA ou no PL: o diferido também vai para lá, "
                   "não para o resultado (ex.: ganhos atuariais)"),
                  ("4. Exceções", "não se reconhece passivo diferido no reconhecimento inicial de "
                   "goodwill e de certos itens que não afetam nenhum lucro na origem")]
        rc = VGroup(*[cartao(a, b, cor=c, larg=6.3, n=42, size=21, alt=2.25)
                      for (a, b), c in zip(regras, [VER, AMA, ROXO, VERM])])
        rc.arrange_in_grid(2, 2, buff=0.25).shift(UP * 0.35)
        for k, card in zip(["c3_r1", "c3_r2", "c3_r3", "c3_r4"], rc):
            self.fala(k)
            self.play(FadeIn(card, shift=UP * 0.2), run_time=0.6)
            if k == "c3_r3":
                ora = caixa(T("ORA = outros resultados abrangentes: ganhos e perdas no PL, fora "
                              "da DRE", size=21, color=ROXO), cor=ROXO, buff=0.12)
                ora.to_edge(DOWN, buff=0.75)
                self.em("ORA quer dizer", FadeIn(ora))
            if k == "c3_r4":
                gw = caixa(T("goodwill = valor pago a mais na compra de uma empresa", size=21,
                             color=VERM), cor=VERM, buff=0.12).to_edge(DOWN, buff=0.75)
                self.em("goodwill", FadeOut(ora), FadeIn(gw))
                sem = caixa(T("o material só lista as exceções, sem exemplo numérico", size=21,
                              color=DIM), cor=DIM, buff=0.12).move_to(gw)
                self.em("sem exemplo numérico", FadeOut(gw), FadeIn(sem))

        # --- método de 8 passos
        self.fala("c3_m1")
        self.limpa()
        self.cabecalho("Como calcular: método do resultado (modelo do professor)")
        self.etapa(3)
        passos = ["Monte a DRE contábil até o LAIR",
                  "(+) Adições: despesas que o Fisco não aceita agora",
                  "(−) Exclusões: deduções que o Fisco permite e a contabilidade não registrou",
                  "(−) Compensação de prejuízo fiscal: trava de 30% do lucro real",
                  "= Lucro real × 34% = IR corrente",
                  "Diferido: diferença temporária × 34%",
                  "Lance a VARIAÇÃO do saldo de diferido, não o saldo",
                  "Prova dos nove: sem permanentes, IR total = 34% × LAIR"]
        cores = [TXT, TXT, TXT, VERM, AMA, AZUL, AZUL, VER]
        itens = VGroup()
        for k, (s, c) in enumerate(zip(passos, cores)):
            n = T(f"{k + 1}", size=26, color=BG, weight=BOLD)
            bola = Circle(radius=0.24, color=c, stroke_width=0).set_fill(c, 1)
            n.move_to(bola)
            it = VGroup(VGroup(bola, n), T(s, size=25, color=c)).arrange(RIGHT, buff=0.3)
            if it.width > 12.4:
                it.scale_to_fit_width(12.4)
            itens.add(it)
        itens.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(DOWN * 0.15).to_edge(LEFT, buff=1.0)
        for k, it in enumerate(itens):
            if k:
                self.fala(f"c3_m{k + 1}")
            self.play(FadeIn(it, shift=RIGHT * 0.3), run_time=0.5)
            if k == 3:
                self.em("erro clássico", Indicate(it, color=VERM, scale_factor=1.04), rt=0.9)
            if k == 7:
                self.em("todas as questões de imposto", Indicate(it, color=VER, scale_factor=1.05),
                        rt=1.0)


class Cena04(Aula):
    CENA = "c4"

    def construct(self):
        # ---------------------------------------------------------------- trator (slide do professor)
        self.fala("c4_intro")
        ab = self.abertura(4, "Unidade 2 — Contas de tributo diferido", "Trator · A1 · A2")
        self.em("slide do próprio professor", FadeOut(ab))
        a1 = caixa(P("Exemplo do trator: slide do professor, alíquota de 30%. É a exceção.",
                     n=40, size=30, color=AMA), cor=AMA).shift(UP * 0.9)
        a2 = caixa(P("Questões de treino A1, A2, B1, B2, C1 e C2: alíquota de 34%.", n=40,
                     size=30, color=VER), cor=VER).next_to(a1, DOWN, buff=0.5)
        self.em("Atenção", FadeIn(a1, shift=UP * 0.2))
        self.em("usam 34%", FadeIn(a2, shift=UP * 0.2))

        self.fala("c4_enunc")
        self.limpa()
        self.cabecalho("Exemplo do trator (slide do professor)")
        itens = [("trator de R$ 600.000", "Trator: R$ 600.000, vida útil de 3 anos"),
                 ("tudo no ano 1", "Fisco: permite deduzir tudo no ano 1"),
                 ("200.000 por ano", "Contabilidade: deprecia 200.000 por ano"),
                 ("1.000.000 por ano", "Lucro contábil: R$ 1.000.000 por ano"),
                 ("30%", "Alíquota: 30% (exceção)")]
        lin = VGroup(*[T("• " + s, size=30) for _, s in itens]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        lin[4].set_color(AMA)
        lin.move_to(UP * 0.5)
        for (tr, _), m in zip(itens, lin):
            self.em(tr, FadeIn(m, shift=RIGHT * 0.2))
        dep = T("depreciação = despesa que reparte o custo da máquina pelos anos de uso",
                size=24, color=DIM).next_to(lin, DOWN, buff=0.6)
        self.em("Depreciação, lembrando", FadeIn(dep))

        self.fala("c4_t_lucro")
        d = self.dados("Trator 600.000 · 3 anos · Fisco deduz tudo no ano 1 · contábil 200.000/ano · "
                       "lucro 1.000.000/ano · 30%")
        rot = ["Lucro contábil", "(+) Depreciação contábil", "(−) Depreciação fiscal", "Lucro real",
               "IR corrente (30%)", "Saldo do passivo diferido", "IR diferido no resultado",
               "IR total"]
        g = Grade(rot, ["Ano 1", "Ano 2", "Ano 3"], larg_rot=4.9, larg_col=2.85, alt=0.56, size=24)
        g.move_to(DOWN * 0.3)
        self.play(FadeOut(VGroup(lin, dep)), FadeIn(d), FadeIn(g.linhas), FadeIn(g.cab), run_time=0.7)
        self.linha(g, 0, [("no ano 1", 0, "1.000.000"), ("no ano 2", 1, "1.000.000"),
                          ("no ano 3", 2, "1.000.000")])
        self.fala("c4_t_dep")
        self.linha(g, 1, [("200.000 por ano", None, "600.000 ÷ 3 = 200.000 por ano"),
                          ("Ano 1", 0, "200.000"), ("ano 2", 1, "200.000"), ("ano 3", 2, "200.000")])
        self.fala("c4_t_fisc")
        self.linha(g, 2, [("600.000 inteiros", 0, "(600.000)"), ("No ano 2, zero", 1, "0"),
                          ("No ano 3, zero", 2, "0")])
        self.fala("c4_t_lr1")
        self.rotulo(g, 3)
        src = self.destaque(g, [(0, 0), (1, 0), (2, 0)])
        self.em("Lucro real do ano 1", Create(src), *self.conta("1.000.000 + 200.000 − 600.000 = 600.000"))
        self.em("Dá 600.000", self.escreve(g, 3, 0, "600.000", AMA), FadeOut(src))
        self.fala("c4_t_lr2")
        self.linha(g, 3, [("menos zero", None, "1.000.000 + 200.000 − 0 = 1.200.000"),
                          (": 1.200.000", 1, "1.200.000", AMA),
                          ("igual: 1.200.000", 2, "1.200.000", AMA)], rot=False)
        self.fala("c4_t_irc")
        self.linha(g, 4, [("30% de 600.000", None, "30% × 600.000 = 180.000"),
                          ("600.000, 180.000", 0, "180.000"),
                          ("30% de 1.200.000", None, "30% × 1.200.000 = 360.000"),
                          ("1.200.000, 360.000", 1, "360.000"),
                          ("também 360.000", 2, "360.000")])
        self.fala("c4_t_saldo1")
        self.rotulo(g, 5)
        self.em("200.000 de depreciação", *self.conta("valor contábil: 600.000 − 200.000 = 400.000  ·  base fiscal: 0"))
        self.em("A diferença é de 400.000", *self.conta("diferença: 400.000 − 0 = 400.000"))
        self.em("30% disso", *self.conta("30% × 400.000 = 120.000  →  passivo diferido"))
        self.em("passivo diferido de 120.000", self.escreve(g, 5, 0, "120.000", VERM))
        self.em("vai pagar depois", *self.conta("dívida com o Fisco que fica para depois", cor=VERM))
        self.fala("c4_t_saldo2")
        self.linha(g, 5, [("30% de 200.000", None, "ano 2: 30% × (200.000 − 0) = 60.000"),
                          ("saldo de 60.000", 1, "60.000", VERM),
                          ("vale zero para os dois", None, "ano 3: 30% × (0 − 0) = 0"),
                          ("Saldo zero", 2, "0", VERM)], rot=False)
        self.fala("c4_t_var1")
        self.rotulo(g, 6)
        self.em("e não o saldo", *self.conta("no resultado: VARIAÇÃO do saldo (passo 7)", cor=AZUL))
        self.em("de zero para 120.000", *self.conta("120.000 − 0 = 120.000  →  despesa"))
        self.em("uma despesa", self.escreve(g, 6, 0, "120.000 (despesa)", VERM))
        self.fala("c4_t_var2")
        self.linha(g, 6, [("de 120.000 para 60.000", None, "60.000 − 120.000 = −60.000  →  receita"),
                          ("uma receita", 1, "60.000 (receita)", VER),
                          ("de 60.000 para zero", None, "0 − 60.000 = −60.000  →  receita"),
                          ("Outra receita de 60.000", 2, "60.000 (receita)", VER)], rot=False)
        self.fala("c4_t_total")
        self.linha(g, 7, [("120.000 de diferido", None, "180.000 + 120.000 = 300.000"),
                          ("diferido, 300.000", 0, "300.000", AMA),
                          ("menos 60.000", None, "360.000 − 60.000 = 300.000"),
                          ("60.000, 300.000", 1, "300.000", AMA),
                          ("o mesmo, 300.000", 2, "300.000", AMA)])
        self.fala("c4_t_prova")
        r0, r7 = g.linha_ret(0, VER), g.linha_ret(7, VER)
        self.em("1.000.000 de lucro contábil", Create(r0))
        self.em("igual a 300.000", Create(r7), *self.conta("Prova dos nove: 30% × 1.000.000 = 300.000  ✓", cor=VER))
        self.em("alinhada com o lucro contábil", Indicate(self._conta, color=VER, scale_factor=1.08), rt=1.0)

        # ---------------------------------------------------------------- A1
        self.fala("c4_a1_aviso")
        self.limpa()
        self._conta = None
        self.cabecalho("Questão A1 — Depreciação acelerada")
        av = caixa(P("Questões de treino, no estilo das listas do professor. Não são questões "
                     "oficiais dele.", n=44, size=30, color=AMA), cor=AMA).shift(UP * 0.6)
        ali = caixa(T("A partir daqui: alíquota de 34%", size=32, color=VER), cor=VER)
        ali.next_to(av, DOWN, buff=0.5)
        self.em("Lembrando", FadeIn(av, shift=UP * 0.2))
        self.em("a alíquota é 34%", FadeIn(ali, shift=UP * 0.2))

        self.fala("c4_a1_enunc")
        self.play(FadeOut(VGroup(av, ali)), run_time=0.4)
        en = self.enunciado(
            "Uma empresa compra uma máquina por R$ 90.000, vida útil de 3 anos, sem valor residual. "
            "Contabilmente deprecia em linha reta. O Fisco permite depreciar 100% no ano da compra. "
            "O lucro antes da depreciação é de R$ 100.000 por ano. Faça a DRE e a apuração fiscal "
            "dos 3 anos e os lançamentos do ano 1.")
        self.play(FadeIn(en, shift=UP * 0.2), run_time=0.8)
        lr = T("linha reta = o mesmo valor de depreciação todo ano", size=24, color=DIM)
        lr.next_to(en, DOWN, buff=0.4)
        self.em("linha reta", FadeIn(lr))

        self.fala("c4_a1_ident")
        self.play(FadeOut(lr), run_time=0.3)
        ide = VGroup(pilula("Fisco deduz ANTES", AZUL, 22), T("→", size=30),
                     pilula("hoje paga menos, depois mais", AMA, 22), T("→", size=30),
                     pilula("PASSIVO diferido", VERM, 22)).arrange(RIGHT, buff=0.2)
        ide.next_to(en, DOWN, buff=0.5)
        self.em("deduzir antes da contabilidade", FadeIn(ide[0]))
        self.em("depois pago mais", FadeIn(ide[1]), FadeIn(ide[2]))
        self.em("passivo diferido", FadeIn(ide[3]), FadeIn(ide[4]))

        self.fala("c4_a1_lad")
        d = self.dados("Máquina 90.000 · 3 anos · Fisco: 100% no ano 1 · lucro antes da dep. "
                       "100.000/ano · 34%")
        rot = ["Lucro antes da depreciação", "(−) Depreciação contábil", "LAIR",
               "(+) Adição: depreciação contábil", "(−) Exclusão: depreciação fiscal", "Lucro real",
               "IR corrente (34%)", "Valor contábil no fim do ano", "Base fiscal",
               "Passivo fiscal diferido (34% × diferença)", "IR diferido no resultado (variação)",
               "IR total", "Lucro líquido"]
        g = Grade(rot, ["Ano 1", "Ano 2", "Ano 3"], larg_rot=5.95, larg_col=2.55, alt=0.41, size=22,
                  n_rot=50)
        g.move_to(DOWN * 0.38)
        self.play(FadeOut(VGroup(en, ide)), FadeIn(d), FadeIn(g.linhas), FadeIn(g.cab), run_time=0.7)
        self.linha(g, 0, [("100.000", 0, "100.000"), ("100.000", 1, "100.000"),
                          ("100.000", 2, "100.000")])
        self.fala("c4_a1_dep")
        self.linha(g, 1, [("dá 30.000 por ano", None, "90.000 ÷ 3 = 30.000 por ano"),
                          ("Ano 1", 0, "(30.000)"), ("ano 2", 1, "(30.000)"), ("ano 3", 2, "(30.000)")])
        self.fala("c4_a1_lair")
        self.linha(g, 2, [("menos 30.000", None, "100.000 − 30.000 = 70.000"),
                          ("no ano 1", 0, "70.000", AMA), ("no ano 2", 1, "70.000", AMA),
                          ("no ano 3", 2, "70.000", AMA)])
        sep = self.separador(g, 2)
        self.em("Daqui para baixo", Create(sep), *self.conta("daqui para baixo: apuração fiscal", cor=AZUL))
        self.fala("c4_a1_ad")
        self.rotulo(g, 3)
        self.em("30.000 volta", self.escreve(g, 3, 0, "30.000"))
        self.em("nos três anos", self.varias(g, 3, [1, 2], ["30.000", "30.000"]), rt=0.9)
        self.fala("c4_a1_ex")
        self.linha(g, 4, [("No ano 1, 90.000", 0, "(90.000)"), ("No ano 2, zero", 1, "0"),
                          ("No ano 3, zero", 2, "0")])
        self.fala("c4_a1_lr")
        self.linha(g, 5, [("menos 90.000", None, "70.000 + 30.000 − 90.000 = 10.000"),
                          ("igual a 10.000", 0, "10.000", AMA),
                          ("Ano 2: 70.000 mais 30.000", None, "70.000 + 30.000 − 0 = 100.000"),
                          ("30.000, 100.000", 1, "100.000", AMA),
                          ("também 100.000", 2, "100.000", AMA)])
        self.fala("c4_a1_irc")
        self.linha(g, 6, [("34% de 10.000", None, "34% × 10.000 = 3.400"),
                          ("10.000, 3.400", 0, "3.400"),
                          ("34% de 100.000", None, "34% × 100.000 = 34.000"),
                          ("100.000, 34.000", 1, "34.000"), ("Ano 3: 34.000", 2, "34.000")])
        self.fala("c4_a1_vc")
        self.linha(g, 7, [("90.000 menos 30.000", None, "90.000 − 30.000 = 60.000"),
                          ("30.000, 60.000", 0, "60.000"),
                          ("60.000 menos 30.000", None, "60.000 − 30.000 = 30.000"),
                          ("30.000, 30.000", 1, "30.000"),
                          ("30.000 menos 30.000", None, "30.000 − 30.000 = 0"),
                          ("zero", 2, "0")])
        self.fala("c4_a1_bf")
        self.linha(g, 8, [("zero", 0, "0"), ("zero", 1, "0"), ("zero", 2, "0")])
        self.fala("c4_a1_pd")
        self.linha(g, 9, [("34% de 60.000", None, "34% × (60.000 − 0) = 20.400"),
                          ("60.000, 20.400", 0, "20.400", VERM),
                          ("34% de 30.000", None, "34% × (30.000 − 0) = 10.200"),
                          ("30.000, 10.200", 1, "10.200", VERM),
                          ("Ano 3: zero", 2, "0", VERM)])
        self.fala("c4_a1_var")
        self.linha(g, 10, [("de zero para 20.400", None, "20.400 − 0 = 20.400  →  despesa"),
                           ("despesa de 20.400", 0, "20.400 despesa", VERM),
                           ("de 20.400 para 10.200", None, "10.200 − 20.400 = −10.200  →  receita"),
                           ("receita de 10.200", 1, "(10.200) receita", VER),
                           ("de 10.200 para zero", None, "0 − 10.200 = −10.200  →  receita"),
                           ("receita de 10.200", 2, "(10.200) receita", VER)])
        self.fala("c4_a1_tot")
        self.linha(g, 11, [("mais 20.400", None, "3.400 + 20.400 = 23.800"),
                           ("20.400, 23.800", 0, "23.800", AMA),
                           ("menos 10.200", None, "34.000 − 10.200 = 23.800"),
                           ("10.200, 23.800", 1, "23.800", AMA),
                           ("o mesmo, 23.800", 2, "23.800", AMA)])
        self.fala("c4_a1_ll")
        self.linha(g, 12, [("menos 23.800", None, "70.000 − 23.800 = 46.200"),
                           ("Ano 1", 0, "46.200"), ("ano 2", 1, "46.200"), ("ano 3", 2, "46.200")])
        self.fala("c4_a1_prova")
        rl, rt = g.linha_ret(2, VER), g.linha_ret(11, VER)
        self.em("70.000 de LAIR", Create(rl))
        self.em("tem que dar 23.800", Create(rt), *self.conta("Prova dos nove: 34% × 70.000 = 23.800  ✓", cor=VER))
        self.fala("c4_a1_porque")
        self.play(FadeOut(VGroup(rl, rt)), run_time=0.3)
        self.em("mais depois", *self.conta("deduziu antes → paga menos agora e mais depois → dívida futura = PASSIVO", cor=VERM))

        self.fala("c4_a1_lanc")
        self.limpa()
        self._conta = None
        self.cabecalho("Questão A1 — lançamentos do ano 1")
        leg = T("D = débito   ·   C = crédito", size=26, color=DIM).shift(UP * 2.4)
        l1 = lancamento([("D", "Despesa com IR/CSLL corrente", "3.400"),
                         ("C", "IR/CSLL a recolher", "3.400")], titulo="Corrente").shift(UP * 0.9)
        self.em("D é débito", FadeIn(leg))
        self.em("o corrente", FadeIn(l1, shift=UP * 0.2))
        rec = T("a recolher = imposto que ainda vai ser pago ao governo", size=22, color=DIM)
        rec.next_to(l1, DOWN, buff=0.2)
        self.em("A recolher é", FadeIn(rec))
        self.fala("c4_a1_lanc2")
        l2 = lancamento([("D", "Despesa com IR/CSLL diferido", "20.400"),
                         ("C", "IR/CSLL diferido a recolher (passivo não circulante)", "20.400")],
                        titulo="Diferido", cor=VERM).next_to(rec, DOWN, buff=0.35)
        self.em("o diferido", FadeIn(l2, shift=UP * 0.2))
        nc = T("passivo não circulante = parte de longo prazo do passivo", size=22, color=DIM)
        nc.next_to(l2, DOWN, buff=0.2)
        self.em("parte de longo prazo", FadeIn(nc))

        # ---------------------------------------------------------------- A2
        self.fala("c4_a2_enunc")
        self.limpa()
        self.cabecalho("Questão A2 — PECLD (ativo diferido) com multa (permanente)")
        en = self.enunciado(
            "No ano 1, uma empresa vendeu a prazo e constituiu PECLD de R$ 10.000, que o Fisco só "
            "aceita como dedução quando a perda for efetiva. Também pagou multa de R$ 5.000, "
            "indedutível. No ano 2 a perda de R$ 10.000 se confirma e passa a ser dedutível. O lucro "
            "antes dessas operações é de R$ 100.000 em cada ano. Calcule DRE, IR corrente e diferido.",
            y=0.5)
        self.play(FadeIn(en, shift=UP * 0.2), run_time=0.8)
        pe = T("PECLD = perdas estimadas em créditos de liquidação duvidosa: clientes que não vão pagar",
               size=22, color=DIM).next_to(en, DOWN, buff=0.35)
        self.em("PECLD são", FadeIn(pe))
        self.fala("c4_a2_enunc2")
        ind = T("indedutível = o Fisco não aceita deduzir", size=22, color=DIM).next_to(pe, DOWN, buff=0.15)
        self.em("indedutível", FadeIn(ind))

        self.fala("c4_a2_ident")
        self.play(FadeOut(VGroup(pe, ind)), run_time=0.3)
        p1 = pilula("PECLD: temporária → ATIVO diferido", VER, 26)
        p2 = pilula("Multa: permanente → só adição, sem diferido", VERM, 26)
        VGroup(p1, p2).arrange(DOWN, buff=0.25).next_to(en, DOWN, buff=0.4)
        self.em("gera ativo diferido", FadeIn(p1, shift=UP * 0.2))
        self.em("não gera diferido", FadeIn(p2, shift=UP * 0.2))

        self.fala("c4_a2_l1")
        d = self.dados("PECLD 10.000 (dedutível só quando efetiva) · multa 5.000 indedutível · "
                       "lucro antes 100.000/ano · 34%")
        rot = ["Lucro antes das operações", "(−) PECLD", "(−) Multa", "LAIR",
               "(+) Adição: PECLD (temporária)", "(+) Adição: multa (permanente)",
               "(−) Exclusão: perda efetiva", "Lucro real", "IR corrente (34%)",
               "Ativo fiscal diferido (34% × 10.000)", "IR diferido no resultado", "IR total",
               "Lucro líquido"]
        g = Grade(rot, ["Ano 1", "Ano 2"], larg_rot=6.2, larg_col=3.2, alt=0.41, size=22, n_rot=50)
        g.move_to(DOWN * 0.38)
        self.play(FadeOut(VGroup(en, p1, p2)), FadeIn(d), FadeIn(g.linhas), FadeIn(g.cab), run_time=0.7)
        self.linha(g, 0, [("100.000 no ano 1", 0, "100.000"), ("100.000 no ano 2", 1, "100.000")])
        self.fala("c4_a2_l2")
        self.linha(g, 1, [("10.000 no ano 1", 0, "(10.000)"), ("No ano 2, zero", 1, "0")])
        self.fala("c4_a2_l3")
        self.linha(g, 2, [("5.000 no ano 1", 0, "(5.000)"), ("Zero no ano 2", 1, "0")])
        self.fala("c4_a2_lair")
        self.linha(g, 3, [("menos 5.000", None, "100.000 − 10.000 − 5.000 = 85.000"),
                          ("igual a 85.000", 0, "85.000", AMA),
                          ("Ano 2: 100.000", None, "100.000 − 0 − 0 = 100.000"),
                          ("2: 100.000", 1, "100.000", AMA)])
        sep = self.separador(g, 3)
        self.play(Create(sep), run_time=0.4)
        self.fala("c4_a2_ad1")
        self.linha(g, 4, [("10.000 no ano 1", 0, "10.000"), ("Zero no ano 2", 1, "0")])
        self.fala("c4_a2_ad2")
        self.linha(g, 5, [("5.000 no ano 1", 0, "5.000"), ("Zero no ano 2", 1, "0")])
        ra, rb = g.linha_ret(4), g.linha_ret(5)
        self.em("as duas entram na adição", Create(ra), Create(rb))
        self.em("só aparece no diferido", FadeOut(ra), FadeOut(rb))
        self.fala("c4_a2_ex")
        self.linha(g, 6, [("zero no ano 1", 0, "0"), ("No ano 2, 10.000", 1, "(10.000)")])
        self.fala("c4_a2_lr")
        self.linha(g, 7, [("mais 5.000", None, "85.000 + 10.000 + 5.000 = 100.000"),
                          ("5.000, 100.000", 0, "100.000", AMA),
                          ("menos 10.000", None, "100.000 − 10.000 = 90.000"),
                          ("10.000, 90.000", 1, "90.000", AMA)])
        self.fala("c4_a2_irc")
        self.linha(g, 8, [("34% de 100.000", None, "34% × 100.000 = 34.000"),
                          ("100.000, 34.000", 0, "34.000"),
                          ("34% de 90.000", None, "34% × 90.000 = 30.600"),
                          ("90.000, 30.600", 1, "30.600")])
        self.fala("c4_a2_afd")
        self.linha(g, 9, [("34% de 10.000", None, "34% × 10.000 = 3.400 (só a PECLD)"),
                          ("10.000, 3.400", 0, "3.400", VER),
                          ("saldo zero", 1, "0", VER)])
        rm = g.linha_ret(5, VERM)
        self.em("A multa não entra aqui", Create(rm), *self.conta("multa: permanente → fora do diferido", cor=VERM))
        self.fala("c4_a2_var")
        self.play(FadeOut(rm), run_time=0.3)
        self.linha(g, 10, [("de zero para 3.400", None, "saldo 0 → 3.400: o ativo aumentou  →  receita"),
                           ("uma receita de 3.400", 0, "(3.400) receita", VER),
                           ("voltou a zero", None, "saldo 3.400 → 0: o ativo foi usado  →  despesa"),
                           ("uma despesa de 3.400", 1, "3.400 despesa", VERM)])
        self.fala("c4_a2_tot")
        self.linha(g, 11, [("menos 3.400", None, "34.000 − 3.400 = 30.600"),
                           ("3.400, 30.600", 0, "30.600", AMA),
                           ("mais 3.400", None, "30.600 + 3.400 = 34.000"),
                           ("3.400, 34.000", 1, "34.000", AMA)])
        self.fala("c4_a2_ll")
        self.linha(g, 12, [("menos 30.600", None, "85.000 − 30.600 = 54.400"),
                           ("30.600, 54.400", 0, "54.400"),
                           ("menos 34.000", None, "100.000 − 34.000 = 66.000"),
                           ("34.000, 66.000", 1, "66.000")])
        self.fala("c4_a2_prova1")
        r1 = g.celula_ret(11, 0, VER)
        self.em("então ajustamos", *self.conta("com permanente: 34% × (LAIR + multa)", cor=AZUL))
        self.em("que é 30.600", Create(r1), *self.conta("Ano 1: 34% × (85.000 + 5.000) = 34% × 90.000 = 30.600  ✓", cor=VER))
        self.fala("c4_a2_prova2")
        r2 = g.celula_ret(11, 1, VER)
        self.em("34% de 100.000", Create(r2), *self.conta("Ano 2: 34% × 100.000 = 34.000  ✓", cor=VER))
        self.fala("c4_a2_porque")
        self.play(FadeOut(VGroup(r1, r2)), run_time=0.3)
        self.em("vai ser recuperado", *self.conta("despesa agora, dedução depois → paga mais hoje → crédito com o Fisco = ATIVO", cor=VER))

        self.fala("c4_a2_lanc")
        self.limpa()
        self._conta = None
        self.cabecalho("Questão A2 — lançamentos do ano 1")
        nota = T("O arquivo não traz estes lançamentos: montados no mesmo modelo da A1", size=24,
                 color=AMA).shift(UP * 2.4)
        self.em("não traz os lançamentos", FadeIn(nota))
        l1 = lancamento([("D", "Despesa com IR/CSLL corrente", "34.000"),
                         ("C", "IR/CSLL a recolher", "34.000")], titulo="Corrente").shift(UP * 0.8)
        self.em("Corrente", FadeIn(l1, shift=UP * 0.2))
        self.fala("c4_a2_lanc2")
        l2 = lancamento([("D", "Ativo fiscal diferido", "3.400"),
                         ("C", "Despesa com IR/CSLL diferido (resultado)", "3.400")],
                        titulo="Diferido", cor=VER).next_to(l1, DOWN, buff=0.45)
        self.em("Diferido", FadeIn(l2, shift=UP * 0.2))
        rc = T("crédito na despesa = funciona como receita, reduz a despesa de imposto", size=22,
               color=DIM).next_to(l2, DOWN, buff=0.25)
        self.em("funciona como receita", FadeIn(rc))


class Cena05(Aula):
    CENA = "c5"

    def construct(self):
        self.fala("c5_intro")
        ab = self.abertura(5, "Unidade 3 — Pagamento baseado em ações", "CPC 10: plano liquidado em ações")
        self.em("Vou chamar de PBA", FadeOut(ab))
        pba = caixa(T("PBA = pagamento baseado em ações", size=40, color=AMA), cor=AMA)
        self.play(FadeIn(pba, scale=1.1), run_time=0.6)

        self.fala("c5_oque")
        self.play(FadeOut(pba), run_time=0.3)
        self.cabecalho("O que é PBA (CPC 10)")
        self.add(self.faixa_etapas().to_edge(DOWN, buff=0.25))
        self.etapa(0)
        topo = T("a empresa paga empregados (ou fornecedores) com…", size=30).shift(UP * 2.3)
        self.play(FadeIn(topo), run_time=0.5)
        fs = VGroup(cartao("ações", "um pedaço do capital da empresa", cor=AZUL, larg=4.1, n=20, alt=2.0),
                    cartao("opções de ações", "um direito ligado às ações, concedido como pagamento",
                           cor=VER, larg=4.1, n=20, alt=2.0),
                    cartao("dinheiro", "atrelado ao preço das ações", cor=AMA, larg=4.1, n=20, alt=2.0))
        fs.arrange(RIGHT, buff=0.3).shift(UP * 0.5)
        for f in fs:
            f[2].set_opacity(0)
            self.add(f[2])
        self.em("com ações", FadeIn(fs[0][:2]))
        self.em("opções de ações", FadeIn(fs[1][:2]))
        self.em("dinheiro atrelado", FadeIn(fs[2][:2]), fs[2][2].animate.set_opacity(1))
        self.em("Ação é", fs[0][2].animate.set_opacity(1))
        self.em("Opção de ação é", fs[1][2].animate.set_opacity(1))

        self.fala("c5_porque")
        self.etapa(1)
        po = caixa(P("O serviço do empregado é uma DESPESA, mesmo sem pagar em dinheiro, reconhecida "
                     "ao longo do período de aquisição.", n=52, size=28, color=AMA), cor=AMA)
        po.next_to(fs, DOWN, buff=0.45)
        self.em("é uma despesa", FadeIn(po, shift=UP * 0.2))

        # termos-chave + régua do período de aquisição
        self.fala("c5_outorga")
        self.limpa()
        self.cabecalho("Termos-chave")
        self.etapa(0)
        x0, x1, y = -5.2, 4.0, 1.9
        regua = Line([x0, y, 0], [x1, y, 0], color=DIM, stroke_width=4)
        marcas = VGroup(*[Line([x, y - 0.12, 0], [x, y + 0.12, 0], color=DIM, stroke_width=3)
                          for x in np.linspace(x0, x1, 4)])
        anos = VGroup(*[T(f"ano {k}", size=20, color=DIM).move_to([x0 + (x1 - x0) * (k - 0.5) / 3, y + 0.32, 0])
                        for k in (1, 2, 3)])
        ou = VGroup(Dot([x0, y, 0], radius=0.13, color=AMA),
                    T("outorga", size=22, color=AMA).move_to([x0, y - 0.45, 0]))
        dire = T("direito", size=22, color=VER).move_to([x1 + 0.7, y, 0])
        termos = [("Data da outorga", "quando a empresa promete as ações", AMA),
                  ("Período de aquisição (vesting)", "tempo até o empregado ter direito", AZUL),
                  ("Condição de serviço", "ficar por um prazo; se sair, perde → ajusta a quantidade", VER),
                  ("Condição de desempenho", "atingir uma meta (ex.: ROI) → também ajusta a quantidade", VER),
                  ("Valor justo", "quanto vale cada opção: é a base da despesa", AMA)]
        lista = VGroup(*[VGroup(T(a + ":", size=24, color=c, weight=BOLD), T(b, size=24))
                         .arrange(RIGHT, buff=0.2) for a, b, c in termos])
        for item in lista:
            if item.width > 13:
                item.scale_to_fit_width(13)
        lista.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 1.05).to_edge(LEFT, buff=0.6)
        self.play(Create(regua), FadeIn(marcas), FadeIn(anos), run_time=0.6)
        self.em("Data da outorga", FadeIn(ou), FadeIn(lista[0], shift=RIGHT * 0.2))
        self.fala("c5_vest")
        br = BraceBetweenPoints([x0, y + 0.55, 0], [x1, y + 0.55, 0], direction=UP, color=AZUL)
        brt = T("período de aquisição", size=22, color=AZUL).next_to(br, UP, buff=0.08)
        self.em("Período de aquisição", GrowFromCenter(br), FadeIn(brt), FadeIn(lista[1], shift=RIGHT * 0.2))
        self.em("ter direito", FadeIn(dire))
        self.fala("c5_serv")
        self.em("Condição de serviço", FadeIn(lista[2], shift=RIGHT * 0.2))
        self.em("90% das opções", Indicate(lista[2], color=VER, scale_factor=1.03))
        self.fala("c5_desemp")
        self.em("Condição de desempenho", FadeIn(lista[3], shift=RIGHT * 0.2))
        self.fala("c5_vj")
        self.em("Valor justo", FadeIn(lista[4], shift=RIGHT * 0.2))

        self.fala("c5_analogia")
        self.etapa(3)
        seg = [Line([x0 + (x1 - x0) * k / 3, y, 0], [x0 + (x1 - x0) * (k + 1) / 3, y, 0],
                    color=AMA, stroke_width=12) for k in range(3)]
        bon = pilula("bônus prometido hoje: só é seu se ficar 3 anos", AMA, 22)
        bon.move_to([0, 3.05, 0]).to_edge(RIGHT, buff=0.4)
        self.em("bônus prometido hoje", FadeIn(bon))
        self.em("um pedaço por ano", Create(seg[0]), rt=0.7)
        self.wait(0.3)
        self.play(Create(seg[1]), run_time=0.7)
        self.em("nos três anos", Create(seg[2]), rt=0.7)

        # tipos de plano
        self.fala("c5_tipos")
        self.limpa()
        self.cabecalho("Liquidado em ações × liquidado em caixa")
        self.etapa(2)
        pg = caixa(T("Como a empresa vai pagar?", size=34, color=AMA), cor=AMA).shift(UP * 1.6)
        ra = caixa(P("entregando ações → liquidado em AÇÕES (instrumentos patrimoniais)", n=30, size=26,
                     color=AZUL), cor=AZUL).shift(LEFT * 3.4 + DOWN * 0.6)
        rc = caixa(P("em dinheiro, pelo preço da ação → liquidado em CAIXA", n=30, size=26, color=VER),
                   cor=VER).shift(RIGHT * 3.4 + DOWN * 0.6)
        aa = Arrow(pg.get_bottom(), ra.get_top(), color=DIM, buff=0.1)
        ac = Arrow(pg.get_bottom(), rc.get_top(), color=DIM, buff=0.1)
        self.em("como a empresa vai pagar", FadeIn(pg))
        self.em("liquidado em ações", GrowArrow(aa), FadeIn(ra))
        self.em("liquidado em caixa", GrowArrow(ac), FadeIn(rc))

        self.fala("c5_q1")
        self.play(FadeOut(VGroup(pg, ra, rc, aa, ac)), run_time=0.4)
        self.etapa(0)
        rot = ["Contrapartida da despesa", "Valor justo usado", "Muda quando o preço da ação muda?",
               "O que se revisa ao longo do tempo"]
        g = Grade(rot, ["Em ações", "Em caixa"], larg_rot=4.7, larg_cols=[4.3, 4.6], alt=0.62,
                  alts=[0.85, 0.62, 0.85, 0.85], size=23, alinhar_valores=LEFT, n_rot=24)
        g.move_to(UP * 0.4)
        self.play(FadeIn(g.linhas), FadeIn(g.cab), run_time=0.5)
        quadro = [("PL (reserva de capital)", "Passivo"),
                  ("O da outorga, congelado", "Remensurado a cada balanço"),
                  ("Não", "Sim"),
                  ("Só a quantidade esperada", "Quantidade e valor justo")]
        for i, (k, (a, b)) in enumerate(zip(["c5_q1", "c5_q2", "c5_q3", "c5_q4"], quadro)):
            if i:
                self.fala(k)
            self.rotulo(g, i)
            self.em("Em ações", self.escreve(g, i, 0, a, AZUL))
            if k == "c5_q1":
                rcap = T("reserva de capital = conta do patrimônio líquido (PL)", size=22, color=DIM)
                rcap.to_edge(DOWN, buff=1.0)
                self.em("conta do patrimônio líquido", FadeIn(rcap))
            self.em("Em caixa", self.escreve(g, i, 1, b, VER))
            if k == "c5_q2":
                self.play(FadeOut(rcap), run_time=0.3)
        self.fala("c5_q_prova")
        self.etapa(4)
        dis = caixa(T("Plano em AÇÕES: valores justos dos anos seguintes são DISTRATORES", size=26,
                      color=VERM), cor=VERM).to_edge(DOWN, buff=0.95)
        self.em("distratores", FadeIn(dis, shift=UP * 0.2), Indicate(g.vals[(1, 0)], color=AMA))

        # fórmula + exemplo do material
        self.fala("c5_form")
        self.limpa()
        self.cabecalho("A fórmula (plano em ações)")
        self.etapa(3)
        partes = [("Despesa acumulada", AMA), (" = ", TXT), ("quantidade esperada", VER), (" × ", TXT),
                  ("valor justo", AZUL), (" × ", TXT), ("(anos decorridos ÷ anos totais)", ROXO)]
        f = formula(partes).shift(UP * 1.75)
        self.em("Despesa acumulada", FadeIn(f[0]), FadeIn(f[1]))
        self.em("quantidade esperada", FadeIn(f[2]), FadeIn(f[3]))
        self.em("o valor justo", FadeIn(f[4]), FadeIn(f[5]))
        self.em("anos totais", FadeIn(f[6]))
        self.fala("c5_form2")
        f2 = T("Despesa do ano = acumulada deste ano − acumulada do ano anterior", size=28, color=AMA)
        f2.next_to(f, DOWN, buff=0.4)
        self.em("despesa do ano", FadeIn(f2, shift=UP * 0.2))
        self.fala("c5_ex")
        ex = T("Exemplo do material: 15.000 opções · valor justo na outorga R$ 32 · 3 anos", size=26,
               color=DIM).next_to(f2, DOWN, buff=0.6)
        self.play(FadeIn(ex), run_time=0.5)
        c1 = T("Total: 15.000 × 32 = 480.000", size=32).next_to(ex, DOWN, buff=0.35)
        c2 = T("Por ano: 480.000 ÷ 3 = 160.000", size=32, color=AMA).next_to(c1, DOWN, buff=0.25)
        self.em("igual a 480.000", FadeIn(c1, shift=UP * 0.2))
        self.em("igual a 160.000", FadeIn(c2, shift=UP * 0.2))
        self.fala("c5_ex_lanc")
        lc = lancamento([("D", "Despesa com PBA", "160.000"), ("C", "Reserva de capital (PL)", "160.000")],
                        titulo="Lançamento de cada ano", larg=9.0, size=24)
        lc.next_to(c2, DOWN, buff=0.3)
        self.em("débito", FadeIn(lc, shift=UP * 0.2))

        # ---------------------------------------------------------------- B1
        self.fala("c5_b1_enunc")
        self.limpa()
        self.tira_faixa()
        self.cabecalho("Questão B1 — estimativa de desligamento revisada (treino)")
        en = self.enunciado(
            "A empresa outorga 10.000 opções, valor justo na outorga R$ 20, com condição de "
            "permanência por 4 anos. Estimativa de desligamento: 10% no ano 1, revisada para 20% nos "
            "anos 2 e 3. No ano 4, 15% realmente saíram.", y=0.9)
        self.play(FadeIn(en, shift=UP * 0.2), run_time=0.8)
        self.fala("c5_b1_enunc2")
        en2 = self.enunciado("Os valores justos das ações foram R$ 25, 22, 30 e 28 nos anos 1 a 4. "
                             "Calcule a despesa de cada ano e o efeito fiscal.", y=-1.4)
        self.play(FadeIn(en2, shift=UP * 0.2), run_time=0.6)

        self.fala("c5_b1_ident")
        self.play(FadeOut(VGroup(en, en2)), run_time=0.4)
        acoes = caixa(T("Como paga? Em AÇÕES", size=32, color=AZUL), cor=AZUL).shift(UP * 1.6)
        vjs = VGroup(*[T(f"R$ {v}", size=36) for v in (25, 22, 30, 28)]).arrange(RIGHT, buff=0.7)
        cortes = VGroup(*[Line(v.get_corner(DL), v.get_corner(UR), color=VERM, stroke_width=5) for v in vjs])
        dist = T("distratores", size=26, color=VERM).next_to(vjs, DOWN, buff=0.25)
        out = caixa(T("valor justo da outorga: R$ 20", size=34, color=VER, weight=BOLD), cor=VER)
        out.shift(DOWN * 1.9)
        self.em("Em ações", FadeIn(acoes))
        self.em("risque", FadeIn(vjs))
        self.em("28", *[Create(c) for c in cortes], rt=0.8)
        self.em("São distratores", FadeIn(dist))
        self.em("R$ 20", FadeIn(out, scale=1.1))

        self.fala("c5_b1_op1")
        self.play(FadeOut(VGroup(acoes, vjs, cortes, dist, out)), run_time=0.4)
        d = self.dados("10.000 opções · VJ na outorga R$ 20 (congelado) · 4 anos · desligamento: 10% → 20% "
                       "→ 20% → real 15%")
        rot = ["Opções esperadas", "Despesa acumulada (opções × 20 × n/4)", "Despesa do ano",
               "Ativo fiscal diferido (34% da despesa do ano)"]
        g = Grade(rot, ["Ano 1", "Ano 2", "Ano 3", "Ano 4"], larg_rot=4.9, larg_col=2.15, alt=0.62,
                  alts=[0.62, 0.9, 0.62, 0.9], size=24, n_rot=24)
        g.move_to(UP * 0.55)
        self.play(FadeIn(d), FadeIn(g.linhas), FadeIn(g.cab), run_time=0.6)
        self.linha(g, 0, [("90% de 10.000", None, "10.000 × 90% = 9.000"), (": 9.000", 0, "9.000")])
        self.fala("c5_b1_op2")
        self.linha(g, 0, [("ficam 80%", None, "10.000 × 80% = 8.000"), ("80%: 8.000", 1, "8.000"),
                          ("continua 20%, 8.000", 2, "8.000"),
                          ("ficam 85%", None, "10.000 × 85% = 8.500 (desligamento real)"),
                          ("85%: 8.500", 3, "8.500")], rot=False)
        for k, (n_op, frac, val, nome) in enumerate([("9.000", "1/4", "45.000", "um quarto"),
                                                     ("8.000", "2/4", "80.000", "dois quartos"),
                                                     ("8.000", "3/4", "120.000", "três quartos"),
                                                     ("8.500", "4/4", "170.000", "quatro quartos")]):
            self.fala(f"c5_b1_ac{k + 1}")
            if k == 0:
                self.rotulo(g, 1)
            src = g.celula_ret(0, k)
            self.em(nome, Create(src), *self.conta(f"{n_op} × 20 × {frac} = {val}"))
            self.em(f"quartos: {val}" if k else f"quarto: {val}", self.escreve(g, 1, k, val), FadeOut(src))
        self.fala("c5_b1_da1")
        self.linha(g, 2, [("Ano 1: 45.000", 0, "45.000", AMA)])
        self.fala("c5_b1_da2")
        self.linha(g, 2, [("80.000 menos 45.000", None, "80.000 − 45.000 = 35.000"),
                          ("45.000, 35.000", 1, "35.000", AMA),
                          ("120.000 menos 80.000", None, "120.000 − 80.000 = 40.000"),
                          ("80.000, 40.000", 2, "40.000", AMA),
                          ("170.000 menos 120.000", None, "170.000 − 120.000 = 50.000"),
                          ("120.000, 50.000", 3, "50.000", AMA)], rot=False)
        self.fala("c5_b1_conf")
        r2 = g.linha_ret(2, VER)
        self.em("dá 170.000", Create(r2), *self.conta("45.000 + 35.000 + 40.000 + 50.000 = 170.000 = 8.500 × 20  ✓", cor=VER))
        self.fala("c5_b1_fisc")
        self.play(FadeOut(r2), run_time=0.3)
        self.em("na entrega das ações", *self.conta("Lei 12.973/14, art. 33: adiciona agora, deduz na entrega das ações", cor=AZUL))
        self.em("gera ativo fiscal diferido", *self.conta("→ diferença temporária → ATIVO fiscal diferido", cor=VER))
        av = pilula("⚠ confirme com o professor se ele adota este critério", AMA, 22)
        av.next_to(g, DOWN, buff=0.35)
        self.em("Lembre de confirmar", FadeIn(av, shift=UP * 0.2))
        self.fala("c5_b1_afd")
        self.play(FadeOut(av), run_time=0.3)
        self.rotulo(g, 3)
        tag = pilula("aqui: efeito no resultado do ano", AMA, 22).next_to(g, DOWN, buff=0.35)
        self.em("efeito no resultado do ano", FadeIn(tag, scale=1.1))
        for k, (desp, v) in enumerate([("45.000", "15.300"), ("35.000", "11.900"), ("40.000", "13.600"),
                                       ("50.000", "17.000")]):
            self.em(f"34% de {desp}", *self.conta(f"34% × {desp} (despesa do ano) = {v}"))
            self.em(f"{desp}, {v}", self.escreve(g, 3, k, v, VER))
        self.fala("c5_b1_afd2")
        self.em("Não é o saldo acumulado", *self.conta("sem reversão ainda: efeito do ano = movimentação do ativo no ano. Não é o saldo.", cor=AMA))
        self.fala("c5_b1_lanc")
        lc = lancamento([("D", "Despesa com remuneração baseada em ações", "despesa do ano"),
                         ("C", "Reserva de capital (PL)", "despesa do ano")], titulo="Lançamento de cada ano",
                        larg=12.0, size=24)
        lc.next_to(g, DOWN, buff=0.3)
        self.em("débito", FadeOut(tag), *self.sem_conta(), FadeIn(lc, shift=UP * 0.2))

        # ---------------------------------------------------------------- B2
        self.fala("c5_b2_enunc")
        self.limpa()
        self._conta = None
        self.cabecalho("Questão B2 — DRE completa (treino)")
        en = self.enunciado(
            "A empresa outorga 12.000 opções, valor justo R$ 15, condição de permanência de 3 anos, "
            "sem desligamentos. O lucro antes do PBA é de R$ 200.000 por ano. Faça a DRE.", y=0.8)
        self.play(FadeIn(en, shift=UP * 0.2), run_time=0.8)
        self.fala("c5_b2_desp")
        dp = caixa(T("Despesa por ano = 12.000 × 15 ÷ 3 = 60.000", size=34, color=AMA), cor=AMA)
        dp.next_to(en, DOWN, buff=0.6)
        self.em("igual a 60.000", FadeIn(dp, shift=UP * 0.2))

        self.fala("c5_b2_l1")
        d = self.dados("12.000 opções · VJ R$ 15 · 3 anos · sem desligamentos · lucro antes do PBA "
                       "200.000/ano · despesa 60.000/ano · 34%")
        rot = ["Lucro antes do PBA", "(−) Despesa com PBA", "LAIR",
               "IR corrente (lucro real 200.000 × 34%)", "IR diferido (ativo)", "Lucro líquido"]
        g = Grade(rot, ["Ano 1", "Ano 2", "Ano 3"], larg_rot=6.3, larg_col=2.4, alt=0.6, size=24,
                  n_rot=60)
        g.move_to(UP * 0.55)
        self.play(FadeOut(VGroup(en, dp)), FadeIn(d), FadeIn(g.linhas), FadeIn(g.cab), run_time=0.6)
        for i, (tr, v, cor) in enumerate([("PBA: 200.000", "200.000", TXT),
                                          ("PBA: 60.000", "(60.000)", TXT),
                                          (": 140.000", "140.000", AMA)]):
            self.rotulo(g, i)
            if i == 2:
                self.em("LAIR", *self.conta("200.000 − 60.000 = 140.000"))
            self.em(tr, self.varias(g, i, [0, 1, 2], [v] * 3, cor), rt=1.1)
        self.fala("c5_b2_irc")
        self.rotulo(g, 3)
        self.em("lucro real de 200.000", *self.conta("lucro real = 140.000 + 60.000 (adição do PBA) = 200.000"))
        self.em("é 68.000", *self.conta("34% × 200.000 = 68.000"))
        self.em("negativo na DRE", self.varias(g, 3, [0, 1, 2], ["(68.000)"] * 3), rt=1.1)
        self.fala("c5_b2_dif")
        self.rotulo(g, 4)
        self.em("20.400 de ativo diferido", *self.conta("34% × 60.000 = 20.400 (ativo diferido)"))
        self.em("positivo na DRE", self.varias(g, 4, [0, 1, 2], ["20.400"] * 3, VER), rt=1.1)
        self.fala("c5_b2_ll")
        self.rotulo(g, 5)
        self.em("igual a 92.400", *self.conta("140.000 − 68.000 + 20.400 = 92.400"))
        self.em("em cada ano", self.varias(g, 5, [0, 1, 2], ["92.400"] * 3, AMA), rt=1.1)
        self.fala("c5_b2_prova")
        self.em("igual a 47.600", *self.conta("IR total = 68.000 − 20.400 = 47.600"))
        self.em("também dá 47.600", *self.conta("Prova dos nove: 34% × 140.000 = 47.600  ✓", cor=VER))
        self.fala("c5_b2_lanc")
        lc = lancamento([("D", "Despesa com PBA", "60.000"), ("C", "Reserva de capital (PL)", "60.000")],
                        titulo="Lançamento anual", larg=9.0, size=24)
        lc.next_to(g, DOWN, buff=0.35)
        self.em("débito", *self.sem_conta(), FadeIn(lc, shift=UP * 0.2))


class Cena06(Aula):
    CENA = "c6"

    def construct(self):
        self.fala("c6_intro")
        ab = self.abertura(6, "PBA liquidado em caixa", "CPC 10")
        self.em("liquidado em caixa", FadeOut(ab))
        self.cabecalho("Liquidado em caixa")
        p1 = cartao("Contrapartida", "PASSIVO: a empresa vai pagar em dinheiro", cor=VERM, larg=6.0, n=26, alt=2.0)
        p2 = cartao("Valor justo", "remensurado a cada ano (o do ano)", cor=VER, larg=6.0, n=26, alt=2.0)
        VGroup(p1, p2).arrange(RIGHT, buff=0.4).shift(UP * 1.3)
        self.em("contrapartida é passivo", FadeIn(p1, shift=UP * 0.2))
        self.em("remensurado a cada ano", FadeIn(p2, shift=UP * 0.2))

        self.fala("c6_form")
        partes = [("Passivo acumulado", VERM), (" = ", TXT), ("quantidade esperada", VER), (" × ", TXT),
                  ("valor justo DO ANO", AZUL), (" × ", TXT), ("(anos decorridos ÷ anos totais)", ROXO)]
        f = formula(partes).shift(DOWN * 0.75)
        self.em("Passivo acumulado", FadeIn(f[0]), FadeIn(f[1]))
        self.em("quantidade esperada", FadeIn(f[2]), FadeIn(f[3]))
        self.em("valor justo do ano", FadeIn(f[4]), FadeIn(f[5]), Indicate(f[4], color=AMA))
        self.em("anos totais", FadeIn(f[6]))
        f2 = T("Despesa do ano = variação do passivo", size=30, color=AMA).next_to(f, DOWN, buff=0.45)
        self.em("variação do passivo", FadeIn(f2, shift=UP * 0.2))

        # exemplo do material
        self.fala("c6_guia")
        self.limpa()
        self.cabecalho("Exemplo do material: o mesmo plano, pago em caixa")
        d = self.dados("15.000 opções · 3 anos · valor justo: R$ 35 (ano 1), R$ 30 (ano 2), R$ 40 (ano 3)",
                       size=24)
        self.em("pago em caixa", FadeIn(d))
        g = Grade(["Passivo acumulado", "Despesa do ano"], ["Ano 1", "Ano 2", "Ano 3"], larg_rot=4.4,
                  larg_col=2.8, alt=0.7, size=26)
        g.move_to(UP * 1.0)
        self.em("nos anos 1, 2 e 3", FadeIn(g.linhas), FadeIn(g.cab))
        self.fala("c6_g1")
        self.linha(g, 0, [("um terço", None, "15.000 × 35 × 1/3 = 175.000"),
                          ("175.000 de passivo", 0, "175.000", VERM)])
        self.linha(g, 1, [("Despesa do ano: 175.000", 0, "175.000", AMA)])
        self.fala("c6_g2")
        self.linha(g, 0, [("dois terços", None, "15.000 × 30 × 2/3 = 300.000"),
                          ("terços: 300.000", 1, "300.000", VERM),
                          ("já reconhecidos", None, "300.000 − 175.000 = 125.000"),
                          ("despesa de 125.000", 1, "125.000", AMA)], rot=False)
        self.fala("c6_g3")
        self.linha(g, 0, [("três terços", None, "15.000 × 40 × 3/3 = 600.000"),
                          ("terços: 600.000", 2, "600.000", VERM),
                          ("Menos 300.000", None, "600.000 − 300.000 = 300.000"),
                          ("despesa de 300.000", 2, "300.000", AMA)], rot=False)
        self.fala("c6_g_comp")
        cmp1 = T("Em ações (VJ 32 congelado):   160.000 · 160.000 · 160.000", size=26, color=AZUL)
        cmp2 = T("Em caixa (VJ do ano):            175.000 · 125.000 · 300.000", size=26, color=VER)
        VGroup(cmp1, cmp2).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(g, DOWN, buff=0.6)
        self.em("160.000 por ano", *self.sem_conta(), FadeIn(cmp1, shift=UP * 0.2))
        self.em("oscila", FadeIn(cmp2, shift=UP * 0.2))

        # ---------------------------------------------------------------- C1
        self.fala("c6_c1_enunc")
        self.limpa()
        self._conta = None
        self.cabecalho("Questão C1 — valor justo variando (treino)")
        en = self.enunciado(
            "A empresa outorga 6.000 direitos de receber em dinheiro o valor da ação (SARs). Condição "
            "de permanência de 3 anos, sem desligamentos, pagamento no início do ano 4. Valor justo: "
            "R$ 10 (ano 1), R$ 14 (ano 2) e R$ 12 (ano 3). Calcule a despesa de cada ano e o pagamento.",
            y=0.6)
        self.play(FadeIn(en, shift=UP * 0.2), run_time=0.8)
        self.fala("c6_c1_ident")
        pc = pilula("pagamento em dinheiro → liquidado em CAIXA → o valor justo de cada ano vale", VER, 24)
        pc.next_to(en, DOWN, buff=0.5)
        self.em("liquidado em caixa", FadeIn(pc, shift=UP * 0.2))

        self.fala("c6_c1_p1")
        d = self.dados("6.000 SARs · 3 anos · sem desligamentos · VJ: 10, 14, 12 · pagamento no início do ano 4")
        rot = ["Passivo acumulado", "Despesa do ano", "Ativo fiscal diferido (34% do passivo)"]
        g = Grade(rot, ["Ano 1", "Ano 2", "Ano 3"], larg_rot=5.2, larg_col=2.6, alt=0.66,
                  alts=[0.66, 0.66, 0.9], size=25, n_rot=24)
        g.move_to(UP * 1.0)
        self.play(FadeOut(VGroup(en, pc)), FadeIn(d), FadeIn(g.linhas), FadeIn(g.cab), run_time=0.6)
        self.linha(g, 0, [("um terço", None, "6.000 × 10 × 1/3 = 20.000"), ("terço: 20.000", 0, "20.000", VERM)])
        self.fala("c6_c1_p2")
        self.linha(g, 0, [("dois terços", None, "6.000 × 14 × 2/3 = 56.000"), ("terços: 56.000", 1, "56.000", VERM)], rot=False)
        self.fala("c6_c1_p3")
        self.linha(g, 0, [("três terços", None, "6.000 × 12 × 3/3 = 72.000"), ("terços: 72.000", 2, "72.000", VERM)], rot=False)
        self.fala("c6_c1_d")
        self.linha(g, 1, [("Ano 1: 20.000", 0, "20.000", AMA),
                          ("56.000 menos 20.000", None, "56.000 − 20.000 = 36.000"),
                          ("20.000, 36.000", 1, "36.000", AMA),
                          ("72.000 menos 56.000", None, "72.000 − 56.000 = 16.000"),
                          ("56.000, 16.000", 2, "16.000", AMA)])
        self.fala("c6_c1_afd")
        self.rotulo(g, 2)
        tag = pilula("aqui: SALDO acumulado", VER, 22).next_to(g, DOWN, buff=0.35)
        self.em("o saldo acumulado", FadeIn(tag, scale=1.1))
        for k, (p, v) in enumerate([("20.000", "6.800"), ("56.000", "19.040"), ("72.000", "24.480")]):
            self.em(f"34% de {p}", *self.conta(f"34% × {p} (passivo acumulado) = {v}"))
            self.em(f"{p}, {v}", self.escreve(g, 2, k, v, VER))
        self.fala("c6_c1_afd2")
        b1 = caixa(P("B1: efeito no resultado do ano (34% da despesa do ano)", n=30, size=24, color=AMA), cor=AMA)
        c1 = caixa(P("C1: saldo acumulado (34% do passivo acumulado)", n=30, size=24, color=VER), cor=VER)
        VGroup(b1, c1).arrange(RIGHT, buff=0.5).next_to(g, DOWN, buff=0.35)
        self.em("efeito no resultado do ano", FadeOut(tag), *self.sem_conta(), FadeIn(b1, shift=UP * 0.2))
        self.em("o saldo acumulado", FadeIn(c1, shift=UP * 0.2))
        self.em("não se contradizem", Indicate(VGroup(b1, c1), color=TXT, scale_factor=1.03), rt=1.0)
        self.fala("c6_c1_afd3")
        self.play(FadeOut(VGroup(b1, c1)), run_time=0.3)
        nossa = pilula("conta nossa (não está no arquivo)", DIM, 20).next_to(g, DOWN, buff=0.3)
        self.em("não está no arquivo", FadeIn(nossa))
        r1, r2 = g.celula_ret(2, 0), g.celula_ret(2, 1)
        self.em("dá 12.240", Create(r1), Create(r2), *self.conta("efeito do ano 2 = 19.040 − 6.800 = 12.240"))
        r3 = g.celula_ret(1, 1, VER)
        self.em("despesa de 36.000", Create(r3), *self.conta("12.240 = 34% × 36.000 (despesa do ano 2)  ✓", cor=VER))
        self.fala("c6_c1_lanc")
        self.play(FadeOut(VGroup(r1, r2, r3, nossa)), *self.sem_conta(), run_time=0.3)
        l1 = lancamento([("D", "Despesa com PBA", "despesa do ano"), ("C", "Passivo por PBA a liquidar", "despesa do ano")],
                        titulo="Lançamento anual", larg=11.0, size=24).next_to(g, DOWN, buff=0.3)
        self.em("débito", FadeIn(l1, shift=UP * 0.2))
        self.fala("c6_c1_pag")
        l2 = lancamento([("D", "Passivo por PBA", "72.000"), ("C", "Caixa", "72.000")],
                        titulo="Pagamento (início do ano 4)", larg=11.0, size=24, cor=VERM).move_to(l1)
        self.em("Pagamento", FadeOut(l1), FadeIn(l2, shift=UP * 0.2))
        self.em("exclusão fiscal", *self.conta("exclusão fiscal de 72.000 (valor pago) + reversão do ativo diferido", cor=AZUL, y=-3.65))
        self.fala("c6_c1_dif")
        self.play(FadeOut(l2), *self.sem_conta(), run_time=0.3)
        rd = g.celula_ret(1, 2)
        self.em("cai para 16.000", Create(rd))
        self.em("de 14 para 12", *self.conta("VJ caiu de 14 para 12 → a despesa do ano 3 cai para 16.000"))
        self.em("isso não acontece", *self.conta("em plano em AÇÕES isso não acontece: VJ congelado", cor=AZUL))

        # ---------------------------------------------------------------- C2
        self.fala("c6_c2_enunc")
        self.limpa()
        self._conta = None
        self.cabecalho("Questão C2 — valor justo e desligamento variando (treino)")
        en = self.enunciado(
            "A empresa outorga 200 direitos em dinheiro a cada um de 100 empregados (20.000 no total), "
            "com permanência de 3 anos. Estimativa de desligamento: 10% no ano 1, 15% no ano 2 e "
            "desligamento real de 12% no ano 3. Valor justo: R$ 8, R$ 9 e R$ 11.", y=0.5)
        self.play(FadeIn(en, shift=UP * 0.2), run_time=0.8)
        self.fala("c6_c2_desl")
        d = self.dados("20.000 direitos (200 × 100 empregados) · 3 anos · liquidado em caixa")
        rot = ["Desligamento", "Direitos esperados", "Valor justo", "Passivo acumulado", "Despesa do ano"]
        g = Grade(rot, ["Ano 1", "Ano 2", "Ano 3"], larg_rot=4.4, larg_col=2.8, alt=0.6, size=25)
        g.move_to(UP * 0.75)
        self.play(FadeOut(en), FadeIn(d), FadeIn(g.linhas), FadeIn(g.cab), run_time=0.6)
        self.linha(g, 0, [("10%", 0, "10%"), ("15%", 1, "15%"), ("12%", 2, "12%")])
        self.fala("c6_c2_dir")
        self.linha(g, 1, [("90% de 20.000", None, "20.000 × 90% = 18.000"), ("20.000, 18.000", 0, "18.000"),
                          ("ficam 85%", None, "20.000 × 85% = 17.000"), ("85%, 17.000", 1, "17.000"),
                          ("ficam 88%", None, "20.000 × 88% = 17.600 (desligamento real)"),
                          ("88%, 17.600", 2, "17.600")])
        self.fala("c6_c2_vj")
        self.linha(g, 2, [("8", 0, "8"), ("9", 1, "9"), ("11", 2, "11")])
        for k, (q_, vj, frac, nome, val) in enumerate([("18.000", "8", "1/3", "um terço", "48.000"),
                                                      ("17.000", "9", "2/3", "dois terços", "102.000"),
                                                      ("17.600", "11", "3/3", "três terços", "193.600")]):
            self.fala(f"c6_c2_p{k + 1}")
            if k == 0:
                self.rotulo(g, 3)
            src = VGroup(g.celula_ret(1, k), g.celula_ret(2, k))
            self.em(nome, Create(src), *self.conta(f"{q_} × {vj} × {frac} = {val}"))
            self.em(f"{'terço' if k == 0 else 'terços'}: {val}", self.escreve(g, 3, k, val, VERM), FadeOut(src))
        self.fala("c6_c2_d")
        self.linha(g, 4, [("Ano 1: 48.000", 0, "48.000", AMA),
                          ("102.000 menos 48.000", None, "102.000 − 48.000 = 54.000"),
                          ("48.000, 54.000", 1, "54.000", AMA),
                          ("193.600 menos 102.000", None, "193.600 − 102.000 = 91.600"),
                          ("102.000, 91.600", 2, "91.600", AMA)])
        self.fala("c6_c2_conf")
        r = g.linha_ret(4, VER)
        self.em("dá 193.600", Create(r), *self.conta("48.000 + 54.000 + 91.600 = 193.600 = valor pago ao final  ✓", cor=VER))
        self.fala("c6_c2_lanc")
        self.play(FadeOut(r), *self.sem_conta(), run_time=0.3)
        l1 = lancamento([("D", "Despesa com PBA", "do ano"), ("C", "Passivo por PBA a liquidar", "do ano")],
                        titulo="Lançamento anual", larg=6.4, size=21)
        l2 = lancamento([("D", "Passivo por PBA", "193.600"), ("C", "Caixa", "193.600")],
                        titulo="Liquidação", larg=5.4, size=21, cor=VERM)
        VGroup(l1, l2).arrange(RIGHT, buff=0.3).next_to(g, DOWN, buff=0.35)
        self.em("débito", FadeIn(l1, shift=UP * 0.2))
        self.em("Na liquidação", FadeIn(l2, shift=UP * 0.2))


class Cena07(Aula):
    CENA = "c7"

    def construct(self):
        self.fala("c7_intro")
        ab = self.abertura(7, "Unidade 3 — Benefícios a empregados", "CPC 33")
        self.em("só teoria", FadeOut(ab), FadeIn(pilula("no material: só teoria, sem cálculo", AMA, 28)))
        self.fala("c7_oque")
        self.limpa()
        self.cabecalho("Benefícios a empregados: os 4 grupos (CPC 33)")
        self.add(self.faixa_etapas().to_edge(DOWN, buff=0.25))
        self.etapa(0)
        topo = T("o que a empresa dá ao empregado em troca do trabalho", size=28, color=DIM).shift(UP * 2.5)
        self.em("em troca do trabalho", FadeIn(topo))
        grupos = [("Curto prazo", "salários, férias, 13º. Despesa e passivo no período do serviço.", AZUL),
                  ("Pós-emprego", "aposentadoria e assistência médica depois de sair", VER),
                  ("Outros de longo prazo", "licença-prêmio, jubileu (muitos anos de casa)", ROXO),
                  ("Rescisão", "indenização por desligamento", VERM)]
        cs = VGroup(*[cartao(a, b, cor=c, larg=6.2, n=34, size=24, alt=2.1) for a, b, c in grupos])
        cs.arrange_in_grid(2, 2, buff=0.3).shift(DOWN * 0.15)
        for k, card in zip(["c7_cp", "c7_pos", "c7_lp", "c7_resc"], cs):
            self.fala(k)
            self.play(FadeIn(card, shift=UP * 0.2), run_time=0.6)
        self.fala("c7_ident")
        self.etapa(2)
        for tr, card in zip(["é curto prazo", "sai, pós-emprego", "outros de longo prazo",
                             "desligamento, rescisão"], cs):
            self.em(tr, Indicate(card[1], color=AMA, scale_factor=1.15))

        self.fala("c7_planos")
        self.limpa()
        self.cabecalho("Pós-emprego: contribuição definida × benefício definido")
        self.etapa(0)
        pq = caixa(T("De quem é o risco?", size=34, color=AMA), cor=AMA).shift(UP * 2.2)
        self.em("de quem é o risco", FadeIn(pq, scale=1.1))
        self.fala("c7_cd")
        cd = cartao("Contribuição definida", "a empresa só paga a contribuição combinada.\n"
                    "Despesa = contribuição do período.", cor=VER, larg=6.2, n=34, size=24, alt=2.5,
                    rodape="risco: do EMPREGADO")
        bd = cartao("Benefício definido", "a empresa garante o benefício. Exige cálculo atuarial "
                    "(método da unidade de crédito projetada).", cor=VERM, larg=6.2, n=34, size=24,
                    alt=2.5, rodape="risco: da EMPRESA")
        VGroup(cd, bd).arrange(RIGHT, buff=0.35).shift(UP * 0.2)
        self.em("Contribuição definida", FadeIn(cd[:3], shift=UP * 0.2))
        self.em("risco é do empregado", FadeIn(cd[3]))
        an = T("analogia: a empresa faz a parte dela; o tamanho da aposentadoria depende do rendimento",
               size=21, color=DIM).next_to(VGroup(cd, bd), DOWN, buff=0.35)
        self.em("Analogia", FadeIn(an))
        self.fala("c7_bd")
        self.play(FadeOut(an), run_time=0.3)
        self.em("Benefício definido", FadeIn(bd[:3], shift=UP * 0.2))
        self.em("risco é da empresa", FadeIn(bd[3]))
        at = T("cálculo atuarial = estimativa de quanto a empresa vai ter que pagar no futuro", size=21,
               color=DIM).next_to(VGroup(cd, bd), DOWN, buff=0.3)
        self.em("cálculo atuarial", FadeIn(at))
        nao = T("o material só cita o nome do método; os detalhes do cálculo não estão nele", size=21,
                color=AMA).next_to(at, DOWN, buff=0.12)
        self.em("não estão nele", FadeIn(nao))
        self.fala("c7_ora")
        self.play(FadeOut(VGroup(at, nao)), run_time=0.3)
        ora = caixa(P("Benefício definido: ganhos e perdas atuariais → ORA (não vão para o resultado)",
                      n=60, size=24, color=ROXO), cor=ROXO, buff=0.15)
        ora.next_to(VGroup(cd, bd), DOWN, buff=0.3)
        self.em("vão para ORA", FadeIn(ora, shift=UP * 0.2))
        ga = T("ganho/perda atuarial = ajuste quando as estimativas do cálculo atuarial mudam", size=20,
               color=DIM).next_to(ora, DOWN, buff=0.12)
        self.em("Ganho ou perda atuarial é", FadeIn(ga))
        cp = T("CPC 32: o diferido desse item também vai para ORA", size=22, color=AMA)
        cp.next_to(ga, DOWN, buff=0.1)
        self.em("o diferido dele também vai", FadeIn(cp))
        self.fala("c7_prova")
        self.etapa(4)
        self.em("quatro grupos", Indicate(pq, color=AMA, scale_factor=1.05))
        self.em("pelo risco", Indicate(cd[3], color=AMA), Indicate(bd[3], color=AMA))
        self.em("vão para ORA", Indicate(ora, color=AMA, scale_factor=1.04))


class Cena08(Aula):
    CENA = "c8"

    def construct(self):
        self.fala("c8_intro")
        ab = self.abertura(8, "Os 6 erros que mais custam nota", "e o jeito de evitar cada um")
        self.em("Para cada um", FadeOut(ab))
        self.cabecalho("Os 6 erros que mais custam nota", cor=VERM)
        erros = [("Diferido sobre diferença permanente",
                  "Pergunte: o Fisco um dia aceita? Multa: nunca → só adição, sem diferido (A2)."),
                 ("Lançar o saldo em vez da variação",
                  "No resultado: saldo final − saldo inicial. C1, ano 2: saldo 19.040, efeito do ano 12.240."),
                 ("Trocar o sinal",
                  "Paga menos agora → passivo (depreciação acelerada). Paga mais agora → ativo (PECLD)."),
                 ("Esquecer a trava de 30%",
                  "Compensação de prejuízo fiscal ≤ 30% do lucro real. Não é a alíquota de 30% do trator."),
                 ("Valor justo do ano em PBA em ações",
                  "Em ações: VJ da outorga, congelado. B1: 25, 22, 30 e 28 eram distratores; só R$ 20."),
                 ("Não remensurar o PBA em caixa",
                  "Em caixa: VJ de cada ano, recalcula o passivo inteiro. C1, ano 3: usa 12, não 14.")]
        cards = VGroup()
        for k, (a, b) in enumerate(erros):
            c = cartao(f"{k + 1}. ✗ {a}", "✓ " + b, cor=VERM, larg=4.35, n=26, size=20, alt=2.75)
            c[2].set_color(VER)
            cards.add(c)
        cards.arrange_in_grid(2, 3, buff=0.2).shift(DOWN * 0.2)
        nomes = ["Um", "Dois", "Três", "Quatro", "Cinco", "Seis"]
        for k, (card, nome) in enumerate(zip(cards, nomes)):
            self.fala(f"c8_e{k + 1}")
            self.em(nome, FadeIn(card[:2], shift=UP * 0.2), rt=0.5)
            self.wait(max(0, self.resto() * 0.35))
            self.play(FadeIn(card[2]), run_time=0.5)
        self.fala("c8_extra")
        ex = caixa(T("Extra: “ativo fiscal diferido” = efeito do ano (B1) ou saldo acumulado (C1)? "
                     "Veja o que a questão pede.", size=22, color=AMA), cor=AMA, buff=0.12)
        if ex.width > 13.6:
            ex.scale_to_fit_width(13.6)
        self.play(cards.animate.shift(UP * 0.25), run_time=0.4)
        ex.to_edge(DOWN, buff=0.12)
        self.em("cuidado extra", FadeIn(ex, shift=UP * 0.2))


class Cena09(Aula):
    CENA = "c9"

    def construct(self):
        self.fala("c9_resumo")
        ab = self.abertura(9, "Fechamento", "os dois roteiros, treino e avisos")
        self.em("Recapitulando", FadeOut(ab))
        self.cabecalho("Roteiro de uma questão de imposto")
        passos = ["LAIR", "+ adições", "− exclusões", "= lucro real", "× 34% = IR corrente",
                  "diferido: variação do saldo", "prova dos nove"]
        trs = ["LAIR", "adições", "exclusões", "lucro real", "IR corrente", "variação do saldo",
               "prova dos nove"]
        chips = VGroup(*[pilula(p, AMA if k < 5 else (AZUL if k == 5 else VER), 24)
                         for k, p in enumerate(passos)])
        l1 = VGroup(*chips[:4]).arrange(RIGHT, buff=0.4)
        l2 = VGroup(*chips[4:]).arrange(RIGHT, buff=0.3)
        VGroup(l1, l2).arrange(DOWN, buff=0.45).shift(UP * 1.5)
        for tr, c in zip(trs, chips):
            self.em(tr, FadeIn(c, shift=RIGHT * 0.2), rt=0.4)
        self.fala("c9_resumo2")
        t2 = T("Roteiro de PBA", size=30, color=AZUL, weight=BOLD).shift(DOWN * 0.4).to_edge(LEFT, buff=0.35)
        pb = [("em ações ou em caixa?", "em ações ou em caixa"),
              ("quantidade × valor justo × fração do tempo", "fração do tempo"),
              ("despesa do ano = diferença das acumuladas", "diferença entre as acumuladas")]
        pc = VGroup(*[pilula(a, VER, 24) for a, _ in pb]).arrange(DOWN, buff=0.25)
        pc.next_to(t2, DOWN, buff=0.35).set_x(0)
        self.play(FadeIn(t2), run_time=0.4)
        for (_, tr), c in zip(pb, pc):
            self.em(tr, FadeIn(c, shift=RIGHT * 0.2), rt=0.5)
        self.fala("c9_pratica")
        self.limpa()
        self.cabecalho("Treino")
        tr = cartao("Pause e refaça sozinha", "Questões A1 e B1, sem olhar. Depois confira com a "
                    "prova dos nove e com a soma das despesas.", cor=VER, larg=9.0, n=44, size=30)
        self.em("A1 e B1", FadeIn(tr, shift=UP * 0.2))
        self.fala("c9_avisos")
        self.limpa()
        self.cabecalho("Os 3 avisos", cor=AMA)
        avisos = [("1. Questões de treino", "Elaboradas para treino; não são do professor."),
                  ("2. PBA e imposto", "Lei 12.973/14, art. 33, como diferença temporária. Confirme "
                   "com o professor se ele adota o mesmo critério."),
                  ("3. Data da prova", "Confirme a data da prova com o professor.")]
        acs = VGroup(*[cartao("⚠ " + a, b, cor=AMA, larg=4.2, n=24, size=22, alt=3.0)
                       for a, b in avisos]).arrange(RIGHT, buff=0.3)
        for tr_, c in zip(["As questões resolvidas", "Lei 12.973", "data da prova"], acs):
            self.em(tr_, FadeIn(c, shift=UP * 0.3))
        self.fala("c9_fim")
        self.limpa()
        self.play(FadeOut(self.titulo_atual), run_time=0.3)
        self.titulo_atual = None
        fim = T("Bons estudos, e boa prova!", size=56, color=AMA, weight=BOLD)
        self.em("Bons estudos", FadeIn(fim, scale=1.1), rt=0.8)
