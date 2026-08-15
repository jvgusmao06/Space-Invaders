from PPlay.window import *
from PPlay.keyboard import *
from PPlay.mouse import *
from PPlay.sprite import *
from constantes import*
from classes.player import*
from classes.inimigos import*
from hud import*

# Codigo do Heitor Gomes

#Criar a tela
res = 70
janela = Window(16 * res, 9 * res)
janela.set_title("João Vitor Gusmão de Souza")
janela.set_background_color((0,0,0))

#Funçãos que pega as posições no meio
def meio (cord, obj):
    cord = cord.lower()
    meio = 0
    if cord == "y":
        meio = janela.height/2 - (obj.height / 2)

    elif cord == "x":
        meio = janela.width/2 - (obj.width / 2)
    return meio

#Inputs
teclado = janela.get_keyboard()

mouseh = janela.get_mouse()

#sprites do menu
Menu_sprites = {
    "titulo" : Sprite("assets/space_invaders.png"),
    "play": Sprite("assets/jogar.png"),
    "dificuldade": Sprite("assets/dificuldade.png"),
    "ranking": Sprite("assets/ranking.png"),
    "sair": Sprite("assets/sair.png")
}
#posição dos sprites do menu inicial
Menu_sprites["titulo"].set_position(meio('x', Menu_sprites["titulo"]),20)
Menu_sprites["play"].set_position(meio('x',Menu_sprites["play"]), Menu_sprites["titulo"].y + Menu_sprites["titulo"].height + 40)
Menu_sprites["dificuldade"].set_position(meio('x', Menu_sprites["dificuldade"]), Menu_sprites["play"].y + Menu_sprites["play"].height + 10)
Menu_sprites["ranking"].set_position(meio('x',Menu_sprites["ranking"]), Menu_sprites["dificuldade"].y + Menu_sprites["dificuldade"].height + 10)
Menu_sprites["sair"].set_position(meio('x',Menu_sprites["sair"]),Menu_sprites["ranking"].y + Menu_sprites["ranking"].height + 10)

#Sprites do menu de dificuldade
Dificuldades_sprites = {
    "facil": Sprite("assets/facil.png"),
    "medio": Sprite("assets/medio.png"),
    "dificil": Sprite("assets/dificil.png"),
}
Dificuldades_sprites["facil"].set_position(meio('x',Dificuldades_sprites["facil"]), 200)
Dificuldades_sprites["medio"].set_position(meio('x',Dificuldades_sprites["medio"]), Dificuldades_sprites["facil"].y + Dificuldades_sprites["facil"].height + 10)
Dificuldades_sprites["dificil"].set_position(meio('x',Dificuldades_sprites["dificil"]), Dificuldades_sprites["medio"].y + Dificuldades_sprites["medio"].height + 10)

#Variáveis importantes
gamestate = MENU
dificuldade = FACIL
vitorias = 0
nome_jogador = ""
pontuacao_final = 0
player_quente = 0

player = Player("assets/nave.png", dificuldade, janela)
pos_x = (meio("x", player))
pos_y = (janela.height - player.height - 10)
player.set_position(pos_x, pos_y)

#Função que detecta se um objeto foi clicado
def mouse_menu (obj):
    if mouseh.is_over_object(obj) and mouseh.is_button_pressed(1):
        while mouseh.is_button_pressed(1):
            janela.update()
        return True
    return False

def salvar_pontucao(nome, pontuacao):
    try:
        with open('ranking.txt', 'a') as arquivo:
            arquivo.write(f'{nome}, {pontuacao}\n')
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o ranking: {e}")

def carregar_ranking():
    jogadores = []
    try:
        with open('ranking.txt', 'r') as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(',')
                if len(partes) == 2:
                    nome = partes[0]
                    try:
                        pontos = int(partes[1])
                        jogadores.append({'nome' : nome, 'pontos' : pontos})
                    except ValueError:
                        continue
    except FileNotFoundError:
        return []
    
    ranking_ordenado = sorted(jogadores, key=lambda jogador: jogador['pontos'], reverse=True)

    return ranking_ordenado[:5]

while True:
    #Vai para o menu ao clicar esc
    if teclado.key_pressed('esc'):
        gamestate = MENU

    #Mostra o menu
    if gamestate == MENU:
        janela.set_background_color((0, 50, 30))

        #Cria uma nova matriz de inimigos toda vez que volta pro menu
        enemies = Inimigos(dificuldade, vitorias, pontuacao = 0)

        #Volta a posição do player e desespawna as balas quando volta para o menu
        player = Player("assets/nave.png", dificuldade, janela)
        player.set_position(meio("x", player), janela.height - player.height - 10)
        player.tiros = []

        #Desenha os sprites do menu
        for sprite in Menu_sprites.values():
            sprite.draw()
            if mouse_menu(Menu_sprites["play"]):
                gamestate = RODANDO
            elif mouse_menu(Menu_sprites["dificuldade"]):
                gamestate = DIFICULDADE
            elif mouse_menu(Menu_sprites["ranking"]):
                gamestate = RANKING
            elif mouse_menu((Menu_sprites["sair"])):
                gamestate = SAIR

    #Quando o jogo está rodando
    elif gamestate == RODANDO:
        janela.set_background_color((0, 5, 15))

        if player.nave == 0 and player_quente != 0 and player.mortal:
            x = player.x
            y = player.y
            vidas = player.vidas
            player = Player("assets/nave.png", dificuldade, janela, vidas, player.nave, player.contador_quente)
            player.set_position(x, y)
            player_quente = 0

        elif player.nave == 1 and player_quente < 1:
            x = player.x
            y = player.y
            vidas = player.vidas
            player = Player("assets/nave_quente.png", dificuldade, janela, vidas, player.nave, player.contador_quente)
            player.set_position(x, y)
            player_quente = 1

        elif player.nave == 2 and player_quente != 2:
            x = player.x
            y = player.y
            vidas = player.vidas
            player = Player("assets/nave_quente1.png", dificuldade, janela, vidas, player.nave, player.contador_quente)
            player.set_position(x, y)
            player_quente = 2

        #Cuida da movimentação do player
        player.player_movimento()
        #Se acaba as vidas o player vai para a tela de game over
        gamestate = player.update(enemies, pos_x, pos_y)
        #Cuida do sitema de atirar do player
        player.atirar(teclado, pos_x, pos_y)
        player.draw()
        print(player_quente)

        if not player.mortal:
            player.contador_imortal += janela.delta_time()
            intervalo = 0.4
            if player.contador_imortal % (2 * intervalo) <= intervalo:
                janela.set_background_color((0, 5, 15))
        
        #Se o player não perdeu todas as vidas
        if not gamestate == PERDEU:
            #Checa se os inimigos chegaram na posição do player e cuida das 
            gamestate = enemies.inimigos_movimento(janela, player.y)
        #Checa as colisões e atualiza as pontuações
        pontuacao = enemies.update(player.tiros)
        Hud(player.vidas, janela).mostrar_hud(pontuacao)
        enemies.atirar(janela)
        enemies.draw()

    elif gamestate == PERDEU:
        janela.set_background_color((0, 0, 0))
        gameover = Sprite("assets/gameover.png")
        gameover.set_position(meio('x', gameover), 150)
        gameover.draw()

        janela.draw_text("Digite seu nome:", 350, 420, 30, color=(255, 255, 255))

        caixa_input_rect = pygame.Rect(350, 460, 400, 50)
        pygame.draw.rect(janela.screen, (255, 255, 255), caixa_input_rect, 2)

        janela.draw_text(nome_jogador, caixa_input_rect.x + 10, caixa_input_rect.y + 10, 30, color=(255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # Se pressionar ENTER
                    if nome_jogador: # Só salva se o nome não for vazio
                        salvar_pontucao(nome_jogador, pontuacao)
                        nome_jogador = "" # Limpa o nome para a próxima vez
                        gamestate = MENU # Volta para o menu
                elif event.key == pygame.K_BACKSPACE:
                    nome_jogador = nome_jogador[:-1] # Apaga o último caractere
                else:
                    if len(nome_jogador) < 12: # Limita o tamanho do nome
                        nome_jogador += event.unicode # Adiciona a letra digitada

    elif gamestate == RANKING:
        janela.set_background_color((20, 20, 80))

        janela.draw_text("Top 5 Jogadores", 50, 50, 50, color=(255, 255, 0))

        top_jogadores = carregar_ranking()

        if not top_jogadores:
            janela.draw_text("Ninguém no ranking ainda!", 50, 250, 30, color=(255, 255, 255))
        else:
            y_pos = 150
            for i, jogador in enumerate(top_jogadores):
                texto_nome = f"{i + 1}. {jogador['nome']}"
                texto_pontos = str(jogador['pontos'])

                janela.draw_text(texto_nome, 100, y_pos, 35, color=(255, 255, 255))
                janela.draw_text(texto_pontos, 600, y_pos, 35, color=(0, 255, 0))
                y_pos += 50

    #Quando o player mata todos os inimigos a matriz é recriada
    elif gamestate == VITORIA:
            vitorias += 1
            enemies = Inimigos(dificuldade, vitorias, pontuacao)
            player.vidas = 3
            gamestate = RODANDO
            

    elif gamestate == DIFICULDADE:
        janela.set_background_color((10, 0, 30))
        for sprite in Dificuldades_sprites.values():
            sprite.draw()
            if mouse_menu(Dificuldades_sprites["facil"]):
                dificuldade = FACIL
                gamestate = MENU    
            elif mouse_menu(Dificuldades_sprites["medio"]):
                dificuldade = MEDIO
                gamestate = MENU 
            elif mouse_menu(Dificuldades_sprites["dificil"]):
                dificuldade = DIFICIL
                gamestate = MENU 

    elif gamestate == SAIR:
        janela.close()

    janela.update()