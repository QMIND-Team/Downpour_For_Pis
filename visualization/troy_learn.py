"""Learning Pygame"""
import sys

import pygame
import pygame.freetype

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class Device(pygame.sprite.Sprite):
    """Device Object, extends """
    def __init__(self, font, name, x, y):
        super(Device, self).__init__()
        self.active = True
        self.name = name
        self.images = []
        base_images = [
            pygame.image.load("resources/computer-clip-art.png").convert_alpha(),
            pygame.image.load("resources/computer-clip-art-black.png").convert_alpha()
        ]
        for temp_image in base_images:
            temp_rect = temp_image.get_rect()
            new_image = pygame.transform.smoothscale(
                temp_image,
                (120, round((temp_rect.height/temp_rect.width)*120))
            )
            self.images.append(new_image)
        self.surf = self.images[0]
        self.rect = self.surf.get_rect()
        self.rect.center = (x, y)
        self.text_surf, self.text_rect = pygame.freetype.Font.render(font, name)
        self.text_rect.center = (self.rect.centerx, self.rect.centery+100)
    
    # def update(self, pressed_keys):
    #     if pressed_keys[pygame.K_UP]:
    #         self.rect.move_ip(0, -5)
    #     if pressed_keys[pygame.K_DOWN]:
    #         self.rect.move_ip(0, 5)
    #     if pressed_keys[pygame.K_LEFT]:
    #         self.rect.move_ip(-5, 0)
    #     if pressed_keys[pygame.K_RIGHT]:
    #         self.rect.move_ip(5, 0)

    def change_pic(self):
        """Toggle the sprite's image.
        We don't need to worry about the rects because the images are the same size.
        """
        if self.active:
            self.active = False
            self.surf = self.images[1]
        else:
            self.active = True
            self.surf = self.images[0]



def init():
    """Initialization stuff"""
    pygame.init()
    myfont = pygame.freetype.SysFont('consolas', 30)
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    pygame.display.toggle_fullscreen()
    pygame.display.set_caption("CUCAI 2020 - Distributed Computing")
    clock = pygame.time.Clock()

    # Create the sprites
    manager = Device(myfont, "Manager", SCREEN_WIDTH//2, SCREEN_HEIGHT //6)

    # Collect the sprites
    sprites = pygame.sprite.Group()
    sprites.add(manager)

    # Create user event
    CHANGE = pygame.USEREVENT+1

    return screen, clock, sprites, CHANGE, myfont



def main():
    """Main"""
    screen, clock, sprites, CHANGE, myfont = init()

    # Main loop
    running = True
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    my_event = pygame.event.Event(CHANGE)
                    pygame.event.post(my_event)
            elif event.type == pygame.QUIT:
                running = False
            elif event.type == CHANGE:
                for sprite in sprites:
                    sprite.change_pic()

        # Respond to keypresses
        pressed_keys = pygame.key.get_pressed()
        for sprite in sprites:
            sprite.update(pressed_keys)

        # Draw
        screen.fill((255, 255, 255))

        for sprite in sprites:
            screen.blit(sprite.surf, sprite.rect)
            screen.blit(sprite.text_surf, sprite.text_rect)

        pygame.display.flip()

        # Run at 60 fps (max)
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
