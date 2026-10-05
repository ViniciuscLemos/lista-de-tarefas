import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import todo  # noqa: E402


class TestRegras(unittest.TestCase):
    def setUp(self):
        self.tarefas = []

    def test_criar_tarefa_preenche_campos(self):
        tarefa = todo.criar_tarefa(self.tarefas, "  Estudar  ", "alta")
        self.assertEqual(tarefa["nome"], "Estudar")
        self.assertEqual(tarefa["prioridade"], "alta")
        self.assertFalse(tarefa["concluida"])
        self.assertIsNotNone(tarefa["criada_em"])
        self.assertEqual(len(self.tarefas), 1)

    def test_criar_tarefa_rejeita_nome_vazio(self):
        with self.assertRaises(ValueError):
            todo.criar_tarefa(self.tarefas, "   ")

    def test_criar_tarefa_rejeita_prioridade_invalida(self):
        with self.assertRaises(ValueError):
            todo.criar_tarefa(self.tarefas, "x", "urgente")

    def test_concluir_e_reabrir(self):
        todo.criar_tarefa(self.tarefas, "A")
        todo.concluir(self.tarefas, 1)
        self.assertTrue(self.tarefas[0]["concluida"])
        self.assertIsNotNone(self.tarefas[0]["concluida_em"])
        with self.assertRaises(ValueError):
            todo.concluir(self.tarefas, 1)

        todo.reabrir(self.tarefas, 1)
        self.assertFalse(self.tarefas[0]["concluida"])
        self.assertIsNone(self.tarefas[0]["concluida_em"])

    def test_numero_invalido(self):
        todo.criar_tarefa(self.tarefas, "A")
        for numero in (0, 2, -1):
            with self.assertRaises(IndexError):
                todo.concluir(self.tarefas, numero)

    def test_editar(self):
        todo.criar_tarefa(self.tarefas, "A")
        todo.editar(self.tarefas, 1, nome="B", prioridade="baixa")
        self.assertEqual(self.tarefas[0]["nome"], "B")
        self.assertEqual(self.tarefas[0]["prioridade"], "baixa")
        # None mantém o valor atual
        todo.editar(self.tarefas, 1)
        self.assertEqual(self.tarefas[0]["nome"], "B")

    def test_remover(self):
        todo.criar_tarefa(self.tarefas, "A")
        todo.criar_tarefa(self.tarefas, "B")
        removida = todo.remover(self.tarefas, 1)
        self.assertEqual(removida["nome"], "A")
        self.assertEqual([t["nome"] for t in self.tarefas], ["B"])

    def test_limpar_concluidas(self):
        for nome in "ABC":
            todo.criar_tarefa(self.tarefas, nome)
        todo.concluir(self.tarefas, 1)
        todo.concluir(self.tarefas, 3)
        self.assertEqual(todo.limpar_concluidas(self.tarefas), 2)
        self.assertEqual([t["nome"] for t in self.tarefas], ["B"])

    def test_resumo(self):
        todo.criar_tarefa(self.tarefas, "A")
        todo.criar_tarefa(self.tarefas, "B")
        todo.concluir(self.tarefas, 2)
        self.assertEqual(todo.resumo(self.tarefas), {"total": 2, "concluidas": 1, "pendentes": 1})


class TestPersistencia(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.arquivo = os.path.join(self.pasta.name, "tarefas.json")

    def tearDown(self):
        self.pasta.cleanup()

    def test_salvar_e_carregar(self):
        tarefas = []
        todo.criar_tarefa(tarefas, "Ler", "alta")
        todo.salvar_tarefas(tarefas, self.arquivo)
        self.assertEqual(todo.carregar_tarefas(self.arquivo), tarefas)

    def test_arquivo_inexistente_retorna_lista_vazia(self):
        self.assertEqual(todo.carregar_tarefas(self.arquivo), [])

    def test_formato_antigo_e_completado(self):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump([{"nome": "Antiga", "concluida": True}], f)
        tarefa = todo.carregar_tarefas(self.arquivo)[0]
        self.assertEqual(tarefa["prioridade"], "media")
        self.assertIn("criada_em", tarefa)

    def test_arquivo_corrompido_gera_backup(self):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            f.write("{isso não é json")
        self.assertEqual(todo.carregar_tarefas(self.arquivo), [])
        self.assertTrue(os.path.exists(self.arquivo + ".corrompido"))


if __name__ == "__main__":
    unittest.main()
