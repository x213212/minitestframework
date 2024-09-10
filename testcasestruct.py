import os
import sys
import abc
from vresult_types import vresult_types
from elf import elf

# save the results to json
global final_json_result
final_json_result = {}



class testcasestruct(metaclass=abc.ABCMeta):
    def __init__(self, name, key_t, toolchain_t, compiler_t, ori_id, skip):
        print("init")
        print( name, key_t, toolchain_t, compiler_t, ori_id, skip)
        self.name = name
        self.key_t = key_t
        self.toolchain_t = toolchain_t
        self.toolchain_key = toolchain_t.split('/')[-1]
        self.compiler_t = compiler_t
        self.ori_id = ori_id
        self.skip = skip
        self.test()

    def test(self):
        result = self.validate(elf(self)) 
        tmp_str = f'{self.toolchain_key} {self.compiler_t}'
        if 'ID' not in final_json_result:
            final_json_result['ID'] = []
        if tmp_str not in final_json_result:
            final_json_result[tmp_str] = ['Pending'] * len(final_json_result['ID'])
        if self.ori_id not in final_json_result['ID']:
            final_json_result['ID'].append(self.ori_id)
            for key in final_json_result:
                if key != 'ID':
                    final_json_result[key].append('Pending')
        index = final_json_result['ID'].index(self.ori_id)
        final_json_result[tmp_str][index] = vresult_types.dict[result]