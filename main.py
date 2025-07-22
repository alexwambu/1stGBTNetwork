from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from web3 import Web3

# Replace this with your live Layer 1 RPC URL
w3 = Web3(Web3.HTTPProvider("https://GBTNetwork"))

app = FastAPI()

@app.get("/")
def root():
    return {"message": "GBTNetwork Backend API is Live"}

@app.get("/api/get-balance")
def get_balance(address: str):
    try:
        balance = w3.eth.get_balance(address)
        ether = w3.from_wei(balance, 'ether')
        return {"address": address, "balance": str(ether)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/send-tx")
async def send_transaction(req: Request):
    try:
        data = await req.json()
        signed_tx = data.get("signedTx")
        if not signed_tx:
            return JSONResponse(status_code=400, content={"error": "signedTx not provided"})
        tx_hash = w3.eth.send_raw_transaction(bytes.fromhex(signed_tx[2:]))  # strip '0x'
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
