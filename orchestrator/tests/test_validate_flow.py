from django.test import TestCase

from orchestrator.services.flow.spectrum_flow_v2 import SpectrumFlow
from orchestrator.tests.data.test_data_validation import (
    SINGLE_FULL_FLOW_INVALID,
    SINGLE_FULL_FLOW_VALID,
)


class ValildateFlowTest(TestCase):
    pass
    # @staticmethod
    # def test_full_single_flow_invalid():
    #     flow = SpectrumFlow(
    #         SINGLE_FULL_FLOW_INVALID["nodeList"], SINGLE_FULL_FLOW_INVALID["edgeList"]
    #     )

    #     assert flow.is_valid is False

    # @staticmethod
    # def test_full_single_flow_valid():
    #     flow = SpectrumFlow(
    #         SINGLE_FULL_FLOW_VALID["nodeList"], SINGLE_FULL_FLOW_VALID["edgeList"]
    #     )

    #     assert flow.is_valid is True
