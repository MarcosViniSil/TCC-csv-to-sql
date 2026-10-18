# Comparação de Modelos de Tradução Inglês → Português

Este projeto faz parte do TCC de comparação entre modelos de tradução e compara varios aspectos da tradução na tarefa de inglês para português. A ideia é responder a duas perguntas:

1. **Qual modelo traduz melhor?** (qualidade)
2. **Qual modelo é mais leve e rápido?** (eficiência)

## Modelos avaliados

| Apelido | Modelo |
|---|---|
| MarianMT | `Helsinki-NLP/opus-mt-tc-big-en-pt` |
| NLLB | `facebook/nllb-200-distilled-600M` |
| M2M | `facebook/m2m100_418M` |


## Como o projeto funciona

O fluxo é simples:

```
Dados das traduções (CSV)
        │
        ▼
  filter.py  ──►  gera comandos INSERT em SQL
        │
        ▼
PostgreSQL (via Docker)  ◄──  insert_*.sql
        │
        ▼
  queries.py  ──►  consulta o banco e gera
                   tabelas e gráficos comparativos
```

## Estrutura do projeto

| Arquivo / pasta | Função |
|---|---|
| `queries.py` | Consulta o PostgreSQL e gera os gráficos (boxplots e barras) e tabelas de comparação. |
| `filter.py` | Converte os CSVs de resultados em comandos `INSERT` para popular o banco. |
| `docker-compose.yaml` | Sobe o PostgreSQL e o pgAdmin em containers. |
| `insert_mdn.sql` | Dados de tradução da base MDN. |
| `insert_php.sql` | Dados de tradução da base PHP. |
| `insert_open_subtitles.sql` | Dados de tradução da base OpenSubtitles. |
| `results/` | Gráficos gerados pela análise. |

## Resultados

Os gráficos ficam em `results/`:

- `BLEU_GENERAL_TEXTS.png` e `BLEU_SPECIFC_TEXTS.png`
- `CHRF-GENERAL.png` e `CHRF-SPECIFIC.png`
- `BERTSCORE-GENERAL.png` e `BERTSCORE_SPECIFIC.png`
- `AVERAGE-CPU-USAGE.png`
- `PEAK-MEMORY.png` e `PEAK-MEMORY2.png`
- `INFERENCE-TIME.png` e `INFERENCE-TIME2.png`

Os arquivos com prefixo `BACKUP-` são versões anteriores dos mesmos gráficos.

## Como executar

Pré-requisitos: Docker, Python 3 e as bibliotecas `psycopg2`, `matplotlib`, `numpy` e `tabulate`.

```bash
# 1. Suba o banco de dados
docker compose up -d

# 2. Carregue os dados
psql -h localhost -U postgres -d corn_party -f insert_mdn.sql
psql -h localhost -U postgres -d corn_party -f insert_php.sql
psql -h localhost -U postgres -d corn_party -f insert_open_subtitles.sql

# 3. Gere as tabelas e gráficos
python queries.py
```

O pgAdmin fica disponível em `http://localhost:8080` (usuário `user@localhost.com`, senha `password`).


