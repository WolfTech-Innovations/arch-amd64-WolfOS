# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc
from chromite.contrib.cros_sdk_server_poc import sdk_server_pb2 as sdk__server__pb2


class UpdateServiceStub(object):
    # missing associated documentation comment in .proto file
    pass

    def __init__(self, channel):
        """Constructor.

        Args:
          channel: A grpc.Channel.
        """
        self.UpdateChroot = channel.unary_unary(
            "/UpdateService/UpdateChroot",
            request_serializer=sdk__server__pb2.UpdateRequest.SerializeToString,
            response_deserializer=sdk__server__pb2.UpdateResponse.FromString,
        )


class UpdateServiceServicer(object):
    # missing associated documentation comment in .proto file
    pass

    def UpdateChroot(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_UpdateServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "UpdateChroot": grpc.unary_unary_rpc_method_handler(
            servicer.UpdateChroot,
            request_deserializer=sdk__server__pb2.UpdateRequest.FromString,
            response_serializer=sdk__server__pb2.UpdateResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "UpdateService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


class StreamServiceStub(object):
    # missing associated documentation comment in .proto file
    pass

    def __init__(self, channel):
        """Constructor.

        Args:
          channel: A grpc.Channel.
        """
        self.GetStream = channel.unary_stream(
            "/StreamService/GetStream",
            request_serializer=sdk__server__pb2.StreamRequest.SerializeToString,
            response_deserializer=sdk__server__pb2.StreamResponse.FromString,
        )


class StreamServiceServicer(object):
    # missing associated documentation comment in .proto file
    pass

    def GetStream(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_StreamServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "GetStream": grpc.unary_stream_rpc_method_handler(
            servicer.GetStream,
            request_deserializer=sdk__server__pb2.StreamRequest.FromString,
            response_serializer=sdk__server__pb2.StreamResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "StreamService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
