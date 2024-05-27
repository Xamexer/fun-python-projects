import sys
# enumerate through a list
data = [1,2,-4,-3]

for index, value in enumerate(data): # for value in data:
    if value < 0:
        data[index] = 0

print(data)


# Use List Comprehensions Instead of for raw loops
# new_list = [expression for member in iterable (if condition)]

squares = []
for i in range(10):
    squares.append(i*i)

squares = [i*i for i in range(10)]

def cube(x):
    return x*x*x

squares = [cube(i) for i in range(10)]

evens = [i for i in range(10) if i % 2 == 0]

a = [1,2,3,4,5,6,7,8,9,10]
b = [0 if i < 4 else i for i in a]

quote = "hello everyobody"
unique_vowels = {i for i in quote if i in "aeiou"} # [which number to set, for i in list, when to set] {} = set; unique elements

matrix2d = [[i*j for i in range(5)] for j in range(3)]

s = sum((i*i for i in range(1000))) # instead of v

s = sum([i*i for i in range(1000)])

# Sort Complex Lists with sorted

data = [3,5,1,10,9]
sorted_date = sorted(data, reverse=True)

print(sorted_date)

data = [{"name": "apple", "price": 0.99}, {"name": "banana", "price": 0.50}, {"name": "orange", "price": 0.75}, {"name": "grape", "price": 1.99}]

sorted_data = sorted(data, key=lambda x: x["price"])

# Sort Unique values with sets

my_list = [1,2,3,4,5,6,7,7,7]
my_set = set(my_list)
print(my_set)

primes = {2,3,5,7,11,13}
print(primes)

# Save Memory with Generators

my_list = [i for i in range(10000)]
print(sum(my_list))
print(sys.getsizeof(my_list))

my_gen = (i for i in range(10000))
print(sum(my_gen))
print(sys.getsizeof(my_gen))

# Define default values in Dictionaries with .get() and .setdefault()

my_dict = {"item": "apple", "price": 0.99}
count = my_dict.get("count") # better than my_dict["count"] -> error
print(count)

count = my_dict.setdefault("count", 0)
print(count)

# Count hashable objects with collections.Counter()
from collections import Counter
my_list = [10,10,10,5,5,2,9,9,9,9,9,9]
counter = Counter(my_list)
print(counter[10])
most_common = counter.most_common(1) # which common value is most common
print(most_common[0][0])


# Join Strings with join
list_of_strings = ["Hello","my","name","is","John"]

my_string = " ".join(list_of_strings)
print(my_string)

# Merge two dictionaries with **

d1 = {"name": "John", "age": 30}
d2 = {"name": "Jane", "city": "New York"}

merged_dict = {**d1, **d2}
print(merged_dict)

# simplyfy with ifwith if x in list

colors = ["red", "green", "blue", "yellow"]

c = "red"

if c in colors:
    print("yes")

#zipping together

students = ["John", "Jane", "Mary"]
grades = [10, 9, 8]
colors = ["red", "green", "blue"]

for student, grade, colors in zip(students, grades,colors):
    print(f"{student}: {grade} : {colors}")

#lambda function

def add(x, y):
    return x + y

add = lambda x, y: x + y

add(1, 2)

x = (lambda x,y: x+y)(1,2)
#lambda with filter

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

even_numbers = list(filter(lambda x: x % 2 == 0, numbers))

# for else & while else flag

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
find = 5

for num in numbers:
    if num == find:
        print("found")
        break
else:
    print("not found")

count = 5

while count > 0:
    print(count)
    count -= 1
else:
    print("done")

# swap variable
x,y = 1,2

x,y = y,x

# advanced variable operator assignment
age = 25
smokes = True

health = "Poor" if age > 60 or smokes else "Good" if age < 18 else "Fair"