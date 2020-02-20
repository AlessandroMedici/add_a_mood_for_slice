class ExtendedSlicing():
    """
    This class adds a 'reverse' (?) mode to slice operator.

    where in __init__ :

    object ->   must be an spiceable object, like a list,
                a tuple or any self-made object that accepts ":" (slice) operator.
                (remember that no one generator is admitted, because generator isn't slicing object:
                calling ExtendedSlicing(i for i in range(10)) get a TypeError Error from Python,
                but calling ExtendedSlicing([i for i in range(10)]) or ExtendedSlicing(aList)
                is admitted from Python.

    return -> a normal object the same class of original object NOT one instance of ExtendedSlicing class.
    
    
    Normally, if you type object[start:stop:step] with start <= stop, ("step" isn't relevant), you obtain an empty
    element.

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

    I don't know if this overlapping is a your request or not, but if it this class raise a ValueError

    all other normally slicing modes operate as usual.

    A last very obvius advise:

    if you type:
    aList = [1,2,3,4]
    aList = ExtendedSlicing(aList)
    aList = aList[3:4]

    the original aList are overwritted AND the resulting aList is a normal class of list.
    """
    
    #TODO: check for limits before create a big sub list
    
    def __init__(self, oBject: object):
        """
        @param oBject: a spliceable object
        """
        self.oBject = oBject

    def __getitem__(self, item):
        """oBject.__getitem__ reused"""
        oBject = self.oBject

        start = item.start
        stop = item.stop
        step = item.step

        if start >= stop:
            # extended slicing request
            length = len(oBject)
            if length == 0:
                return []
            
            a = oBject[start::step]
            b = oBject[:stop:step]
            
            if stop < 0 and step < 0:

                # aSet = set(a)
                # bSet = set(b)

                # lenInterS = len(set(a).intersection(bSet))  # -> the lenght of intersection is the lenght of overlap
                if lenInterS:= len(set(a).intersection(set(b))):
                    # affordable error detecting, but too slow for a very large oBject
                    raise ValueError('Too many overlapping here!',  # arg[0]
                                    "get " + str(lenInterS) + " but not one is admitted.",  # arg[1]
                                    start,  # arg[2]
                                    stop,  # arg[3]
                                    step,  # arg[4]
                                    len(a) + len(b),  # arg[5]
                                    len(oBject)  # arg[6]
                                    )
            return a + b

        return self.oBject[start:stop:step]


def test(n=20):

    for step in range(-n, n):  # for all reasonable index step
        if step == 0:
            continue  # step=0 isn't never admitted

        for j in range(n):  # lenghts of objects in test

            a = tuple(i for i in range(j))  # for all reasonable object's length
            lis = ExtendedSlicing(a)  # create a new object of this length

            for start in range(-n, n):  # for all reasonable index start
                for stop in range(-n, n):  # for all reasonable index stop
                    try:
                        b = lis[start:stop:step]  # call spicing function
                    except ValueError as ve:
                        print(ve.args)


if __name__ == '__main__':

    test(n=20)
