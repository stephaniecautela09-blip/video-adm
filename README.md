# Vídeos de revisão

Dois vídeos de estudo narrados em português, gerados por código.

- [Contabilidade Avançada II — Aval 1](#contabilidade-avançada-ii-aval-1) (`contabilidade/`, Manim)
- [Administração Financeira](#administração-financeira-aula-de-revisão-em-vídeo) (`src/`)

## Contabilidade Avançada II — Aval 1

Revisão de cerca de 43 minutos para a Aval 1 (Prof. Ilirio José Rech, UFG), com as tabelas, as fórmulas e os
diagramas construídos linha por linha em [Manim Community](https://www.manim.community/) e a narração
gerada pelo Piper (voz pt-BR "faber"). Cada número aparece na tela no momento em que é falado, com a conta
que o originou na barra de baixo.

| Cena | Tema | Contas resolvidas |
|---|---|---|
| 1 | Abertura: mapa da prova e os 3 avisos | — |
| 2 | Unidade 1: comparabilidade, code × common law, convergência, linha do tempo, CPC × ICPC × OCPC, IASB/ISSB, ESG, Relato Integrado | — |
| 3 | Unidade 2: conceitos do CPC 32, as 5 situações, 4 regras, método de 8 passos | — |
| 4 | Unidade 2: contas de tributo diferido | trator (slide do professor, 30%), A1, A2 |
| 5 | Unidade 3: PBA liquidado em ações (CPC 10) | exemplo do guia, B1, B2 |
| 6 | Unidade 3: PBA liquidado em caixa | exemplo do guia, C1, C2 |
| 7 | Unidade 3: benefícios a empregados (CPC 33) | — |
| 8 | Os 6 erros que mais custam nota | — |
| 9 | Fechamento | — |

Todo o conteúdo vem do *Guia de estudo enxuto* e das *Questões resolvidas* da Aval 1. As poucas contas
que não estão nesses arquivos (os lançamentos da A2 e a variação do ativo diferido no ano 2 da C1) são
avisadas na narração como "conta nossa".

Arquivos gerados (`saida/`): `aula_contabilidade_avancada_ii.mp4` (1920×1080, com capítulos),
`aula_contabilidade_avancada_ii.srt` (legendas) e `capitulos_contabilidade.txt`.

### Como gerar de novo

```sh
# dependências de sistema: ffmpeg, libcairo2-dev, libpango1.0-dev
python3 -m venv venv && . venv/bin/activate
pip install manim piper-tts numpy
./voices/baixar_voz.sh
cd contabilidade && python build.py          # narração → cenas → MP4 (1080p)
python build.py --rapido                      # versão 480p para revisar
python build.py Cena04                        # refaz só uma cena e remonta
```

- `contabilidade/roteiro.md`: o roteiro, com o texto completo da narração de cada cena. Cada trecho
  `[chave]` é uma batida de áudio.
- `contabilidade/cenas.py`: as 9 cenas em Manim. `self.fala("chave")` começa uma batida, e
  `self.em("trecho", animação)` espera a voz chegar naquele trecho para animar.
- `contabilidade/visual.py`: a cena-base com a sincronia, a tabela célula a célula (`Grade`), os cartões e os
  lançamentos.
- `contabilidade/audio.py` e `fala.py`: narração com o Piper e a leitura de números e siglas por extenso.
- `contabilidade/build.py`: renderiza as cenas em paralelo, posiciona cada áudio no instante registrado e
  junta tudo com capítulos e legendas.

# Administração Financeira: aula de revisão em vídeo

Vídeo de revisão para a prova de Administração Financeira (Ross, 9ª edição), com cerca de 30 minutos,
narrado em português e dividido em 6 blocos. O foco é saber **qual fórmula usar, como montar a conta e
como interpretar o resultado**. A ideia é que você tenha a folha de fórmulas na prova.

| Bloco | Tema | Exemplo resolvido |
|---|---|---|
| 1 | Objetivo da empresa, teoria da agência, Selic × VPL | VPL do mesmo projeto a 10%, 12% e 14% |
| 2 | Fluxo de caixa dos ativos, liquidez, endividamento, ROA/ROE, Du Pont | Dahlia (Ross 2.21), Marcos Golfe (prova 2025), Du Pont invertido (Ross 3.18) |
| 3 | Crescimento interno e sustentável, VPL, TIR, payback, IL | Hoffman (prova 2025) e um projeto resolvido pelos 4 métodos |
| 4 | Retorno esperado, desvio-padrão, risco sistemático, CAPM, alfa | Cenários (Ross 13.23a), CAPM Vale/Sabesp, alfa e SML |
| 5 | CMPC, Gordon × CAPM, preço de título, Modigliani-Miller | CMPC 12,5%, Ross 14.23, título da prova 2025, Ross 16.16 |
| 6 | As 10 pegadinhas mais comuns | — |

Cada bloco termina com a pegadinha mais provável do tema.

## Arquivos gerados (`saida/`)

- `aula_adm_financeira.mp4`: o vídeo (1920×1080, com capítulos por bloco)
- `aula_adm_financeira.srt`: legendas em português
- `capitulos.txt`: o tempo em que começa cada bloco

## Como gerar de novo

```sh
pip install piper-tts pillow matplotlib
./voices/baixar_voz.sh          # voz pt-BR "faber" (Piper, CC0)
cd src && python3 build.py      # gráficos → slides → narração → MP4
```

- `src/roteiro.py`: o roteiro. Cada cena tem o texto do slide e a narração.
- `src/slides.py`: desenha os slides no estilo de quadro.
- `src/graficos.py`: gera os gráficos (matplotlib).
- `src/fala.py`: lê números, siglas e símbolos por extenso para a voz.
- `src/build.py`: junta tudo com o ffmpeg e gera as legendas e os capítulos.

Os exemplos foram tirados do *Guia Completo — Adm Financeira — Prova 05/10* (questões do Ross, slides e
prova de 2025). Todas as contas foram conferidas.
