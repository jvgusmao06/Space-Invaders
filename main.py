from PPlay.window import *
from PPlay.keyboard import *
from PPlay.mouse import *
from PPlay.sprite import *
from constantes import*
from classes.player import*
from classes.inimigos import*

# Codigo do Heitor Gomes
res = 70
janela = Window(16 * res, 9 * res)
janela.set_title("João Vitor Gusmão de Souza")
janela.set_background_color((0,0,0))
def meio (cord, obj):
    cord = cord.lower()
    meio = 0
    if cord == "y":
        meio = janela.height/2 - (obj.height / 2)

    elif cord == "x":
        meio = janela.width/2 - (obj.width / 2)
    return meio

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

Dificuldades_sprites = {
    "facil": Sprite("assets/facil.png"),
    "medio": Sprite("assets/medio.png"),
    "dificil": Sprite("assets/dificil.png"),
}
Dificuldades_sprites["facil"].set_position(meio('x',Dificuldades_sprites["facil"]), 200)
Dificuldades_sprites["medio"].set_position(meio('x',Dificuldades_sprites["medio"]), Dificuldades_sprites["facil"].y + Dificuldades_sprites["facil"].height + 10)
Dificuldades_sprites["dificil"].set_position(meio('x',Dificuldades_sprites["dificil"]), Dificuldades_sprites["medio"].y + Dificuldades_sprites["medio"].height + 10)

gamestate = MENU
dificuldade = FACIL

def mouse_menu (obj):
    if mouseh.is_over_object(obj) and mouseh.is_button_pressed(1):
        return True
    return False

while True:
    print(gamestate)
    if teclado.key_pressed('esc'):
        gamestate = MENU

    if gamestate == MENU:
        janela.set_background_color((0, 50, 30))
        enemies = Inimigos(pontuacao = 0, dificuldade = dificuldade)

        player = Player("assets/nave.png", dificuldade)
        player.set_position(meio("x", player), janela.height - player.height - 10)
        player.tiros = []

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
    
    elif gamestate == VITORIA:
            enemies = Inimigos(pontuacao, dificuldade)
            gamestate = RODANDO

    elif gamestate == RODANDO:
        janela.set_background_color((0, 5, 15))

        player.player_movimento(janela)
        gamestate = player.update(enemies)
        player.atirar(janela, teclado)
        player.draw()
        if not gamestate == PERDEU:
            gamestate = enemies.inimigos_movimento(janela, player.y)
            pontuacao = enemies.update(player.tiros)
            enemies.atirar(janela)
            enemies.draw()

        janela.draw_text(f"{pontuacao}", 0, 0, 50, (255, 255, 255), "Arial")

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
        gameover.draw()

    elif gamestate == SAIR:
        janela.close()

    janela.update()
