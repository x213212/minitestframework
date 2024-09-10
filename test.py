import subprocess
import crawler
from validate import validate
from report import report
from argparse import ArgumentParser
from time import time
import json
import configparser
import threading
from time import time
from threading import Lock
import os
import concurrent.futures

parser = ArgumentParser()
parser.add_argument("-t", "--test", dest="ids",
                    help="specify a bugzilla id or list", nargs="+")
parser.add_argument("-a", "--version", dest="version",
                    help="specify a toolchain version or list", nargs="+")
parser.add_argument("-toolchain", "--toolchain", dest="tool",
                    help="specify a toolchain path", nargs="+")
parser.add_argument("-component", "--component", dest="type",
                    help="specify a Component at Bugzilla (Tool-Linker/Tool-Compiler/...)", nargs="+")
confiure_file = "test.cfg"
cfg = configparser.ConfigParser()
cfg.read(confiure_file)

def main():
    print("==========================")
    print("Start Test Automation")
    print("==========================")
    args = parser.parse_args()
    start_time = time()
    
    toolchain_path_list = []
    compiler_list = []
    try:
        toolchain_path_list = json.loads(cfg.get("validate","toolchain_path_list"))
        compiler_list = json.loads(cfg.get("validate","compiler_list"))
    except Exception as ex:
        print(ex)
    print(toolchain_path_list)
    print(compiler_list)

    # # set test Component at Bugzilla 
    if (args.type is not None):
        type_t=args.type
    else:
        type_t=None 

    # # setup online status at Bugzilla
    results = []
    futures =[]
    print("Get bug status at Bugzilla, please wait...")
    print("--------------------------")

    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor: 
        if (args.ids is None):
            for get_id in os.listdir("testfolder"):
                if os.path.isdir(f"testfolder/{get_id}"):
                    futures.append(executor.submit(crawler.get_bug_status, get_id, type_t) )    
        else:
            for get_id in (args.ids):
                futures.append(executor.submit(crawler.get_bug_status, get_id,None))
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            # print(result)


    # for key in toolchain_path_list:
    #     toolchain = toolchain_path_list[key]
    #     for compiler in compiler_list:
    #         if (args.ids is None):
    #             # print(key,toolchain, compiler, type_t)
    #             validate.test_all(key, toolchain, compiler, type_t)
    #         else:
    #             # print(args.ids, key, toolchain, compiler)
    #             validate.test(args.ids, key, toolchain, compiler)
    def execute_test(key, toolchain, compiler, type_t, ids=None):
        if ids is None:
            validate.test_all(key, toolchain, compiler, type_t)
        else:
            validate.test(ids, key, toolchain, compiler)
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        futures = []
        for key in toolchain_path_list:
            toolchain = toolchain_path_list[key]
            for compiler in compiler_list:
                if (args.ids is None):
                    futures.append(executor.submit(execute_test, key, toolchain, compiler, type_t, args.ids))

                else:
                    futures.append(executor.submit(execute_test, key, toolchain, compiler, type_t, args.ids))
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)

    # # output to xlsx
    # report = report()
    report().process_xlsx()
    print("==========================")
    print("Total Execution time: ", str(round(time()-start_time,2)) + "s")

if __name__ == '__main__':
    main()