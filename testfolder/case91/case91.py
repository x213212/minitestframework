
import sys
import random
sys.path.append("../../")
from testcasestruct import testcasestruct
from vresult_types import vresult_types
class case91(testcasestruct):
    def validate(self, elf):
        print("hook")
        if(random.random()<0.5):
            return vresult_types.BUGZILLA_PASS
        else:
            return vresult_types.BUGZILLA_FAIL
    