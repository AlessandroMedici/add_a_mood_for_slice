class Repslicing():
    """
    This class adds a 'replay' (?) mode to slice operator.

    where:

    object ->   must be an iterable and sequentially object, like a list,
                a tuple or any self-made object that accepts ":" (slice) operator...
    maxOverlap more than 0 -> that'is the max overlap admitted
                maxOverlap = 0 -> no overlap admitted, if any then program raise an Exception
                maxOverlap = -1 -> check disabled
                look for example past class declaration.
                DANGER: check is inefective when step is more than 1
                

    Normally, if you type[a:b:step] with a < b, (step isn't relevant), you obtain a empty element.
    It's the same if you type type[a:b:step] with a == b

    using this class you get these results:

    result = type[a::step]+type[:b:step]

    obviously if you type a == b you get the entire object but with a partially reversed order:
    
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
        It's a overlapping mode.

    other normally slicing modes operate as usual.
    """

    def __init__(self, object, maxOverlap = 0):
        """
        maxOverlap more than 0 -> that'is the max overlap admitted
        maxOverlap = 0 -> no overlap admitted, if any then program raise an Exception
        maxOverlap = -1 -> check disabled
        look for example past class declaration.
        DANGER: check is inefective when step is more than 1
        """

        self.object = object
        self.overlap = maxOverlap

    def __getitem__(self, item):
        """object.__getitem__ reused"""

        start = item.start
        stop = item.stop
        step = item.step

        if item.start >= item.stop:

            lenght= len(self.object)

            result = self.object[start::step] + self.object[:stop:step]
            lenResult = len(result) - lenght

            if type(start) == type(stop) == type(1) and item.start >= item.stop:
                raise Exception('Too more overlapping there!', "get "+str(lenResult - self.overlap)+" but only "+str(self.overlap)+" is admitted.")

            return result

        return self.object[item.start:item.stop:item.step]

# Example code:

a = (i for i in range(10))
aRs = Repslicing(list(a), 3)
'''
above is granted for max 3 overlap on a list object
'''


print(aRs[-2:-6])
print(aRs[-6:2])
print(aRs[2:6])
print(aRs[4:4])
print(aRs[6:2])
print(aRs[2:-6]) # that's for two overlapping code

print(2*"\n")

a = (i for i in range(10))
aRs = Repslicing(list(a), -1)
'''
above is stated for no check for overlap
'''


print(aRs[-2:-6])
print(aRs[-6:2])
print(aRs[2:6])
print(aRs[4:4])
print(aRs[6:2])
print(aRs[2:-6]) # that's for two overlapping code

print(2*"\n")

a = tuple(i for i in range(10))
aRs = Repslicing(a, 0)
'''
above is granted for NO overlap on tuple object
'''

print(aRs[-2:-6])
print(aRs[-6:-2])
print(aRs[2:6])
print(aRs[4:4])
print(aRs[6:2])
print(aRs[2:-6]) # that's for two overlapping code BUT no overlap admitted there.

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
    print(aRs[2:-6])  # that's for two overlapping code BUT no overlap admitted there.
  File "/home/alex/PycharmProjects/robaGenerica/RepSlip.py", line 53, in __getitem__
    raise Exception('Too more overlapping there!',
Exception: ('Too more overlapping there!', 'get 2 but only 0 is admitted.')

Process finished with exit code 1'''
