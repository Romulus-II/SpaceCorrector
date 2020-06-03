import pickle
import sys
import os

def main(argv):

    os.chdir('../.')

    file_name = ""
    #print("Performing operation on ", argv[1:])
    print()

    if len(argv)>1:

        file_name = ' '.join(argv[1:])
        input_file_name = './output/' + file_name

    new_stack = pickle.load(open(input_file_name,"rb"))

    print("This is our pickle!!")
    print()

    for i in new_stack:
        print(i.text)

    print()
    print("End of program")
    return


if __name__ == '__main__':
    sys.exit(main(sys.argv))
