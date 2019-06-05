#!/usr/bin/env python
from rpc_client import RpcClient


# Exemplo de requisição com RPC

rpc = RpcClient()

print("[x] Requesting altura")
response = rpc.call('altura')
print("[x] Got {response}".format(response=response))
