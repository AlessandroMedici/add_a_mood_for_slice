class Repslicing():
    """
    This class adds a 'replay' (?) mode to slice operator.

    where:

    object ->   must be an iterable and sequentially object, like a list,
                a tuple or any self-made object that accepts ":" (slice) operator...
                
    maxOverlap -> must be an integer that set the max overlapping admitted
                when maxOverlap = 0 -> no overlap admitted
                when maxOverlap < 0 -> no check for overlap
                other .... obvius. 

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

    a = Reslicing(["a", "b", "c", "d", "e", "f"], maxOverlap = 0)
    a[4:2]
    ["e", "f", "a", "b", "c"]
    a[4:4]
    ["e", "f", "a", "b", "c", "d"]

    other normally slicing modes operate as usual.
    """

    def __init__(self, object, maxOverlap = 0):
        """
        maxOverlap = 0 -> no overlap, if any then program raise an Exception
        maxOverlap = -1 -> check disabled
        look for example running this code.
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

            if self.overlap < lenResult:
                raise Exception('Too more overlapping there!', "get "+str(lenResult - self.overlap)+" but only "+str(self.overlap)+" is admitted.")

            return result

        return self.object[item.start:item.stop:item.step]


a = (i for i in range(10))
aRs = Repslicing(list(a), 3)
'''
above is granted for max 3 overlap
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
above is granted for NO overlap
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



(8, 9, 0, 1, 2, 3)
(4, 5, 6, 7)
(2, 3, 4, 5)
(4, 5, 6, 7, 8, 9, 0, 1, 2, 3)
(6, 7, 8, 9, 0, 1)
Traceback (most recent call last):
  File "/home/alex/.local/share/JetBrains/Toolbox/apps/PyCharm-C/ch-0/193.5233.109/plugins/python-ce/helpers/pydev/pydevd.py", line 1434, in _exec
    pydev_imports.execfile(file, globals, locals)  # execute the script
  File "/home/alex/.local/share/JetBrains/Toolbox/apps/PyCharm-C/ch-0/193.5233.109/plugins/python-ce/helpers/pydev/_pydev_imps/_pydev_execfile.py", line 18, in execfile
    exec(compile(contents+"\n", file, 'exec'), glob, loc)
  File "/home/alex/PycharmProjects/robaGenerica/RepSlip.py", line 97, in <module>
    print(aRs[2:-6]) # that's for two overlapping code
  File "/home/alex/PycharmProjects/robaGenerica/RepSlip.py", line 63, in __getitem__
    raise Exception('Too more overlapping there!', "get "+str(lenResult - self.overlap)+" but only "+str(self.overlap)+" is admitted.")
Exception: ('Too more overlapping there!', 'get 2 but only 0 is admitted.')
Exception ignored in: <module 'threading' from '/usr/lib/python3.8/threading.py'>
Traceback (most recent call last):
  File "/usr/lib/python3.8/threading.py", line 1388, in _shutdown
    lock.acquire()
KeyboardInterrupt: 

Process finished with exit code 1'''
