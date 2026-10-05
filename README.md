# 📝 Lista de Tarefas

![Testes](https://github.com/ViniciuscLemos/lista-de-tarefas/actions/workflows/testes.yml/badge.svg)

Aplicação de lista de tarefas no terminal feita em Python, sem dependências externas.

## Funcionalidades

- Adicionar tarefas com prioridade (🟢 baixa, 🟡 média, 🔴 alta)
- Listar todas as tarefas ou só as pendentes, com resumo de progresso
- Marcar tarefa como concluída (registra data e hora) e reabrir
- Editar nome e prioridade
- Remover uma tarefa ou limpar todas as concluídas de uma vez
- Salva automaticamente em `tarefas.json`, ao lado do script
  - escrita segura (arquivo temporário + troca), sem risco de corromper no meio
  - se o arquivo estiver corrompido, faz um backup e começa do zero
  - lê sem problemas arquivos da versão antiga

## Como usar

**1. Clone o repositório**
```bash
git clone https://github.com/ViniciuscLemos/lista-de-tarefas
cd lista-de-tarefas
```

**2. Execute o programa**
```bash
python todo.py
```

Só precisa de Python 3.10+.

## Testes

```bash
python -m unittest discover -s tests -v
```

Os testes rodam automaticamente no GitHub Actions a cada push.

## Estrutura

```
todo.py              # regras (criar, concluir, editar...) + menu do terminal
tests/test_todo.py   # testes unitários das regras e da persistência
```

As regras ficam em funções que não usam `input`/`print`, o que permite testá-las isoladamente; o menu só cuida da interação com o usuário.

## Tecnologias

- Python 3
- JSON (para salvar os dados)
- unittest (testes)

## Autor

Feito por [Vinicius Lemos](https://github.com/ViniciuscLemos)
