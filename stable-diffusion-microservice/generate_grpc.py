from grpc_tools import protoc

protoc.main([
    'grpc_tools.protoc',
    '-I./protos',
    '--python_out=.',
    '--grpc_python_out=.',
    './protos/image_generation.proto',
])