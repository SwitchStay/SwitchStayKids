import itertools
import random
import numpy as np

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

for block in blockOrder:
    # Placeholder for new block screen
    newBlock = {'type': 'new_block', 'advisor_state': block}
    trialOrder.append(newBlock)
    
    # Shuffle card combinations to generate trial order for this block
    blockTrials = random.sample(cardCombos, nCombos)
    blockAdvice = [advisorFun(block, t) for t in blockTrials] # Advice
    
    for trial, advice in zip(blockTrials, blockAdvice):
        newTrial = {'type': 'card_game',
        'advisor_state': block,
        'advice': advice,
        'visible_card': trial[0],
        'hidden_card': trial[1]}
        
        trialOrder.append(newTrial)
        
print trialOrder