import sys; args = sys.argv[1:]


switcher = {
    "40": r"//",
    "41": r"//",
    "42": r"//",
    "43": r"/\b.(..)*\b/m",
    "44": r"//",
    "45": r"/\b\w*([aeiou])(?!\1)[aeiou]\w*\b/i",
    "46": r"/^((110)?.)*$/",
    "47": r"//",
    "48": r"//",
    "49": r"/^[12][012]*[02]$/"

    
}
  
print(switcher.get(args[0]))

# Medha Pappula, 6, 2026