import sys
import os
import subprocess as sp
import threading as th
import time


class Test:
    def __init__(self):
        self.tl_time = 1  # time in sec
        self.ml_memory = 16 * 1024  # in kB 

    def compile(self, name_file, out_name="a.out"):
        sp.call(["g++", "-std=c++2a", name_file, "-o", out_name])

    def run_all_tests(self, tests_dir, file_name="a.out"):
        for n, file in enumerate(sorted(filter(lambda x: not x.endswith(".a"), os.listdir(tests_dir)), key=lambda x: int(x))):
            status = self.run_one_test(f"{tests_dir}/{file}", f"{tests_dir}/{file}.a", file_name)
            if status:
                return status, n
        return True

    def mem(self, pid): # returns mem in kB
        try:
            col_mem = sp.check_output([f"cat /proc/{pid}/status | grep -i VMSIZE"], shell=True).rstrip()
            return int(col_mem.decode()[11:-3])
        except BaseException:
            return 0  # todo: refactor it

    def get_ans(self, ans_file):
        with open(ans_file, 'r') as content_file:
            return content_file.read().rstrip()

    def run_one_test(self, test_file, ans_file, file_name): # returns False if tests works else Name of error
            with open(test_file) as inp:
                tl = False
                ml = False
                proc = sp.Popen([f'exec ./{file_name}'], shell=True, stdin=inp, stdout=sp.PIPE, stderr=sp.PIPE)
                time_start = time.time()
                while True:
                    if proc.poll() is None and time.time() - time_start >= self.tl_time:
                        tl = True
                        proc.kill()
                        break
                    
                    elif self.mem(proc.pid) >= self.ml_memory:
                        ml = True
                        proc.kill()
                        break

                    elif proc.poll() is not None:
                        break

                if tl:
                    return "TL"
                if ml:
                    return "ML"
                output, err = proc.communicate()
                ret = proc.returncode
                # print([output.decode().rstrip(), self.get_ans(ans_file)])
                if output.decode().rstrip() == self.get_ans(ans_file):
                    return False  # if all ok return false :) NICE )) 
                return "WA"


test = Test()
# print([test.get_ans('tests/0.a')])
# print(test.mem("23229"))
# print(test.run_one_test("tests/0", 'tests/0.a', 'a.out'))
print(test.run_all_tests("tests"))
# print(test.run_test("tests/0", "tests/0.a"))
# test.compile("main.cpp")