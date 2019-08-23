from assumptions import *

## Create blank node for the model

def CreateNode():
    Node = {'R'     : 0,
            'CF'    : 0,
            'V'     : 0}
    return Node

## Initialize output variable
Output = {}


## Initialize a blank model to be populated
def BlankModel(T=T, Output=Output):
    for x in range(T+1):
        # H & L Variables for name of each node
        Key = x
        # List object indexed to T in output
        OutputAtT = {}
        # Populate OutputAtT with blank nodes and 
        # Names for each node
        while Key >= (0):
            OutputAtT[Key] = CreateNode()
            Key -=1
        # Populate Output with Nodes indexed by T
        Output[x] = OutputAtT

# Populate discount rates for each node
def PopulateRates(T=T, Rf=Rf, V=V, Output=Output):
    # Loop thrugh years
    for x in range(T):
        # Disregard years that are not calculated
        if (x != T) and (x > 0):
            CurrentNodeI = x + 0
            # Calculate highest rate for year
            HighestRate = ((1+V)**x) * Rf
            # Multiplier & factor for each node below highest
            DownFactor = 1 / ((1+V)**2)
            DownMultiplier = 0
            # Populate rates in each node
            while CurrentNodeI >= 0:
                if DownMultiplier != 0:
                    NodeRate = HighestRate * (DownFactor**DownMultiplier)
                    Output[x][CurrentNodeI]['R'] = NodeRate
                else:
                    Output[x][CurrentNodeI]['R'] = HighestRate
                # Move to next node in loop
                CurrentNodeI -= 1
                DownMultiplier += 1
        # Set current risk free rate for T = 0
        else:
            Output[0][0]['R'] = Rf

"""
################################################
## Explanation of variables in above function ##
################################################

CurrNodeI (Current Node Index): Key for node that is being updated
HighestRate: Highest rate calculated in this period
DownFactor: Used to calculate rate one node lower
DownMultiplier: How many nodes below the highest node in the year
"""

def PopulateVandCF(Output=Output, Coupon=Coupon):
    # Set parameters for final year of the bond
    for x in range(T+1):
        Output[T][x]['V'] = K + Coupon
        Output[T][x]['R'] = 'N/A'
        Output[T][x]['CF'] = K + Coupon
    # Placeholder variable for loop through years
    X = T-1
    while X >= 0:
        # Set indexes for loop through years
        SourceI = X + 1
        OutputI = X + 0
        CurrNodeI = X
        while CurrNodeI >= 0:
            # Set indexes for loop through nodes
            UpperNodeI = CurrNodeI + 1
            LowerNodeI = CurrNodeI
            # Read values from output variable
            UpperNodeV = Output[SourceI][UpperNodeI]['V']
            LowerNodeV = Output[SourceI][LowerNodeI]['V']
            # Calculate risk neutral Cash Flows
            CurrNodeCF = (UpperNodeV+LowerNodeV+Coupon)/2
            # Discount risk neutral Cash Flows
            CurrNodeV = CurrNodeCF / (1+Output[OutputI][CurrNodeI]['R'])
            # Write Cash Flow and Value to Node
            Output[OutputI][CurrNodeI]['CF'] = CurrNodeCF
            Output[OutputI][CurrNodeI]['V'] = CurrNodeV
            # Move to next node in loop
            CurrNodeI -= 1
        # Move to next year in loop
        X -=1

"""
################################################
## Explanation of variables in above function ##
################################################

SourceI (Source Index): Year that Source factors come from
OutputI (Output Index): Year of nodes that are being updated
UpperNodeI (UpperNode Index): Key for upper source node (source year, rates increase)
LowerNodeI (LowerNode Index): Key for upper source node (source year, rates decrease)
UpperNodeV (UpperNode Value): Value for upper source node
LowerNodeV (LowerNode Value): Value for lower source node
CurrNodeI (Current Node Index): Key for node that is being updated
CurrNodeCF (Current Node Cash Flow): Risk neutral cash flow at node being written to
CurrNodeV (Current Node Value): Discounted cash flow at current node
"""
