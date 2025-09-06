import string, json

class Rotor:
    def __init__(self, wiring, notch, position=0):
        self.wiring = wiring  # mapping A-Z
        self.notch = notch    # the position to turn next rotor
        self.position = position  # current rotor position

    def encode_forward(self, c):
        # Convert letter c through rotor forward
        index = (string.ascii_uppercase.index(c) + self.position) % 26
        encoded_letter = self.wiring[index]
        return string.ascii_uppercase[(string.ascii_uppercase.index(encoded_letter) - self.position) % 26]

    def encode_backward(self, c):
        # Convert back through rotor (reverse mapping)
        index = (string.ascii_uppercase.index(c) + self.position) % 26
        decoded_index = self.wiring.index(string.ascii_uppercase[index])
        return string.ascii_uppercase[(decoded_index - self.position) % 26]

    def rotate(self):
        # Rotate rotor by one position
        self.position = (self.position + 1) % 26
        # Return True if rotor hits notch (means next rotor rotates)
        return string.ascii_uppercase[self.position] == self.notch


class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, c):
        index = string.ascii_uppercase.index(c)
        return self.wiring[index]


class Plugboard:
    def __init__(self, connections=[]):
        # connections is list of swapped letter pairs e.g. [('A','B'),('C','D')]
        self.mapping = {c: c for c in string.ascii_uppercase}
        for a, b in connections:
            self.mapping[a] = b
            self.mapping[b] = a

    def swap(self, c):
        return self.mapping[c]


class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

    def encode_letter(self, c):
        if c not in string.ascii_uppercase:
            return c  # Non-alphabetic characters are not encoded
        # Step rotors
        rotate_next = self.rotors[0].rotate()
        if rotate_next:
            rotate_next_2 = self.rotors[1].rotate()
            if rotate_next_2:
                self.rotors[2].rotate()

        # Plugboard in
        c = self.plugboard.swap(c)

        # Forward through rotors
        for rotor in self.rotors:
            c = rotor.encode_forward(c)

        # Reflect
        c = self.reflector.reflect(c)

        # Backward through rotors reversed
        for rotor in reversed(self.rotors):
            c = rotor.encode_backward(c)

        # Plugboard out
        c = self.plugboard.swap(c)

        return c

    def encode_message(self, message):
        result = ""
        for c in message.upper():
            result += self.encode_letter(c)
        return result

# Hardcoded example configuration
""" rotor_I = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", notch='Z')
rotor_II = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", notch='E')
rotor_III = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", notch='V')
reflector_B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
plugboard = Plugboard([('A','B'), ('C','D')])

enigma = EnigmaMachine([rotor_I, rotor_II, rotor_III], reflector_B, plugboard)

standard_input = "HELLO WORLD"
input_message = input("Enter message to encode: ")
encoded = enigma.encode_message(input_message)
print("Encoded:", encoded) """

# JSON Configuration loader
def loadkeys(config):
    with open(config, "r") as f:
        keys = json.load(f)
    rotors = [
        Rotor(r["wiring"], r["notch"], r.get("position", 0))
        for r in keys["rotors"]
    ]
    reflector = Reflector(keys["reflector"])
    plugboard = Plugboard(keys.get("plugboard", []))
    return rotors, reflector, plugboard

rotors, reflector, plugboard = loadkeys("config.json")
enigma = EnigmaMachine(rotors, reflector, plugboard)

standard_input = 'HELLO WORLD'
input_message = input("\n\n\nEnter message to encode: \n")

encoded = enigma.encode_message(input_message)
print("\n\n   --- ENCODED ---\n", encoded, "\n\n")