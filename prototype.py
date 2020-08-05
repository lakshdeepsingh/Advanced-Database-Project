#!/usr/bin/env python
#Project Group 30
# Following is the python script to remove duplicate files
#We are using CHecksum to remove duplicate files
import hashlib, os, optparse, sys

#function to calculate md5checksum for a given file
def md5(m):
    #takes one file m as an argument and calculates md5checksum for that file
    md5Hash=hashlib.md5()
    with open(m,'rb') as m:
        for chunk in iter(lambda: m.read(4096),b""):
            md5Hash.update(chunk)
    return md5Hash.hexdigest()

#define our main function:
def remove_duplicate(path, exps):
    #based on the md5 function above to remove duplicate files
    if not os.path.isdir(path): #make sure the given directory exists
        print('specified directory does not exist!')
    else:
        md5_dict={}
        if exps:
            exp_list=exps.split("-")
        else:
            exp_list = []
        print('Working on it...')
        print()
        #the os.walk function allows checking subdirectories too...
        for root, files in os.walk(path): 
            for f in files:
                filePath=os.path.join(root,f)
                md5Hash=md5(filePath)
                size=os.path.getsize(filePath)
                fileComb=str(md5Hash)+str(size)
                if fileComb in md5_dict:
                    md5_dict[fileComb].append(filePath)
                else:
                    md5_dict.update({fileComb:[filePath]})
        ignore_list=[]
        for key in md5_dict:
            for item in md5_dict[key]:
                for p in exp_list:
                    if item.endswith(p):
                        ignore_list.append(item)
                        while md5_dict[key].count(item)>0:
                            md5_dict[key].remove(item)

        print("Done! Following files will be deleted:\n")
        for key in md5_dict:
            for item in md5_dict[key][:-1]:
                print(item)
        if input("\nEnter (y)es to confirm operation or (n)o to abort the operation: ").lower() not in ("y", "yes"):
            sys.exit("Operation cancelled by user. Exiting...")

        print("We are deleting the files...")
        c=0
        for key in md5_dict:
            while len(md5_dict[key])>1:
                for item in md5_dict[key]:
                    os.remove(item)
                    md5_dict[key].remove(item)
                    c += 1
        if len(ignore_list)>0:
            print('Done! Found {} duplicate files, deleted {}, and ignored {} on user\'s request...'.format(c+len(ignore_list),c,len(ignore_list)))
        else:
            print('Done! Found and deleted {} files...'.format(c))

if __name__=='__main__':
    print('*************** Python prototype to remove duplicate files ***************')
    print('*              The script works on the understanding             *')
    print('*             that if 2 files have the same md5checksum          *')
    print('*              they most likely have the same content           *')
    print('**************************************************************************')
    parser = optparse.OptionParser("usage: python %prog -p <target path> -e <file extensions to ignore separated by ->")
    parser.add_option("-p", dest="target_path", type="string", help="provide target path")
    parser.add_option("-e", dest="ext2ignore", type="string", help="(optional) provide file extensions to ignore separated by - eg: -e .py-.doc")
    (options, args) = parser.parse_args()
    p = options.target_path
    e = options.ext2ignore
    #calling the remove duplicate function defined above
    remove_duplicate(p, e) 