import os
import random


for x in range(500):
    os.mkdir(f'case{x}')
    with open(f'case{x}/'+f'case{x}.cfg','w') as f:
        f.write(
f"""
[case{x}]
cflags = -O3
skip = 
description = case{x}
"""
        )
    with open(f'case{x}/'+f'case{x}.py','w') as f:
    
            f.write(
            f"""
import sys
import random
sys.path.append("../../")
from testcasestruct import testcasestruct
from vresult_types import vresult_types
class case{x}(testcasestruct):
    def validate(self, elf):
        print("hook")
        if(random.random()<0.5):
            return vresult_types.BUGZILLA_PASS
        else:
            return vresult_types.BUGZILLA_FAIL
    """
            )

