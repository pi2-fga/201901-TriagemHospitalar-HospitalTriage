#!/usr/bin/env python
from rpc_client import RpcClient


# Exemplo de requisição com RPC

rpc = RpcClient()

print("[x] Requesting temperature")
response = rpc.call('temperature')
print("[x] Got {response}".format(response=response))
