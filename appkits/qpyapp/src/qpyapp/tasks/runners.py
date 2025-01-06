from typing import Union, Any

from qpyapp.tasks.containers import AbsContainer


class SpellRunner:

    def __init__(self):
        self.handlers = {}
        self.run_data = []

    def run_script(self, data: Any):
        self.run_data = data

    def run(self):
        for item in self.run_data:
            processor = self.handlers["providers"].get(HttpProcessor)
            result = processor.invoke(item)
            print(result.json())

    def add_spells(self, container: Union[AbsContainer, Any], identity: Any):
        self.handlers[identity] = container


runner = SpellRunner()
