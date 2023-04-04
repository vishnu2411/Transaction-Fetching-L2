import websocket
import json
import logging

logging.basicConfig(filename='transaction_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def on_message(ws, message):
    data = json.loads(message)
    print(f'Received data: {data}')
    if 'params' in data:
        txns = data['params']['result']['transaction']
        logging.info(f"Transaction Hash: {txns['hash']}, Block Number: {txns['blockNumber']}, From: {txns['from']}, To: {txns['to']}, Value: {txns['value']}")

def on_error(ws, error):
    logging.error(error)

def on_close(ws):
    logging.info("WebSocket closed")

def on_open(ws):
    logging.info("WebSocket opened")

    # Subscribe to the Arbitrum Sequencer websocket feed
    #for all mixed transactions
    subscribe_message = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_subscribe",
        "params": ["alchemy_minedTransactions", {}]
    })

    #for filtered transactions
    '''subscribe_message = json.dumps({
        "jsonrpc": "2.0",
       "method": "eth_subscribe",
       "params": ["alchemy_minedTransactions", {"addresses": [{"to": "0x9f3ce0ad29b767d809642a53c2bccc9a130659d7", "from": "0x228f108fd09450d083bb33fe0cc50ae449bc7e11"},
                                                              {"to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"}]
                                                ,"includeRemoved": false,  "hashesOnly": true}],
       "id": 1
    })'''

    #for logs
    '''subscribe_message = json.dumps({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "eth_subscribe",
        "params": ["logs", {"address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", "topics": ["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"]}]
    })'''
     
    ws.send(subscribe_message)

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "wss://arb-mainnet.g.alchemy.com/v2/2Tr4ddoBTTbiUsUsoA_ZP5-qlfEHNlYr",
        on_message = on_message,
        on_error = on_error,
        on_close = on_close,
        on_open = on_open
    )
    ws.run_forever()
