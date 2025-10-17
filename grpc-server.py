#!/usr/bin/env python3
from concurrent import futures
import base64
import io

import grpc
from PIL import Image

import lab6_pb2
import lab6_pb2_grpc


class Lab6ServiceServicer(lab6_pb2_grpc.Lab6ServiceServicer):
    def Add(self, request, context):
        return lab6_pb2.addReply(sum=int(request.a) + int(request.b))

    def RawImage(self, request, context):
        try:
            img = Image.open(io.BytesIO(request.img))
            w, h = img.size
            return lab6_pb2.imageReply(width=w, height=h)
        except Exception:
            return lab6_pb2.imageReply(width=0, height=0)

    def DotProduct(self, request, context):
        try:
            a = list(request.a)
            b = list(request.b)
            if len(a) != len(b):
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Vectors must be the same length.")
                return lab6_pb2.dotProductReply(dotproduct=0.0)

            dot = 0.0
            for x, y in zip(a, b):
                dot += float(x) * float(y)
            return lab6_pb2.dotProductReply(dotproduct=dot)
        except Exception as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return lab6_pb2.dotProductReply(dotproduct=0.0)

    def JsonImage(self, request, context):
        try:
            img_bytes = base64.b64decode(request.img)
            img = Image.open(io.BytesIO(img_bytes))
            w, h = img.size
            return lab6_pb2.imageReply(width=w, height=h)
        except Exception:
            return lab6_pb2.imageReply(width=0, height=0)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lab6_pb2_grpc.add_Lab6ServiceServicer_to_server(Lab6ServiceServicer(), server)
    server.add_insecure_port("[::]:5000")
    server.start()
    print("gRPC server started on port 5000")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()