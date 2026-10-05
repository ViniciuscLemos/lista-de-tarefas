import json
import os
from datetime import datetime

# O arquivo fica ao lado do script, não importa de onde o programa é executado.
# A variável de ambiente TODO_ARQUIVO permite trocar o caminho (usado nos testes).
ARQUIVO = os.environ.get(
    "TODO_ARQUIVO",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "tarefas.json"),
)

PRIORIDADES = ("baixa", "media", "alta")
ICONES_PRIORIDADE = {"baixa": "🟢", "media": "🟡", "alta": "🔴"}
FORMATO_DATA = "%d/%m/%Y %H:%M"


# ---------------------------------------------------------------------------
# Persistência
# ---------------------------------------------------------------------------

def _normalizar(tarefa):
    """Completa tarefas salvas por versões antigas, que só tinham nome e concluida."""
    tarefa.setdefault("concluida", False)
    tarefa.setdefault("prioridade", "media")
    tarefa.setdefault("criada_em", None)
    tarefa.setdefault("concluida_em", None)
    return tarefa


def carregar_tarefas(arquivo=None):
    arquivo = arquivo or ARQUIVO
    if not os.path.exists(arquivo):
        return []
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return [_normalizar(t) for t in json.load(f)]
    except (json.JSONDecodeError, OSError):
        # Arquivo corrompido: guarda uma cópia para não perder os dados e começa do zero
        backup = arquivo + ".corrompido"
        os.replace(arquivo, backup)
        print(f"  ⚠️  Arquivo de tarefas inválido. Uma cópia foi salva em {backup}.")
        return []


def salvar_tarefas(tarefas, arquivo=None):
    arquivo = arquivo or ARQUIVO
    # Escreve num arquivo temporário e depois substitui: se o programa
    # cair no meio da escrita, o arquivo original não fica pela metade.
    temporario = arquivo + ".tmp"
    with open(temporario, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=2)
    os.replace(temporario, arquivo)


# ---------------------------------------------------------------------------
# Regras (sem input/print — fáceis de testar)
# ---------------------------------------------------------------------------

def _agora():
    return datetime.now().strftime(FORMATO_DATA)


def criar_tarefa(tarefas, nome, prioridade="media"):
    nome = nome.strip()
    if not nome:
        raise ValueError("Nome não pode ser vazio.")
    if prioridade not in PRIORIDADES:
        raise ValueError("Prioridade deve ser: baixa, media ou alta.")
    tarefa = {
        "nome": nome,
        "concluida": False,
        "prioridade": prioridade,
        "criada_em": _agora(),
        "concluida_em": None,
    }
    tarefas.append(tarefa)
    return tarefa


def obter_tarefa(tarefas, numero):
    """Recebe o número exibido ao usuário (começa em 1)."""
    if not 1 <= numero <= len(tarefas):
        raise IndexError("Número inválido.")
    return tarefas[numero - 1]


def concluir(tarefas, numero):
    tarefa = obter_tarefa(tarefas, numero)
    if tarefa["concluida"]:
        raise ValueError("Tarefa já está concluída.")
    tarefa["concluida"] = True
    tarefa["concluida_em"] = _agora()
    return tarefa


def reabrir(tarefas, numero):
    tarefa = obter_tarefa(tarefas, numero)
    if not tarefa["concluida"]:
        raise ValueError("Tarefa ainda não foi concluída.")
    tarefa["concluida"] = False
    tarefa["concluida_em"] = None
    return tarefa


def editar(tarefas, numero, nome=None, prioridade=None):
    tarefa = obter_tarefa(tarefas, numero)
    if nome is not None:
        nome = nome.strip()
        if not nome:
            raise ValueError("Nome não pode ser vazio.")
        tarefa["nome"] = nome
    if prioridade is not None:
        if prioridade not in PRIORIDADES:
            raise ValueError("Prioridade deve ser: baixa, media ou alta.")
        tarefa["prioridade"] = prioridade
    return tarefa


def remover(tarefas, numero):
    obter_tarefa(tarefas, numero)  # valida o número
    return tarefas.pop(numero - 1)


def limpar_concluidas(tarefas):
    """Remove as concluídas e retorna quantas foram removidas."""
    antes = len(tarefas)
    tarefas[:] = [t for t in tarefas if not t["concluida"]]
    return antes - len(tarefas)


def resumo(tarefas):
    concluidas = sum(1 for t in tarefas if t["concluida"])
    return {"total": len(tarefas), "concluidas": concluidas, "pendentes": len(tarefas) - concluidas}


# ---------------------------------------------------------------------------
# Interface de terminal
# ---------------------------------------------------------------------------

def listar_tarefas(tarefas, somente_pendentes=False):
    visiveis = [(i, t) for i, t in enumerate(tarefas, 1)
                if not (somente_pendentes and t["concluida"])]
    if not visiveis:
        print("\n  Nenhuma tarefa para mostrar.\n")
        return
    titulo = "📋 Tarefas pendentes:" if somente_pendentes else "📋 Suas tarefas:"
    print(f"\n  {titulo}")
    print("  " + "-" * 45)
    for i, tarefa in visiveis:
        status = "✅" if tarefa["concluida"] else "⬜"
        icone = ICONES_PRIORIDADE.get(tarefa["prioridade"], "")
        print(f"  {i}. {status} {icone} {tarefa['nome']}")
        if tarefa["concluida_em"]:
            print(f"        concluída em {tarefa['concluida_em']}")
    r = resumo(tarefas)
    print("  " + "-" * 45)
    print(f"  {r['concluidas']}/{r['total']} concluídas · {r['pendentes']} pendente(s)\n")


def ler_numero(mensagem):
    try:
        return int(input(mensagem))
    except ValueError:
        return -1


def ler_prioridade(atual=None):
    padrao = atual or "media"
    texto = input(f"  Prioridade (baixa/media/alta) [{padrao}]: ").strip().lower()
    return texto or padrao


def executar(acao, *args, **kwargs):
    """Roda uma regra e mostra o erro de forma amigável."""
    try:
        return acao(*args, **kwargs)
    except (ValueError, IndexError) as erro:
        print(f"  ⚠️  {erro}\n")
        return None


def menu():
    print("\n  ================================")
    print("        📝 Lista de Tarefas       ")
    print("  ================================")
    print("  1. Ver todas as tarefas")
    print("  2. Ver tarefas pendentes")
    print("  3. Adicionar tarefa")
    print("  4. Concluir tarefa")
    print("  5. Reabrir tarefa")
    print("  6. Editar tarefa")
    print("  7. Remover tarefa")
    print("  8. Limpar tarefas concluídas")
    print("  0. Sair")
    print("  ================================")
    return input("  Escolha uma opção: ").strip()


def main():
    tarefas = carregar_tarefas()
    while True:
        try:
            opcao = menu()
        except (EOFError, KeyboardInterrupt):
            opcao = "0"

        if opcao == "1":
            listar_tarefas(tarefas)
        elif opcao == "2":
            listar_tarefas(tarefas, somente_pendentes=True)
        elif opcao == "3":
            nome = input("  Nome da tarefa: ")
            tarefa = executar(criar_tarefa, tarefas, nome, ler_prioridade())
            if tarefa:
                salvar_tarefas(tarefas)
                print(f"  ✅ Tarefa '{tarefa['nome']}' adicionada!\n")
        elif opcao == "4":
            listar_tarefas(tarefas, somente_pendentes=True)
            tarefa = executar(concluir, tarefas, ler_numero("  Número da tarefa a concluir: "))
            if tarefa:
                salvar_tarefas(tarefas)
                print(f"  ✅ '{tarefa['nome']}' marcada como concluída!\n")
        elif opcao == "5":
            listar_tarefas(tarefas)
            tarefa = executar(reabrir, tarefas, ler_numero("  Número da tarefa a reabrir: "))
            if tarefa:
                salvar_tarefas(tarefas)
                print(f"  🔄 '{tarefa['nome']}' voltou para pendente.\n")
        elif opcao == "6":
            listar_tarefas(tarefas)
            numero = ler_numero("  Número da tarefa a editar: ")
            atual = executar(obter_tarefa, tarefas, numero)
            if atual:
                novo_nome = input(f"  Novo nome [{atual['nome']}]: ").strip() or None
                tarefa = executar(editar, tarefas, numero, novo_nome, ler_prioridade(atual["prioridade"]))
                if tarefa:
                    salvar_tarefas(tarefas)
                    print("  ✏️  Tarefa atualizada!\n")
        elif opcao == "7":
            listar_tarefas(tarefas)
            removida = executar(remover, tarefas, ler_numero("  Número da tarefa a remover: "))
            if removida:
                salvar_tarefas(tarefas)
                print(f"  🗑️  '{removida['nome']}' removida!\n")
        elif opcao == "8":
            quantidade = limpar_concluidas(tarefas)
            salvar_tarefas(tarefas)
            print(f"  🧹 {quantidade} tarefa(s) concluída(s) removida(s).\n")
        elif opcao == "0":
            print("\n  Até mais! 👋\n")
            break
        else:
            print("  ⚠️  Opção inválida.\n")


if __name__ == "__main__":
    main()
