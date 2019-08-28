import sys
import os
import subprocess as sp


class Test:
    def compile(self, name_file, out_name="a.out"):
        subprocess.call(["g++", "-std=c++2a", name_file, "-o", out_name])

    def test(self, tests_dir):
        for n, file in enumerate(filter(lambda x: not x.endswith(".a"), os.listdir(tests_dir))):
            if not self.run_test(f"{tests_dir}/{file}", f"{tests_dir}/{file}.a"):
                return n
        return True

    def run_test(self, test_file, ans_file):
        with open(test_file) as inp:
            ans = open(ans_file).read().rstrip()
            output = sp.check_output(["./a.out"], stdin=inp, shell=True).rstrip()
            if output.decode() == ans:
                return True
            return False

    def for_test(self, test_file, file_name='a.out'): #WORKS!!! ALEXEY LOOK HERE!!!!!
        with open(test_file) as inp:
            proc = sp.Popen([f'./{file_name}'], shell=True, stdin=inp, stdout=sp.PIPE, stderr=sp.PIPE)
            output, err = proc.communicate()
            ret = proc.returncode
            return output, ret, err, proc.pid


test = Test()
print(test.for_test("tests/0", 'a.out'))
# print(test.test("tests"))
# print(test.run_test("tests/0", "tests/0.a"))
# test.compile("main.cpp")
