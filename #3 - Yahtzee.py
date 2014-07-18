"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def gen_all_combinations(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            outcomes_filtered = tuple_diff(outcomes, partial_sequence)
            for item in outcomes_filtered:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                new_sequence = sorted(new_sequence)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def tuple_diff(tup1, tup2):
    """
    Helper function that computes the difference of two tuples
    """
    list1 = list(tup1)
    list2 = list(tup2)
    
    for idx in range(len(list2)):
        list1.remove(list2[idx])
    return list1

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.
    hand: full yahtzee hand
    Returns an integer score 
    """
    max_score = 0
    
    scores = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
    
    for card in hand:
        max_score += card
        scores[card] += card
                
    max_score = max(scores.values())
    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    expected_val = 0.0
    outcomes = []
    for idx in range(1, num_die_sides + 1):
        outcomes.append(idx)
        
    all_rolls = gen_all_sequences(outcomes, num_free_dice)
    scores = [score(held_dice + roll) for roll in all_rolls]
    expected_val = sum(scores) / float(len(scores))
    return expected_val


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.
    hand: full yahtzee hand set.union(other_set)
    Returns a set of tuples, where each tuple is dice to hold
    """
    ans = set([()])   
    for dummy_idx in range(len(hand)+1):
        temp = set()
        temp = gen_all_combinations(hand, dummy_idx)
        ans = ans.union(temp)
    return ans
       
 
def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """

    all_holds = gen_all_holds(hand)
    max_exp_val = 0.0
    max_hold = ()
    
    for hold in all_holds:
        exp_val = expected_value(hold, num_die_sides, len(hand)-len(hold))
        if exp_val > max_exp_val:
            max_exp_val = exp_val
            max_hold = hold
     return (max_exp_val, max_hold)

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    #hand = (1, 1, 1, 5, 1)
    #hand = (1,2,3)
    #hand = (4,4,3)
    #print "length of hand", len(hand)
    #print"all perms: ", gen_all_permutations(hand, 3)
    
    #print "all holds: ", gen_all_holds(hand)
    
    #print "score", score(hand)
    #hand = (2,1)
    hand = (1,)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    #print "expected value", expected_value((2,2),6, 2)
    
run_example()

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)