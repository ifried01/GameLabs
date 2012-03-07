import pygame, sys

# Pong
# Thanks Ming
 
def load_sound(sound_name):
    try:
        sound = pygame.mixer.Sound(sound_name)
    except pygame.error, message:
        print "Cannot load sound: " + sound_name
        raise SystemExit, message
    return sound

def load_image(image_name):
    ''' The proper way to load an image '''
    try:
        image = pygame.image.load(image_name)
    except pygame.error, message:
        print "Cannot load image: " + image_name
        raise SystemExit, message
    return image.convert_alpha()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_START_X = 10
PADDLE_START_Y = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 10
BALL_WIDTH_HEIGHT = 16

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# This is a rect that contains the ball at the beginning it is set in the center of the screen
# The array is used to add and remove a new ball everyime a point is scored
# There is only one ball in the array at any given time
ball_list = []
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
ball_list.append(ball_rect)

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Your paddle vertically centered on the left side
paddle_rect1 = pygame.Rect((PADDLE_START_X, 250), (PADDLE_WIDTH, PADDLE_HEIGHT))
paddle_rect2 = pygame.Rect((780, 250), (PADDLE_WIDTH, PADDLE_HEIGHT))


# Dashed line in the middle
dotted_line = []
i = 12.5

while i <= 800: 
    paddle_line = pygame.Rect((400, i), (5, 25))
    dotted_line.append(paddle_line)
    i += 50

# Scoring: 1 point if you hit the ball, -5 point if you miss the ball
score = 0
op_score = 0

# Gets incremented every game lopp
counter = 0

# Gets set to (counter + constant) when a point is scored and makes a little wait before game continues
start_wait = 0

# gets subtracted from the location of the ball to throw off the computer
ball_pos_delay = 0

# Load the font for displaying the score
font = pygame.font.Font(None, 39)

# Determines the different screens
screen_id = 0

# gets set to true when someone gets to 11
win = False

# Load ball hit sound
ball_hit = load_sound("laser.wav")

# Game loop
while True:

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
            pygame.quit()
        # Control the paddle with the mouse
        elif event.type == pygame.MOUSEMOTION:
            paddle_rect1.centery = event.pos[1]
            # correct paddle position if it's going out of window
            if paddle_rect1.top < 0:
                paddle_rect1.top = 0
            elif paddle_rect1.bottom >= SCREEN_HEIGHT:
                paddle_rect1.bottom = SCREEN_HEIGHT

    # This test if up or down keys are pressed; if yes, move the paddle number 1
    if pygame.key.get_pressed()[pygame.K_w] and paddle_rect1.top > 0:
        paddle_rect1.top -= BALL_SPEED
    elif pygame.key.get_pressed()[pygame.K_s] and paddle_rect1.bottom < SCREEN_HEIGHT:
        paddle_rect1.top += BALL_SPEED
    elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
        sys.exit(0)
        pygame.quit()
    elif pygame.key.get_pressed()[pygame.K_1] and screen_id == 0:
        screen_id = 1 # Begin game from intro screen, computer player
    elif pygame.key.get_pressed()[pygame.K_2] and screen_id == 0:
        screen_id = 2 # Begin game from intro screen, multiplayer
    elif pygame.key.get_pressed()[pygame.K_RETURN] and screen_id == 3:
        # Restart screen after game ends
        screen_id = 0
        score = 0
        op_score = 0
        win = False
       
    # Computer player
    #for the_ball in ball_list:
        #give the computer a little delay
    #    paddle_rect2.top = the_ball.top - ball_pos_delay

    if screen_id == 0:
        intro = load_image("background.png")
        screen.blit(intro, (0,0))
        instructions = font.render("Welcome to Pong!", 1, (255, 255, 255))
        instructions1 = font.render("Press 1 for One Player Mode", 1, (255, 255, 255))
        instructions2 = font.render("Press 2 for Two Player Mode", 1, (255, 255, 255))
        screen.blit(instructions, (100, 200))
        screen.blit(instructions1, (100, 250))
        screen.blit(instructions2, (100, 300))
        pygame.display.flip()


    # Single Player Mode 
    elif screen_id == 1: 
    
        # Computer player
        for the_ball in ball_list:
            #give the computer a little delay
            paddle_rect2.top = the_ball.top - ball_pos_delay
    
        # Update ball position
        for ball in ball_list:
            if start_wait < counter:
                ball.left += ball_speed[0]
                ball.top += ball_speed[1]

            ball_scored = False

            # Ball collision with rails
            # Top and bottom of screen
            if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
                ball_speed[1] = -ball_speed[1]
  
            # Left side of screen 
            if ball.left <= 0 and ball_scored == False:
                ball_scored = True 
            
                # Remove the old ball from the list 
                ball_list.remove(ball)
                
                # Make a new ball that will start at the middle of the playing field
                new_ball = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
                ball_list.append(new_ball)

                # Makes the new ball wait for a little before restarting the next ball
                start_wait = counter + 100      
 
                op_score += 1

                # reset the delay for the computer paddle
                ball_pos_delay = 0

            # Right side of screen
            if ball.right >= SCREEN_WIDTH and ball_scored == False:
                ball_scored = True 
            
                # Remove the old ball from the list 
                ball_list.remove(ball)
            
                # Make a new ball that will start at the middle of the playing field
                new_ball = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
                ball_list.append(new_ball)
                
                # Makes the new ball wait for a little before restarting the next ball
                start_wait = counter + 100        
                
                score += 1

                # reset the delay for the computer paddle
                ball_pos_delay = 0
    
            # Test if the ball is hit by the paddle1; if yes reverse speed
            if paddle_rect1.colliderect(ball) and ball_scored == False:
                ball_speed[0] = -ball_speed[0]

                # delay the computer player a little
                ball_pos_delay += 10
 
                ball_hit.play()
    
            # Test if the ball is hit by the paddle2; if yes reverse speed
            if paddle_rect2.colliderect(ball) and ball_scored == False:
                ball_speed[0] = -ball_speed[0]
                
                ball_hit.play()
    
            # Clear screen
            screen.fill((255, 255, 255))

            # Render the paddle and the score
            pygame.draw.rect(screen, (0, 0, 0), paddle_rect1) # Your paddle
            pygame.draw.rect(screen, (0, 0, 0), paddle_rect2) # Enemy paddle
   
            # Render the ball 
            for ball in ball_list:
                pygame.draw.circle(screen, (0, 0, 0), ball.center, ball.width / 2) # The ball
   
            # Render the red line
            for lines in dotted_line:
                pygame.draw.rect(screen, (255, 0, 0), lines) # Dotted line
    
            # My score
            score_text1 = font.render(str(score), True, (0, 0, 0))
            screen.blit(score_text1, ((SCREEN_WIDTH / 4) - font.size(str(score))[0] / 2, 5)) # The score
    
            # Opponent score
            score_text2 = font.render(str(op_score), True, (0, 0, 0))
            screen.blit(score_text2, ((SCREEN_WIDTH - (SCREEN_WIDTH / 4)) - font.size(str(op_score))[0] / 2, 5)) # The op_score

    # Two Player Mode
    elif screen_id == 2: 

        # This test if up or down keys are pressed; if yes, move the paddle number 2
        if pygame.key.get_pressed()[pygame.K_UP] and paddle_rect2.top > 0:
            paddle_rect2.top -= BALL_SPEED
        elif pygame.key.get_pressed()[pygame.K_DOWN] and paddle_rect2.bottom < SCREEN_HEIGHT:
            paddle_rect2.top += BALL_SPEED

        # Update ball position
        for ball in ball_list:
            if start_wait < counter:
                ball.left += ball_speed[0]
                ball.top += ball_speed[1]

            ball_scored = False

            # Ball collision with rails
            # Top and bottom of screen
            if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
                ball_speed[1] = -ball_speed[1]
  
            # Left side of screen 
            if ball.left <= 0 and ball_scored == False:
                ball_scored = True 
            
                # Remove the old ball from the list 
                ball_list.remove(ball)
                
                # Make a new ball that will start at the middle of the playing field
                new_ball = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
                ball_list.append(new_ball)

                # Makes the new ball wait for a little before restarting the next ball
                start_wait = counter + 100      
 
                op_score += 1

            # Right side of screen
            if ball.right >= SCREEN_WIDTH and ball_scored == False:
                ball_scored = True 
            
                # Remove the old ball from the list 
                ball_list.remove(ball)
            
                # Make a new ball that will start at the middle of the playing field
                new_ball = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
                ball_list.append(new_ball)
                
                # Makes the new ball wait for a little before restarting the next ball
                start_wait = counter + 100        
                
                score += 1
    
            # Test if the ball is hit by the paddle1; if yes reverse speed
            if paddle_rect1.colliderect(ball) and ball_scored == False:
                ball_speed[0] = -ball_speed[0]
                
                ball_hit.play()
    
            # Test if the ball is hit by the paddle2; if yes reverse speed
            if paddle_rect2.colliderect(ball) and ball_scored == False:
                ball_speed[0] = -ball_speed[0]
                
                ball_hit.play()
    
            # Clear screen
            screen.fill((255, 255, 255))

            # Render the paddle and the score
            pygame.draw.rect(screen, (0, 0, 0), paddle_rect1) # Your paddle
            pygame.draw.rect(screen, (0, 0, 0), paddle_rect2) # Enemy paddle
   
            # Render the ball 
            for ball in ball_list:
                pygame.draw.circle(screen, (0, 0, 0), ball.center, ball.width / 2) # The ball
   
            # Render the red line
            for lines in dotted_line:
                pygame.draw.rect(screen, (255, 0, 0), lines) # Dotted line
    
            # My score
            score_text1 = font.render(str(score), True, (0, 0, 0))
            screen.blit(score_text1, ((SCREEN_WIDTH / 4) - font.size(str(score))[0] / 2, 5)) # The score
    
            # Opponent score
            score_text2 = font.render(str(op_score), True, (0, 0, 0))
            screen.blit(score_text2, ((SCREEN_WIDTH - (SCREEN_WIDTH / 4)) - font.size(str(op_score))[0] / 2, 5)) # The op_score


    # Screen for end of game, winner at 11 points
    elif screen_id == 3 and win == True:
        intro = load_image("background.png")
        screen.blit(intro, (0,0))
        
        winner = font.render(str(winner) + " is the winner!!!", 1, (255, 255, 255))
        screen.blit(winner, (100, 100))
        
        instructions = font.render("To Play Again ENTER/RETURN", 1, (255, 255, 255))
        screen.blit(instructions, (100, 150))
        
        instructions = font.render("To Exit ESCAPE", 1, (255, 255, 255))
        screen.blit(instructions, (100, 185))
        
        pygame.display.flip()
    
    # Checks for winner 
    if score == 11:
        winner = "Player 1"
        win = True
        screen_id = 3
    elif op_score == 11:
        winner = "Player 2"
        win = True
        screen_id = 3


       
    # Update screen and wait 20 milliseconds
    pygame.display.flip()
    pygame.time.delay(20)

    # Increment counter
    counter += 1

