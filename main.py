import sys
import os
import subprocess as sp
import threading as th
import time


class Test:
    def __init__(self):
        pass

    def compile(self, name_file, out_name="a.out"):
        sp.call(["g++", "-std=c++2a", name_file, "-o", out_name])

    def run_all_tests(self, tests_dir):
        for n, file in enumerate(filter(lambda x: not x.endswith(".a"), os.listdir(tests_dir))):
            if not self.run_test(f"{tests_dir}/{file}", f"{tests_dir}/{file}.a"):
                return n
        return True
        
    def run_one_test(self, test_file, ans_file):
        with open(test_file) as inp:
            ans = open(ans_file).read().rstrip()
            output = sp.check_output(["./a.out"], stdin=inp, shell=True).rstrip()
            if output.decode() == ans:
                return True
            return False

    def mem(self, pid): # returns mem in kB
        time_start = time.time()
        col_mem = sp.check_output([f"cat /proc/{pid}/status | grep -i VMSIZE"], shell=True).rstrip()
        return col_mem.decode()[11:-3]

    def for_test(self, test_file, file_name='a.out'): #WORKS!!! ALEXEY LOOK HERE!!!!!
            with open(test_file) as inp:
                tl = False
                proc = sp.Popen([f'./{file_name}'], shell=True, stdin=inp, stdout=sp.PIPE, stderr=sp.PIPE)
                time.sleep(1)
                if proc.poll() is None:
                    tl = True
                    proc.kill()
                output, err = proc.communicate()
                ret = proc.returncode
                return output, ret, err, proc.pid, tl


test = Test()
print(test.mem("23229"))
# print(test.for_test("tests/0", 'a.out'))
# print(test.test("tests"))
# print(test.run_test("tests/0", "tests/0.a"))
# test.compile("main.cpp")
