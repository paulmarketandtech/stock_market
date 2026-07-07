"""
workflow:
YTD returns
last correction returns. remove previous correction. count also over here weekly change returns
market breadth:
- trading view, download indicators and populate DB.
  based on that check if close price above or below SMAs - booleans.
  count above/below SMAs for nasdaq and nyse.
  create chart screens

ytd corrections: pull data from stock_market, sort it and populate desired tables
like YTD20Best, LastCorrectionBest etc.

weekly change: calculate weekly returns and then populate tables: Weekly20Best

indexes returns: works only on saturday. put the calculations in the 1 step.
weekly change is calculated everyday.
it should be counted everyday, but only displayed on Sat? have to think this through
"""
