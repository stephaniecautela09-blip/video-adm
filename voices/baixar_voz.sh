#!/bin/sh
# Baixa a voz pt-BR "faber" (Piper, licença CC0) usada na narração.
set -e
cd "$(dirname "$0")"
curl -sSL -o faber.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-pt_BR-faber-medium.tar.bz2
tar xjf faber.tar.bz2
cp vits-piper-pt_BR-faber-medium/pt_BR-faber-medium.onnx* .
rm -rf faber.tar.bz2 vits-piper-pt_BR-faber-medium
