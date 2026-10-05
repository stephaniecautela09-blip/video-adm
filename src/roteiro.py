"""Roteiro da aula: cada cena = um slide + a narração daquele trecho.

Marcações nos slides: [y]amarelo[/y] [g]verde[/g] [r]vermelho[/r] [c]azul[/c] [b]negrito[/b].
Na narração, números ficam em algarismos (formato brasileiro); fala.normalizar() lê por extenso.
"""

CENAS = []


def add(base=None, **kw):
    CENAS.append({**(base or {}), **kw})


def passo_a_passo(base, narracoes, inicio=1):
    """Gera uma cena por passo, revelando o slide aos poucos (efeito quadro)."""
    for i, n in enumerate(narracoes):
        CENAS.append(dict(base, reveal=inicio + i, narr=n))


# =====================================================================
# ABERTURA
# =====================================================================
add(tipo="capa", bloco=0, kicker="Aula de revisão para a prova",
    titulo="Administração Financeira",
    sub="Ross, Westerfield, Jordan e Lamb · 9ª edição",
    tempo="6 blocos · cerca de 35 minutos",
    narr="Olá! Esta é a nossa aula de revisão de Administração Financeira, baseada no livro do Ross, "
         "nona edição. Você vai fazer a prova com a folha de fórmulas na mão, então o objetivo aqui não é "
         "decorar nada. O objetivo é saber três coisas: qual fórmula usar, como montar a conta e como "
         "interpretar o resultado.")

add(tipo="lista", bloco=0, titulo="Como esta aula funciona",
    itens=["[b]Qual fórmula?[/b] Reconhecer o tipo de questão pelo que o enunciado pede.",
           "[b]Como montar?[/b] Um exemplo numérico resolvido em cada bloco, passo a passo, como no quadro.",
           "[b]O que significa?[/b] Toda questão prática termina com [y]“analise”[/y] ou [y]“interprete”[/y].",
           "[r]Nunca entregue só o número[/r]: escreva 2 linhas dizendo o que ele significa.",
           "No fim de cada bloco: a [r]pegadinha[/r] mais provável daquele tema."],
    narr="Funciona assim. Em cada bloco eu mostro como reconhecer o tipo de questão, resolvo um exemplo "
         "numérico completo, passo a passo, e no final destaco a pegadinha mais provável. E guarde a regra de ouro: "
         "toda questão prática do professor termina com analise ou interprete. Nunca entregue só o número. "
         "Escreva pelo menos duas linhas dizendo o que ele significa.")

add(tipo="tabela", bloco=0, titulo="Roteiro da aula",
    cab=["Bloco", "Tema", "Na folha, procure…"], cols=[0.8, 3, 2.2], size=32,
    linhas=[["1", "Introdução: objetivo, agência, Selic", "Cap. 1 (teoria)"],
            ["2", "Fluxo de caixa e indicadores", "Caps. 2 e 3"],
            ["3", "Crescimento e avaliação de projetos", "Caps. 4 e 9"],
            ["4", "Risco, retorno e CAPM", "Caps. 12 e 13"],
            ["5", "Custo de capital e estrutura", "Caps. 7, 8, 14 e 16"],
            ["6", "Resumo: as 10 pegadinhas", "—"]],
    narr="São seis blocos. Introdução. Fluxo de caixa e indicadores. Crescimento e avaliação de projetos. "
         "Risco, retorno e CAPM. Custo de capital e estrutura de capital. E um resumo final com as dez "
         "pegadinhas mais comuns. Na coluna da direita está o capítulo do Ross onde você acha cada fórmula na folha, "
         "porque a folha é organizada por capítulo.")

# =====================================================================
# BLOCO 1 — INTRODUÇÃO
# =====================================================================
add(tipo="capa", bloco=1, kicker="Bloco 1", titulo="Introdução",
    sub="Objetivo da empresa · Teoria da agência · Selic e VPL", tempo="≈ 3 minutos",
    narr="Bloco um: introdução. Essa parte quase sempre cai como questão teórica, então é ponto fácil, "
         "desde que você saiba justificar.")

base = dict(tipo="tabela", bloco=1, titulo="Objetivo: maximizar o valor da ação, não o lucro",
            cab=["Critério", "Lucro contábil", "Valor da ação"], cols=[1.3, 2.2, 2.2], size=34,
            notas=["O valor da ação é o único objetivo que considera [y]retorno, tempo e risco[/y] ao mesmo tempo.",
                   "Maximizar participação de mercado também é ruim: dá para crescer vendendo barato e destruir valor."],
            linhas=[["[y]1. Tempo[/y]", "Ignora [b]quando[/b] o lucro chega", "Desconta os fluxos futuros"],
                    ["[y]2. Risco[/y]", "Ignora o risco", "Embute o risco na taxa de desconto"],
                    ["[y]3. Horizonte[/y]", "Pode ser de curto prazo e insustentável", "Olha todo o futuro"]])
passo_a_passo(dict(base, notas=[]), [
    "O objetivo da administração financeira é maximizar o valor de mercado da ação existente, ou seja, "
    "a riqueza do acionista. Não é maximizar o lucro. E a prova costuma pedir os três motivos. "
    "Primeiro motivo: tempo. O lucro contábil ignora quando o dinheiro chega. Um real hoje vale mais que um real daqui a cinco anos, "
    "e o valor da ação leva isso em conta, porque desconta os fluxos futuros.",
    "Segundo motivo: risco. Dois projetos podem ter o mesmo lucro esperado, mas um ser muito mais arriscado. "
    "O lucro não enxerga essa diferença. O valor da ação enxerga, porque o risco entra na taxa de desconto.",
    "Terceiro motivo: horizonte. Dá para inflar o lucro de curto prazo cortando manutenção, pesquisa ou treinamento, "
    "e destruir a empresa no longo prazo. O preço da ação olha todo o futuro.",
])
add(dict(base, narr="Resumindo para escrever na prova: o valor da ação é o único objetivo que considera, ao mesmo tempo, "
         "retorno, tempo e risco. E cuidado com a alternativa maximizar participação de mercado: "
         "dá para crescer vendendo barato e destruir margem e valor."))

add(tipo="lista", bloco=1, titulo="Teoria da agência (Jensen & Meckling, 1976)",
    itens=["[y]Principal[/y] = acionista (dono)  ·  [y]Agente[/y] = gestor (quem controla)",
           "A separação entre [b]propriedade[/b] e [b]controle[/b] gera conflito: o gestor pode buscar salário, poder e segurança, em vez do valor da ação.",
           "[c]Custos de agência[/c] = gastos para monitorar + prejuízo das decisões ruins do gestor."],
    narr="Agora, teoria da agência. Na sociedade anônima, quem é dono não é quem administra. O acionista é o principal, "
         "o gestor é o agente. Essa separação entre propriedade e controle gera um conflito: o gestor pode buscar "
         "o próprio interesse, como salário alto, poder, segurança no cargo, em vez de maximizar o valor da ação. "
         "Os custos de agência são os gastos para monitorar o gestor mais o prejuízo das decisões ruins que ele toma.")

base = dict(tipo="tabela", bloco=1, titulo="Os 3 mecanismos de mitigação",
            cab=["Mecanismo", "Exemplos", "Funciona por…"], cols=[2.2, 2.6, 1.6], size=34,
            linhas=[["[y]Governança corporativa[/y]", "Conselho, comitês, auditoria independente", "[g]Monitoramento[/g]"],
                    ["[y]Mercado de controle corporativo[/y]", "Takeover, disputa de procurações", "[g]Ameaça[/g]"],
                    ["[y]Remuneração por desempenho[/y]", "Stock options, bônus por resultado", "[g]Alinhamento[/g]"]],
            notas=["No Brasil: Lei das S/A, CVM e segmentos da B3 (Novo Mercado, Nível 1 e 2)."])
passo_a_passo(dict(base, notas=[]), [
    "Para mitigar esse conflito, existem três mecanismos, e cada um tem uma lógica diferente. "
    "O primeiro é a governança corporativa: conselho de administração, comitês, auditoria independente. Ele funciona por monitoramento.",
    "O segundo é o mercado de controle corporativo: takeover e disputa de procurações. Funciona por ameaça. "
    "Se a gestão é ruim, a ação cai, e isso atrai um comprador que assume a empresa e troca a diretoria.",
    "O terceiro é a remuneração por desempenho: stock options e bônus. Funciona por alinhamento. O gestor ganha quando o acionista ganha.",
])
add(dict(base, narr="Dica de prova: escreva o mecanismo junto com a lógica. Governança monitora, mercado de controle ameaça, "
         "remuneração alinha. E no Brasil, cite a Lei das S/A, a CVM e os segmentos de listagem da B3, como o Novo Mercado."))

add(tipo="grafico", bloco=1, titulo="Como a Selic afeta o VPL dos projetos", img="selic_vpl",
    notas=["[y]Selic alta[/y] → taxa de desconto sobe",
           "→ [r]VPL dos projetos cai[/r]",
           "→ menos projetos aprovados",
           "Também encarece a dívida e aumenta o custo de oportunidade do acionista."],
    narr="Por fim, a Selic. A Selic é a taxa básica de juros, e ela serve de base para a taxa de desconto. "
         "Olhe o gráfico. É o mesmo projeto que vamos resolver no bloco três. Descontado a 10%, o VPL é de 19.176 reais. "
         "A 12%, cai para 14.233. A 14%, cai para 9.617. Ou seja: Selic sobe, taxa de desconto sobe, VPL cai, "
         "e projetos que antes eram aprovados passam a ser rejeitados. Além disso, a Selic alta encarece a dívida "
         "e aumenta o custo de oportunidade do acionista, que pode simplesmente aplicar em renda fixa.")

add(tipo="pegadinha", bloco=1, titulo="Bloco 1 · Pegadinha",
    texto="O objetivo é maximizar o [y]valor da ação[/y] — não o lucro, nem a participação de mercado. "
          "E justifique com os 3 motivos: [y]tempo, risco e horizonte[/y].",
    narr="A pegadinha do bloco um: o objetivo é maximizar o valor da ação, não o lucro e nem a participação de mercado. "
         "E se pedirem para justificar, os três motivos são tempo, risco e horizonte.")

# =====================================================================
# BLOCO 2 — FLUXO DE CAIXA E INDICADORES
# =====================================================================
add(tipo="capa", bloco=2, kicker="Bloco 2", titulo="Fluxo de caixa e indicadores",
    sub="Fluxo de caixa dos ativos · Liquidez · Endividamento · ROA, ROE · Du Pont", tempo="≈ 9 minutos",
    narr="Bloco dois: fluxo de caixa e indicadores. Esta é a parte mais cobrada em questão prática. Na folha, "
         "procure os capítulos dois e três.")

add(tipo="lista", bloco=2, titulo="Fluxo de caixa dos ativos: sempre nesta ordem", size=36, numerada=True,
    itens=["[y]LAJIR[/y] = Vendas − Custos − Depreciação   [d](sem juros!)[/d]",
           "[y]Impostos[/y] = (LAJIR − Juros) × alíquota",
           "[y]FCO[/y] = LAJIR + Depreciação − Impostos",
           "[y]Gastos líquidos de capital[/y] = Imobilizado final − Imobilizado inicial + Depreciação",
           "[y]ΔCCL[/y] = CCL final − CCL inicial   [d](CCL = AC − PC)[/d]",
           "[y]FC dos ativos[/y] = FCO − Gastos de capital − ΔCCL",
           "[y]Conferência[/y]: FC credores (Juros − Novos empréstimos) + FC acionistas (Dividendos − Novas ações) = FC dos ativos"],
    narr="O fluxo de caixa dos ativos tem um roteiro fixo de sete passos. Primeiro o LAJIR, que é vendas menos custos menos depreciação, "
         "sem os juros. Depois os impostos, calculados sobre o LAJIR menos os juros. Aí vem o fluxo de caixa operacional, o FCO: "
         "LAJIR mais depreciação menos impostos. Depois os gastos líquidos de capital, depois a variação do capital circulante líquido, "
         "e o fluxo de caixa dos ativos é o FCO menos esses dois investimentos. No fim, conferimos dividindo esse fluxo entre credores e acionistas. "
         "Vamos fazer isso num exemplo real do Ross.")

base = dict(tipo="calc", bloco=2, titulo="Exemplo: Dahlia S/A (Ross, cap. 2, q. 21)", dados_w=600, size=35,
            dados=["Vendas: 22.800", "CMV: 16.050", "Depreciação: 4.050", "Juros: 1.830", "Dividendos: 1.300",
                   "Alíquota: 34%", "Imobilizado: 13.650 → 16.800", "AC: 4.800 → 5.930", "PC: 2.700 → 3.150",
                   "Nenhuma dívida nova"],
            passos=["① LAJIR = 22.800 − 16.050 − 4.050 = [y]2.700[/y]",
                    "② Impostos = (2.700 − 1.830) × 0,34 = [y]295,80[/y]",
                    "③ FCO = 2.700 + 4.050 − 295,80 = [y]6.454,20[/y]",
                    "④ Gastos de capital = 16.800 − 13.650 + 4.050 = [y]7.200[/y]",
                    "⑤ ΔCCL = (5.930 − 3.150) − (4.800 − 2.700) = 2.780 − 2.100 = [y]680[/y]",
                    "⑥ FC dos ativos = 6.454,20 − 7.200 − 680 = [r]−1.425,80[/r]",
                    "⑦ FC credores = 1.830 − 0 = 1.830  →  FC acionistas = −1.425,80 − 1.830 = [r]−3.255,80[/r]"])
add(dict(base, reveal=0, narr="Os dados da Dahlia estão aqui na esquerda. Vendas de 22.800, custo das mercadorias de 16.050, "
         "depreciação de 4.050, juros de 1.830, dividendos de 1.300, alíquota de 34%. O imobilizado foi de 13.650 para 16.800, "
         "o ativo circulante de 4.800 para 5.930, e o passivo circulante de 2.700 para 3.150. Nenhuma dívida nova."))
passo_a_passo(base, [
    "Passo um, LAJIR. Vendas, 22.800, menos o custo, 16.050, menos a depreciação, 4.050. Dá 2.700. "
    "Repare que eu não tirei os juros. Juros não entram no LAJIR.",
    "Passo dois, impostos. Agora sim os juros aparecem, porque eles são dedutíveis. O lucro tributável é 2.700 menos 1.830, "
    "que dá 870. Vezes 34%, os impostos são 295,80.",
    "Passo três, FCO. Pego o LAJIR, 2.700, somo de volta a depreciação, 4.050, porque ela não é saída de caixa, "
    "e tiro os impostos, 295,80. O fluxo de caixa operacional é 6.454,20. Mais uma vez: os juros não entram aqui. "
    "Eles são fluxo para credores, não fluxo operacional.",
    "Passo quatro, gastos líquidos de capital. Imobilizado final, 16.800, menos o inicial, 13.650, mais a depreciação, 4.050. "
    "Dá 7.200. Por que somar a depreciação? Porque a depreciação reduziu o imobilizado líquido sem sair dinheiro. "
    "Para saber quanto a empresa realmente comprou, eu somo de volta.",
    "Passo cinco, variação do capital circulante líquido. O CCL final é 5.930 menos 3.150, igual a 2.780. "
    "O inicial é 4.800 menos 2.700, igual a 2.100. A variação é 680. A empresa investiu 680 em capital de giro.",
    "Passo seis, fluxo de caixa dos ativos. FCO de 6.454,20, menos 7.200, menos 680. Resultado: menos 1.425,80.",
    "Passo sete, a conferência. Fluxo para credores é juros menos novos empréstimos líquidos: 1.830 menos zero, 1.830. "
    "Como o total tem que fechar, o fluxo para acionistas é menos 1.425,80 menos 1.830, igual a menos 3.255,80. "
    "Se o enunciado der as novas ações, confira por dividendos menos novas ações.",
])

add(tipo="grafico", bloco=2, titulo="Interpretando o fluxo de caixa da Dahlia", img="cascata",
    notas=["FC dos ativos [r]negativo[/r] é possível: a empresa [y]investiu mais do que gerou[/y].",
           "Como os credores receberam 1.830, os [y]acionistas tiveram de aportar[/y] dinheiro (FC acionistas negativo).",
           "O FCA é mais amplo que o lucro: mede caixa efetivo depois de reinvestir em imobilizado e giro."],
    narr="E agora a interpretação, que vale ponto. Fluxo de caixa dos ativos negativo não é erro de conta. "
         "A empresa gerou 6.454 na operação, mas investiu 7.200 em imobilizado e mais 680 em giro. Ou seja, investiu mais do que gerou. "
         "Como pagou 1.830 aos credores, alguém teve que cobrir a diferença: os acionistas. Fluxo para acionistas negativo "
         "significa aporte de capital. E a frase teórica: o fluxo de caixa dos ativos é mais amplo que o lucro, "
         "porque mede o caixa efetivo depois de reinvestir em imobilizado e em giro.")

base = dict(tipo="tabela", bloco=2, titulo="Indicadores: qual fórmula usar", size=32, cols=[2, 2.6, 3.2],
            cab=["Indicador", "Fórmula", "Leitura"],
            linhas=[["Liquidez corrente", "AC ÷ PC", "Acima de 1: cobre o curto prazo"],
                    ["Liquidez [y]seca[/y]", "(AC − [y]Estoques[/y]) ÷ PC", "Sem depender de vender estoque"],
                    ["Liquidez [r]imediata[/r]", "[r]Caixa[/r] ÷ PC", "Só com dinheiro em mãos"],
                    ["Endividamento total", "(PC + PNC) ÷ Ativo total", "Quanto do ativo é financiado por terceiros"],
                    ["ROA", "LL ÷ Ativo total", "Rentabilidade do ativo"],
                    ["ROE", "LL ÷ PL", "Rentabilidade do acionista"]])
add(dict(base, narr="Segunda parte do bloco: indicadores. Liquidez corrente é ativo circulante sobre passivo circulante. "
         "Liquidez seca tira os estoques do ativo circulante. Liquidez imediata usa só o caixa. "
         "Endividamento total é passivo circulante mais não circulante, sobre o ativo total. "
         "ROA é lucro líquido sobre ativo total. ROE é lucro líquido sobre patrimônio líquido. "
         "A diferença entre seca e imediata é a que mais derruba gente: a seca ainda conta contas a receber, "
         "a imediata conta só o dinheiro que já está em caixa."))

base = dict(tipo="calc", bloco=2, titulo="Exemplo: Marcos Golfe (prova de 2025, q. 4)", dados_w=560, size=35,
            dados=["Ativo circulante: 56.260", "Estoques: 23.084", "Caixa: 5.000", "Passivo circulante: 43.235",
                   "Passivo não circ.: 85.000", "Ativo total: 321.075", "PL: 192.840", "Lucro líquido: 36.475"],
            passos=["Corrente = 56.260 ÷ 43.235 = [y]1,30[/y]",
                    "Seca = (56.260 − 23.084) ÷ 43.235 = [y]0,77[/y]",
                    "Imediata = 5.000 ÷ 43.235 = [r]0,12[/r]   [d](0,77 é a seca: foi o erro de 2025)[/d]",
                    "Endividamento = (43.235 + 85.000) ÷ 321.075 = [y]0,40[/y]",
                    "ROA = 36.475 ÷ 321.075 = [y]11,36%[/y]",
                    "ROE = 36.475 ÷ 192.840 = [y]18,91%[/y]"],
            resultado="[g]Interpretação:[/g] liquidez corrente confortável, mas caixa baixo; endividamento moderado; ROE > ROA → a dívida alavanca o acionista.")
add(dict(base, reveal=0, narr="Vamos aplicar com a questão quatro da prova de 2025, a Marcos Golfe. Os dados estão na esquerda."))
passo_a_passo(base, [
    "Liquidez corrente: 56.260 dividido por 43.235. Dá 1,30. Para cada real de dívida de curto prazo, há 1,30 de ativo circulante.",
    "Liquidez seca: tiro os estoques. 56.260 menos 23.084, dividido por 43.235. Dá 0,77.",
    "Liquidez imediata: só o caixa. 5.000 dividido por 43.235. Dá 0,12. Atenção: em 2025, muita gente respondeu 0,77 aqui, "
    "que é a seca. A imediata usa só o caixa.",
    "Endividamento: passivo circulante mais não circulante, 128.235, dividido pelo ativo total, 321.075. Dá 0,40. "
    "Quarenta por cento do ativo é financiado por terceiros.",
    "ROA: lucro líquido de 36.475 sobre ativo de 321.075. Dá 11,36%.",
    "ROE: o mesmo lucro sobre o patrimônio líquido de 192.840. Dá 18,91%.",
])
add(dict(base, narr="E a interpretação: a liquidez corrente é confortável, mas o caixa é muito baixo, então a empresa depende "
         "de vender estoque e receber dos clientes para pagar as contas. O endividamento é moderado, quarenta por cento. "
         "E o ROE bem acima do ROA mostra que a dívida está alavancando o retorno do acionista."))

add(tipo="grafico", bloco=2, titulo="Seca × imediata: a diferença que cai na prova", img="liquidez",
    notas=["[y]Seca[/y]: tira só os estoques. Ainda conta contas a receber.",
           "[r]Imediata[/r]: só o caixa. É o teste mais rigoroso.",
           "Corrente ≥ seca ≥ imediata, sempre."],
    narr="Visualmente fica fácil. Do mais amplo para o mais restrito: a corrente, 1,30; a seca, 0,77; a imediata, 0,12. "
         "A ordem é sempre essa: corrente maior ou igual à seca, que é maior ou igual à imediata. "
         "Se a sua imediata deu maior que a seca, você errou alguma coisa.")

base = dict(tipo="lista", bloco=2, titulo="Identidade de Du Pont", size=38,
            itens=["[y]Margem[/y] = LL ÷ Vendas  → eficiência operacional",
                   "[y]Giro do ativo[/y] = Vendas ÷ Ativo  → eficiência no uso dos ativos",
                   "[y]Multiplicador do PL[/y] = Ativo ÷ PL [r]= 1 + D/E[/r]  → alavancagem financeira",
                   "Marcos Golfe: ROA × multiplicador = 11,36% × (321.075 ÷ 192.840 = 1,665) = [g]18,91%[/g] ✓"],
            formula="[c]ROE = Margem × Giro × Multiplicador do PL[/c]")
add(dict(base, reveal=3, narr="Agora a identidade de Du Pont. Ela quebra o ROE em três pedaços. A margem, lucro líquido sobre vendas, "
         "mede eficiência operacional. O giro do ativo, vendas sobre ativo, mede eficiência no uso dos ativos. "
         "E o multiplicador do patrimônio, ativo sobre patrimônio líquido, mede a alavancagem. Detalhe importante: "
         "o multiplicador também é igual a um mais a relação dívida sobre patrimônio. Isso cai muito quando o enunciado dá só o D sobre E."))
add(dict(base, reveal=4, narr="Confira com a Marcos Golfe: margem vezes giro é o ROA. Então ROE é ROA vezes o multiplicador. "
         "11,36% vezes 1,665 dá 18,91%. Bate certinho."))

base = dict(tipo="calc", bloco=2, titulo="Du Pont de trás para frente (Ross, cap. 3, q. 18)", dados_w=520, size=36,
            dados=["Vendas: 5.276", "Ativo total: 3.105", "D/E: 1,40", "ROE: 15%", "", "Pede: lucro líquido"],
            passos=["Multiplicador = 1 + D/E = 1 + 1,40 = [y]2,40[/y]",
                    "Giro = 5.276 ÷ 3.105 = [y]1,6992[/y]",
                    "Margem = ROE ÷ (Giro × Mult.) = 0,15 ÷ (1,6992 × 2,40) = [y]3,68%[/y]",
                    "Lucro líquido = 5.276 × 0,0368 = [g]194,06[/g]"])
passo_a_passo(base, [
    "Um exemplo de trás para frente, do Ross. Vendas de 5.276, ativo de 3.105, D sobre E de 1,40, ROE de 15%. Ache o lucro líquido. "
    "Primeiro, o multiplicador: um mais 1,40, igual a 2,40.",
    "Giro: 5.276 dividido por 3.105. Dá 1,6992.",
    "Agora isolo a margem: ROE dividido por giro vezes multiplicador. 0,15 dividido por 1,6992 vezes 2,40. Dá 3,68%.",
    "E o lucro líquido é vendas vezes margem: 5.276 vezes 3,68%, igual a 194,06.",
])

add(tipo="pegadinha", bloco=2, titulo="Bloco 2 · Pegadinha",
    texto="Liquidez [r]imediata[/r] usa [y]só o caixa[/y] (0,12) — quem tira só os estoques está calculando a [y]seca[/y] (0,77). "
          "E [r]juros não entram[/r] no LAJIR nem no FCO.",
    narr="A pegadinha do bloco dois: liquidez imediata usa só o caixa. Se você tirou só os estoques, calculou a seca. "
         "E, no fluxo de caixa, juros não entram no LAJIR nem no FCO.")

# =====================================================================
# BLOCO 3 — CRESCIMENTO E AVALIAÇÃO DE PROJETOS
# =====================================================================
add(tipo="capa", bloco=3, kicker="Bloco 3", titulo="Crescimento e avaliação de projetos",
    sub="Crescimento interno e sustentável · VPL · TIR · Payback · Índice de lucratividade", tempo="≈ 7,5 minutos",
    narr="Bloco três: crescimento e avaliação de projetos. Na folha, capítulo quatro para crescimento e capítulo nove para VPL, TIR e payback.")

base = dict(tipo="tabela", bloco=3, titulo="Taxa de crescimento interna × sustentável", size=33, cols=[1.6, 2.4, 3],
            cab=["Taxa", "Fórmula", "Quando usar"],
            linhas=[["[y]b[/y] (retenção)", "1 − Payout = Lucro retido ÷ LL", "Entra nas duas fórmulas"],
                    ["[y]g interna[/y]", "(ROA × b) ÷ (1 − ROA × b)", "Crescer [b]sem nenhum[/b] dinheiro de fora"],
                    ["[y]g sustentável[/y]", "(ROE × b) ÷ (1 − ROE × b)", "Sem emitir ações, mas [b]mantendo D/E constante[/b] (pode pegar dívida na mesma proporção)"]],
            notas=["Regra para lembrar: [c]interna → ROA[/c] (só o ativo).  [c]Sustentável → ROE[/c] (o acionista + dívida proporcional)."])
add(dict(base, narr="Começando pelo crescimento. Primeiro você precisa do b, a taxa de retenção: um menos o payout, ou lucro retido sobre lucro líquido. "
         "A taxa de crescimento interna usa o ROA: ROA vezes b, dividido por um menos ROA vezes b. "
         "É quanto a empresa cresce sem nenhum dinheiro de fora, só com lucro retido. "
         "A taxa sustentável usa o ROE, com a mesma estrutura de fórmula. É quanto a empresa cresce sem emitir ações, "
         "mas mantendo a relação dívida sobre patrimônio constante, ou seja, pegando dívida na mesma proporção. "
         "Para lembrar: interna, ROA. Sustentável, ROE. A sustentável é sempre maior, porque permite dívida."))

base = dict(tipo="calc", bloco=3, titulo="Exemplo: Hoffman (prova de 2025, q. 6)", dados_w=520, size=36,
            dados=["Lucro líquido: 66", "Ativo total: 500", "PL: 250", "Lucros retidos: 44"],
            passos=["b = 44 ÷ 66 = [y]0,6667[/y]",
                    "ROA = 66 ÷ 500 = 13,2%   ·   ROE = 66 ÷ 250 = 26,4%",
                    "g interna = (0,132 × 0,6667) ÷ (1 − 0,088) = 0,088 ÷ 0,912 = [g]9,65%[/g]",
                    "g sustentável = (0,264 × 0,6667) ÷ (1 − 0,176) = 0,176 ÷ 0,824 = [g]21,36%[/g]"],
            resultado="Crescer acima de 21,36% exige: emitir ações, aumentar a dívida, reter mais lucro ou melhorar margem e giro.")
passo_a_passo(base, [
    "Exemplo da prova de 2025, a Hoffman. Lucro de 66, ativo de 500, patrimônio de 250, lucros retidos de 44. "
    "Retenção: 44 sobre 66, igual a 0,6667.",
    "ROA: 66 sobre 500, 13,2%. ROE: 66 sobre 250, 26,4%.",
    "Crescimento interno: ROA vezes b dá 0,088. Divido por um menos 0,088, que é 0,912. Resultado: 9,65% ao ano.",
    "Crescimento sustentável: ROE vezes b dá 0,176. Divido por 0,824. Resultado: 21,36%.",
])
add(dict(base, narr="E a interpretação pronta: se a empresa quiser crescer acima da taxa sustentável, tem quatro saídas. "
         "Emitir ações, com diluição e custo de emissão. Aumentar a alavancagem, com mais risco de falência. "
         "Reter mais lucro, deixando o acionista sem dividendo. Ou melhorar margem e giro, que é a única sem custo financeiro, "
         "e também a mais difícil."))

# --- projeto
base = dict(tipo="tabela", bloco=3, titulo="Um projeto, quatro métodos (taxa de 12%)", size=34,
            cab=["Ano", "Fluxo", "Acumulado", "VP a 12%", "VP acumulado"],
            linhas=[["0", "[r]−100.000[/r]", "−100.000", "−100.000", "−100.000"],
                    ["1", "35.000", "−65.000", "35.000 ÷ 1,12 = 31.250,00", "−68.750,00"],
                    ["2", "40.000", "−25.000", "40.000 ÷ 1,12² = 31.887,76", "−36.862,24"],
                    ["3", "45.000", "[g]+20.000[/g]", "45.000 ÷ 1,12³ = 32.030,11", "−4.832,13"],
                    ["4", "30.000", "+50.000", "30.000 ÷ 1,12⁴ = 19.065,54", "[g]+14.233,41[/g]"]],
            cols=[0.6, 1.3, 1.3, 2.9, 1.6])
add(dict(base, reveal=1, narr="Agora a parte principal do bloco: avaliação de projetos. Vou usar um único exemplo e resolver pelos quatro métodos. "
         "Investimento de 100.000 no ano zero. Fluxos de 35.000, 40.000, 45.000 e 30.000 nos anos um a quatro. Taxa de 12%. "
         "Vou montar a tabela linha a linha, como no quadro."))
passo_a_passo(base, [
    "Ano um: entra 35.000. O acumulado simples vai para menos 65.000. Trazendo a valor presente: 35.000 dividido por 1,12, "
    "igual a 31.250. O acumulado descontado fica em menos 68.750.",
    "Ano dois: 40.000. Acumulado simples, menos 25.000. Valor presente: 40.000 dividido por 1,12 ao quadrado, igual a 31.887,76. "
    "Acumulado descontado, menos 36.862,24.",
    "Ano três: 45.000. O acumulado simples vira positivo, mais 20.000. Então o payback simples acontece durante o ano três. "
    "Valor presente: 45.000 dividido por 1,12 ao cubo, 32.030,11. O acumulado descontado ainda é negativo, menos 4.832,13.",
    "Ano quatro: 30.000. Valor presente, 30.000 dividido por 1,12 à quarta, igual a 19.065,54. "
    "E o acumulado descontado vira positivo: mais 14.233,41. Esse número final já é o VPL.",
], inicio=2)

base = dict(tipo="calc", bloco=3, titulo="Resolvendo pelos quatro métodos", size=40,
            passos=["[y]VPL[/y] = −100.000 + 31.250,00 + 31.887,76 + 32.030,11 + 19.065,54 = [g]14.233,41[/g]",
                    "[y]TIR[/y]: a taxa que zera o VPL = [g]18,64%[/g]   [d](na HP 12C: f IRR)[/d]",
                    "[y]Payback simples[/y] = 2 + 25.000 ÷ 45.000 = [g]2,56 anos[/g]",
                    "[y]Payback descontado[/y] = 3 + 4.832,13 ÷ 19.065,54 = [g]3,25 anos[/g]   [d](maior que o simples!)[/d]",
                    "[y]IL[/y] = VP dos fluxos ÷ Investimento = 114.233,41 ÷ 100.000 = [g]1,14[/g]"])
passo_a_passo(base, [
    "Agora os quatro métodos. VPL: menos o investimento, mais a soma dos valores presentes. 114.233,41 menos 100.000, "
    "igual a 14.233,41. VPL positivo: o projeto cria 14 mil reais de riqueza para o acionista, além de remunerar os 12%.",
    "TIR: é a taxa que faz o VPL ser zero. Na prova você usa a calculadora. Na HP 12C: f REG, 100.000 CHS g CF zero, "
    "depois cada fluxo com g CF j, e no fim f IRR. Resultado: 18,64%.",
    "Payback simples: olho a coluna do acumulado. No fim do ano dois faltam 25.000. No ano três entram 45.000. "
    "Então são dois anos mais 25.000 sobre 45.000, igual a 2,56 anos.",
    "Payback descontado: mesma lógica, mas na coluna do valor presente acumulado. No fim do ano três ainda faltam 4.832,13. "
    "No ano quatro entram 19.065,54 em valor presente. Três mais 4.832,13 sobre 19.065,54, igual a 3,25 anos. "
    "Repare: é maior que o simples. Sempre será, porque os fluxos descontados são menores.",
    "Índice de lucratividade: valor presente dos fluxos sobre o investimento. 114.233,41 sobre 100.000, igual a 1,14. "
    "Cada real investido devolve 1,14 em valor presente.",
])

add(tipo="grafico", bloco=3, titulo="A TIR no gráfico", img="perfil_vpl",
    notas=["Cada ponto da curva é o VPL a uma taxa.",
           "A [y]TIR[/y] é onde a curva [y]cruza o zero[/y]: 18,64%.",
           "Se a taxa exigida < TIR → VPL > 0 → [g]aceitar[/g].",
           "Na HP 12C: f REG → 100000 CHS g CF0 → 35000 g CFj → … → 12 i → f NPV → f IRR"],
    narr="Este gráfico mostra a relação entre VPL e TIR. Cada ponto da curva é o VPL do projeto a uma taxa diferente. "
         "A 12%, o VPL é 14.233. A curva cai à medida que a taxa sobe, e cruza o zero em 18,64%. Essa é a TIR. "
         "Então, para um projeto normal, com o investimento no início e fluxos positivos depois, se a taxa exigida é menor que a TIR, "
         "o VPL é positivo, e os dois métodos concordam.")

add(tipo="tabela", bloco=3, titulo="Decisão final", size=34, cols=[2, 1.6, 2.4, 1.3],
    cab=["Método", "Resultado", "Regra", "Decisão"],
    linhas=[["VPL", "14.233,41", "VPL > 0", "[g]Aceitar[/g]"],
            ["TIR", "18,64%", "TIR > taxa exigida (12%)", "[g]Aceitar[/g]"],
            ["Payback simples", "2,56 anos", "Menor que o prazo de corte", "[g]Aceitar*[/g]"],
            ["Payback descontado", "3,25 anos", "Menor que a vida (4 anos) → VPL > 0", "[g]Aceitar[/g]"],
            ["IL (livro)", "1,14", "IL > 1", "[g]Aceitar[/g]"]],
    notas=["[y]Cuidado:[/y] o slide usa IL = VPL ÷ Investimento = 0,14 (aceita se > 0). O livro usa VP ÷ Investimento = 1,14 (aceita se > 1). "
           "[b]Escreva qual fórmula usou.[/b]", "[d]* o payback depende de um prazo de corte que o enunciado precisa dar.[/d]"],
    nota_size=32,
    narr="A decisão final: VPL positivo, TIR maior que 12%, payback descontado menor que a vida do projeto, IL maior que um. "
         "Aceitar. Uma observação sobre o índice de lucratividade: o slide do professor escreve VPL sobre investimento, "
         "que dá 0,14 e se aceita quando é maior que zero. O livro escreve valor presente sobre investimento, que dá 1,14 "
         "e se aceita quando é maior que um. Na prova, escreva qual fórmula você usou.")

base = dict(tipo="grafico", bloco=3, titulo="Quando VPL e TIR discordam, vale o VPL", img="conflito",
            notas=["A: investe 10.000, recebe 15.000 → TIR [y]50%[/y], VPL [y]3.636[/y]",
                   "B: investe 100.000, recebe 130.000 → TIR 30%, VPL [g]18.182[/g]",
                   "[g]VPL escolhe B[/g]: cria mais riqueza em reais.",
                   "A TIR supõe reinvestir à própria TIR e falha com escalas diferentes ou mais de uma troca de sinal."])
add(dict(base, narr="Agora a pergunta teórica clássica: e quando VPL e TIR discordam? Veja dois projetos excludentes, à taxa de 10%. "
         "O projeto A investe 10.000 e recebe 15.000 em um ano: TIR de 50%, VPL de 3.636. "
         "O projeto B investe 100.000 e recebe 130.000: TIR de só 30%, mas VPL de 18.182. "
         "A TIR manda escolher A. O VPL manda escolher B. E vale o VPL."))
add(dict(base, narr="Por quê? Porque o objetivo é maximizar a riqueza do acionista, e o VPL mede exatamente isso, em reais. "
         "Uma taxa alta sobre um investimento pequeno gera menos riqueza que uma taxa menor sobre um investimento grande. "
         "Além disso, a TIR supõe que os fluxos são reinvestidos à própria TIR, o que é irrealista, "
         "e pode ter mais de um resultado quando o fluxo troca de sinal mais de uma vez. "
         "O VPL supõe reinvestimento ao custo de capital e sempre dá uma resposta só."))

add(tipo="pegadinha", bloco=3, titulo="Bloco 3 · Pegadinha",
    texto="O [y]payback descontado[/y] é [r]sempre maior[/r] que o simples (3,25 > 2,56). "
          "Se deu menor, você esqueceu de descontar. E payback < vida do projeto [b]não garante[/b] VPL > 0 — só o descontado garante.",
    narr="A pegadinha do bloco três: o payback descontado é sempre maior que o simples. Se deu menor, você esqueceu de descontar algum fluxo. "
         "E só o payback descontado menor que a vida do projeto garante VPL positivo. O simples não garante.")

# =====================================================================
# BLOCO 4 — RISCO, RETORNO E CAPM
# =====================================================================
add(tipo="capa", bloco=4, kicker="Bloco 4", titulo="Risco, retorno e CAPM",
    sub="Retorno esperado e desvio-padrão · Risco sistemático × não sistemático · CAPM e alfa", tempo="≈ 5 minutos",
    narr="Bloco quatro: risco, retorno e CAPM. Na folha, capítulos doze e treze.")

base = dict(tipo="tabela", bloco=4, titulo="Cenários (Ross, cap. 13, q. 23a) · pesos: 40% A, 40% B, 20% C", size=34,
            cols=[1.4, 0.9, 0.9, 0.9, 0.9, 3.2],
            cab=["Cenário", "Prob.", "A", "B", "C", "Carteira"],
            linhas=[["Expansão", "0,35", "24%", "36%", "55%", "0,4(24) + 0,4(36) + 0,2(55) = [y]35,0%[/y]"],
                    ["Normal", "0,50", "17%", "13%", "9%", "0,4(17) + 0,4(13) + 0,2(9) = [y]13,8%[/y]"],
                    ["Retração", "0,15", "0%", "−28%", "−45%", "0,4(0) + 0,4(−28) + 0,2(−45) = [y]−20,2%[/y]"]])
add(dict(base, reveal=0, narr="Questão com cenários. Três ações, A, B e C, com pesos de 40, 40 e 20 por cento na carteira. "
         "Três cenários: expansão com probabilidade de 35%, normal com 50%, retração com 15%. "
         "O roteiro é: primeiro o retorno da carteira em cada cenário, depois o retorno esperado, depois a variância."))
passo_a_passo(base, [
    "Na expansão: 0,4 vezes 24, mais 0,4 vezes 36, mais 0,2 vezes 55. Dá 35%. É uma média ponderada pelos pesos.",
    "No cenário normal: 0,4 vezes 17, mais 0,4 vezes 13, mais 0,2 vezes 9. Dá 13,8%.",
    "Na retração: zero, mais 0,4 vezes menos 28, mais 0,2 vezes menos 45. Dá menos 20,2%.",
])

base = dict(tipo="calc", bloco=4, titulo="Retorno esperado e desvio-padrão", size=35,
            passos=["E(R) = Σ prob × retorno = 0,35(35,0) + 0,50(13,8) + 0,15(−20,2) = [g]16,12%[/g]",
                    "Desvios: 35,0 − 16,12 = 18,88 · 13,8 − 16,12 = −2,32 · −20,2 − 16,12 = −36,32",
                    "σ² = 0,35(0,1888)² + 0,50(−0,0232)² + 0,15(−0,3632)² = 0,01248 + 0,00027 + 0,01979 = [y]0,03253[/y]",
                    "σ = √0,03253 = [g]18,04%[/g]",
                    "Prêmio de risco (Rf = 3,8%) = 16,12 − 3,80 = [g]12,32%[/g]"])
passo_a_passo(base, [
    "Retorno esperado: soma de probabilidade vezes retorno. 0,35 vezes 35, mais 0,50 vezes 13,8, mais 0,15 vezes menos 20,2. "
    "Dá 16,12%.",
    "Para a variância, primeiro os desvios em relação à média: 35 menos 16,12 dá 18,88. 13,8 menos 16,12 dá menos 2,32. "
    "E menos 20,2 menos 16,12 dá menos 36,32.",
    "Variância: cada desvio ao quadrado, em decimal, vezes a probabilidade. Somando: 0,03253. "
    "Atenção: com cenários e probabilidades, você não divide por n menos um. A probabilidade já faz o papel da ponderação.",
    "Desvio-padrão: raiz quadrada de 0,03253. Dá 18,04%.",
    "E se a taxa livre de risco for 3,8%, o prêmio de risco da carteira é 16,12 menos 3,8, igual a 12,32%.",
])

add(tipo="grafico", bloco=4, titulo="Visualizando a carteira", img="cenarios",
    notas=["O retorno esperado (16,12%) é a [y]média ponderada[/y] dos cenários.",
           "O desvio-padrão (18,04%) mede o quanto os cenários se afastam dessa média.",
           "Retorno da carteira [b]é[/b] média ponderada. Risco (σ) da carteira [r]não é[/r]."],
    narr="No gráfico, cada barra é o retorno da carteira em um cenário, e a linha tracejada é o retorno esperado de 16,12%. "
         "O desvio-padrão mede o quanto os resultados se espalham em torno dessa linha. "
         "E guarde isso: o retorno da carteira é média ponderada dos retornos. O desvio-padrão da carteira não é média ponderada "
         "dos desvios dos ativos. Ele é menor, por causa da diversificação.")

add(tipo="grafico", bloco=4, titulo="Risco sistemático × não sistemático", img="diversificacao",
    notas=["[r]Não sistemático[/r] (específico): greve, processo, falha de produto, saída de um executivo. [b]Some[/b] com a diversificação.",
           "[y]Sistemático[/y] (de mercado): juros, inflação, PIB, crise. [b]Fica[/b] — medido pelo [y]beta[/y].",
           "Só o sistemático é [g]remunerado[/g]: o mercado não paga por um risco que qualquer um elimina de graça."],
    nota_size=32,
    narr="Risco total tem duas partes. O risco não sistemático, ou específico, afeta uma empresa só: uma greve, um processo, "
         "uma falha de produto. Ele some com a diversificação, como você vê na curva caindo. "
         "O risco sistemático, ou de mercado, afeta todas as empresas ao mesmo tempo: juros, inflação, PIB, uma crise. "
         "Esse fica, não importa quantas ações você tenha, e é medido pelo beta. "
         "Por isso só o risco sistemático é remunerado. O mercado não paga prêmio por um risco que qualquer investidor elimina sozinho, sem custo.")

base = dict(tipo="calc", bloco=4, titulo="CAPM: o retorno exigido", size=36,
            dados=["Rf (Selic): 12%", "Rm (Ibovespa): 19%", "Prêmio de mercado: 7%", "β da Vale: 1,2", "β da Sabesp: 0,5"],
            dados_titulo="Dados (slides)", dados_w=520,
            passos=["[c]E(R) = Rf + β × (Rm − Rf)[/c]",
                    "Vale: 12% + 1,2 × (19% − 12%) = 12% + 8,4% = [g]20,4%[/g]",
                    "Sabesp: 12% + 0,5 × 7% = 12% + 3,5% = [g]15,5%[/g]",
                    "Beta da carteira = [y]média ponderada[/y] dos betas · ativo sem risco: β = 0 · mercado: β = 1"])
passo_a_passo(base, [
    "Agora o CAPM. O retorno exigido é a taxa livre de risco mais o beta vezes o prêmio de risco de mercado. "
    "Esse termo, Rm menos Rf, é o prêmio de mercado.",
    "Exemplo dos slides. Selic de 12%, Ibovespa rendendo 19%, então o prêmio é 7%. A Vale tem beta 1,2. "
    "Retorno exigido: 12 mais 1,2 vezes 7, igual a 20,4%. Beta maior que um: mais arriscada que o mercado, exige mais que o mercado.",
    "A Sabesp tem beta 0,5. 12 mais 0,5 vezes 7, igual a 15,5%. Menos arriscada, exige menos.",
    "E lembre: o beta da carteira é média ponderada dos betas. O ativo sem risco tem beta zero, e o mercado tem beta um.",
])

base = dict(tipo="grafico", bloco=4, titulo="Alfa: acima ou abaixo da SML?", img="sml",
            notas=["Ação com β = 1,15 · Rf = 10,5% · Rm = 16,5%",
                   "Exigido = 10,5 + 1,15 × 6 = [y]17,4%[/y]",
                   "Oferece [g]18%[/g] → alfa = 18 − 17,4 = [g]+0,6%[/g]",
                   "Alfa > 0 → [g]acima da SML[/g] → subvalorizada → [g]comprar[/g]",
                   "Alfa < 0 → [r]abaixo da SML[/r] → sobrevalorizada → [r]vender[/r]"])
add(dict(base, narr="E o alfa. Uma ação com beta 1,15, taxa livre de risco de 10,5% e retorno de mercado de 16,5%. "
         "O prêmio de mercado é 6%. Retorno exigido: 10,5 mais 1,15 vezes 6, igual a 17,4%. "
         "Mas a ação oferece 18%. O alfa é o retorno esperado menos o exigido: 18 menos 17,4, mais 0,6%."))
add(dict(base, narr="Interpretação: alfa positivo significa que a ação está acima da linha do mercado de títulos, a SML. "
         "Ela entrega mais retorno do que o risco dela exige. Está subvalorizada: comprar. "
         "Alfa negativo é o contrário: abaixo da SML, sobrevalorizada, vender."))

add(tipo="pegadinha", bloco=4, titulo="Bloco 4 · Pegadinha",
    texto="Se o enunciado já der o [y]prêmio de risco de mercado[/y], ele [b]já é[/b] (Rm − Rf): "
          "[r]não subtraia Rf de novo[/r]. Use E(R) = Rf + β × prêmio.",
    narr="A pegadinha do bloco quatro: se o enunciado já der o prêmio de risco de mercado, ele já é Rm menos Rf. "
         "Não subtraia a taxa livre de risco de novo. É só Rf mais beta vezes o prêmio.")

# =====================================================================
# BLOCO 5 — CUSTO DE CAPITAL E ESTRUTURA
# =====================================================================
add(tipo="capa", bloco=5, kicker="Bloco 5", titulo="Custo de capital e estrutura",
    sub="CMPC · Gordon × CAPM · Preço de título · Modigliani-Miller", tempo="≈ 6 minutos",
    narr="Bloco cinco: custo de capital e estrutura de capital. Na folha, capítulos sete, oito, catorze e dezesseis.")

base = dict(tipo="calc", bloco=5, titulo="CMPC (custo médio ponderado de capital)", size=36,
            dados=["E (ações, mercado): 60 milhões", "D (dívida, mercado): 40 milhões", "Re: 16%", "Rd: 11%", "T: 34%"],
            dados_w=560,
            passos=["[c]CMPC = (E/V) × Re + (D/V) × Rd × (1 − T)[/c]   [d]V = E + D, a valor de mercado[/d]",
                    "V = 60 + 40 = 100 → E/V = [y]0,60[/y] · D/V = [y]0,40[/y]",
                    "CMPC = 0,60 × 16% + 0,40 × 11% × (1 − 0,34)",
                    "CMPC = 9,60% + 2,90% = [g]12,50%[/g]",
                    "Se der D/E: [y]D/V = (D/E) ÷ (1 + D/E)[/y] · ex.: D/E = 0,90 → D/V = 0,90 ÷ 1,90 = 0,474"],
            resultado="[g]Interpretação:[/g] é o retorno mínimo que os projetos de risco médio da empresa precisam render para criar valor.")
passo_a_passo(base, [
    "O CMPC é a média dos custos de cada fonte de capital, ponderada pelo peso de cada uma, a valor de mercado. "
    "Capital próprio pesa E sobre V, vezes o custo do capital próprio. Dívida pesa D sobre V, vezes o custo da dívida, "
    "vezes um menos a alíquota de imposto, porque os juros são dedutíveis.",
    "Exemplo: ações valendo 60 milhões, dívida de 40 milhões. O valor total é 100. Peso das ações, 0,60. Peso da dívida, 0,40.",
    "Custo do capital próprio de 16%, custo da dívida de 11%, alíquota de 34%. Monto a conta: 0,60 vezes 16%, "
    "mais 0,40 vezes 11% vezes 0,66.",
    "9,60% mais 2,90%. CMPC de 12,50%.",
    "E se o enunciado der a relação dívida sobre patrimônio, converta antes: D sobre V é D sobre E dividido por um mais D sobre E. "
    "Com D sobre E de 0,90, o peso da dívida é 0,90 sobre 1,90.",
])
add(dict(base, narr="Interpretação: 12,5% é o retorno mínimo que um projeto com o risco médio da empresa precisa render para criar valor. "
         "E por que a dívida entra depois dos impostos e as ações não? Porque juros são dedutíveis do imposto de renda, e dividendos não."))

base = dict(tipo="calc", bloco=5, titulo="Custo do capital próprio: dois métodos (Ross, cap. 14, q. 23)", size=36,
            dados=["β: 1,50", "Dividendo recém-pago (D0): 0,80", "Crescimento g: 5%", "Preço: 61", "Rm: 12%", "Rf: 5,5%"],
            dados_w=560,
            passos=["[y]Gordon[/y]: Re = D1 ÷ P0 + g",
                    "D1 = D0 × (1 + g) = 0,80 × 1,05 = [y]0,84[/y]",
                    "Re = 0,84 ÷ 61 + 0,05 = 1,38% + 5% = [g]6,38%[/g]",
                    "[y]CAPM[/y]: Re = 5,5% + 1,50 × (12% − 5,5%) = 5,5% + 9,75% = [g]15,25%[/g]"],
            resultado="Diferem pelas premissas: Gordon supõe g constante para sempre e não mede risco; o CAPM mede o risco sistemático.")
passo_a_passo(base, [
    "O custo do capital próprio, o Re, pode vir de dois métodos. O primeiro é o modelo de dividendos de Gordon: "
    "o próximo dividendo dividido pelo preço, mais a taxa de crescimento.",
    "Cuidado aqui. O enunciado deu o dividendo recém-pago, D zero, de 0,80. Gordon usa o próximo, D um. "
    "Então multiplico por um mais g: 0,80 vezes 1,05, igual a 0,84.",
    "Re igual a 0,84 dividido por 61, que dá 1,38%, mais 5% de crescimento. Total: 6,38%.",
    "O segundo método é o CAPM: 5,5% mais 1,5 vezes o prêmio de 6,5%. Dá 15,25%.",
])
add(dict(base, narr="Os dois dão números bem diferentes, e isso é normal. Gordon supõe crescimento constante para sempre, "
         "só serve para quem paga dividendos e é muito sensível ao g. O CAPM mede o risco explicitamente pelo beta "
         "e serve para qualquer empresa, mas depende de estimar a taxa livre de risco, o prêmio e o beta."))

base = dict(tipo="calc", bloco=5, titulo="Preço de título de dívida (prova de 2025, q. 8)", size=35,
            dados=["Valor de face: 1.000", "Prazo: 10 anos", "Cupom: 8% → 80 por ano", "YTM (taxa de mercado): 10%"],
            dados_w=540,
            passos=["[c]Preço = VP dos cupons + VP do principal[/c]",
                    "VP dos cupons = 80 × [1 − 1 ÷ 1,10¹⁰] ÷ 0,10 = 80 × 6,1446 = [y]491,57[/y]",
                    "VP do principal = 1.000 ÷ 1,10¹⁰ = 1.000 ÷ 2,5937 = [y]385,54[/y]",
                    "Preço = 491,57 + 385,54 = [g]877,11[/g]  → deságio (abaixo de 1.000)",
                    "HP 12C: f FIN → 10 n → 10 i → 80 PMT → 1000 FV → PV = −877,11"])
passo_a_passo(base, [
    "Preço de título de dívida. Questão oito da prova de 2025. Face de 1.000, dez anos, cupom de 8% ao ano, ou seja, 80 reais por ano, "
    "e a taxa de mercado é 10%. O preço é a soma de duas partes: o valor presente dos cupons e o valor presente do principal.",
    "Os cupons são uma anuidade: 80 vezes um menos um sobre 1,10 elevado a dez, tudo dividido por 0,10. O fator dá 6,1446. "
    "Vezes 80: 491,57.",
    "O principal é pago uma vez só, no ano dez: 1.000 dividido por 1,10 elevado a dez, que é 2,5937. Dá 385,54.",
    "Somando: 491,57 mais 385,54, igual a 877,11. O título é negociado com deságio, abaixo do valor de face.",
    "Na HP 12C: f FIN, 10 n, 10 i, 80 PMT, 1000 FV, e aperta PV. Aparece menos 877,11. Não esqueça de preencher os dois: PMT e FV.",
])

add(tipo="grafico", bloco=5, titulo="Juros sobem → preço do título cai", img="titulo",
    notas=["Cupom é [b]fixo[/b]: se a taxa de mercado sobe, o preço cai.",
           "Cupom > taxa de mercado → [g]ágio[/g] (7% → 1.070,24)",
           "Cupom < taxa de mercado → [r]deságio[/r] (10% → 877,11)",
           "Quanto mais longo o prazo, mais o preço oscila (risco de taxa de juros)."],
    narr="Por que o preço ficou abaixo de mil? Porque o cupom é fixo em 8%, e o mercado exige 10%. Para render 10%, o título precisa ser mais barato. "
         "Se a taxa de mercado cair para 7%, o mesmo título vale 1.070,24: ágio. Regra: cupom maior que a taxa de mercado, ágio. "
         "Cupom menor, deságio. Juros sobem, preço cai.")

base = dict(tipo="lista", bloco=5, titulo="Modigliani-Miller", size=36,
            itens=["[y]MM I sem impostos[/y]: VL = VU — a estrutura de capital não muda o valor. “A pizza é a mesma, só muda o número de fatias.”",
                   "[y]MM II[/y]: Re = Ra + (Ra − Rd) × D/E — mais dívida → Re sobe e compensa a dívida barata → CMPC constante.  Ex.: Ra 12%, Rd 8%, D/E 1 → Re = 16%",
                   "[y]MM com impostos[/y]: [c]VL = VU + T × D[/c] — o benefício fiscal dos juros aumenta o valor.",
                   "Na prática, custos de falência e de agência limitam a dívida (teoria do trade-off)."])
passo_a_passo(base, [
    "Por fim, Modigliani e Miller. Proposição um, sem impostos: o valor da empresa alavancada é igual ao da não alavancada. "
    "A estrutura de capital não altera o valor. A pizza é a mesma, só muda o número de fatias.",
    "Proposição dois: o custo do capital próprio sobe com a dívida. Re igual a Ra mais Ra menos Rd, vezes D sobre E. "
    "Com Ra de 12%, Rd de 8% e D sobre E igual a um, o Re vai para 16%. Esse aumento compensa exatamente a dívida mais barata, "
    "e o CMPC continua 12%.",
    "Com impostos, muda tudo: o valor da alavancada é o valor da não alavancada mais T vezes D, o benefício fiscal dos juros. "
    "No extremo, cem por cento de dívida seria ótimo.",
    "Na prática isso não acontece porque custos de falência e de agência limitam a dívida. Essa é a teoria do trade-off.",
])

add(tipo="calc", bloco=5, titulo="MM com impostos (Ross, cap. 16, q. 16)", size=36,
    dados=["LAJIR perpétuo: 64.000", "T: 34%", "Dívida: 95.000 a 8,5%", "Ru: 15%"], dados_w=520,
    passos=["VU = LAJIR × (1 − T) ÷ Ru = 64.000 × 0,66 ÷ 0,15 = [y]281.600[/y]",
            "Benefício fiscal = T × D = 0,34 × 95.000 = [y]32.300[/y]",
            "VL = 281.600 + 32.300 = [g]313.900[/g]"],
    narr="Um exemplo do Ross. LAJIR perpétuo de 64.000, alíquota de 34%, dívida de 95.000, custo do capital não alavancado de 15%. "
         "O valor sem dívida é uma perpetuidade: 64.000 vezes 0,66, dividido por 0,15, igual a 281.600. "
         "O benefício fiscal é 34% de 95.000, igual a 32.300. Então o valor alavancado é 313.900. "
         "Repare que a taxa da dívida, 8,5%, nem foi usada: na fórmula de MM com impostos, só entram T e D.")

add(tipo="grafico", bloco=5, titulo="A dívida aumenta o valor (com impostos)", img="mm",
    notas=["Sem impostos: as duas barras seriam [y]iguais[/y] (MM I).",
           "Com impostos: a barra cresce [g]T × D = 32.300[/g].",
           "Esse ganho é o governo “pagando” parte dos juros."],
    narr="No gráfico: sem impostos, as duas barras seriam iguais. Com impostos, a empresa com dívida vale 32.300 a mais, "
         "que é o imposto que ela deixa de pagar por causa dos juros.")

add(tipo="pegadinha", bloco=5, titulo="Bloco 5 · Pegadinha",
    texto="No CMPC a dívida entra [y]após impostos[/y]: Rd × (1 − T). Mas se o enunciado já der o custo da dívida "
          "“após impostos”, [r]não multiplique por (1 − T) de novo[/r]. E use [y]pesos a valor de mercado[/y].",
    narr="A pegadinha do bloco cinco: no CMPC, a dívida entra depois dos impostos, Rd vezes um menos T. "
         "Mas se o enunciado já der o custo da dívida após impostos, não multiplique de novo. E os pesos são a valor de mercado.")

# =====================================================================
# BLOCO 6 — RESUMO FINAL
# =====================================================================
add(tipo="capa", bloco=6, kicker="Bloco 6", titulo="Resumo final: as 10 pegadinhas",
    sub="Leia esta lista antes de entrar na sala", tempo="≈ 3 minutos",
    narr="Bloco seis: o resumo final. As dez pegadinhas mais comuns. Se der tempo, revise esta lista antes de entrar na sala.")

P1 = ["[y]Juros não entram[/y] no LAJIR nem no FCO — só no cálculo do imposto e no FC para credores.",
      "Gastos de capital: [y]some a depreciação de volta[/y] (Imob. final − inicial + depreciação).",
      "Liquidez [y]imediata usa só o caixa[/y]. Tirar só os estoques é a seca.",
      "Multiplicador do PL = Ativo ÷ PL = [y]1 + D/E[/y].",
      "Payback descontado é [y]sempre maior[/y] que o simples."]
P2 = ["Prêmio de risco de mercado já dado → [y]não subtraia Rf de novo[/y].",
      "Risco da carteira [y]não é média ponderada[/y] dos desvios (o retorno e o beta são).",
      "Gordon usa [y]D1 = D0 × (1 + g)[/y], não o dividendo já pago.",
      "CMPC: Rd × (1 − T) [y]uma vez só[/y], com pesos a [y]valor de mercado[/y].",
      "Título: preço = [y]VP dos cupons + VP do principal[/y] (na HP, preencha PMT e FV)."]
base = dict(tipo="lista", bloco=6, titulo="Pegadinhas 1 a 5", itens=P1, numerada=True, size=38)
passo_a_passo(base, [
    "Um: juros não entram no LAJIR nem no fluxo de caixa operacional. Eles só aparecem no cálculo do imposto e no fluxo para credores. "
    "Lembre da Dahlia: o FCO foi LAJIR mais depreciação menos impostos, 6.454,20, sem tirar os 1.830 de juros.",
    "Dois: nos gastos de capital, some a depreciação de volta. Imobilizado final menos inicial, mais depreciação. "
    "Na Dahlia, a variação do imobilizado foi só 3.150, mas a empresa comprou 7.200 em ativos.",
    "Três: liquidez imediata usa só o caixa. Se você tirou só os estoques, calculou a seca. "
    "Foi exatamente o erro de 2025: 0,77 em vez de 0,12.",
    "Quatro: o multiplicador do patrimônio líquido é um mais D sobre E. Não é D sobre E sozinho. "
    "Com D sobre E de 1,40, o multiplicador é 2,40.",
    "Cinco: o payback descontado é sempre maior que o simples. "
    "No nosso projeto, 3,25 anos contra 2,56. Se der o contrário, revise o desconto.",
])
base = dict(tipo="lista", bloco=6, titulo="Pegadinhas 6 a 10", itens=P2, numerada=True, num_ini=6, size=38)
passo_a_passo(base, [
    "Seis: se o prêmio de risco de mercado já foi dado, não subtraia a taxa livre de risco de novo. "
    "Com Selic de 12% e prêmio de 7%, a Vale exige 12 mais 1,2 vezes 7, e não 1,2 vezes 7 menos 12.",
    "Sete: o risco da carteira não é média ponderada dos desvios-padrão. O retorno é, o beta é, mas o desvio não. "
    "Calcule o retorno da carteira em cada cenário e só depois a variância.",
    "Oito: Gordon usa o próximo dividendo, D um. Se o enunciado der o dividendo recém-pago, multiplique por um mais g. "
    "0,80 vira 0,84 antes de dividir pelo preço.",
    "Nove: no CMPC, a dívida entra vezes um menos T uma vez só, e os pesos são a valor de mercado. "
    "Se o enunciado disser custo da dívida após impostos, ele já está multiplicado.",
    "Dez: preço de título é valor presente dos cupons mais valor presente do principal. Na calculadora, preencha PMT e FV. "
    "Esquecer o principal transforma 877,11 em 491,57, e a questão inteira se perde.",
])

add(tipo="lista", bloco=6, titulo="Na hora da prova",
    itens=["Identifique o tipo de questão → ache o [y]capítulo[/y] na folha de fórmulas.",
           "Monte a conta [y]em passos[/y], escrevendo cada resultado intermediário.",
           "Na HP 12C: [y]f REG[/y] antes de cada questão nova; investimento inicial com [y]CHS[/y].",
           "Termine [b]sempre[/b] com 2 linhas de [g]interpretação[/g]: o que o número significa e qual a decisão."],
    narr="E para fechar, o método na hora da prova. Identifique o tipo de questão e ache o capítulo na folha. "
         "Monte a conta em passos, escrevendo cada resultado intermediário, porque isso vale ponto parcial. "
         "Na HP 12C, limpe a memória com f REG antes de cada questão e lance o investimento inicial com CHS. "
         "E termine sempre com duas linhas de interpretação: o que o número significa e qual é a decisão. "
         "Boa prova!")

add(tipo="capa", bloco=0, kicker="Fim da revisão", titulo="Boa prova!",
    sub="Qual fórmula · como montar · como interpretar", tempo="Adm. Financeira · Ross, 9ª edição",
    narr="Até a próxima.")
