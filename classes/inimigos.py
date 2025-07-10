from PPlay.sprite import*
from classes.tiros import*
from constantes import*
import random

#tiros entre 1 e 2 segundos
class Inimigos():
    def __init__(self, dificuldade, vitorias, pontuacao):
        #Criando a matriz de inimigos
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

            self.dificuldade = dificuldade

            #Velocidade dos inimigos muda de acordo com a velocidade
            self.speed = (75 + self.dificuldade * 25) + vitorias * 25
            
            #Pontuação do jogador
            self.pontuacao = pontuacao

            #Lista de tiros desparados pelos inimigos
            self.tiros = []
            self.contador = 0 #Tempo desde o último tiro

            #Tempo de recarga dos inimigos também muda de acordo com a dificuldade
            self.contador_max = random.randint(10, 20) / (5 * self.dificuldade)

            #Calcula o inimigo das extremidades afim de otimizações e colisão dos inimigos com as paredes
            self.inimigo_esquerda = min(inimigo.x for linha in self.inimigos for inimigo in linha)
            self.inimigo_direita = max(inimigo.x + inimigo.width for linha in self.inimigos for inimigo in linha)
            self.inimigo_cima = min(inimigo.y for linha in self.inimigos for inimigo in linha)
            self.inimigo_baixo = max(inimigo.y + inimigo.height for linha in self.inimigos for inimigo in linha)

    def inimigos_movimento(self, janela, limit):
        if not any(self.inimigos) or not any (linha for linha in self.inimigos):
            return VITORIA
        self.inimigo_esquerda = min(inimigo.x for linha in self.inimigos for inimigo in linha)
        self.inimigo_direita = max(inimigo.x + inimigo.width for linha in self.inimigos for inimigo in linha)

        for linha in self.inimigos:
            for inimigo in linha:
                inimigo.move_x(self.speed * janela.delta_time())

        if (self.inimigo_esquerda <= 0 and self.speed < 0) or (self.inimigo_direita >= janela.width and self.speed > 0):
            self.speed *= -1
            for linha in self.inimigos:
                for inimigo in linha:
                    inimigo.y += inimigo.height

        self.inimigo_baixo = max(inimigo.y + inimigo.height for linha in self.inimigos for inimigo in linha)

        if self.inimigo_baixo >= limit:
            return PERDEU
        else:
            return RODANDO

    def atirar(self, janela):
        self.contador += janela.delta_time()
        if self.contador >= self.contador_max:
            inimigos_ativos = [inimigo for linha in self.inimigos for inimigo in linha if inimigo]
            if inimigos_ativos:
                inimigo = random.choice(inimigos_ativos)
                self.tiros.append(Tiro("assets/bala1.png", inimigo, 1))
                self.contador = 0
                self.contador_max = random.randint(10, 20)/ (5 * self.dificuldade)

        for bala in self.tiros:
            bala.bala_movimento(janela)
            if bala.y >= janela.width:
                self.tiros.remove(bala)
            bala.draw()

    def draw(self):
        for linha in self.inimigos:
            for inimigo in linha:
                inimigo.draw()
    
    def update(self, tiros):
        for bala in tiros:
            if (bala.y > self.inimigo_cima and bala.y < self.inimigo_baixo) and (bala.x > self.inimigo_esquerda and bala.x < self.inimigo_direita):
                for linha in self.inimigos:
                    for inimigo in linha:
                        if inimigo.collided(bala):
                            linha.remove(inimigo)
                            tiros.remove(bala)
                            if self.dificuldade == FACIL:
                                self.pontuacao += 10
                            elif self.dificuldade == MEDIO:
                                self.pontuacao += 30
                            else:
                                self.pontuacao += 50
        return self.pontuacao
                    