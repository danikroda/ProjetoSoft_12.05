# Entrega da Parte 2 - Sistema de Avaliação de RH

## Tarefa 2.1: Definição da Arquitetura

### 1. Padrão Arquitetural Escolhido e Justificativa

O padrão arquitetural selecionado para o desenvolvimento do protótipo é o **MVC (Model-View-Controller)**. 

**Justificativa:** O domínio do sistema de avaliação de desempenho envolve regras de negócio claras, múltiplos perfis de acesso (Administrador, RH e Funcionário) e a manipulação de persistência local de dados. A escolha do MVC justifica-se pelos seguintes pontos:
* **Isolamento da Lógica de Negócio:** Permite separar completamente as regras de validação de acesso e a estruturação dos dados de avaliação (Model) da forma como o menu interativo é exibido no terminal (View).
* **Facilidade de Evolução:** Se houver a necessidade futura de migrar a interface do sistema de uma linha de comando (CLI) para uma aplicação Web ou Mobile, toda a camada de inteligência e exportação de dados permanecerá intacta.
* **Testabilidade:** Torna viável a criação de testes unitários automatizados e isolados na camada Model, garantindo que os fluxos críticos funcionem de forma independente da interface.

### 2. Representação dos Componentes e Relacionamentos

A arquitetura do sistema segue o fluxo unidirecional de controle e comunicação entre as três camadas principais, conforme ilustrado abaixo:

```text
       +---------------------------------------+
       |                 VIEW                  |
       |  (Exibe menus e captura entradas)     |
       +------------------+--------------------+
                          |
                          | (1) Envia comandos do usuário
                          v
       +---------------------------------------+
       |              CONTROLLER               |
       |  (Processa rotas e regras de acesso)  |
       +------------------+--------------------+
                          |
                          | (2) Solicita / Altera dados
                          v
       +---------------------------------------+
       |                 MODEL                 |
       |  (Entidades, Validações e Gerador CSV)|
       +---------------------------------------+


3. Componentes Principais e Responsabilidades
A estrutura organizacional do projeto distribui as responsabilidades da seguinte forma:

Model (modelos.py):

Representa o núcleo do sistema contendo as entidades principais (Usuario, Avaliacao).Detém a responsabilidade exclusiva de manipular a persistência de dados e a formatação para a exportação de relatórios em formato CSV.Executa validações de regras de negócio cruciais, garantindo que as operações respeitem estritamente os dados enviados.

View (interface.py ou funções de exibição no console):

Responsável pela interação direta com o usuário final.Renderiza os menus contextuais baseados nas permissões de cada perfil (Admin, RH ou Funcionário).Captura as entradas do teclado e as envia para processamento.

Controller (main.py):

Coordena o fluxo da aplicação agindo como o intermediário entre a View e o Model.Interpreta as ações submetidas na interface, invoca os métodos apropriados na camada de negócio e determina o próximo estado do sistema.


4. Limitações e Trade-offs
A adoção do padrão MVC neste contexto acarreta uma limitação específica:

Aumento da Complexidade Inicial (Overengineering): Para um protótipo focado em funcionalidades iniciais bem definidas, dividir o fluxo de execução de ações simples (como a listagem de um perfil) obrigatoriamente por três camadas distintas exige a criação de mais arquivos e linhas de código redundantes. Contudo, este custo inicial é aceitável, dado que mitiga o risco de acoplamento prejudicial e viabiliza a manutenção sustentável a longo prazo.

Minha reflexão: Escolhi pelo padrão MVC fundamentado na necessidade de garantir que o sistema possua uma fundação sólida e modular, especialmente no que diz respeito ao controle rígido de perfis de acesso. Separar a lógica que gera e exporta os dados em CSV da camada que interage com o usuário impede que erros de interface corrompam as regras de negócio. Esta arquitetura garante uma separação clara de responsabilidades, facilitando a escrita de testes unitários para a camada de dados e assegurando que o sistema possa crescer de forma organizada.

Implementação com Padrões de Projeto
Neste protótipo, foram atendidas histórias de usuário principais ligadas à criação/autenticação de diferentes perfis (Admin, RH, Funcionário) e à persistência centralizada desses dados. Para isso, aplicamos os seguintes padrões:

1. Padrão: Factory Method
Categoria: Criacional

Onde foi aplicado no código: Arquivo modelos.py, na classe UsuarioFactory e método criar_usuario().

Diagrama do Padrão Aplicado:

      +-------------------+
      |  UsuarioFactory   |
      +-------------------+
      | + criar_usuario() |
      +---------+---------+
                | (instancia)
                v
      +-------------------+
      |     Usuario       | <--- (Classe Base abstrata)
      +-------------------+
         /      |      \
        /       |       \
 +-------+  +----+  +-------------+
 | Admin |  | RH |  | Funcionario |
 +-------+  +----+  +-------------+

2. Padrão: Singleton
Categoria: Criacional
Onde foi aplicado no código: Arquivo modelos.py, na classe GerenciadorCSV, método __new__().

      +---------------------------+
      |      GerenciadorCSV       |
      +---------------------------+
      | - instancia_unica         |
      | - arquivo_destino         |
      +---------------------------+
      | + get_instancia()         |
      | + salvar_usuario()        |
      +-------------+-------------+
                    | (retorna a mesma instância
                    |  para o Controller)
                    v
            [ main.py (Controller) ]

Revisão Crítica
Considerando os dois padrões aplicados, embora o padrão Singleton garanta um ponto único de manipulação do arquivo CSV na camada Model (evitando conflitos de gravação simultânea), ele introduz um estado global oculto na aplicação. Em um cenário concreto de crescimento do sistema ou incorporação de um novo membro na equipe para escrever testes unitários, esse padrão se torna um problema: os testes da camada Model podem interferir uns nos outros compartilhando a mesma instância, sujando o arquivo base de testes e quebrando o isolamento de estados esperado por uma arquitetura MVC limpa.

---

## Testes Automatizados

### Estratégia de Testes Adotada
A estratégia adotada foi a de **Testes Unitários** utilizando o framework nativo `unittest` do Python. Essa abordagem é altamente adequada para o que foi implementado porque, graças à arquitetura MVC, conseguimos isolar completamente a camada de domínio (Model) e testar as lógicas dos padrões de projeto (Factory e Singleton) sem depender da interface do usuário. 

**Aspectos não cobertos:** Não foram cobertos pelos testes a camada View (menus e prints) e o Controller (`main.py`). Testar interações diretas no terminal e I/O (Input/Output) exigiria a criação de simulações (Mocks e Patches) do teclado do usuário, o que introduziria uma complexidade artificial e desnecessária para a validação da segurança das regras de negócio deste protótipo.

### Revisão Crítica
A parte do código implementada na Tarefa 2.2 que seria mais difícil de testar em larga escala é o **GerenciadorCSV (Singleton)**. Como o Singleton mantém um estado global e contínuo durante toda a execução da aplicação (o endereço do arquivo em memória), um teste que modifique esse estado pode "poluir" o ambiente e causar falhas imprevisíveis em testes subsequentes. Em um projeto real com dezenas de testes, essa dificuldade exigiria a implementação de métodos rigorosos de limpeza (teardown) para "destruir" a instância do Singleton após a execução de cada teste, violando o princípio básico do próprio padrão.
