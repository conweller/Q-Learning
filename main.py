import sys
import board


assert len(sys.argv) > 1
assert len(sys.argv[1]) == 4 or len(sys.argv[1]) == 5
assert (sys.argv[1][:3] + sys.argv[1][4:]).isdigit()
assert sys.argv[1][3] in ["p", "q"]
