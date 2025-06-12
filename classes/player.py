from PPlay.sprite import*
from PPlay.keyboard import*
from classes.tiros import*
from constantes import*

#Classe que cuida de todas propriedades do player
class Player(Sprite):
    def __init__(self, imagem_caminho, dificuldade):
        super().__init__(imagem_caminho)
        self.contador = 1
        self.tiros = []
        self.dificuldade = dificuldade
        self.vidas = 3
    
    def player_movimento(self, janela):
        speed = 300 - self.dificuldade * 50
        self.move_key_x(speed * janela.delta_time())
        if self.x >= janela.width:
            self.set_position(0 - self.width, self.y)
        elif self.x <= 0 - self.width:
            self.set_position(janela.width, self.y)

    def atirar(self, janela, teclado):
        self.contador += janela.delta_time()
        if teclado.key_pressed("space") and self.contador >= 1 * self.dificuldade:
            self.tiros.append(Tiro("assets/bala.png", self, -1))
            self.contador = 0
        for bala in self.tiros:
            bala.bala_movimento(janela)
            if bala.y <= -bala.height:
                self.tiros.remove(bala)
            bala.draw()

    def update(self, enemies):
        for bala in enemies.tiros:
            if bala.y - bala.height >= self.y:
                if self.collided(bala):
                    self.vidas -= 1
                    enemies.tiros.remove(bala)
                    enemies.atirou = False
        
        if self.vidas <= 0:
            return PERDEU
        else:
            return RODANDO
