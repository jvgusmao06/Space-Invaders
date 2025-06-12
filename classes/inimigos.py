from PPlay.sprite import*
from classes.tiros import*
from constantes import*
import random

class Inimigos():
    def __init__(self, pontuacao, dificuldade):
        self.inimigos = []
        self.linha = 3
        self.coluna = 5
        for linha in range(self.coluna):
            linha_inimigos = []
            for coluna in range(self.linha):
                inimigo = Sprite("assets/inimigo.png")
                espaco_h = inimigo.width * 1.5
                espaco_v = inimigo.height * 1.5
                inimigo.set_position(linha * espaco_h, coluna * espaco_v)
                linha_inimigos.append(inimigo)
            self.inimigos.append(linha_inimigos)
            self.speed = 50 + dificuldade * 50
            self.pontuacao = pontuacao
            self.tiros = []
            self.atirou = False

    def inimigos_movimento(self, janela, limit):
        if not any(self.inimigos) or not any (linha for linha in self.inimigos):
            return VITORIA
        inimigo_esquerda = min(inimigo.x for linha in self.inimigos for inimigo in linha)
        inimigo_direita = max(inimigo.x + inimigo.width for linha in self.inimigos for inimigo in linha)

        for linha in self.inimigos:
            for inimigo in linha:
                inimigo.move_x(self.speed * janela.delta_time())

        if (inimigo_esquerda <= 0 and self.speed < 0) or (inimigo_direita >= janela.width and self.speed > 0):
            self.speed *= -1
            for linha in self.inimigos:
                for inimigo in linha:
                    inimigo.y += inimigo.height

        inimigo_baixo = max(inimigo.y + inimigo.height for linha in self.inimigos for inimigo in linha)

        if inimigo_baixo >= limit:
            return PERDEU
        else:
            return RODANDO

    def atirar(self, janela):
        if not self.atirou:
            inimigos_ativos = [inimigo for linha in self.inimigos for inimigo in linha if inimigo]
            if inimigos_ativos:
                inimigo = random.choice(inimigos_ativos)
                self.tiros.append(Tiro("assets/bala.png", inimigo, 1))
                self.atirou = True

        for bala in self.tiros:
            bala.bala_movimento(janela)
            if bala.y >= janela.width:
                self.tiros.remove(bala)
                self.atirou = False
            bala.draw()

    def draw(self):
        for linha in self.inimigos:
            for inimigo in linha:
                inimigo.draw()
    
    def update(self, tiros):
        for bala in tiros:
            #if bala.y > self.inimigos[0][0].y and bala.y < self.inimigos[4][2].y:
                for linha in self.inimigos:
                    for inimigo in linha:
                        if inimigo.collided(bala):
                            linha.remove(inimigo)
                            tiros.remove(bala)
                            self.pontuacao += 10
        return self.pontuacao
                    