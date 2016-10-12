from pygame.locals import *
import pygame, sys, eztext
import gtk.gdk

width = gtk.gdk.screen_width()
height = gtk.gdk.screen_height()

def passChk(password):
    # initialize pygame
    pygame.init()

    # create the screen
    screen = pygame.display.set_mode((width,height))
    # screen = pygame.display.set_mode((1280,1024))
    
    # fill the screen black
    screen.fill((255,255,255))

    txtbx = eztext.Input(maxlength=40, color=(255,255,255), prompt='PASSWORD:')
    # create the pygame clock
    
    clock = pygame.time.Clock()
    # main loop!

    while 1:
        # make sure the program is running at 30 fps
        clock.tick(15)
        txtbx.set_pos(width/2.0,height/2.0)

        # events for txtbx
        events = pygame.event.get()

        # process other events
        for event in events:
            # close it x button si pressed
            if event.type == QUIT: return

        # clear the screen
        screen.fill((0,0,0))
        
        # update txtbx
        txtbx.update(events)

        # check password input
        if txtbx.chk_value(password):
            print "correct"
            return True
        else:
            print "something wrong"

        # blit txtbx on the sceen
        txtbx.draw(screen)
        
        # refresh the display
        pygame.display.flip()
