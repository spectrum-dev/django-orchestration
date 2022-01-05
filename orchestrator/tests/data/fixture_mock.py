# TODO: Find a way to mock returned value without writing many classes
# Not really important because return value is not checked for now
class GenericCeleryMockClass:
    def get(self):
        return "mock-result-value-here"
