## C: Coupon (or premium over Rf) in bps
## K: Price at Par
## T: Years until Maturity
## F: Is bond Floating Rate
BondAttrs = {'C'      : 200,
             'K'      : 100,
             'T'      : 9,
             'F'      : True}

## Interest Rate Volatility
V = .15

## Current Risk Free Rate
Rf = .05

#################
## Optionality ##
#################

## Terms of options
## Exists: Does option exist
## Price: Price at which option is executed
## T: Time at end of holdout period
## Type: 'A'(American) or 'E' (European)
CallTerms = {'Exists':    False,
             'Price' :    101,
             'T'     :    3,
             'Type'  :    'A'}

PutTerms = {'Exists' :    False,
            'Price'  :    100,
            'T'      :    3,
            'Type'   :    'A'}

## Calculate Coupon
def Coupon(R,
           C=BondAttrs['C'],
           K=BondAttrs['K'],
           F=BondAttrs['F']):
    if F == True:
        return ((C*.0001)+R)*K
    else:
        return(C*.0001)*K
