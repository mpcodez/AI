import sys; args = sys.argv[1:]


switcher = {
    "50": r"/\w*(\w)\w*\1\w*/i",
    "51": r"/\w*(\w)\w*(\1\w*){3}/i",
    "52": r"/^([01])([10]*\1)*$/",
    "53": r"/(?=\b\w{6}\b)\w*cat\w*/i",
    "54": r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i",
    "55": r"/\b(?!\w*cat)\w{6}\b/i",
    "56": r"/\b(?!\w*(\w)\w*\1)\w+/i",
    "57": r"/^(1(?!0011)|0)*$/",
    "58": r"/\w*([aeiou])(?!\1)[aeiou]\w*/i",
    "59": r"/^(1(?!11)(?!01)|0)*$/",
}
  
print(switcher.get(args[0]))

# Medha Pappula, 6, 2026