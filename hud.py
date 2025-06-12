from PPlay.sprite import*

class Hud():
    def __init__(self, vidas, janela):
        self.coracoes = []
        self.janela = janela
        for i in range(vidas):
            self.coracoes.append(Sprite("assets/life.png"))
            self.coracoes[i].set_position(janela.width - self.coracoes[i].width * (i + 1), 0)

    def mostrar_hud(self, pontuacao):
        for coracao in self.coracoes:
            coracao.draw()
        if self.janela.delta_time() > 0:
            fps = 1/self.janela.delta_time()
        else:
            fps = 0
        self.janela.draw_text(f"{fps}", 0, 0, 50, (255, 255, 255), "Arial")
        #self.janela.draw_text(f"{pontuacao}", 0, 0, 50, (255, 255, 255), "Arial")