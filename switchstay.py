from psychopy import gui, core, visual, event, data, monitors
from psychopy.visual import ShapeStim
import numpy as np
import random
import os

# Create monitor
exp_monitor = monitors.Monitor('Maya_Laptop')
w=visual.Window(size = exp_monitor.getSizePix())

# Save responses
responses=[]

background = visual.ImageStim(w, image= 'cardbackgroundmain.jpg', size=(2.25,3))

#Draw card
card = visual.Rect(w, width=0.5, height=1.2, fillColor='white', lineColor='black')
name_1 = visual.TextStim(w, text = 'Keep', color='black', height =.2, pos=(-0.5,0.25))
name_2 = visual.TextStim(w, text = 'Switch', color='black', height =.2, pos=(0.5,0.25))

#Draw star
def makeStar(center, scale):
    baseCoords = np.array([(-.45, .1), (-.15, .1), (0, .55), (.15, .1), (.45, .1), (.25, -.3), (.35, -.85), (0, -.5), (-.35, -.85), (-.25, -.3)])
    starCoords = baseCoords * scale + center
    
    return starCoords

#star5Vert1 = makeStar((0, .4), .25)
#star5Vert2 = makeStar((0, 0), .25)
#star5Vert3 = makeStar((0, -.35), .25)
#star51 = ShapeStim(w, vertices = star5Vert1, fillColor='green', lineWidth=2, lineColor='white')
#star52 = ShapeStim(w, vertices = star5Vert2, fillColor='green', lineWidth=2, lineColor='white')
#star53 = ShapeStim(w, vertices = star5Vert3, fillColor='green', lineWidth=2, lineColor='white')

### Create trial order ###
# Helper function: Generates advice
def advisorFun(block, cards):
    if block == 'none':
        coin_flip = np.random.binomial(1, .5) 
        advice = 'switch' if coin_flip else 'keep'
    elif block == 'hidden':
        advice = 'switch' if cards[1] >=3 else 'keep'
    else:
        advice = 'switch' if cards[1] > cards[0] else 'keep'
        
    return advice

# Get all pairings of cards
allCards = range(1,5)
cardCombos = [(x, y) for x in allCards for y in allCards if x != y]
nCombos = len(cardCombos)

# Get block order
blockTypes = ['none', 'hidden', 'both']
nBlocks = len(blockTypes)
blockOrder = random.sample(blockTypes, nBlocks)

# Initialize trial order
trialOrder = []

# Add each block to trial order
for block in blockOrder:
    # Placeholder for new block screen
    newBlock = {'type': 'new_block', 'advisor_state': block}
    trialOrder.append(newBlock)
    
    # Shuffle card combinations to generate trial order for this block
    blockTrials = random.sample(cardCombos, nCombos)
    
    # Generate advice
    blockAdvice = [advisorFun(block, t) for t in blockTrials]
    
    for trial, advice in zip(blockTrials, blockAdvice):
        newTrial = [{'type': 'advice', 'advisor_state': block, 'advice': advice},
        {'type': 'card_game', 'advisor_state': block, 'advice': advice,'visible_card': trial[0], 'hidden_card': trial[1]},
        {'type': 'feedback'}]
 
        trialOrder += newTrial

### Present stimuli ### 
lastReward = 0 # Reward from last trial (used for feedback)
totalScore = 0 # Total score
for trial in trialOrder:
    if trial['type'] == 'card_game':
        # Draw card
        background.draw()
        card.draw()
        name_1.draw()
        name_2.draw()
        
        # Get coordinates for stars! (different depending on value of visible card)
        if trial['visible_card'] == 1:
            starLocations = [(0, 0)]
            
        elif trial['visible_card'] == 2:
            starLocations = [(0, 0.2), (0, -0.2)]
            
        elif trial['visible_card'] == 3:
            starLocations = [(.12, .45), (0, .05), (-.12, -.35)]
            
        else: # visible_card is 4
            starLocations = [(.12, .45), (-.12, .45), (-.12, -.35), (.12, -.35)]
            
        starVertices = [makeStar(coords, .25) for coords in starLocations]
        for star in starVertices:
            starStim = ShapeStim(w, vertices = star, fillColor='green', lineWidth=2, lineColor='white')
            starStim.draw()

        w.flip()
        rt = core.Clock()

        keys=event.waitKeys(keyList=['z', 'm'], timeStamped=rt)
        trialData = trial.copy()
        trialData['key'] = keys[0][0]
        trialData['rt'] = keys[0][1]
        trialData['response'] = 'keep' if trialData['key'] == 'z' else 'switch'
        trialData['reward'] = trialData['hidden_card'] if trialData['response']  == 'switch' else trialData['visible_card']
        lastReward = trialData['reward']
        totalScore += trialData['reward']
        
        responses.append(trialData)
        w.flip()
        
    elif trial['type'] == 'advice':
        videoFile = '%s_%s.mov' % (trial['advisor_state'], trial['advice'])
        #print os.path.isfile(videoFile)
        #adviceStim = visual.MovieStim(w, filename = videoFile)
        adviceStim = visual.TextStim(w, text = videoFile)
        adviceStim.draw()
        
        w.flip()
        core.wait(3)
        
    elif trial['type'] == 'feedback':
#        # Debugging only: Text placeholder version
#        rewardStim = visual.TextStim(w, text = str(lastReward))
#        rewardStim.draw()
        
        if lastReward == 1:
            starLocations = [(0, 0)]
            
        elif lastReward == 2:
            starLocations = [(-0.15, 0), (0.15, 0)]
            
        elif lastReward == 3:
            starLocations = [(-0.3, 0), (0, 0), (0.3, 0)]
            
        else: # visible_card is 4
            starLocations = [(-0.45, 0), (-0.15, 0), (0.15, 0), (0.45, 0)]
        
        starVertices = [makeStar(coords, .25) for coords in starLocations]
        for star in range(len(starVertices)):
            # Draw all stars that have already been presented
            prevStars = []
            for s in range(star):
                prevStar = ShapeStim(w, vertices = starVertices[s], fillColor='green', lineWidth=2, lineColor='white')
                prevStars.append(prevStar)
            
            # Helper function to draw all previous stars quickly
            def drawStars():
                for s in prevStars:
                    s.draw()
                    
            # Draw new star
            newStar = ShapeStim(w, vertices = starVertices[star], fillColor='green', lineWidth=2, lineColor='white')
            
            endSize = np.array(newStar.size)
            animationTimer = core.CountdownTimer(1)
            
            while animationTimer.getTime() > 0:
                newStar.setSize(endSize-animationTimer.getTime())
                drawStars()
                newStar.draw()
                w.flip()
                
            newStar.setSize(endSize)
            drawStars()
            newStar.draw()
            w.flip()
        
        core.wait(1)
                
#            while starStim.size < endSize:
#                starStim.setSize(starStim.size + startSize)
#                starStim.draw()
#                w.flip()
#                
#            starStim.setSize(endSize)
#            starStim.draw()
#            w.flip()
         

#            while animationTimer.getTime() > 0:
#                # First: turn to the left
#                while starStim.ori > -15:
#                    starStim.setOri(1, '-') # rotate
#                    starStim.draw()
#                    w.flip()
#                
#                # Next: Turn all the way to the right
#                while starStim.ori < 15:
#                    starStim.setOri(1, '+') # rotate
#                    starStim.draw()
#                    w.flip()
#                
#                # Finally: Turn all the way to the center
#                while starStim.ori > 0:
#                    starStim.setOri(1, '-') # rotate
#                    starStim.draw()
#                    w.flip()
                
                #print animationTimer.getTime()
                       
        #core.wait(1)
        #w.flip()
        
    else:
        blockType = trial['advisor_state']
        advisorDict = {'none': 'NO cards', 'hidden': 'the HIDDEN card', 'both': 'BOTH cards'}
        announceTxt = 'Get ready! The advisor can now see %s.' % advisorDict[blockType]
        announceStim = visual.TextStim(w, text = announceTxt, color= 'black', alignHoriz= 'center', alignVert='center')
        announcebackground = visual.ImageStim(w, image = 'backgroundkids2.jpg')
        announcebackground.draw()
        announceStim.draw()
        
        w.flip()
        event.waitKeys()

print responses
print 'Congratulations! You earned %i points.' % totalScore