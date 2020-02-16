class Repslicing():
    """
    This class adds a 'replay' (?) mode to slice operator.

    where:

    object ->   must be an iterable and sequentiable object, like a list,
                a tuple or any self-made object that accepts ":" (slice) operator.
    maxOverlap -> it's the max overlap admitted (default = 0)
                maxOverlap = -1 -> the check is disabled
                look the example that's past the class declaration.
                

    Normally, if you type[start:stop:step] with start <= stop, ("step" isn't relevant), you obtain an empty element.

    Instead using this class you get these results:
    result = type[start::step]+type[:stop:step]
    obviously if you type start == stop in this class you get the entire object but with a partially reversed order:
    
    i.e.:

    a = Reslicing(["a", "b", "c", "d", "e", "f"], maxOverlap = 0)
    a[4:2]
    ["e", "f", "a", "b", "c"]
    a[4:4]
    ["e", "f", "a", "b", "c", "d"]

    WARNING!:
        but if:
        print(aRs[2:-6])
        [2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3]
        It's an overlapping mode.

    other normally slicing modes operate as usual.
    """

    def __init__(self, object, maxOverlap = 0):
        """
        maxOverlap => 0 -> that's the max overlap admitted
        i.e.:  with maxOverlap = 0 -> there's no overlap admitted, if there's any, then the program raises an Exception
        maxOverlap = -1 -> the check is disabled
        look at the example that's past the class declaration.
        """

        self.object = object
        self.overlap = maxOverlap

    def __getitem__(self, item):
        """object.__getitem__ reused"""

        start = item.start
        stop = item.stop
        step = item.step

        if type(start) == type(stop) == type(1) and start >= stop:
            a = self.object[start::step]
            b = self.object[:stop:step]

            aSet = set(a)
            lenInterS = len(aSet.intersection(set(b))) # -> the lenght of intersection is the lenght of overlap

            if self.overlap >= 0 and (self.overlap < lenInterS):
                raise Exception('Too many overlapping here!',
                                "get " + str(lenInterS) + " but only " + str(
                                    self.overlap) + " is/are admitted.")

            return a + b

        return self.object[start:stop:step]

# Example code:

a = (i for i in range(10))
aRs = Repslicing(list(a), 3) # here the most overlaps granted from a list object are 3 

print(aRs[-2:-6])
print(aRs[-6:2])
print(aRs[2:6])
print(aRs[4:4])
print(aRs[6:2])
print(aRs[2:-6]) # this is for two overlaps

print(2*"\n")

a = (i for i in range(10))
aRs = Repslicing(list(a), -1) # here there's no check for overlaps

print(aRs[-2:-6])
print(aRs[-6:2])
print(aRs[2:6])
print(aRs[4:4])
print(aRs[6:2])
print(aRs[2:-6]) # this is for two overlaps

print(2*"\n")

a = tuple(i for i in range(10))
aRs = Repslicing(a, 0) # here no overlap is admitted (on tuple object)

print(aRs[-2:-6])
print(aRs[-6:-2])
print(aRs[2:6])
print(aRs[4:4])
print(aRs[6:2])
print(aRs[2:-6]) # this is for two overlapping codes BUT no overlap is admitted here.

'''
/usr/bin/python3.8 /home/alex/PycharmProjects/robaGenerica/RepSlip.py
[8, 9, 0, 1, 2, 3]
[]
[2, 3, 4, 5]
[4, 5, 6, 7, 8, 9, 0, 1, 2, 3]
[6, 7, 8, 9, 0, 1]
[2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3]



[8, 9, 0, 1, 2, 3]
[]
[2, 3, 4, 5]
[4, 5, 6, 7, 8, 9, 0, 1, 2, 3]
[6, 7, 8, 9, 0, 1]
[2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3]



(8, 9, 0, 1, 2, 3)
()
(2, 3, 4, 5)
(4, 5, 6, 7, 8, 9, 0, 1, 2, 3)
(6, 7, 8, 9, 0, 1)
Traceback (most recent call last):
  File "/home/alex/PycharmProjects/robaGenerica/RepSlip.py", line 105, in <module>
    print(aRs[2:-6])  # this is for two overlapping codes BUT no overlap is admitted here.
  File "/home/alex/PycharmProjects/robaGenerica/RepSlip.py", line 53, in __getitem__
    raise Exception('Too many overlapping here!',
Exception: ('Too many overlapping there!', 'get 2 but only 0 is/are admitted.')

Process finished with exit code 1'''
