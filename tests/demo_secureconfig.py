from __future__ import print_function

import os

from secureconfig import SecureConfig

CWD = os.path.dirname(os.path.realpath(__file__))
TEST_KEYSTRING = 'sFbO-GbipIFIpj64S2_AZBIPBvX80Yozszw7PR2dVFg='

thing = SecureConfig.from_key(TEST_KEYSTRING)

print("Start with an blank slate: ")
print(thing.cfg)
print()

print("Add a section with add_section: ")
thing.add_section('family')
print(thing.cfg)
print()

print("Stick some values in it: ")
thing.set('family', 'grandma', 'Kay')
thing.set('family', 'granddad', 'John')
print(thing.cfg)
print()

print("Now let's write it to disk.")
filename_input = input ("Input a location where you can create a new file: ")
thing.write(filename_input)
print()



