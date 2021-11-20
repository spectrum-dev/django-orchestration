# TODO: Find a way to mock returned value without writing many classes
# Not really important because return value is not checked for now
class GenericCeleryMockClass:
    def get(self):
        return "mock-result-value-here"


MULTIPLE_STRATEGY_BLOCK_MOCK_RESPONSE = [
    (
        "DATA_BLOCK-1-1",
        GenericCeleryMockClass(),
        None,
    ),
    (
        "COMPUTATIONAL_BLOCK-1-3",
        GenericCeleryMockClass(),
        None,
    ),
    (
        "COMPUTATIONAL_BLOCK-1-2",
        GenericCeleryMockClass(),
        None,
    ),
    (
        "SIGNAL_BLOCK-1-4",
        GenericCeleryMockClass(),
        None,
    ),
    (
        "STRATEGY_BLOCK-1-5",
        GenericCeleryMockClass(),
        None,
    ),
    (
        "STRATEGY_BLOCK-1-6",
        GenericCeleryMockClass(),
        None,
    ),
]
