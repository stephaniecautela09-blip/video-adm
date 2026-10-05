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
