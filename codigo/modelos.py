
# ==========================================
# PADRÃO 1: SINGLETON
# ==========================================
class GerenciadorCSV:
    """ Singleton para garantir um único ponto de acesso e escrita no arquivo de dados """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GerenciadorCSV, cls).__new__(cls)
            cls._instancia.arquivo = "dados_rh.csv"
            print("[Sistema] Instância do Banco CSV iniciada.")
        return cls._instancia

    def salvar_usuario(self, nome, tipo):
        # Simula a gravação física dos dados estruturados em formato CSV
        print(f"[GerenciadorCSV] Gravando no arquivo '{self.arquivo}': {nome},{tipo}")


# ==========================================
# PADRÃO 2: FACTORY METHOD
# ==========================================
class Usuario:
    """ Classe base (Produto) que define a estrutura comum de um usuário """
    def __init__(self, nome):
        self.nome = nome

    def acessar_painel(self):
        raise NotImplementedError("Este método deve ser implementado pelas subclasses.")


class Admin(Usuario):
    """ Produto Concreto: Administrador com acesso total """
    def acessar_painel(self):
        return f"Painel ADMIN: O usuário '{self.nome}' tem controle total do sistema corporativo."


class RH(Usuario):
    """ Produto Concreto: Profissional de RH com permissões de gestão """
    def acessar_painel(self):
        return f"Painel RH: O usuário '{self.nome}' pode gerar links de avaliação e exportar relatórios."


class Funcionario(Usuario):
    """ Produto Concreto: Funcionário comum com acesso limitado """
    def acessar_painel(self):
        return f"Painel FUNCIONÁRIO: O usuário '{self.nome}' pode responder avaliações pendentes."


class UsuarioFactory:
    """ Fábrica (Creator) responsável por instanciar os perfis corretos isolando a lógica """
    @staticmethod
    def criar_usuario(tipo, nome):
        tipo = tipo.lower().strip()
        if tipo == "admin":
            return Admin(nome)
        elif tipo == "rh":
            return RH(nome)
        elif tipo in ["funcionario", "funcionário"]:
            return Funcionario(nome)
        else:
            raise ValueError(f"Tipo de usuário '{tipo}' é desconhecido pelo sistema.")