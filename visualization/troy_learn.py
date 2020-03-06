"""Learning Pygame"""
import sys

import pygame

class Device(pygame.sprite.Sprite):
    """Device Object, extends """
    def __init__(self, name):
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
                (65, round((temp_rect.height/temp_rect.width)*65))
            )
            self.images.append(new_image)
        self.surf = self.images[0]
        self.rect = self.surf.get_rect()
        self.rect.center = (400, 300)
    
    def update(self, pressed_keys):
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

    def change_pic(self):
        if self.active:
            self.active = False
            self.surf = self.images[1]
        else:
            self.active = True
            self.surf = self.images[0]



def init():
    """Initialization stuff"""
    pygame.init()
    size = width, height = (800, 600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("CUCAI 2020 - Distributed Computing")
    clock = pygame.time.Clock()

    # Create the sprites
    manager = Device("Manager")

    # Collect the sprites
    sprites = pygame.sprite.Group()
    sprites.add(manager)

    # Create user event
    CHANGE = pygame.USEREVENT+1

    return screen, clock, sprites, CHANGE



def main():
    """Main"""
    screen, clock, sprites, CHANGE = init()

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

        pygame.display.flip()

        # Run at 60 fps (max)
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
