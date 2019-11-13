import pickle
import sys


def main(argv):

    file_name = ""
    #print("Performing operation on ", argv[1:])
    print()

    if len(argv)>1:

        file_name = ' '.join(argv[1:])

    new_stack = pickle.load(open(file_name,"rb"))

    print("This is our pickle!!")
    print()

    for i in new_stack:
        print(i.text)

    print()
    print("End of program")
    return


if __name__ == '__main__':
    sys.exit(main(sys.argv))
