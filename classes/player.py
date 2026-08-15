from PPlay.sprite import*
from PPlay.keyboard import*
from classes.tiros import*
from constantes import*

#Classe que cuida de todas propriedades do player
class Player(Sprite):
    def __init__(self, imagem, dificuldade, janela, vidas=3, nave=0, contador=0):
        super().__init__(imagem)
        self.contador_tiros = 1
        self.tiros = []

        self.dificuldade = dificuldade

        self.sprites = {
            'nave' : "assets/nave.png",
            'quente1' : "assets/nave_quente.png",
        }
        self.vidas = vidas

        self.nave = nave
        self.mortal = True
        self.contador_imortal = 0
        self.contador_piscada = 0
        self.contador_quente = contador


        self.janela = janela
    
    def player_movimento(self):
        speed = 300 - self.dificuldade * 50
        self.move_key_x(speed * self.janela.delta_time())
        if self.x >= self.janela.width:
            self.set_position(0 - self.width, self.y)
        elif self.x <= 0 - self.width:
            self.set_position(self.janela.width, self.y)

    def atirar(self, teclado, pos_x, pos_y):
        self.contador_tiros += self.janela.delta_time()
        if self.contador_quente < 2:
            self.nave = 0
        if teclado.key_pressed("space"):
            self.contador_quente += self.janela.delta_time()
            if self.contador_quente >= 2 and self.contador_quente < 4:
                self.nave = 1
            elif self.contador_quente >= 4 and self.contador_quente < 6:
                self.nave = 2
            elif self.contador_quente >= 6:
                self.nave = 3
                self.contador_quente = 0

            if  self.contador_tiros >= 0.5:
                self.tiros.append(Tiro("assets/bala.png", self, -1))
                self.contador_tiros = 0

        else:
            if self.contador_quente > 0:
                self.contador_quente -= self.janela.delta_time()

        print(self.nave)
        for bala in self.tiros:
            bala.bala_movimento(self.janela)
            if bala.y <= -bala.height:
                self.tiros.remove(bala)
            bala.draw()

    def update(self, enemies, pos_x, pos_y, contador_imortal = 0):
        #self.janela.draw_text(f"{self.contador_quente}", 0, 0, 50, (255, 255, 255), "Arial")
        for bala in enemies.tiros:
            if bala.y - bala.height >= self.y:
                if self.collided(bala) and self.mortal:
                    self.vidas -= 1
                    enemies.tiros.remove(bala)
                    self.set_position(pos_x, pos_y)
                    self.mortal = False
                    self.contador_imortal = 0

            if self.nave == 3:
                self.vidas -= 1
                self.set_position(pos_x, pos_y)
                self.mortal = False
                self.contador_imortal = 0
                self.contador_quente = 0

        if self.contador_imortal >= 2:
            self.mortal = True

        self.contador_imortal += self.janela.delta_time()

        if self.vidas <= 0:
            return PERDEU
        else:
            return RODANDO
