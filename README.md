The code is used to fetch transaction data from L2's i.e arbitrum and optimism.

The first code Transaction_fetching_arbitrum.py fetches transaction data only from arbitrum sequencer through websocket connection and can also be used to connect to optimism.
The Second code Transaction_fetching_async.py fetches transaction data from both the L2's in asynchronous manner.


The requirements for running the codes are:
1. Python : version 3.7.2+
2. Web3 package 
3. Websocket : websocket 0.2.1

When the above codes are run they generate log file with data corresponding to the fetched transaction.
