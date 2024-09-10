import os
import sys

class vresult_types:
    BUGZILLA_PASS = 1
    BUGZILLA_FAIL = 0
    BUGZILLA_BUILD_ERROR = -1
    BUGZILLA_PENDING = -2
    dict = {BUGZILLA_PASS: 'Pass', BUGZILLA_FAIL: 'Fail',
            BUGZILLA_BUILD_ERROR: 'Error', BUGZILLA_PENDING: 'Pending'}