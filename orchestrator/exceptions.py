class BlockDoesNotExist(Exception):
    """
    Block does not exist in registry
    """


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


class ScreenerBulkDataBlockDneException(Exception):
    """
    Bulk Data Block does not exist in the screener
    """
