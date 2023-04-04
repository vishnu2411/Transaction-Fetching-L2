import asyncio
import websockets
import json
import logging

logging.basicConfig(filename='transaction_log_async.log', level=logging.INFO, format='%(asctime)s - %(message)s')

async def handle_message(data):
    print(f'Received data: {data}')
    if 'params' in data:
        chain_id = data['params']['subscription']
        txns = data['params']['result']['transaction']

        print(f'transaction: {txns}')
        logging.info(f"Chain ID: {chain_id}, Transaction Hash: {txns['hash']}, Block Number: {txns['blockNumber']}, From: {txns['from']}, To: {txns['to']}, Value: {txns['value']}")
        
async def subscribe(chain_id, ws):
    subscribe_message = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_subscribe",
        "params": ["alchemy_minedTransactions", {}]
    })

    #for logs
    '''subscribe_message = json.dumps({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "eth_subscribe",
        "params": ["logs", {}]
    })'''
    await ws.send(subscribe_message)
    while True:
        try:
            data = json.loads(await asyncio.wait_for(ws.recv(), timeout=5))
            asyncio.create_task(handle_message(data))
            
        except asyncio.TimeoutError:
            pass

async def main():
    tasks = []
    try:
        arb_ws = await websockets.connect('wss://arb-mainnet.g.alchemy.com/v2/2Tr4ddoBTTbiUsUsoA_ZP5-qlfEHNlYr')
        logging.info("Arbitrum WebSocket connected")
        tasks.append(asyncio.create_task(subscribe('arbitrum', arb_ws)))
    except Exception as e:
        logging.error(f"Arbitrum WebSocket error: {e}")

    try:
        ovm_ws = await websockets.connect('wss://opt-mainnet.g.alchemy.com/v2/pXUHiwhSGSLfCQJ1tjM8LJqRGvYNxhBx')
        logging.info("Optimism WebSocket connected")
        tasks.append(asyncio.create_task(subscribe('optimism', ovm_ws)))
    except Exception as e:
        logging.error(f"Optimism WebSocket error: {e}")
        
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
