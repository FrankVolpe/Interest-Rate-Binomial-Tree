# Binomial Interest Rate Tree Valuation Model

## Summary

This program is designed for the valuation of a bond using a binomial interest rate tree. This program does not yet support continuous compounding for interest rate projections. To accomodate beginners, I "over-documented" (if thats even possible) this program. It should be extremely straightforward to understand how everything works. Should you need any clarification, or to report any issues/improvements, do not hesitate to reach out. 

One clear constraint I am choosing to undertake in building this program is avoiding the use of object oriented programming (OOP) in the back end calculations. The purpose of this is to minimize computational burden.

## Current Functionality

Construction of a binomial interest rate tree for a risk-free, bond. Also supports Options and Floating rate bonds.

## Updates To Be Added

* Stronger command line functionality 
  * Updating assumptions & running program in the command line
* Support of caps and floors on floating rate bonds
* Non risk-neutral probabilities between nodes
* Continuously compounded volatility assumptions

## How to use:

### Set Bond Attributes

Assumptions are set via the *BondAttrs* variable in the *assumptions.py* file. Assumptions are all labeled in the file. The excerpt below shows the *BondAttrs* variable:

```python
## C: Coupon (or premium over Rf) in bps
## K: Price at Par
## T: Years until Maturity
## F: Is bond Floating Rate
BondAttrs = {'C'      : 200,
             'K'      : 100,
             'T'      : 9,
             'F'      : True}
```

The above shows a bond with a Par value of 100, 9 years until maturity, and a floating rate coupon (*'BondAttrs['F'] == True*) that pays the risk free rate +200bps

For a bond that pays a fixed coupon of 5% and a par value of 1000 that matures in 3 years, you would change the above variables to the following:

```python
## C: Coupon (or premium over Rf) in bps
## K: Price at Par
## T: Years until Maturity
## F: Is bond Floating Rate
BondAttrs = {'C'      : 500,
             'K'      : 1000,
             'T'      : 3,
             'F'      : False}
```

### Pricing Bonds With Options

Relevant data surrounding embedded options on the bonds are also set in the *assumptions.py* file and are as follows:

```python
## Terms of options
## Exists: Does option exist
## Price: Price at which option is executed
## T: Time at end of holdout period
## Type: 'A'(American) or 'E' (European)

CallTerms = {'Exists':    True,
             'Price' :    101,
             'T'     :    5,
             'Type'  :    'A'}

PutTerms = {'Exists' :    False,
            'Price'  :    100,
            'T'      :    3,
            'Type'   :    'A'}
```

The above shows a bond that has an embedded call option (*CallTerms['Exists'] == True*), it is callable at T=5 for 101. The Option is American (For a European Option, set *CallTerms['Type'] to 'E'*) The bond does not have an embedded put option (*PutTerms['Exists'] == False*)

### Import Global Variables & Functions

```python
from calculations import *
```

Importing *calculations.py* will also import *assumptions.py*

### Create A Blank Binomial Tree

```python
BlankModel()
```

This function takes the years until maturity from the *assumptions.py* file and saves a blank binomial tree to the *Output* variable

### Populate The Binomial Tree With Interest Rates

```python
PopulateRates()
```

This function uses the volatility assumption and current risk free rate to populate the binomial tree with relevant interest rate projections

### Populate The Remainder Of The Model

```python
PopulateVandCF()
```

Populates the remainder of the model (Values and Cash Flows)

### Reflect The Exercise of Options

```python
AdjustForOptions()
```

Uses *PutTerms* and *CallTerms* from *assumptions.py* to to change the value of a called or put bond at their respective nodes, it also readjusts nodes to reflect changes in value

### Understanding The Output

The *Output* variable is used to store all of the nodes and their respective parameters. It is a dictionary, structured as follows:

```python
{ Time : { Node Key : { 'CF'     : Cash Flow at Node,
                        'R'      : Rate at Node,
                        'C'      : Coupon at Node,
                        'V'      : Value at Node,
                        'Called' : Call Option Exercised,
                        'Put'    : Put Option Exercised }}}
```

* Time, *int* 
  * Starts at **T = 0** and increases to the year in which the bond matures

* NodeKey, *int*
  * The higher the number, the higher the node
  * 0 is always the lowest node in the tree during the period

* Rate at Node, *float*
  * Effective interest rate at node

* Coupon at Node, *usually float*
  * Coupon to be discounted at node

* Cash Flow at Node, *usually float*
  * Expected cash flow at node (risk-neutral probability)

* Value at Node, *float*
  * Discounted Cash Flow at node

* Call Option Executed, *bool*
  * Only added at Nodes where bond is called

* Put Option Executed, *bool*
  * Only added at Nodes where bond is put
