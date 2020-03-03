import sys, pygame
from time import sleep
from math import floor

class Device():
    """For tracking relevant visualization data."""
    def __init__(self, name: str, manager = False):
        self.name = name
        self.manager = manager
        self.border = 2
        if self.manager:
            self.radius = 30
        else:
            self.radius = 15



def create_visual(device_list: list):
    """Return screen."""
    pygame.init()

    size  = 600, 400 # width, height
    screen = pygame.display.set_mode(size)

    return update_visual(screen, device_list)


def update_visual(screen: pygame.Surface, device_list: list):
    """Update based on device list."""

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            sys.exit()
            return None

    white = (255, 255, 255)
    black = (0, 0, 0)
    blue = (0, 0, 128)

    screen.fill(white)

    dev_num = 1
    num_devs = len(device_list)
    manager_center = floor(screen.get_size()[0]/2), floor(screen.get_size()[1]/6)


    for dev in device_list:
        if dev.manager:
            pygame.draw.circle(screen, blue, manager_center, dev.radius, dev.border)
        else:
            center = floor(screen.get_size()[0]*dev_num/num_devs), floor(5*screen.get_size()[1]/6)
            pygame.draw.aaline(screen, black, center, manager_center)
            pygame.draw.circle(screen, blue, center, dev.radius, dev.border)
            dev_num += 1

    pygame.display.flip()



def main():
    devices = [
        Device('pi1', False),
        Device('manager', True),
        Device('pi6', False),
        Device('pi2', False),
        Device('pi2', False),
        Device('pi2', False),
        Device('pi2', False)
        ]
    screen = create_visual(devices)

    # Main loop
    while 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                sys.exit()

    sleep(3)


if __name__ == '__main__':
    main()
