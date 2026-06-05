import pygame as pg
import sys
import random


class Bala:
    def __init__(self, player_x, player_y):  # atributos iniciais
        self.pos = pg.Rect(player_x + 20, player_y, 10, 10)
        self.speed = 15
        self.color = "yellow"

    def update(self):
        self.pos.y -= self.speed

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.pos)


class Inimigo:
    def __init__(self):  # atributos iniciais
        self.pos = pg.Rect(random.randint(0, 540), 0, 60, 60)
        self.speed = 3
        self.color = "red"

    def update(self):
        self.pos.y += self.speed

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.pos)


class Player:
    def __init__(self):  # atributos iniciais
        self.pos = pg.Rect(300, 300, 50, 50)
        self.speed = 10
        self.color = "cyan"

    def handle_input(self):  # movimento do player
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and self.pos.top > 0:
            self.pos.y -= self.speed
        if keys[pg.K_DOWN] and self.pos.bottom < 600:
            self.pos.y += self.speed
        if keys[pg.K_LEFT] and self.pos.left > 0:
            self.pos.x -= self.speed
        if keys[pg.K_RIGHT] and self.pos.right < 600:
            self.pos.x += self.speed

    def draw(self, surface):  # renderizar o player
        pg.draw.rect(surface, self.color, self.pos)


class Jogo:
    def __init__(self):
        pg.init()
        self.score = 0
        self.screen = pg.display.set_mode((600, 600))  # tela
        pg.display.set_caption("Shot-Shot-Shot")  # título
        self.clock = pg.time.Clock()  # ticks
        self.running = True  # define se o jogo roda ou não
        self.player = Player()  # para chamar a classe do player depois
        self.balas = []  # conta as balas no cenário
        self.inimigos = []  # conta os inimigos no cenário
        self.SPAWN = pg.USEREVENT + 1
        pg.time.set_timer(self.SPAWN, random.randint(1000, 2000))
        self.fonte = pg.font.SysFont(None, 36)

    def run(self):
        while self.running:
            self._check_events()  # Lida com fechar o jogo
            self._update()  # Lida com a lógica de movimento
            self._draw()  # Lida com o visual
            self.clock.tick(60)  # tickspeed

    def _check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    nova_bala = Bala(self.player.pos.x, self.player.pos.y)
                    self.balas.append(nova_bala)
            if event.type == self.SPAWN:
                novo_inimigo = Inimigo()
                self.inimigos.append(novo_inimigo)

    def _update(self):
        self.player.handle_input()  # fala para o player verificar os inputs

        for tiro in self.balas:
            tiro.update()

        for bicho in self.inimigos:
            bicho.update()

        for tiro in self.balas[:]:
            if tiro.pos.bottom < 0:
                self.balas.remove(tiro)

        for bicho in self.inimigos[:]:
            if bicho.pos.bottom > 630:
                self.inimigos.remove(bicho)
                self.score -= 10

        for bicho in self.inimigos[:]:
            for tiro in self.balas[:]:
                if bicho.pos.colliderect(tiro.pos):
                    if tiro in self.balas:
                        self.balas.remove(tiro)
                    if bicho in self.inimigos:
                        self.inimigos.remove(bicho)
                        self.score += 100

    def _draw(self):
        self.screen.fill("black")  # cor da tela
        self.player.draw(self.screen)  # fala para o player renderizar

        for tiro in self.balas:
            tiro.draw(self.screen)

        for bicho in self.inimigos:
            bicho.draw(self.screen)

        texto_score = self.fonte.render(f"Score: {self.score}", True, "white")
        self.screen.blit(texto_score, (10, 10))

        pg.display.flip()  # muda o buffer


if __name__ == "__main__":
    jogo = Jogo()
    jogo.run()
