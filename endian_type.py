from enum import Enum

class EndianType(Enum):
    AB = 1
    BA = 2
    ABCD = 3
    CDAB = 4
    BADC = 5
    DCBA = 6
    ABCDEFGH = 7
    GHEFCDAB = 8
    BADCFEHG = 9
    HGFEDCBA = 10