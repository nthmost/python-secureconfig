from __future__ import print_function

import os

from secureconfig import SecureConfig

# here we're going to open the file we encrypted in the previous demo
# and make sure we can decrypt and parse it using the same keystring.


CWD = os.path.dirname(os.path.realpath(__file__))
output_path = os.path.join(CWD, 'demo_secureconfig_data.enc')
TEST_KEYSTRING = 'sFbO-GbipIFIpj64S2_AZBIPBvX80Yozszw7PR2dVFg='

thing = SecureConfig.from_key(TEST_KEYSTRING, filepath=output_path)

print("In our last episode, we created an encrypted serialized dictionary using SecureConfig.")
print("Now we're going to use the same key to decrypt and read the data back.")
print()

print("What's in this file? Use .sections() to see top-level dictionary data.")
print(thing.sections())
print()

print("So, who is in the family? Use .options('family') and .get('family', member) to see. ")

for member in thing.options('family'):
    print(  member + ": " + thing.get('family', member))

