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
player = Player("assets/nave.png", dificuldade)
player.set_position(meio("x", player), janela.height - player.height - 10)

#Função que detecta se um objeto foi clicado
def mouse_menu (obj):
    if mouseh.is_over_object(obj) and mouseh.is_button_pressed(1):
        while mouseh.is_button_pressed(1):
            janela.update()
        return True
    return False

while True:
    #Vai para o menu ao clicar esc
    if teclado.key_pressed('esc'):
        gamestate = MENU

    #Mostra o menu
    if gamestate == MENU:
        janela.set_background_color((0, 50, 30))

        #Cria uma nova matriz de inimigos toda vez que volta pro menu
        enemies = Inimigos(pontuacao = 0, dificuldade = dificuldade)

        #Volta a posição do player e desespawna as balas quando volta para o menu
        player = Player("assets/nave.png", dificuldade)
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
                gamestate = MENU
            elif mouse_menu((Menu_sprites["sair"])):
                gamestate = SAIR
    
    #Quando o player mata todos os inimigos a matriz é recriada
    elif gamestate == VITORIA:
            enemies = Inimigos(pontuacao, dificuldade)
            gamestate = RODANDO

    #Quando o jogo está rodando
    elif gamestate == RODANDO:
        janela.set_background_color((0, 5, 15))

        #Cuida da movimentação do player
        player.player_movimento(janela)
        #Se acaba as vidas o player vai para a tela de game over
        gamestate = player.update(enemies)
        #Cuida do sitema de atirar do player
        player.atirar(janela, teclado)
        player.draw()

        #Se o player não perdeu todas as vidas
        if not gamestate == PERDEU:
            #Checa se os inimigos chegaram na posição do player e cuida das 
            gamestate = enemies.inimigos_movimento(janela, player.y)
        #Checa as colisões e atualiza as pontuações
        pontuacao = enemies.update(player.tiros)
        Hud(player.vidas, janela).mostrar_hud(pontuacao)
        enemies.atirar(janela)
        enemies.draw()

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

    elif gamestate == PERDEU:
        janela.set_background_color((0, 0, 0))
        gameover = Sprite("assets/gameover.png")
        gameover.set_position(meio('x', gameover), meio('y', gameover))
        #pedir_nome(teclado)
        gameover.draw()

    elif gamestate == SAIR:
        janela.close()

    janela.update()
