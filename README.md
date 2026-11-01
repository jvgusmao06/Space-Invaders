# 👾 Space Invaders (Python + PPlay)

Projeto desenvolvido para a disciplina de Programação de Computadores / Jogos da **UFF (Universidade Federal Fluminense)**. Trata-se de uma recriação clássica do jogo arcade **Space Invaders**, construído em **Python** utilizando o framework/módulo gráfico **PPlay** (baseado em Pygame).

---

## 🎮 Funcionalidades

- **Menu Principal Interativo**: Navegação por cliques de mouse para Iniciar o Jogo, Configurar Dificuldade, Visualizar Ranking e Sair.
- **Níveis de Dificuldade**:
  - **Fácil**: Velocidade do jogador maior, menor velocidade e cadência de disparos inimigos.
  - **Médio**: Velocidade e cadência equilibradas.
  - **Difícil**: Menor velocidade do jogador e ataques mais rápidos dos invasores.
- **Sistema de Ondas / Vitórias Consecutivas**: A cada onda eliminada, uma nova matriz de invasores é gerada com dificuldade progressiva.
- **Mecânica de Superaquecimento da Nave**: Atirar continuamente aquece a nave do jogador, mudando seu visual visualmente (`nave_quente.png`, `nave_quente1.png`).
- **Sistema de Vidas e Imunidade Temporária**: O jogador conta com 3 vidas e ganha tempo de invulnerabilidade após ser atingido.
- **Ranking / Placar de Líderes**: Salva a pontuação em arquivo (`ranking.txt`) e exibe o Top 5 melhores pontuações no menu.
- **HUD Completo**: Contador de vidas gráficas e placar de pontuação atual.

---

## 🕹️ Controles

| Ação | Tecla / Controle |
| :--- | :--- |
| **Mover para a Esquerda** | Seta para a Esquerda (`Left Arrow`) |
| **Mover para a Direita** | Seta para a Direita (`Right Arrow`) |
| **Atirar** | Barra de Espaço (`Space`) |
| **Voltar ao Menu / Pausar** | Tecla `Esc` |
| **Navegação no Menu** | Botão Esquerdo do Mouse |
| **Inserir Nome no Game Over** | Teclado alfanumérico + `Enter` |

---

## 📁 Estrutura do Projeto

```text
Space-Invaders/
├── assets/             # Texturas, sprites da nave, inimigos, HUD e botões do menu
├── classes/            # Módulos com a lógica orientada a objetos
│   ├── inimigos.py     # Gerenciamento da matriz e lógica dos alienígenas
│   ├── player.py       # Comportamento, movimentação e estado da nave do jogador
│   └── tiros.py        # Projéteis do jogador e dos invasores
├── PPlay/              # Biblioteca de abstração gráfica e de inputs (baseada em Pygame)
├── constantes.py       # Estados de jogo e constantes de dificuldade
├── hud.py              # Interface com contador de vidas e pontuação
├── main.py             # Loop principal do jogo e máquina de estados
├── ranking.txt         # Arquivo de persistência de pontuações
└── README.md           # Documentação do projeto
```

---

## 🚀 Como Executar

### Pré-requisitos

1. **Python 3.8+** instalado em seu sistema ([python.org](https://www.python.org/)).
2. Instalar a dependência necessária (`pygame`):

```bash
pip install pygame
```

> **Nota:** A biblioteca `PPlay` já está inclusa diretamente no repositório na pasta local `PPlay/`.

### Executando o Jogo

Na raiz do repositório, execute:

```bash
python main.py
```

---

## 👨‍💻 Autor

- **João Vitor Gusmão de Souza** - *UFF (Universidade Federal Fluminense)*

