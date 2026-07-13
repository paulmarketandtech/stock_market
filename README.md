Stock Market app.

Whole idea of this app is based on momentum strategy: what's pumping will be still pumping.
This is not a real time market screener but the opposite, it focuses on yesterday's news (which in my opinion, it's still too often).

Everyday (from Tuesday to Saturday) in the morning it downloads data from yfinance.
Then based on those data it calculates returns.
It does basic metrics like weekly and ytd returns but also since any given date. 
You'll find in the code previous_correction variable (any given date). When market does deep corrections I believe then the market leaders change - so imo it's worth of measuring returns since that day.
Right now there's implemented Telegram bot which sends notifications with best and worst performing tickers.
Soon I'm planning to add and api for my DB and build some UI for representing those metrics.
