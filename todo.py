import json
import os

ARQUIVO = "tarefas.json"


def carregar_tarefas():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def salvar_tarefas(tarefas):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=2)


def listar_tarefas(tarefas):
    if not tarefas:
        print("\n  Nenhuma tarefa cadastrada.\n")
        return
    print("\n  📋 Suas tarefas:")
    print("  " + "-" * 35)
    for i, tarefa in enumerate(tarefas, 1):
        status = "✅" if tarefa["concluida"] else "⬜"
        print(f"  {i}. {status} {tarefa['nome']}")
    print("  " + "-" * 35 + "\n")


def adicionar_tarefa(tarefas):
    nome = input("  Nome da tarefa: ").strip()
    if not nome:
        print("  ⚠️  Nome não pode ser vazio.")
        return
    tarefas.append({"nome": nome, "concluida": False})
    salvar_tarefas(tarefas)
    print(f"  ✅ Tarefa '{nome}' adicionada!\n")


def concluir_tarefa(tarefas):
    listar_tarefas(tarefas)
    if not tarefas:
        return
    try:
        num = int(input("  Número da tarefa a concluir: "))
        tarefa = tarefas[num - 1]
        if tarefa["concluida"]:
            print("  ⚠️  Tarefa já está concluída.\n")
        else:
            tarefa["concluida"] = True
            salvar_tarefas(tarefas)
            print(f"  ✅ '{tarefa['nome']}' marcada como concluída!\n")
    except (ValueError, IndexError):
        print("  ⚠️  Número inválido.\n")


def remover_tarefa(tarefas):
    listar_tarefas(tarefas)
    if not tarefas:
        return
    try:
        num = int(input("  Número da tarefa a remover: "))
        removida = tarefas.pop(num - 1)
        salvar_tarefas(tarefas)
        print(f"  🗑️  '{removida['nome']}' removida!\n")
    except (ValueError, IndexError):
        print("  ⚠️  Número inválido.\n")


def menu():
    print("\n  ================================")
    print("        📝 Lista de Tarefas       ")
    print("  ================================")
    print("  1. Ver tarefas")
    print("  2. Adicionar tarefa")
    print("  3. Concluir tarefa")
    print("  4. Remover tarefa")
    print("  0. Sair")
    print("  ================================")
    return input("  Escolha uma opção: ").strip()


def main():
    tarefas = carregar_tarefas()
    while True:
        opcao = menu()
        if opcao == "1":
            listar_tarefas(tarefas)
        elif opcao == "2":
            adicionar_tarefa(tarefas)
        elif opcao == "3":
            concluir_tarefa(tarefas)
        elif opcao == "4":
            remover_tarefa(tarefas)
        elif opcao == "0":
            print("\n  Até mais! 👋\n")
            break
        else:
            print("  ⚠️  Opção inválida.\n")


if __name__ == "__main__":
    main()
