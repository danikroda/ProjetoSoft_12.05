# codigo/main.py
from modelos import UsuarioFactory, GerenciadorCSV

def iniciar_sistema():
    print("==================================================")
    print("      SISTEMA DE AVALIAÇÃO DE DESEMPENHO (RH)     ")
    print("==================================================\n")
    
    # 1. Demonstração prática do Padrão Singleton
    print("--- [Teste 1] Verificando o Padrão Singleton ---")
    banco_instancia_1 = GerenciadorCSV()
    banco_instancia_2 = GerenciadorCSV()
    
    if banco_instancia_1 is banco_instancia_2:
        print("-> Sucesso: Ambas as variáveis apontam para a mesma instância em memória.")
        print(f"-> Endereço de memória único: {id(banco_instancia_1)}\n")
    else:
        print("-> Erro: O Singleton falhou. Instâncias diferentes foram geradas.\n")

    # 2. Demonstração prática do Padrão Factory Method
    print("--- [Teste 2] Criando Usuários com a Factory ---")
    dados_usuarios = [
        ("admin", "Tati"),
        ("rh", "Felipe"),
        ("funcionario", "Daniel")
    ]

    usuarios_ativos = []

    # Cria as entidades via Fábrica e realiza a persistência simulada via Singleton
    for tipo, nome in dados_usuarios:
        try:
            # A Factory cria o objeto correto sem o Main conhecer as classes derivadas
            novo_usuario = UsuarioFactory.criar_usuario(tipo, nome)
            usuarios_ativos.append(novo_usuario)
            
            # O Singleton centraliza a gravação
            banco_instancia_1.salvar_usuario(novo_usuario.nome, tipo)
        except ValueError as e:
            print(f"[Erro] {e}")

    # 3. Execução dos comportamentos específicos (Polimorfismo / MVC Controller)
    print("\n--- [Teste 3] Executando Painéis Baseados no Perfil ---")
    for usuario in usuarios_ativos:
        print(usuario.acessar_painel())

    print("\n==================================================")
    print("          PROTÓTIPO EXECUTADO COM SUCESSO         ")
    print("==================================================")

if __name__ == "__main__":
    iniciar_sistema()