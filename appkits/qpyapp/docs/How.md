# How

## How to Register a Service Into Container

Service is a class with different business methods,
or implement a protocol.

How to register:

```python
class TestSpellContainer:
    container = ServiceContainer()

    def test_register_spell(self):
        self.container.register(invoker_service)
        print(self.container)
        result = self.container.get_spell(invoker_service.HttpInvokerService.invoke.__qualname__)
        print(result("request"))
```

## How to Invoke Service Method through Container

```python
result = self.container.get_spell(invoker_service.HttpInvokerService.invoke.__qualname__)
print(result("request"))
```

## How to init different Service with Parameters
Everything could be decorated, think about to wire thing together.

- Providers
  - Different Providers to inject
  - Init With Providers
- Services

