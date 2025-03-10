from agentsway.agents import doc_wrappers
from pytest_bdd import scenario, given, when, then


@scenario("Simple Convertion")
def test_convert_to_markdown():
    result = doc_wrappers.covert_to_markdown("https://arxiv.org/pdf/2408.09869")
    print(result)

