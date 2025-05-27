from PPlay.sprite import*

class Tiro(Sprite):
    def __init__(self, imagem_caminho, atirador, direcao):
        super().__init__(imagem_caminho)
        self.direcao = direcao
        if self.direcao > 0:
            self.x = atirador.x + (atirador.width - self.width) / 2
            self.y = atirador.y + atirador.height
        else:
            self.x = atirador.x + (atirador.width - self.width) / 2
            self.y = atirador.y

    def bala_movimento(self, janela):
        speed = 250 * self.direcao
        self.move_y(speed * janela.delta_time())
