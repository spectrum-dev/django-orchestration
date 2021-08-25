class StrategyNotValidException(Exception):
    """
    Strategy is invalid
    """


class StrategyDoesNotExistException(Exception):
    """
    Strategy does not exist
    """


class MultipleBacktestBlocksException(Exception):
    """
    More than one backtest block
    """
