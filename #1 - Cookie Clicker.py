"""
Cookie Clicker Simulator
"""

import simpleplot
import math


# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

#########

BUILD_GROWTH = 1.15

class Myinfo:
    """
    Class to track build information.
    """
    
    def __init__(self, build_info = None, growth_factor = BUILD_GROWTH):
        self._build_growth = growth_factor
        if build_info == None:
            self._info = {'Cursor': [15.0, 0.10000000000000001], 'Grandma': [100.0, 0.5]}
        
        else:
            self._info = {}
            for key, value in build_info.items():
                self._info[key] = list(value)
            
    def build_items(self):
        """
        Get a list of buildable items
        """
        return self._info.keys()
            
    def get_cost(self, item):
        """
        Get the current cost of an item
        Will throw a KeyError exception if item is not in the build info.
        """
        return self._info[item][0]
    
    def get_cps(self, item):
        """
        Get the current CPS of an item
        Will throw a KeyError exception if item is not in the build info.
        """
        return self._info[item][1]
    
    def update_item(self, item):
        """
        Update the cost of an item by the growth factor
        Will throw a KeyError exception if item is not in the build info.
        """
        cost, cps = self._info[item]
        self._info[item] = [cost * self._build_growth, cps]
        
    def clone(self):
        """
        Return a clone of this BuildInfo
        """
        return Myinfo(self._info, self._build_growth)
########



# Constants
SIM_TIME = 10000000000.0
#SIM_TIME = 10000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._cookies = 0.0
        self._time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
        
        
    def __str__(self):
        """
        Return human readable state
        """
        result = ""
        result += "total cookies:" + str(self._total_cookies) + "; "
        result += "current cookies:" + str(self._cookies) + "; "
        result += "current time:" + str(self._time) + "; "
        result += "current cps:" + str(self._cps)
        
        return result
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history
    
    def get_total_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._total_cookies

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """

        time = 0.0
        if self._cookies >= cookies:
            return 0.0
        else: 
            time = math.ceil((cookies - self._cookies) / self._cps)
        
        #print "type", type(time)
        return time
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """

        time = float(time)
        if time <= 0.0:
            pass
        else:
            self._time += time
            self._cookies += self._cps * time 
            self._total_cookies += self._cps * time 
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
 
        if self._cookies >= cost:
            self._cookies -= cost  
            self._cps += additional_cps 
            purchase = ()
            purchase = (self._time, item_name, cost, self._total_cookies)
            self._history.append(purchase)
        elif self._cookies < cost:
            pass
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    clicker_state = ClickerState()
    build_info = build_info.clone()

    while clicker_state.get_time() <= duration:

        time_left = duration - clicker_state.get_time()
        item_name = strategy(clicker_state.get_cookies(), clicker_state.get_cps(), time_left, build_info)

        if item_name == None: 
            #print "yuck"
            #print "current time", clicker_state.get_time()
            #print "time left", time_left
            clicker_state.wait(time_left)
            return clicker_state
        #elif item_name == 'Cursor':
        else:
            item_cost = build_info.get_cost(item_name)
            wait_time = clicker_state.time_until(item_cost)

            if time_left >= wait_time:
                clicker_state.wait(wait_time)	
                clicker_state.buy_item(item_name, build_info.get_cost(item_name), build_info.get_cps(item_name))
                build_info.update_item(item_name)

            elif time_left < wait_time:
                break
               
    # Replace with your code
    clicker_state.wait(time_left)
    return clicker_state


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    #print "strat_c"
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Always return 

    This strategy should always select the cheapest item.
    """
    #build_info = build_info.clone()
    #print "in cheap"
    
    items = build_info.build_items()
    cheapest_item = items[0]
    cheapest_price = build_info.get_cost(items[0])
                                              
    for item in items:
        if build_info.get_cost(item) < cheapest_price:  
            cheapest_item = item
            cheapest_price = build_info.get_cost(item)
            
        
    
    #print "price of cursor", build_info.get_cost(items[0])
    #print cheapest_item
    #return "Cursor"
    if (cookies + time_left * cps ) < cheapest_price:
        #print "cheap returning none"
        return None
    else:   
        return cheapest_item

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Always return

    This strategy should always select the most expensive item you can afford in the time left.
    """
    
    items = build_info.build_items()
    expensive_item = items[0]
    expensive_price = build_info.get_cost(items[0])
    
    for item in items:
        if build_info.get_cost(item) >= expensive_price and (cookies + time_left * cps) > build_info.get_cost(item):  
            expensive_item = item
            expensive_price = build_info.get_cost(item)
    
    if (cookies + time_left * cps ) < expensive_price:
        return None
    else:   
        return expensive_item
    
def strategy_best(cookies, cps, time_left, build_info):
    """
    Always return 

    This is the best strategy that you can come up with.
    """
    
    items = build_info.build_items()
    
    best_item = items[0]
    best_price = build_info.get_cost(items[0])
    best_ratio = build_info.get_cps(items[0])/ build_info.get_cost(items[0]) 
    #print "best_ratio", best_ratio
    
    for item in items:
        if build_info.get_cps(item)/ build_info.get_cost(item) >= best_ratio and (cookies + time_left * cps) > build_info.get_cost(item):  
            best_item = item
            best_price = build_info.get_cost(item)
    
    if (cookies + time_left * cps ) < best_price:
        return None
    else:   
        return best_item
 
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    #state = simulate_clicker(my_info, time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor)
    #run_strategy("None", 15000, strategy_none)
    #run_strategy("Cheap", 5000, strategy_cheap)
    #run_strategy("Expensive", 5000, strategy_expensive)
    #binfo = provided.BuildInfo().clone()
    
    #run_strategy("Cheap", 300, strategy_cheap)
    #exp = strategy_expensive(1.0, 3.0, 17.0, my_info)
    #exp = strategy_expensive(500000.0, 1.0, 5.0, my_info)
    
    #exp = strategy_best(1.0, 3.0, 17.0, my_info)
    #exp = strategy_best(500000.0, 1.0, 5.0, my_info)
    #print (exp)
    
    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    #obj = ClickerState()
    #obj.wait(78)
    #obj.buy_item('item', 1.0, 1.0)
    #time = obj.time_until(22)
    #print time
    #print type(time)
    
#my_info = Myinfo()

run()
    
#import user34_gXVabJ5HBR_9 as test_suite
#test_suite.run_simulate_clicker_tests(simulate_clicker,strategy_none,strategy_cursor)
#test_suite.run_clicker_state_tests(ClickerState)