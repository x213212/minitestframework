import os
import sys
import configparser
from configparser import ConfigParser

class validate:
    def __init__(self) -> None:
        pass
    def load_skip(id):
        skip = None
        try:
            get_test_cfg = configparser.ConfigParser()
            get_test_cfg.read("testfolder/"+id+"/"+id+".cfg")
            skip = get_test_cfg.get(str(id),"skip")
            # print(id +":skip="+skip)
        except Exception as ex:
            pass
        return skip
    
    def test_all(key, toolchain, compiler, type_t=None):
        print("==========================")
        print("     Test all Bugzilla    ")
        print("==========================")
        print(key + " " + compiler + ": " + toolchain )
        print("==========================")

        # test all bugzilla
        subfolders = os.listdir("testfolder")
        subfolders.sort(key=lambda x: (os.path.isdir(x), x))
        for id in list(subfolders):
            if os.path.isdir('testfolder/'+id+'/'):
                id = id.split("/")[-1]

                # load skip in config
                skip = None
                try:
                    skip = validate.load_skip(id)
                except Exception as ex:
                    pass
                ori_id = id

                sys.path.append('testfolder/'+id+'/')
                print(id)
                bugzilla = __import__(id)
                eval('bugzilla.'+id)(id,key,toolchain,compiler,ori_id,skip)
                
    def test(ids, key, toolchain, compiler):
        print("==========================")
        print("    Test specified list   ")
        print("==========================")
        print(key + " " + compiler + ": " + toolchain )
        print("--------------------------")
        for id in ids:
            # load skip in config
            skip = None
            try:
                skip = validate.load_skip(id)
            except Exception as ex:
                pass

            try: 
                sys.path.append('testfolder/'+id+'/')
                testcasestruct = __import__(id)
                eval('testcasestruct.'+id)(id,key,toolchain,compiler,id,skip)
            except Exception as ex:
                print(id + ": Excetpion => " + str(ex))