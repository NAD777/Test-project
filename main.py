import os
import subprocess as sp
import time


class Test:
    def __init__(self, tl_time, ml_memory):
        self.tl_time = tl_time  # time in sec
        self.ml_memory = ml_memory * 1024  # in kB

    def create_file(self, text, output_file_name):
        with open(output_file_name, 'w') as inp:
            print(text)
            inp.write(text)
            inp.close()

    def delete_file(self, path):
        os.remove(path)

    def compile_С(self, name_file, out_name="a.out"):
        proc = sp.Popen(["g++", "-std=c++17", name_file, "-o", out_name],
                        stdout=sp.PIPE, stderr=sp.PIPE)
        output, err = proc.communicate()
        if output == b'' and err == b'':
            return True
        else:
            return False

    def compile_pas(self, name_file, out_name="a"):
        proc = sp.Popen(['fpc', "-TLINUX", name_file, f'-o{out_name}'],
                        stdout=sp.PIPE, stderr=sp.PIPE)
        output, err = proc.communicate()
        print(output, err)
        if (err == b'' or
            err == b'/usr/bin/ld.bfd: warning: programms/link.res contains output sections;'
                   b' did you forget -T?\n') and 'compiled' in output.decode():
            return True
        else:
            return False

    def run_all_tests(self, tests_dir, file_name="a.out"):
        for n, file in enumerate(sorted(filter(lambda x: not x.endswith(".a"),
                                               os.listdir(tests_dir)), key=lambda x: int(x))):
            status = self.run_one_test(f"{tests_dir}/{file}", f"{tests_dir}/{file}.a", file_name)
            if status:
                return status, n
        return False

    def mem(self, pid):  # returns mem in kB
        try:
            col_mem = sp.check_output([f"cat /proc/{pid}/status | grep -i VMSIZE"],
                                      shell=True).rstrip()
            return int(col_mem.decode()[11:-3])
        except BaseException:
            return 0  # todo: refactor it

    def get_ans(self, ans_file):
        with open(ans_file, 'r') as content_file:
            return content_file.read().rstrip()

    def run_one_test(self, test_file, ans_file, file_name):
        with open(test_file) as inp:
            tl = False
            ml = False
            proc = sp.Popen([f'exec ./{file_name}'], shell=True,
                            stdin=inp, stdout=sp.PIPE, stderr=sp.PIPE)
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
            if ret != 0:
                return "RE"
            print([output.decode().rstrip(), self.get_ans(ans_file)])
            if output.decode().rstrip() == self.get_ans(ans_file):
                return False  # if all ok return false :) NICE ))
            return "WA"


if __name__ == "__main__":
    test = Test(1, 16)
    # test.create_file("""#include <iostream>
    # using namespace std;
    # int main(){
    #     int a, b;
    #     cin >> a >> b;
    #     cout << a + b;
    #     return 0;
    #     }""", "text.cpp")
    # start_time = time.time()
    # print(test.compile_pas("source/36.pas"))
    # print(test.run_all_tests("tests", "out"))
    # print(time.time() - start_time)
    # print([test.get_ans('tests/0.a')])
    # print(test.mem("23229"))
    # print(test.run_one_test("tests/0", 'tests/0.a', 'a.out'))
    # print(test.run_all_tests("tests"))
    # print(test.run_test("tests/0", "tests/0.a"))
    # test.compile("main.cpp")
