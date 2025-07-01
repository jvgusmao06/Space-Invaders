from PPlay.sprite import*
from PPlay.keyboard import*
from classes.tiros import*
from constantes import*

#Classe que cuida de todas propriedades do player
class Player(Sprite):
    def __init__(self, imagem_caminho, dificuldade, janela):
        super().__init__(imagem_caminho)
        self.contador_tiros = 1
        self.tiros = []

        self.dificuldade = dificuldade

        self.vidas = 3
        self.mortal = True
        self.contador_imortal = 0
        self.contador_piscada = 0

        self.janela = janela
    
    def player_movimento(self):
        speed = 300 - self.dificuldade * 50
        self.move_key_x(speed * self.janela.delta_time())
        if self.x >= self.janela.width:
            self.set_position(0 - self.width, self.y)
        elif self.x <= 0 - self.width:
            self.set_position(self.janela.width, self.y)

    def atirar(self, teclado):
        self.contador_tiros += self.janela.delta_time()
        if teclado.key_pressed("space") and self.contador_tiros >= 1:
            self.tiros.append(Tiro("assets/bala.png", self, -1))
            self.contador_tiros = 0
        for bala in self.tiros:
            bala.bala_movimento(self.janela)
            if bala.y <= -bala.height:
                self.tiros.remove(bala)
            bala.draw()

    def update(self, enemies, pos_x, pos_y, contador_imortal = 0):
        for bala in enemies.tiros:
            if bala.y - bala.height >= self.y:
                if self.collided(bala) and self.mortal:
                    self.vidas -= 1
                    enemies.tiros.remove(bala)
                    self.set_position(pos_x, pos_y)
                    self.mortal = False
                    self.contador_imortal = 0

        if self.contador_imortal >= 2:
            self.mortal = True

        self.contador_imortal += self.janela.delta_time()

        if self.vidas <= 0:
            return PERDEU
        else:
            return RODANDO
