# Análise Oficial: Votos Computados Pós-17h — 2º Turno Eleições 2026

[![Status](https://img.shields.io/badge/Status-Consolidado%20TSE-success.svg)](https://tse.jus.br)
[![Eleições](https://img.shields.io/badge/Pleito-25%20Outubro%202026-blue.svg)](https://tse.jus.br)
[![Vídeo Vertical](https://img.shields.io/badge/Apresenta%C3%A7%C3%A3o-9%3A16%20Reels%2FShorts-orange.svg)](video/apresentacao_vertical.html)

Repositório contendo a auditoria técnica, análise de dados estatísticos e apresentação em vídeo vertical (proporção 9:16) sobre os votos computados após as 17h no 2º turno das eleições presidenciais do Brasil em **25 de outubro de 2026**.

---

## 📊 1. Resumo dos Dados Oficiais (100% Apurado)

* **Luiz Inácio Lula da Silva (PT)**: 64.256.232 votos (**51,79%**) — *Reeleito*
* **Flávio Bolsonaro (PL)**: 59.826.041 votos (**48,21%**)
* **Votos Válidos Totais**: 124.082.273 votos
* **Margem de Vitória**: **4.430.191 votos**

### 🔍 O Volume Real dos Votos Registrados Após as 17h
* **Total de votos pós-17h**: **34.330 votos** (**0,028%** do total nacional).
* **Impacto sobre a margem de vitória**: Representa apenas **0,77%** da vantagem obtida pelo candidato vencedor.
* **Veredito Matemático**: Impossibilidade estatística de alteração do resultado. Mesmo no cenário contrafactual onde 100% dos 34.330 votos fossem concedidos a Flávio Bolsonaro, a margem de Lula permaneceria superior a **4,36 milhões de votos**.

---

## 📁 2. Estrutura do Repositório

```text
├── dados/
│   ├── dados_apuracao_2026.json          # Dataset estruturado em JSON com a apuração e cronologia
│   └── dados_pos_17h.csv                 # Tabela CSV com métricas e comparação proporcional
├── video/
│   ├── analise_eleicoes_2026_vertical.mp4 # VÍDEO FINAL EXPORTADO (1080x1920, 9:16 com áudio pt-BR)
│   ├── apresentacao_vertical.html        # Player interativo web 9:16 com animação em Canvas e voz
│   ├── render_video.py                   # Script Python/FFmpeg de renderização do vídeo MP4
│   └── gerar_audio.ps1                   # Script de síntese de voz (Microsoft Maria Desktop pt-BR)
├── ANALISE_DETALHADA_VOTOS_POS_17H.md     # Relatório técnico aprofundado com jurisprudência do STF
├── setup_git.ps1                          # Script utilitário em PowerShell para publicação no GitHub
└── README.md                              # Este documento
```

---

## 📱 3. O Vídeo Vertical Pronto (MP4 - 9:16)

O arquivo de vídeo renderizado já está gerado e disponível diretamente na pasta do repositório:
👉 **[`video/analise_eleicoes_2026_vertical.mp4`](video/analise_eleicoes_2026_vertical.mp4)**

- **Resolução**: 1080x1920 (proporção 9:16 nativa para Reels, Shorts e TikTok).
- **Duração**: ~70 segundos cobrindo as 5 cenas chave da eleição.
- **Áudio**: Locução em português brasileiro (`pt-BR`) sincronizada com legendas e cartões dinâmicos.
- **Gráficos**: Comparação visual proporcional dos 34.330 votos contra a vantagem de 4,43 milhões e a cronologia da virada.

---

## ⏱️ 4. Cronologia da Noite da Apuração (25/10/2026)

| Horário | Evento | Detalhe |
| :---: | :--- | :--- |
| **16:32** | Liminar do STF | Min. Cristiano Zanin concede extensão até as 19h apenas em seções com falta de ônibus e alagamentos. |
| **17:00** | Fechamento Geral | >99,9% das seções fecham pontualmente e iniciam transmissão. |
| **19:00** | Encerramento Total | Encerramento das seções prorrogadas (totalizando 34.330 votos). |
| **19:46** | Alternância Provisória | Flávio Bolsonaro assume liderança com o avanço acelerado de urnas do Sul e Sudeste. |
| **20:24** | Virada Definitiva | Lula reassume o 1º lugar com a entrada de grandes blocos do Nordeste e capitais. |
| **21:08** | Proclamação do TSE | Com 97,69% totalizado, TSE confirma matematicamente a reeleição de Lula. |

---

## 🚀 5. Como Publicar no seu GitHub

Para enviar este projeto ao seu repositório no GitHub:

1. Crie um repositório vazio na sua conta do [GitHub](https://github.com/new).
2. Execute no PowerShell dentro desta pasta:
```powershell
git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
git branch -M main
git push -u origin main
```
*Ou utilize o script automatizado:*
```powershell
.\setup_git.ps1 -RepoUrl "https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git"
```

---

## ⚖️ Licença e Fontes

Dados extraídos dos registros públicos oficiais de totalização do Tribunal Superior Eleitoral (TSE) e decisões do Supremo Tribunal Federal (STF).
Código e análise disponibilizados sob licença MIT.
