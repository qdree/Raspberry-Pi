from  transitionInit import *

password = "arsenal"

input_name = raw_input("Input name:")

tr_sys = Transition()
path = tr_sys.pathCreation(tr_sys.nameCheck(input_name))
#path = tr_sys.pathCreation("samplevideo")

pygame.init() #initialize pygame
screen = pygame.display.set_mode((tr_sys.width,tr_sys.height), FULLSCREEN) #create the screen
screen.fill((0,0,0)) # fill the screen black
while not tr_sys.kbdIden(): #wait for keyboard
	events = pygame.event.get() 
	# process other events
	for event in events:
        mods = pygame.key.get_mods()
		if event.type == KEYDOWN:
			if event.key == K_F10 and mods & pygame.KMOD_RSHIFT and mods & pygame.KMOD_CTRL:
				quit()
			
print "Keyboard added"

while not tr_sys.passChk(password):
	pass

tr_sys.videoPlayback(path)
print "Door is opened"
tr_sys.fillScreen((0,0,0))
