# This is handy: https://www.ritchieng.com/python/decorators-kwargs-args/

# * allows for the extraction of positional variables from an iterable
def dummy_func_w(*args):
    return (args)

to10 = range(10)

print (f"With *: {dummy_func_w(*to10)}")

# if we don't use * before the args variable, we'd get (in this case) a list returned instead:

def dummy_func_wo(args):
    print (args)

print (f"Without *: ", end="")
print (dummy_func_wo(to10))

# ** is for dictionaries & key value pairs

def dummy_func_kw(**kwargs):
    return kwargs

print (f"With dummy_func_kw(a=0, b=1, c=2): {dummy_func_kw(a=0, b=1, c=2)}")
new_dict = {'a': '10', 'b': '20', 'c': '30'}
# not using ** in this instance would throw up an error message
print (f"Or dummy_func_kw(**new_dict): {dummy_func_kw(**new_dict)}")

# decorators allow modification or replacement of a function without changing the original function's code.
def printall(func):
    def inner(*args, **kwargs):
        print ('Arguments for args: {}'.format(args))
        print ('Arguments for kwargs: {}'.format(kwargs))
        return func(*args, **kwargs)
    return inner

@printall
def random_func(a,b):
    return a * b

a = random_func(2,2)

print(a)

@printall
def random_func_new():
    return 10

b = random_func_new()

print(b)

@printall
def dummy_func_kw(**kwargs):
    return kwargs

print(dummy_func_kw(a=0, b=1, c=2))