# codigo/testes.py
import unittest
from modelos import UsuarioFactory, GerenciadorCSV, Admin, Funcionario

class TestUsuarioFactory(unittest.TestCase):
    
    # 1. Cenário de Sucesso
    def test_criar_usuario_sucesso(self):
        usuario = UsuarioFactory.criar_usuario("admin", "Tati")
        self.assertIsInstance(usuario, Admin)
        self.assertEqual(usuario.nome, "Tati")

    # 2. Cenário de Falha/Exceção
    def test_criar_usuario_falha_tipo_invalido(self):
        # Tentar criar um perfil que não existe deve levantar um ValueError
        with self.assertRaises(ValueError):
            UsuarioFactory.criar_usuario("diretor", "Ana")

    # 3. Cenário de Borda (Edge Case)
    def test_criar_usuario_borda_formatacao(self):
        # A fábrica deve ser capaz de lidar com espaços extras e letras maiúsculas/minúsculas misturadas
        usuario = UsuarioFactory.criar_usuario("  fUnCiOnArIo  ", "Daniel")
        self.assertIsInstance(usuario, Funcionario)


class TestGerenciadorCSV(unittest.TestCase):
    
    # 1. Cenário de Sucesso
    def test_singleton_instancia_unica(self):
        # Duas chamadas independentes devem retornar exatamente a mesma instância
        banco1 = GerenciadorCSV()
        banco2 = GerenciadorCSV()
        self.assertIs(banco1, banco2)

    # 2. Cenário de Falha/Exceção
    def test_singleton_falha_argumentos_invalidos(self):
        # Tentar passar um parâmetro para o construtor Singleton deve gerar TypeError
        with self.assertRaises(TypeError):
            GerenciadorCSV("caminho_invalido.csv")

    # 3. Cenário de Borda (Edge Case)
    def test_singleton_borda_estado_compartilhado(self):
        # Se alterarmos uma propriedade em 'banco1', ela deve refletir em 'banco2'
        banco1 = GerenciadorCSV()
        banco2 = GerenciadorCSV()
        
        banco1.arquivo = "banco_teste.csv"
        self.assertEqual(banco2.arquivo, "banco_teste.csv")
        
        # Limpeza do estado para não prejudicar futuras execuções
        banco1.arquivo = "dados_rh.csv"


if __name__ == '__main__':
    unittest.main()