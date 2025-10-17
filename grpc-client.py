#!/usr/bin/env python3
from __future__ import print_function
import base64
import os
import random
import sys
import time

import grpc

import lab6_pb2
import lab6_pb2_grpc

IMG_PATH = "Flatirons_Winter_Sunrise_edit_2.jpg"
PORT = 5000  # matches server


def doAdd(stub, debug=False):
    resp = stub.Add(lab6_pb2.addMsg(a=5, b=10))
    if debug:
        print(f"Add response: {resp.sum}")
    return resp.sum


def doRawImage(stub, debug=False):
    with open(IMG_PATH, "rb") as f:
        img = f.read()
    resp = stub.RawImage(lab6_pb2.rawImageMsg(img=img))
    if debug:
        print(f"RawImage response: width={resp.width}, height={resp.height}")
    return resp.width, resp.height


def doDotProduct(stub, debug=False, n=100):
    a = [random.random() for _ in range(n)]
    b = [random.random() for _ in range(n)]
    resp = stub.DotProduct(lab6_pb2.dotProductMsg(a=a, b=b))
    if debug:
        print(f"DotProduct response: {resp.dotproduct}")
    return resp.dotproduct


def doJsonImage(stub, debug=False):
    with open(IMG_PATH, "rb") as f:
        img = f.read()
    b64 = base64.b64encode(img).decode("utf-8")
    resp = stub.JsonImage(lab6_pb2.jsonImageMsg(img=b64))
    if debug:
        print(f"JsonImage response: width={resp.width}, height={resp.height}")
    return resp.width, resp.height


def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <host> <cmd> <reps>")
        print("  <cmd> is one of: add, rawImage, dotProduct, jsonImage")
        sys.exit(1)

    host = sys.argv[1]
    cmd = sys.argv[2]
    reps = int(sys.argv[3])

    if cmd in ("rawImage", "jsonImage") and not os.path.exists(IMG_PATH):
        print(f"Image not found: {IMG_PATH}")
        sys.exit(1)

    channel = grpc.insecure_channel(f"{host}:{PORT}")
    stub = lab6_pb2_grpc.Lab6ServiceStub(channel)

    print(f"Running {reps} reps against {host}:{PORT} ({cmd})")
    start = time.perf_counter()

    if cmd == "add":
        for _ in range(reps):
            doAdd(stub)
    elif cmd == "rawImage":
        for _ in range(reps):
            doRawImage(stub)
    elif cmd == "dotProduct":
        for _ in range(reps):
            doDotProduct(stub)
    elif cmd == "jsonImage":
        for _ in range(reps):
            doJsonImage(stub)
    else:
        print("Unknown command:", cmd)
        sys.exit(1)

    delta_ms = (time.perf_counter() - start) / reps * 1000.0
    print(f"Took {delta_ms:.3f} ms per operation")


if __name__ == "__main__":
    main()
