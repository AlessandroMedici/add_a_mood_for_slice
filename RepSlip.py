class Repslicing(object):
    """
    This class adds a 'replay' (?) mode to slice operator.

    where:

    object ->   must be an iterable and sequentially object, like a list,
                a tuple or any self-made object that accepts ":" (slice) operator...

    Normally, if you type[a:b:step] with a < b, (step isn't relevant), you obtain a empty element.
    It's the same if you type type[a:b:step] with a == b

    using this class you get these results:

    result = type[a::step]+type[:b:step]

    obviously if you type a == b you get the entire object but with a partially reversed order:

    WARNING!:
    but if:
    print(aRs[2:-6])
    [2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3]
    It's a overlapping mode.


    i.e.:

    a = Reslicing(["a", "b", "c", "d", "e", "f"])
    a[4:2]
    ["e", "f", "a", "b", "c"]
    a[4:4]
    ["e", "f", "a", "b", "c", "d"]

    other normally slicing modes operate as usual.
    """

    def __init__(self, object):
        self.object = object

    def __getitem__(self, item):
        """object.__getitem__ reused"""

        if item.start >= item.stop:
            return self.object[item.start::item.step] + self.object[:item.stop:item.step]

        return self.object[item.start:item.stop:item.step]


a = (i for i in range(10))
aRs = Repslicing(list(a))

print(aRs[2:-6]) # that's a overlapping mode!
print(aRs[-2:-6])
print(aRs[-6:-2])
print(aRs[2:6])
print(aRs[4:4])
print(aRs[6:2])

print(2*"\n")

a = tuple(i for i in range(10))
aRs = Repslicing(a)

print(aRs[2:-6]) # that's a overlapping mode!
print(aRs[-2:-6])
print(aRs[-6:-2])
print(aRs[2:6])
print(aRs[4:4])
print(aRs[6:2])

'''
/usr/bin/python3.8 /home/alex/PycharmProjects/robaGenerica/RepSlip.py
[2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3]
[8, 9, 0, 1, 2, 3]
[4, 5, 6, 7]
[2, 3, 4, 5]
[4, 5, 6, 7, 8, 9, 0, 1, 2, 3]
[6, 7, 8, 9, 0, 1]



(2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3)
(8, 9, 0, 1, 2, 3)
(4, 5, 6, 7)
(2, 3, 4, 5)
(4, 5, 6, 7, 8, 9, 0, 1, 2, 3)
(6, 7, 8, 9, 0, 1)

Process finished with exit code 0'''




