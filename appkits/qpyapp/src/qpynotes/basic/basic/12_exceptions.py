# Clase en vídeo: https://youtu.be/Kp4Mvapo5kc?t=32030

### Exception Handling ###

numberOne = 5
numberTwo = 1
numberTwo = "1"

# Exceptions base: try except

try:
    print(numberOne + numberTwo)
    print("No Exceptions")
except Exception as e:
    print("Error occurred", e)

try:
    print(numberOne + numberTwo)
    print("No Exceptions")
except ValueError as e:
    print("Error occurred", e)
except TypeError as e:
    print("Error occurred", e)

try:
    print(numberOne + numberTwo)
    print("No Exceptions")
except ValueError as error:
    print(error)
except Exception as my_random_error_name:
    print(my_random_error_name)
finally:
    print("final stage")
