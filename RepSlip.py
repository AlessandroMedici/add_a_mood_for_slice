class ExtendedSlicing():
    """
    This class adds a 'replay' (?) mode to slice operator.

    where in __init__ :

    object ->   must be an iterable and sequentiable object, like a list,
                a tuple or any self-made object that accepts ":" (slice) operator.
                (remember that no one generator is admitted, because generator isn't slicing object:
                calling ExtendedSlicing(i for i in range(10)) get a TypeError Error from python,
                but calling ExtendedSlicing([i for i in range(10)]) or ExtendedSlicing(aList)
                is obviously admitted from python.

    maxOverlap -> it's the max overlap admitted (default = 0)
                maxOverlap = -1 -> the check is disabled
                look the example that's past the class declaration.

    return -> a normal object the same class of original object NOT one instance of ExtendedSlicing class.
    
    Normally, if you type object[start:stop:step] with start <= stop, ("step" isn't relevant), you obtain an empty
    element. Instead, using this class you get these results:
    
    result = object[start::step]+object[:stop:step]

    If start <= stop this class literally get 2 call to __getitem__ method of the underlying sliceable object:
    the first is object[start::step]
    the second is object[:stop:step]

    and return object[start::step]+object[:stop:step]

    obviously if you type start == stop in this class you get the entire object but with a partially reversed order:
    i.e.:
    a = ExtendedSlicing(["a", "b", "c", "d", "e", "f"], maxOverlap = 0)
    a[4:2]
    ["e", "f", "a", "b", "c"]
    a[4:4]
    ["e", "f", "a", "b", "c", "d"]

    admitting this mode in a call, obviously we are risking this case:

    WARNING! Look at this:
        aRs = ExtendedSlicing([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        print(aRs[2:-6])
        [2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3]
        It's an overlapping mode: with one or more duplicated item.

    I don't know if this overlapping is a your request or not, but is possible
    controlling the number of overlapped (like duplicated) item, using maxOverlap
    parameter:
    set maxOverlap at requested value and all is good, or set it at -1 and no check is made.


    all other normally slicing modes operate as usual.

    A last advise:

    if you type:
    aList = [1,2,3,4]
    aList = ExtendedSlicing(aList)
    aList = aList[3:4]

    the original aList are overwritted AND the resulting aList is a normal class of list.
    """

    def __init__(self, oBject, maxOverlap=0, typed = False):
        """
        maxOverlap => 0 -> that's the max overlap admitted
        i.e.:  with maxOverlap = 0 -> there's no overlap admitted, if there's any, then the program raises an Exception
        maxOverlap = -1 -> the check is disabled
        look at the example that's past the class declaration.
        """

        self.oBject = oBject
        self.overlap = maxOverlap

    def __getitem__(self, item):
        """oBject.__getitem__ reused"""

        start = item.start
        stop = item.stop
        step = item.step

        if type(start) == type(stop) == type(1) and start >= stop:
            # extended slicing request

            a = self.oBject[start::step]
            b = self.oBject[:stop:step]

            aSet = set(a)
            lenInterS = len(aSet.intersection(set(b)))  # -> the lenght of intersection is the lenght of overlap

            if self.overlap >= 0 and (self.overlap < lenInterS):
                raise ValueError('Too many overlapping here!',  # arg[0]
                                 "get " + str(lenInterS) + " but only " + str(
                                         self.overlap) + " is/are admitted.",  # arg[1]
                                 start,  # arg[2]
                                 stop,  # arg[3]
                                 step,  # arg[4]
                                 len(a) + len(b),  # arg[5]
                                 len(self.oBject),  # arg[6]
                                 lenInterS, # arg[7]
                                 self.overlap # arg[8])

            return a + b

        return self.oBject[start:stop:step]

def test(n=100, maxoverlap=100):
    case = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    text = '''
    case[0] = start < 0 stop < 0,
    case[1] = start < 0 stop = 0,
    case[2] = start < 0 stop > 0,
    case[3] = start = 0 stop < 0,
    case[4] = start = 0 stop = 0,
    case[5] = start = 0 stop > 0,
    case[6] = start > 0 stop < 0,
    case[7] = start > 0 stop = 0,
    case[8] = start > 0 stop > 0,
    '''
    text = text.split(sep=",")

    for j in range(n):  # lenghts of objects in test
        for overlap in range(-maxoverlap, maxoverlap):  # for all reasonable overlap

            a = tuple(i for i in range(j))  # for all reasonable object's lenght
            lis = ExtendedSlicing(a, overlap)  # create a new object of this lenght

            for start in range(-j, j):  # for all reasonable index start
                for stop in range(-n, n):  # for all reasonable index stop
                    for step in range(0, overlap):  # for all reasonable index step

                        if step == 0:
                            continue  # step=0 isn't never admitted from python

                        try:
                            b = lis[start:stop:step]  # call spicing function
                        except ValueError as ve:  # trapping...
                            args = ve.args
                            # catching problematic case, no other's admitted:
                            if args[2] == 0:
                                if args[3] < 0:
                                    case[3] += 1
                                    continue  # case[3] = start = 0, stop < 0
                            if args[2] > 0:
                                if args[3] < 0:
                                    case[6] += 1
                                    continue  # case[6] = start = 0, stop < 0

                            raise Exception('Unpredicted Error there',  # arg[0]
                                            a, # arg[0],
                                            start,  # arg[2]
                                            stop,  # arg[3]
                                            step,  # arg[4]
                                            b,  # arg[5]
                                            )

    for j, i in enumerate(case):
        print(text[j], i)

def examples():
    """ only a sample running example, full test is made into test method"""

    def l(txt, val=""):
        print(txt, val)

    baseList = [i for i in range(10)]
    l("\nbaseList = [i for i in range(10)]", [i for i in range(10)])

    sliced = ExtendedSlicing(baseList)
    l("\nsliced = Repslicing(baseList)")

    result = sliced[3:3]
    l("\nresult = sliced[3:3] result = ", result)

    result = baseList[3:3]
    l("\nresult = baseList[3:3] result = ", result)

    result = sliced[-2:-3]
    l("\nresult = sliced[-2:-3] result = ", result)

    result = baseList[-2:-3]
    l("\nresult = baseList[-2:-3] result = ", result)

    result = sliced[-3:-3]
    l("\nresult = sliced[-3:-3] result = ", result)

    result = baseList[-3:-3]
    l("\nresult = baseList[-3:-3] result = ", result)

    l("\nwith overlapping set at -1")

    sliced = ExtendedSlicing(baseList, -1)
    l("\nsliced = Repslicing(baseList,-1)")

    result = sliced[-3:3]
    l("\nresult = sliced[-3:3] result = ", result)

    result = baseList[-3:3]
    l("\nresult = baseList[-3:3] result = ", result)

    result = sliced[2:-6]
    l("\nresult = sliced[2:-6] result = ", result)

    result = baseList[2:-6]
    l("\nresult = baseList[2:-6] result = ", result)

    result = sliced[3:-3]
    l("\nresult = sliced[3:-3]  result = ", result)

    result = baseList[3:-3]
    l("\nresult = baseList[3:-3] result = ", result)

if __name__ == '__main__':
    pass
    examples()
    test(n=20, maxoverlap=20)
