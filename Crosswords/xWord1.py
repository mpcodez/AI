"""

1. every puzzle is a rectangle
2. all words/entries are at least 2 characters long
3. every char appears in 2 words (one vertical, and one horizontal)
4. The blocking squares have 180 degree rotational symetry around the center.
| e |   |   |   |   | <- blocking square is also here
|   |   |   |   |   |
|   |   |   |   |   |
|   |   |   |   | x | <- cross is given

5. no disjoint regions
|   |   | - |   |   |
|   |   | - |   |   |
|   |   | - |   |   |
|   |   | - |   |   | not allowed

ARGS ===== ["9x12", "12", "random seeds", "dict.txt"]
-> generate one XWords puzzle that meets all these conditions & displays it in 2D (# blocking)
V{Vertical Position}x{Horizontal Postiion}bro
|   | b |   |   |   |
|   | r |   |   |   |
|   | o |   |   |   |
|   |   |   |   |   |

NO # after V4x0 counts as a blocking square


How many distinct 5by5 boards give >4 blocking sqares

DONE:
| # |   |   |   | # |
| # |   |   |   | # |
| # |   |   |   | # |
| # |   |   |   | # |
| # |   |   |   | # |

| # | # | # | # | # |
|   |   |   |   |   |
|   |   |   |   |   |
|   |   |   |   |   |
| # | # | # | # | # |

| # | # | # | # | # |
| # | # | # | # | # |
| # | # | # | # | # |
| # | # | # | # | # |
| # | # | # | # | # |

| # | # |   |   |   |
| # | # |   |   |   |
|   |   |   |   |   |
|   |   |   | # | # |
|   |   |   | # | # |

|   |   |   | # | # |
|   |   |   | # | # |
|   |   |   |   |   |
| # | # |   |   |   |
| # | # |   |   |   |

| # | # | # | # | # |
| # |   |   |   | # |
| # |   |   |   | # |
| # |   |   |   | # |
| # | # | # | # | # |

| # | # |   |   |   |
| # | # |   |   |   |
| # | # |   |   |   |
| # | # | # | # | # |
| # | # | # | # | # |

|   |   |   | # | # |
|   |   |   | # | # |
|   |   |   | # | # |
| # | # | # | # | # |
| # | # | # | # | # |



CONTINUE:

| # | # |   |   |   |
| # | # |   |   |   |
| # | # |   |   |   |
| # | # | # | # | # |
| # | # | # | # | # |

"""

args = ['13x13', '32', 'dct20k.txt', 'H1x4#Toe#', 'H9x2#', 'V3x6#', 'H10x0Scintillating', 'V0x5stirrup', 'H4x2##Ordained', 'V0x1Very', 'V0x12Arp', 'V5x0orb']

