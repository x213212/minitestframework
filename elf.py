import os
import subprocess
class elf():
    def __init__(self,getstruct) -> None:
        print("elf class")
        # self.toolchain_t = toolchain_t
        # self.toolchain_key = toolchain_t.split('/')[-1]
        # self.compiler_t = compiler_t
        print(getstruct.toolchain_t+"/"+getstruct.compiler_t)
        get_compiler_path = getstruct.toolchain_t+"/"+getstruct.compiler_t
        print("call fake compiler:")
        result = subprocess.run([get_compiler_path], capture_output=True, text=True)
        print("Output:", result.stdout)
        print("Error:", result.stderr)
        pass
    def get_true (self):
        return True
    def get_false (self):
        return False
