# Lista de Tarefas

Lista de tarefas pra usar no terminal, feita em Python. Foi um dos meus primeiros projetos.

Dá pra adicionar tarefas com prioridade (baixa, média ou alta), marcar como concluída, reabrir, editar, remover e limpar as que já foram concluídas. Tudo fica salvo num `tarefas.json` na mesma pasta do script.

## Como usar

```bash
git clone https://github.com/ViniciuscLemos/lista-de-tarefas
cd lista-de-tarefas
python todo.py
```

Não precisa instalar nada além do Python 3.

## Como fica

```
  📋 Suas tarefas:
  ---------------------------------------------
  1. ⬜ 🔴 Estudar SQL pra prova
  2. ✅ 🟢 Comprar pão
        concluída em 08/10/2026 10:02
  3. ⬜ 🟡 Revisar o trabalho de POO
  ---------------------------------------------
  1/3 concluídas · 2 pendente(s)
```

A bolinha é a prioridade (vermelha alta, amarela média, verde baixa). Na hora de escolher a prioridade dá pra digitar `média`, `media` ou só a inicial (`a`, `m`, `b`).

Se o `tarefas.json` estiver corrompido ou num formato estranho, o programa guarda uma cópia dele como `tarefas.json.corrompido` e começa uma lista nova, em vez de travar. E ele salva num arquivo temporário antes de trocar pelo de verdade, então se o computador desligar no meio, a lista antiga continua inteira.

## Testes

```bash
python -m unittest discover -s tests
```
