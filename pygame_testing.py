import pygame


WIDTH = 1200
HEIGHT = 800

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_w,
    K_a,
    K_s,
    K_d,
)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        
        self.image = pygame.image.load("pac_right.png").convert()
        self.image.set_colorkey((255,255,255))
        # return a width and height of an image
        self.size = self.image.get_size()
        self.smaller_img = pygame.transform.scale(self.image, (int(self.size[0]/3), int(self.size[1]/3)))
        self.surf = self.smaller_img
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        
        self.rect = self.surf.get_rect()
        
          
    def update1(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1)
            self.image = pygame.image.load("pac_up.png").convert()
            self.size = self.image.get_size()
            self.smaller_img = pygame.transform.scale(self.image, (int(self.size[0]/3), int(self.size[1]/3)))
            self.surf = self.smaller_img
            self.surf.set_colorkey((255,255,255), RLEACCEL)
        elif pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1)
            self.image = pygame.image.load("pac_down.png").convert()
            self.size = self.image.get_size()
            self.smaller_img = pygame.transform.scale(self.image, (int(self.size[0]/3), int(self.size[1]/3)))
            self.surf = self.smaller_img
            self.surf.set_colorkey((255,255,255), RLEACCEL)
        elif pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
            self.image = pygame.image.load("pac_left.png").convert()
            self.size = self.image.get_size()
            self.smaller_img = pygame.transform.scale(self.image, (int(self.size[0]/3), int(self.size[1]/3)))
            self.surf = self.smaller_img
            self.surf.set_colorkey((255,255,255), RLEACCEL)
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(1, 0)
            self.image = pygame.image.load("pac_right.png").convert()
            self.size = self.image.get_size()
            self.smaller_img = pygame.transform.scale(self.image, (int(self.size[0]/3), int(self.size[1]/3)))
            self.surf = self.smaller_img
            self.surf.set_colorkey((255,255,255), RLEACCEL)
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
    
    def update2(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -1)
        elif pressed_keys[K_s]:
            self.rect.move_ip(0, 1)
        elif pressed_keys[K_a]:
            self.rect.move_ip(-1, 0)
        elif pressed_keys[K_d]:
            self.rect.move_ip(1, 0)
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            
    

            
        

def main():
    pygame.init()

    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    player1 = Player()
    player2 = Player()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        
        pressed_keys = pygame.key.get_pressed()
        player1.update1(pressed_keys)
        player2.update2(pressed_keys)
        screen.fill((0, 0, 0))
        screen.blit(player1.surf, player1.rect)
        screen.blit(player2.surf, player2.rect)
        pygame.display.flip()
    pygame.quit()








if __name__ == "__main__":
    main()