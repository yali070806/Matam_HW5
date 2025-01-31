import json
import sys

ALPHABETSTRING = "abcdefghijklmnopqrstuvwxyz"
ALPHABET = 26
TWO = 2
TEN = 10
FIVE = 5
THREE = 3


class Enigma:
    def __init__(self, hash_map, wheels, reflector_map):
        self.hash = hash_map
        self.wheels = wheels
        self.map = reflector_map

    def encrypt(self, message):
        ret = ""
        encrypted = 0
        w1 = self.wheels[0]
        w2 = self.wheels[1]
        w3 = self.wheels[TWO]
        for c in message:
            if ord('z') >= ord(c) >= ord('a'):
                i = self.hash[c]
                val = ((TWO*self.wheels[0])-self.wheels[1]+self.wheels[TWO]) % ALPHABET
                if val == 0:
                    i += 1
                else:
                    i += val
                i = i % ALPHABET
                c1 = self.hash_opp(i)
                c2 = self.map[c1]
                i = self.hash[c2]
                if val == 0:
                    i -= 1
                else:
                    i -= val
                i = i % ALPHABET
                c3 = self.hash_opp(i)
                ret += c3
                encrypted += 1
            else:
                ret += c

            self.wheels[0] = (self.wheels[0] % 8) + 1
            if encrypted % TWO == 0:
                self.wheels[1] *= TWO
            else:
                self.wheels[1] -= 1
            if encrypted % TEN == 0:
                self.wheels[TWO] = TEN
            elif encrypted % THREE == 0:
                self.wheels[TWO] = FIVE
            else:
                self.wheels[TWO] = 0

        self.wheels[0] = w1
        self.wheels[1] = w2
        self.wheels[TWO] = w3
        return ret

    def hash_opp(self, i):
        for c in ALPHABETSTRING:
            if self.hash[c] == i:
                return c
        return '!'

class JSONFileException(Exception):
    def __init__(self):
        super().__init__()

def load_enigma_from_path(path):
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except:
        raise JSONFileException()

    enigma = Enigma(data["hash_map"], data["wheels"], data["reflector_map"])
    return enigma

def print_error(i):
    if i == 0:
        print("Usage: python3 enigma.py -c <config_file> -i <input_file> -o <output_file>", file=sys.stderr)
    if i == 1:
        print("The enigma script has encountered an error", file=sys.stderr)
    exit(1)

if __name__ == "__main__":
    args = sys.argv
    inpt = ""
    output = ""
    config = ""
    if len(args) != 7 and len(args) != 5:
        print_error(0)
    if len(args) == 5:
        flags = [args[1], args[3]]
        if not ("-c" in flags and "-i" in flags):
            print_error(0)
        for i in range(2):
            if flags[i] == "-i":
                inpt = args[2+2*i]
            elif flags[i] == "-c":
                config = args[2+2*i]
            else:
                print_error(0)

        try:
            with open(inpt, 'r') as input_file:
                enigma = load_enigma_from_path(config)
                for x in input_file:
                    print(enigma.encrypt(x), end="")
        except:
            print_error(1)

    if len(args) == 7:
        flags = [args[1], args[3], args[5]]
        if not ("-c" in flags and "-i" in flags and "-o" in flags):
            print_error(0)
        for i in range(3):
            if flags[i] == "-i":
                inpt = args[2+2*i]
            elif flags[i] == "-c":
                config = args[2+2*i]
            elif flags[i] == "-o":
                output = args[2+2*i]
            else:
                print_error(0)

        try:
            with open(inpt, 'r') as input_file:
                with open(output, 'w') as output_file:
                    enigma = load_enigma_from_path(config)
                    for x in input_file:
                        output_file.write(enigma.encrypt(x))
        except:
            print_error(1)

        
