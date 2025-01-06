# Generators

- yield: yield to execute something 
- __iter__(),__next__()
```python
def my_generator():
  n=1
  print('this is printed one')
  yield n
  n +=1
  print(n)
  print('this is printed two')
  n +=1
  print(n)
  print('this is printed three')
  yield n+1

a= my_generator()
print(next(a))
print(next(a))
for item in my_generator():
  print(item)
```
## Generator

- Generator in list comprehensive
- Memory Efficient: How?
- Represent Infinite Stream: How and Why?
```python
# Initialize the list
my_list = [1, 3, 6, 10]

# square each term using list comprehension
list_ = [x**2 for x in my_list]

# same thing can be done using a generator expression
# generator expressions are surrounded by parenthesis ()
generator = (x**2 for x in my_list)

print(list_)
print(generator)
print(max(generator))
generator = (x**2 for x in my_list)
print(sum(generator))

def pow_two_gen(max=0):
  n=0
  while n<max:
    yield 2**n
    n+=1

for item in pow_two_gen(5):
  print(item)
```
## Pipeline Generator

- How to make a pipeline generator
```python
def fib_num(nums):
  x,y=0,1
  for _ in range(nums):
    x,y=y,x+y
    yield x

def square_num(nums):
  for num in nums:
    yield num**2

print(sum(square_num(fib_num(10)))) ## what this do?
```
