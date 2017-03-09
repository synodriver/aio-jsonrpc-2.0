import json

from aio_jsonrpc_20.builder import RequestBuilder, BatchRequestBuilder


def test_simple_builder():
    builder = RequestBuilder()

    result = builder.call(method="aaa", params=[1, 2])

    assert json.loads(result) == {
        "jsonrpc": "2.0",
        "method": "aaa",
        "params": [1, 2],
        "id": 1
    }

    result = builder.notify(method="aaa", params=[3, 4])

    assert json.loads(result) == {
        "jsonrpc": "2.0",
        "method": "aaa",
        "params": [3, 4]
    }

    result = builder.call(method="aaa", params=[3, 4])

    assert json.loads(result) == {
        "jsonrpc": "2.0",
        "method": "aaa",
        "params": [3, 4],
        "id": 2
    }


def test_simple_builder_without_serialiser():
    builder = RequestBuilder(serializer=None)

    result = builder.call(method="aaa", params=[1, 2])

    assert result == {
        "jsonrpc": "2.0",
        "method": "aaa",
        "params": [1, 2],
        "id": 1
    }

    result = builder.notify(method="aaa", params=[3, 4])

    assert result == {
        "jsonrpc": "2.0",
        "method": "aaa",
        "params": [3, 4]
    }

    result = builder.call(method="aaa", params=[3, 4])

    assert result == {
        "jsonrpc": "2.0",
        "method": "aaa",
        "params": [3, 4],
        "id": 2
    }


def test_simple_batch_builder():
    builder = BatchRequestBuilder()

    assert json.loads(builder.get_request()) == []

    builder.call(method="aaa", params=[1, 2])
    builder.notify(method="aaa", params=[3, 4])
    builder.call(method="aaa", params=[3, 4])

    assert json.loads(builder.get_request()) == [
        {"jsonrpc": "2.0", "method": "aaa", "params": [1, 2], "id": 1},
        {"jsonrpc": "2.0", "method": "aaa", "params": [3, 4]},
        {"jsonrpc": "2.0", "method": "aaa", "params": [3, 4], "id": 2}
    ]
    builder.notify(method="aaa", params=[3, 4])
    assert json.loads(builder.get_request()) == [
        {"jsonrpc": "2.0", "method": "aaa", "params": [1, 2], "id": 1},
        {"jsonrpc": "2.0", "method": "aaa", "params": [3, 4]},
        {"jsonrpc": "2.0", "method": "aaa", "params": [3, 4], "id": 2},
        {"jsonrpc": "2.0", "method": "aaa", "params": [3, 4]}
    ]

    builder.purge()

    print("aaa" + builder.get_request())
    assert json.loads(builder.get_request()) == []


def test_simple_batch_builder_without_serialiser():
    builder = BatchRequestBuilder(serializer=None)

    builder.call(method="aaa", params=[1, 2])
    builder.notify(method="aaa", params=[3, 4])
    builder.call(method="aaa", params=[3, 4])

    assert builder.get_request() == [
        {"jsonrpc": "2.0", "method": "aaa", "params": [1, 2], "id": 1},
        {"jsonrpc": "2.0", "method": "aaa", "params": [3, 4]},
        {"jsonrpc": "2.0", "method": "aaa", "params": [3, 4], "id": 2}
    ]
