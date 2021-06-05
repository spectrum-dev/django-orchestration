from orchestrator.services.flow.spectrum_flow import SpectrumFlow


def run(vertices, edges):
    spectrum_flow = SpectrumFlow(vertices, edges)
    return spectrum_flow
