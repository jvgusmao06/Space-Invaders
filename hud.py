from PPlay.sprite import*

class Hud():
    def __init__(self, vidas, janela):
        self.coracoes = []
        for i in range(vidas):
            self.coracoes.append(Sprite("assets/life.png"))
            self.coracoes[i].set_position(janela.width - self.coracoes[i].width * (i + 1), 0)

    def mostrar_hud(self):
        for coracao in self.coracoes:
            coracao.draw()