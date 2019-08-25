from assumptions import *

## Create blank node for the model

def CreateNode():
    return {'CF'     : 0,
            'R'      : 0,
            'C'      : 0,
            'V'      : 0}

## Initialize output variable
Output = {}

## Initialize a blank model to be populated
def BlankModel(T=BondAttrs['T'], Output=Output):
    for x in range(T+1):
        # Key for each node
        Key = x
        # Dict indexed to T in output
        OutputAtT = {}
        # Populate OutputAtT with blank node and key
        while Key >= 0:
            OutputAtT[Key] = CreateNode()
            Key -=1
        # Populate Output with Nodes indexed by T
        Output[x] = OutputAtT

# Populate discount rates for each node
def PopulateRates(T=BondAttrs['T'], Rf=Rf, V=V, Output=Output):
    # Loop thrugh years
    for x in range(T+1):
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
                    Output[x][CurrentNodeI]['C'] = Coupon(NodeRate)
                else:
                    Output[x][CurrentNodeI]['R'] = HighestRate
                    Output[x][CurrentNodeI]['C'] = Coupon(HighestRate)
                # Move to next node in loop
                CurrentNodeI -= 1
                DownMultiplier += 1
        # Set current risk free rate for T = 0
        else:
            Output[0][0]['R'] = Rf
            Output[0][0]['C'] = Coupon(Rf)

"""
################################################
## Explanation of variables in above function ##
################################################

CurrNodeI (Current Node Index): Key for node that is being updated
HighestRate: Highest rate calculated in this period
DownFactor: Used to calculate rate one node lower
DownMultiplier: How many nodes below the highest node in the year
"""

def UpdateNodes(StartYear,
                Output=Output,
                T=BondAttrs['T']):
    # Placeholder variable for loop through years
    while StartYear >= 0:
        # Set indexes for loop through years
        SourceI = StartYear + 1
        OutputI = StartYear + 0
        CurrNodeI = StartYear
        while CurrNodeI >= 0:
            # Set indexes for loop through nodes
            UpperNodeI = CurrNodeI + 1
            LowerNodeI = CurrNodeI
            # Read values from output variable
            UpperNodeV = Output[SourceI][UpperNodeI]['V']
            LowerNodeV = Output[SourceI][LowerNodeI]['V']
            # Calculate risk neutral Cash Flows
            CurrNodeCF = ((UpperNodeV+LowerNodeV)/2)+Output[OutputI][CurrNodeI]['C']
            # Discount risk neutral Cash Flows & Add Coupon
            CurrNodeV = CurrNodeCF/(1+Output[OutputI][CurrNodeI]['R'])
            # Write Cash Flow and Value to Node
            Output[OutputI][CurrNodeI]['CF'] = CurrNodeCF
            Output[OutputI][CurrNodeI]['V']  = CurrNodeV
            # Move to next node in loop
            CurrNodeI -= 1
        # Move to next year in loop
        StartYear -=1

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

def PopulateVandCF(Output=Output,
                   T=BondAttrs['T'],
                   K=BondAttrs['K']):
    # Set parameters for final year of the bond
    for x in range(T+1):
        Output[T][x]['V']  = K
        Output[T][x]['R']  = 'N/A'
        Output[T][x]['CF'] = K
        Output[T][x]['C']  = 'N/A'
    UpdateNodes(T-1)

# Function to update a node if the bond is to be put
def PutNode(Year, Key, Output=Output, PutTerms=PutTerms):
    if PutTerms['Price'] > Output[Year][Key]['V']:
        Output[Year][Key]['V']   = PutTerms['Price']
        Output[Year][Key]['CF']  = PutTerms['Price']
        Output[Year][Key]['Put'] = True

# Function to update a node if the bond is to be called
def CallNode(Year, Key, Output=Output, CallTerms=CallTerms):
    if CallTerms['Price'] < Output[Year][Key]['V']:
        Output[Year][Key]['V']      = CallTerms['Price']
        Output[Year][Key]['CF']     = CallTerms['Price']
        Output[Year][Key]['Called'] = True

def AdjustForOptions(T=BondAttrs['T'], CallTerms=CallTerms, PutTerms=PutTerms):
    PutYears  = []
    CallYears = []
    if PutTerms['Exists'] == True:
        if PutTerms['Type'] == 'A':
            PutYears = list(range(PutTerms['T'], (T)))
        elif PutTerms['Type'] == 'E':
            PutYears.append(PutTerms['T'])
        else:
            print("Option Type (Put) is invalid, update in assumptions.py")
    if CallTerms['Exists'] == True:
        if CallTerms['Type'] == 'A':
            CallYears = list(range(CallTerms['T'], (T)))
        elif CallTerms['Type'] == 'E':
            CallYears.append(CallTerms['T'])
        else:
            print("Option Type (Call) is invalid, update in assumptions.py")
    for x in range(T, 0, -1):
        if x in PutYears:
            for y in range(x+1):
                PutNode(x, y)
        if x in CallYears:
            for y in range(x+1):
                CallNode(x, y)
        UpdateNodes(x-1)

