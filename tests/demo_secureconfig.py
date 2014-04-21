from __future__ import print_function

import os

from secureconfig import SecureConfig

CWD = os.path.dirname(os.path.realpath(__file__))
output_path = os.path.join(CWD, 'demo_secureconfig_data.enc')
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

print("Now let's write it to disk (%s)" % output_path)
fh = open(output_path, 'w')
thing.write(fh)
fh.close()
print('...done. \n')

print("Continue with demo_secureconfig_2.py !")

