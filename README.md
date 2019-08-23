# Binomial Interest Rate Tree Valuation Model

## Summary

This program is designed for the valuation of a bond using a binomial interest rate tree. This program does not yet support continuous compounding for interest rate projections. For beginners, I feel that I over-documented this program. It should be extremely straightforward to understand how everything works. Should you need any clarification, or to report any issues/improvements, do not hesitate to reach out. 

One clear constraint I am choosing to undertake in building this program is avoiding the use of object oriented programming (OOP) in the back end calculations. The purpose of this is to minimize computational burden.

## Current Functionality

* Construction of a binomial interest rate model for a risk-free, option-free, fixed-rate, coupon-paying bond. 

## Updates To Be Added

* Display of interest rate nodes and parameters
* Stronger command line functionality 
  * Updating assumptions & running program in the command line
* Valuation of bonds with embedded options
* Valuation of floating rate bonds
  * Including caps and floors on floating rate bonds
* Non risk-neutral valuations
* Continuously compounded volatility assumptions

## How to use:

### Set Assumptions

Assumptions are set via global variables in the *assumptions.py* file. Assumptions are all labeled in the file. The excerpt below shows the variables that the program currently utilizes:

```python
## Coupon Rate of Bond
C = .01

## Strike Price
K = 100

## Years Until Maturity
T = 5

## Interest Rate Volatility
V = .15

## Current Risk Free Rate
Rf = .01
```

### Import global variables and functions

```python
from calculations import *
```

Importing *calculations.py* will also import *assumptions.py*

### Create a blank binomial tree

```python
BlankModel()
```

This function takes the years until maturity from the assumptions.py file and saves a blank binomial tree to the *Output* variable

### Populate the binomial tree with interest rates

```python
PopulateRates()
```

This function uses the volatility and current risk free rate to populate the binomial tree with relevant interest rate projections

### Populate the remainder of the model

```python
PopulateVandCF()
```

Populates the remainder of the model (Values and Cash Flows)


### Understanding the output

The *Output* variable is used to store all of the nodes and their respective parameters. It is a dictionary, structured as follows:

```python
{ Time : { Node Key : { 'R' : Rate at Node,
                        'CF' : Cash Flow at Node,
                        'V' : Value at node }}}
```

* Time, *int* 
  * Starts at **T = 0** and increases to the year in which the bond matures

* NodeKey, *int*
  * The higher the number, the higher the node
  * 0 is always the lowest node in the tree during the period

* Rate at Node, *float*
  * Effective interest rate at node

* Cash Flow at Node, *usually float*
  * Expected cash flow at node (risk-neutral probability)

* Value at Node, *float*
  * Discounted Cash Flow at node
