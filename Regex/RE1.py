import sys; args = sys.argv[1:]


switcher = {
    "30": r'/1000/',
    "31": r"//",
    "32": r"//",
    "33": r"//",
    "34": r"//",
    "35": r"//",
    "36": r"//",
    "37": r"/\d{3} *-* *\d{2} *-* *\d{4} *-* */",
    "38": r"//",
    "39": r"//"
}
  
print(switcher.get(args[0]))

# Medha Pappula, 6, 2026