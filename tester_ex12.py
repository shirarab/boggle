import copy
import filecmp
import os
import pickle
import random
import re as regex
import sys
import time
import traceback
import warnings
import zipfile
import tempfile
from colorama import init as colorInit, Fore as CF, Style

#import tqdm cautiously:
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    def replacement(iterable):
        print(CF.LIGHTGREEN_EX+'this may take some time',end='')
        for x in iterable:
            print('.',end='')
            yield x
        print('done!'+CF.WHITE)
    tqdm = replacement
    print(CF.LIGHTBLUE_EX+"For you information, the tqdm module has been deactivated because it is not installed on "
                           "you computer. This will only affect the looks of the tester, and not the actual tests."+CF.WHITE)
try:
    from ex12_utils import load_words_dict, is_valid_path, find_length_n_words
except ModuleNotFoundError as e:
    print(CF.LIGHTRED_EX+'Could not load all required methods from your code!')
    raise e

def build_path(startY:int, startX:int, str_moves):
    path = [(startY, startX)]
    prev = path[0]
    for s in str_moves:
        if s == '-':
            del path[-1]
            continue
        diff = MOVES[s]
        pos = prev[0]+diff[0], prev[1]+diff[1]
        prev = pos
        path.append(pos)
    return path

def build_board(board):
    board = [ row.strip().split(' ') for row in board.split('\n') ]
    return board


BOARD1 = build_board("D C B A\n G A D E\n T J Y T\n N M F I")
BOARD2 = build_board("S D S A\n E I I J\n S E D S\n A J A E")
BOARD_CP1 = build_board('C A T Z\nD O G X\nB I T V\nJ J J J')
BOARD_CP2 = build_board('C D B Z\nA O I X\nT G T V\nJ J J J')
BOARD_CP3 = build_board('Q Q Q Q\nB O B Q\nQ Q Q Q\nQ Q Q Q')
BOARD_Q = build_board("Z W F N\n N E E R\n U N QU O\n D I C Y")
BOARD_M = build_board("M E O W\n M E O T\n M E O H\n M E O W")
BOARD_M2 = build_board('G EOW Z E\n M EO O R\n G W W G\nH T ! G ')
test_boards = {'BOARD1' : BOARD1, 'BOARD2' : BOARD2, 'BOARD_CP1' : BOARD_CP1, 'BOARD_CP2':BOARD_CP2, 'BOARD_CP3':BOARD_CP3, 'BOARD_Q':BOARD_Q, 'BOARD_M':BOARD_M, 'BOARD_M2':BOARD_M2}
WORDS_M = {'MEOW':True,'MEOWTH':True, 'MEOWZER':True,'MEOWOW!':True,'MEOWER':True,'MountMeow':True,"MEOWEST":True}
WORDS_CP1 = {'CAT':True, "DOG":True, "BIT":True}


##############################

#######################################
# TODO: fill out all parameters
# TODO: enter files to tests (without '.py' suffix)
filenames = ['ex12_utils', 'boggle']
zip_filename = 'ex12'
ENABLE_ZIP = False
ENABLE_IMPORTS = True
DEF_COUNT_LIMIT = 9
MAX_METHOD_LENGTH = 16
CONST_COUNT_LIMIT = 2

QUICK_DEF_ANALYZE = True
DYNAMIC_IMPORT = False


def analyze_raw_file(lines, filename):
    linestr = '\n'.join(lines)
    # count things:
    const_count = len(set(regex.findall('[A-Z0-9_]+\\s+', linestr)))
    imports = []
    functions = []
    func_lengths = []
    found_main = False
    def_len_counter = 0
    commented: bool = False
    loop = len(lines)
    warning_lst = []
    time.sleep(0.1)
    for i in tqdm(range(loop)):
        line = lines[i].strip()
        if line.count('"""') % 2 == 1 or line.count("'''") % 2 == 1:
            commented = not commented
            continue
        if commented:
            continue
        match = regex.match(IMPORT_REGEX, line)
        if match is not None:
            imports.append(match.groups())
            continue
        match = regex.match(MAIN_REGEX, line)
        if match is not None:
            if found_main:
                warnings.warn(CF.RED + "ERROR - You have to main blocks in your code!")
            found_main = True
            func_lengths.append(def_len_counter)
            def_len_counter = 0
            continue
        if QUICK_DEF_ANALYZE:
            match = regex.match(QUICK_DEF_ANALYZE, line)
        else:
            match = regex.match(DEF_REGEX, line)
        if match is None:  # count line in counter
            should_count = len(line) > 0 and not line.startswith('#')
            def_len_counter += 1 if should_count else 0
            continue
        # if it is a method line:
        def_name = match.group(1)
        def_args = [arg.strip() for arg in match.group(2).split(',')]
        if len(functions) > 0:
            func_lengths.append(def_len_counter)
        functions.append((def_name, def_args))
        def_len_counter = 0
        if not regex.match(DEF_REGEX_pep8, line):
            warning_lst.append(
                CF.YELLOW + "pep8 Warning: method name is probably not pep8 in line " + str(i) + ' : ' + line)
    time.sleep(0.2)
    func_lengths.append(def_len_counter)
    for warning in warning_lst:
        warnings.warn(warning + CF.RED)
    return const_count, functions, func_lengths, imports, found_main


NAME_REGEX = "[a-zA-Z0-9_]+"
ARGS_REGEX = f"{NAME_REGEX}(?:\\s*:\\s*{NAME_REGEX})?(?:\\s*=\\s*{NAME_REGEX})?"
DEF_REGEX = f"def\\s+({NAME_REGEX})\\s*\\(((?:{ARGS_REGEX}\\s*,?\\s*)*)\\s*\\)"
QUICK_DEF_ANALYZE = f"def\\s+({NAME_REGEX})\\s*\\(((?:))"
DEF_REGEX_pep8 = 'def\\s+[a-z0-9_]+\\s*\\('
IMPORT_REGEX = f"(?:from\\s+({NAME_REGEX})\\s+)?import\\s+({NAME_REGEX})\\s*"
MAIN_REGEX = f"if\\s+__name__\\s*==\\s*[\"']__main__[\"']\\s*:"

code_lines_maya = -1
# TODO: edit raw code tests
def test_raw_code(code, *filenames):
    global code_lines_maya
    code_lines_maya = sum( [ len(f) for f in code ] )
    def_count, const_count = 0, 0
    for file_index in range(len(filenames)):
        lines = code[file_index]
        consts, funcs, func_lens, imports, hasMain = analyze_raw_file(lines, filenames[file_index])
        def_count += len(funcs)
        const_count += consts
        # if hasMain:
        #     print(CF.RED + "You used __name__ == '__main__' to run some code, but you should only have functions!")
        #     return False
        for i, func in enumerate(funcs):
            if func_lens[i] > MAX_METHOD_LENGTH:
                print(
                    CF.YELLOW + f"Warning: the method '{func[0]}' seems a bit long. Please make sure it is readable and consider reformatting it.")
    if def_count < DEF_COUNT_LIMIT:
        print(
            CF.YELLOW + "Warning: it seems your code doesn't use enough methods / doesn't use them correctly. please consult with yair/raz - we'll be happy to help :D")
    if const_count < CONST_COUNT_LIMIT:
        print(
            CF.YELLOW + "Warning: it seems your code doesn't use enough constants / doesn't use them correctly. please consult with yair/raz - we'll be happy to help :)")
    return True


# TODO: match actual program to content
def test_main():
    tests = [test_load_words_dict, test_is_valid_path, test_find_length_n_words]  # TODO enter test method list
    passed = 0
    for i, test in enumerate(tests):
        bul = test()
        passed += 1 if bul else 0
        if bul: print(CF.LIGHTMAGENTA_EX + f'You passed the {ordinal(i+1)} test!'+ f' (tests "{test.__name__[5:]}") ')
    if passed < len(tests):
        print(CF.BLUE +
              f"\n\nYou passed {passed} tests out of {len(tests)}. A little work and you'll do much better!")
        return False
    print(CF.GREEN + (f"We'd like to tell you congradulations for passing all {passed} tests,"
                      f"\nbut you first have to read through the weekly instructions:"))
    print(CF.WHITE + '...')
    print(CF.LIGHTCYAN_EX + 'now what?\t' + CF.WHITE)
    str = f"""
0.   Use Ctrl+F to search for the 'print' function in your code, make sure your program won't print anything unwanted!
{CF.CYAN}1.   Make sure your code is as readable as possible!
        Moreover, make sure it's in pep8 and that it answers all python programming conventions
        (such as function_names and CONSTANT_NAMES)
{CF.WHITE}2.   make sure you're code checks variable types and make sure it doesn't import anything that is not installed on the university's computers!
{CF.CYAN}3. try running the file boggle.py and make sure it activates you're program correctly.
{CF.WHITE}4. make sure you can easily and quickly change the time of each game, and that the game works also when you change the boggle_dict.txt file, or the LETTERS constant in boggle_board_randomizer.
{CF.CYAN}5. Don't forget to make sure you entered all the required files into a zip, and that the boggle_dict.txt and boggle_board_randomizer.py files are unchanged.
{CF.WHITE}6.   Upload your code to the moodle page and check to see if their tester found any errors.

{CF.BLUE}You've read through all our note!
{CF.LIGHTMAGENTA_EX}{Style.BRIGHT}Thank You! Congradulations! And Good Luck! 
"""
    print(str)
    time.sleep(40)
    print(f"{CF.RED}P.S. Message from Yair Tidhar: The secret code is '2gL8w'")

# TODO: enter tests:
######################################
from ex12_utils import load_words_dict
from boggle_board_randomizer import randomize_board

def test_load_words_dict():
    tests = [["a",'b','dad','dab'],['meow'],WORDS_M.keys(),['5^$#!23asd'],['123','!@#','***'],[''],['meow', '', 'hello'],['a a','b b'],[],'asdj sdf asj sd asdk fds sd kf sk aksd aksdka skda skd aksd', 'how did you manage to fail this test? this should not be happening!']
    try:
        global WORDS1
        WORDS1 = load_words_dict('boggle_dict.txt')
    except Exception as e:
        print_error('load_words_dict', e, 'boggle_dict.txt', 'The word dictionary')
        sys.exit(0)
    for check in tests:
        content = ''.join([s+'\n' for s in check])
        expected = { e:True for e in check}
        file = open('load_words_test_file.txt',mode='w+')
        file.write(content)
        file.close()
        if not testMethod('load_words_dict',load_words_dict,expected,file.name):
            sys.exit(0)
            return False
    os.remove('load_words_test_file.txt')
    return True
def test_is_valid_path():
    tests = [
        (BOARD1, WORDS1, build_path(0,2,'dz'), 'BAD'),
        (BOARD1, WORDS1, build_path(1,2,'aq'), 'DAD'),
        (BOARD2, WORDS1, build_path(2,0,'dqe'), 'SEED'),
        (BOARD_M, WORDS_M, build_path(0,0,'dce'), 'MEOW'),
        (BOARD_M, WORDS_M, build_path(0, 0, 'dcess'), 'MEOWTH'),
        (BOARD_CP1, WORDS_CP1, build_path(0,0,'dd'), 'CAT'),
        (BOARD_CP1, {'C':True}, build_path(0,0,''), 'C'),
#when word has QU or weird letters:
        (BOARD_Q, WORDS1, build_path(2,2,'waa'), 'QUEEN'),
        (BOARD_Q, WORDS1, build_path(2,0,'dseq'), 'UNIQUE'),
        (BOARD_M2, WORDS_M, build_path(1,0,'e'), 'MEOW'),
        (BOARD_M2, WORDS_M, build_path(1,0,'dc'), 'MEOW'),
        (BOARD_M2, WORDS_M, build_path(1,0,'edds'), 'MEOWZER'),
        (BOARD_M2, WORDS_M, build_path(1,0,'dcwzc'), 'MEOWOW!'),
    #when path is out of bounds cases:
        (BOARD2, WORDS1, build_path(0,-1,'dccc'), False),
        (BOARD2, WORDS1, build_path(0,0,'dcccc'), False),
        (BOARD2, WORDS1, build_path(-1,2,'sssc'), False),
        (BOARD2, WORDS1, build_path(3, 4,'qqqz'), False),
        (BOARD2, WORDS1, build_path(0,3,'asqzz'), False),
        (BOARD_CP1, WORDS_CP1, build_path(0,0,'dddd'), False),
        (BOARD_CP1, WORDS_CP1, build_path(0,4,'aa'), False),
#when path steps in same spot twice:
        (BOARD1, WORDS1, build_path(1,2,'ad'), False),
        (BOARD2, WORDS1, build_path(0,1,'sw'), False),
        (BOARD2, WORDS1, build_path(2,0,'d0d'), False),
        (BOARD_CP1, WORDS_CP1, build_path(0,0,'da'), False),
#when path is invalid:
        (BOARD_M, WORDS_M, build_path(0,0,'dc-sd'), False),
        (BOARD1, WORDS1, build_path(0,2,'da-a-a'), False),
        (BOARD_CP1, WORDS_CP1, build_path(0,0,'dd-s-s'), False),
#when word is not in dictionary:
        (BOARD_M, WORDS1, build_path(0, 0, 'dcess'), False),
        (BOARD1, WORDS_M, build_path(0, 2, 'dz'), False),
        (BOARD_CP1, WORDS_CP1, build_path(0,0,'d'), False),
        (BOARD_CP1, WORDS_CP1, build_path(0,0,'ddd'), False),
        (BOARD_CP1, WORDS_CP1, build_path(0,0,''), False),
        (BOARD_CP1, WORDS_CP1, [], False)#empty path
    ]
    time.sleep(0.1)
    for test in tqdm(tests):
        args = (test[0], test[2], test[1])
        expected = None if test[3] is False else test[3]
        if not testMethod('is_valid_path',is_valid_path,expected,args):
            return False
    return True

def test_find_length_n_words():
    print(CF.LIGHTGREEN_EX+'The 3rd test takes some time. please kindly wait :)'+CF.WHITE)
    ANS_PATH_N_WORD, ANS_PATH_N_PATH = 'tester directory\\testerEx12File-nW', 'tester directory\\testerEx12File-nP'
    isWordLength : bool = False
    try:
        got = find_length_n_words(3, BOARD_M2, WORDS_M)
        isWordLength = len(got)==0
        print(CF.LIGHTCYAN_EX+f"Detected that the function 'find_length_n_words' treats n as length of {'words' if isWordLength else 'path'}.\n The function will be tested accordingly, Please make sure this is the way the function is expected to act.")
    except:pass
    TEST_ANSWERS_PATH = ANS_PATH_N_WORD if isWordLength else ANS_PATH_N_PATH
    tests = [
        (BOARD1, WORDS_M, 3),
        (BOARD1, WORDS_M, 4),
        (BOARD_M, WORDS_M, 3),
        (BOARD_M, WORDS_M, 4),
        (BOARD_M, WORDS_M, 5),
        (BOARD_M, WORDS_M, 6),
        (BOARD_M, WORDS_M, 7),
        (BOARD_M2, WORDS_M, 3),
        (BOARD_M2, WORDS_M, 4),
        (BOARD_M2, WORDS_M, 5),
        (BOARD_M2, WORDS_M, 7),
        (BOARD_M2, WORDS_M, 8),
        (BOARD_M2, WORDS1, 6),
        (BOARD1, WORDS1, 3),
        (BOARD1, WORDS1, 4),
        (BOARD1, WORDS1, 5),
        (BOARD1, WORDS1, 6),
        (BOARD1, WORDS1, 7),
        (BOARD1, WORDS1, 10),
        (BOARD2, WORDS1, 9),
        (BOARD2, WORDS1, 3),
        (BOARD2, WORDS1, 4),
        (BOARD2, WORDS1, 5),
        (BOARD2, WORDS1, 6),
        (BOARD_Q, WORDS1, 3),
        (BOARD_Q, WORDS1, 5),
        (BOARD_Q, WORDS1, 6),
        (BOARD_CP1, WORDS_CP1, 3),
        (BOARD_CP1, WORDS_CP1, 4),
        (BOARD_CP1, WORDS_CP1, 5),
        (BOARD_CP2, WORDS_CP1, 3),
        (BOARD_CP3, WORDS1, 3),
    ]
    with open(TEST_ANSWERS_PATH, 'r') as f:
        test_answers = f.readlines()
    for i in tqdm(range(len(tests))):
        test, ans = tests[i], test_answers[i*2].strip()
        board, words, n = test[0],test[1],test[2]
        expected = read_ans_from_line(ans)
        if not testMethod('find_length_n_words', find_length_n_words, expected, (n, board, words), check_sorted=True ):
            return False
    return True

    # from hidden_tester_helper import mark_n_words_ans
    # file_w = open(ANS_PATH_N_WORD,'w')
    # file_p = open(ANS_PATH_N_PATH,'w')
    # for test in tqdm(tests):
    #     xw = mark_n_words_ans(test[0], test[1], test[2], isWordLength=True)
    #     xp = mark_n_words_ans(test[0], test[1], test[2], isWordLength=False)
    #     file_w.write(xw+'\n\n');file_p.write(xp+'\n\n')
    # file_w.close();file_p.close()

def read_ans_from_line(line:str):
    elements = line.strip().split('@')
    ans = []
    for elem in elements:
        proc = elem.strip().split(':')
        if len(proc)<=1: continue
        word, path = proc
        path = [ (int(path[i]), int(path[i+1])) for i in range(0,len(path),2) ]
        ans.append( (word, path) )
    return ans;

########################################TODO: enter useful methods:





MOVES = {'0':(0,0),'q':(-1,-1),'w':(-1,0),'e':(-1,1),'a':(0,-1),'s':(1,0),'d':(0,1),'z':(1,-1),'c':(1,1)}
#################################################
#TODO: enter special __eq__s
def equate(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is list or type(a) is tuple:
        if len(a) != len(b):
            return False
        for i in range(len(a)):
            if not equate(a[i], b[i]):
                return False
        return True
    return a == b

######YOU_DONT_HAVE_ANY_THING_TO_DO_BELOW_THIS_LINE###########

def ordinal(num: int) -> str:
    num = str(int(num))
    if num[-1] == '1':
        return f'{num}st'
    if num[-1] == '2':
        return f'{num}nd'
    if num[-1] == '3':
        return f'{num}rd'
    return f'{num}th'


def randomD(minval, maxval):
    return random.random() * (maxval - minval) + minval


def list_has_duplicates(lst):
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] == lst[j]:
                return True
    return False


def unordered_lists_equal(lstA, lstB):
    for i in lstA:
        if i not in lstB:
            return False
    for i in lstB:
        if i not in lstA:
            return False
    return True


def generate_vec(dim):
    vec = []
    for i in range(dim):
        vec.append(randomD(-50, 50))
    return vec
##########################################
def repr_obj(obj, title=True):
    #TODO: enter special __str__ of objs.
    if obj is WORDS1: return '{the boggle_dict.txt words dictionary}'
    if obj is WORDS_M and title: return repr_obj(obj,False)+'\nNOTE: you can import the variable WORDS_M from the the tester file for testing :)'
    if obj is WORDS_CP1 and title: return repr_obj(obj, False)+'\nNOTE: you can import the variable WORDS_CP1 from the the tester file for testing :)'
    if type(obj) is list and len(obj) > 0:
        if title:
            for bb in test_boards:
                if obj == test_boards[bb]: return repr_obj(obj, False)+f"NOTE: you can import the variable {bb} from the tester file for testing :)\n"
        if type(obj[0]) is list:
            ss = 'The board:\n' if title else ''
            for line in obj:
                s = repr_obj(line)+'\n'
                ss+=s
            return ss
        if type(obj[0]) is tuple and title:
            return 'The path:'+repr_obj(obj, title=False)
    if type(obj) == list: return '[' + ', '.join([repr_obj(e) for e in obj]) + ']'
    return str(obj)


def input_str(tup):
    if len(tup) == 0:
        return 'No Input'
    return ', '.join([repr_obj(elem) for elem in tup])


def print_error(method_name, error, arguments, expected, object):
    err = f"{CF.RED}{Style.BRIGHT}An error occurred while running the function {method_name}:\n" \
          f"{Style.NORMAL}Error: {error.__class__.__name__}\n" \
          f"Input:{CF.WHITE}{input_str(arguments)}{CF.RED}\n"  \
          f"Expected: {CF.WHITE}{repr_obj(expected)}{CF.RED}\n" \
          f"Object: {CF.WHITE}{repr_obj(object)}"
    print(CF.RED + err, '\n')
    print(CF.YELLOW + "Error data is specified below:")
    time.sleep(0.01)
    traceback.print_exc()


def print_fail(method_name, args, expected, actual, object, issue=None, exp_note=''):
    if type(exp_note) is not str:
        exp_note = str(exp_note) + '\n'
    elif len(exp_note) > 0 and not exp_note.endswith('\n'):
        exp_note += '\n'
    err = Style.BRIGHT + f"{CF.RED}The function {method_name} did not return expectedly:\n" \
                         f"{Style.NORMAL}Input: {CF.WHITE}{input_str(args)}{CF.RED}\n" \
                         f"Expected: {CF.WHITE}{repr_obj(expected)}{CF.RED}\n" \
                         f"{exp_note}" \
                         f"Returned Value: {CF.WHITE}{repr_obj(actual)}{CF.RED}\n"
    if issue is not None:
        err += f"Issue: {CF.WHITE}{issue}{CF.RED}\n"
    if object is not None:
        err += f"Object: {CF.WHITE}{repr_obj(object)}\n"
    print(CF.RED + err, '\n')


def print_prob(method_name, args, expected, actual, object, problem):
    err = f"{CF.RED}{Style.BRIGHT}The function {method_name} did not act expectedly:\n" \
          f"{Style.NORMAL}Input: {input_str(args)}\n" \
          f"Expected: {repr_obj(expected)}\n" \
          f"Actual: {repr_obj(actual)}\n" \
          f"The problem: {problem}\n" \
          f"Object: {repr_obj(object)}"
    print(err, '\n')

def measure_time(func):
    start = time()
    output = func()
    end = time()
    return end-start, output

def matchFileContent_predicate(fileA, fileB):
    return filecmp.cmp(fileA, fileB)


def testMethod_err(func_name, check_func, err_type, args, obj=None):
    if type(args) != tuple:
        args = (args,)
    act_args = copy.deepcopy(args)
    try:
        val = check_func(*act_args)
    except Exception as e:
        if type(e) is err_type:
            return True
        print_fail(func_name, args, f"Error of type {err_type}", f"Error of type {type(e)}", obj)
        time.sleep(0.01)
        print(CF.LIGHTCYAN_EX + 'The Error details are specified below for you comfort:')
        time.sleep(0.01)
        traceback.print_exc()
        return False
    print_prob(func_name, args, f"Error of type {err_type}", f"Returned {val}", obj,
               problem="Didn't raise error when should have.")


def testMethod_options(func_name, check_func, expected_options, args, obj=None, check_sorted=False,
                       mutableArgCheck=True, mutableObjCheck=True):
    expected_msg = f'One of the {len(expected_options)} following options:\n' + '\nor '.join(
        [repr_obj(opt) for opt in expected_options])

    def predicate(val, act_args, org_args, obj):
        ok_types = {type(expected) for expected in expected_options}
        if type(val) not in ok_types:
            expected_types_str = ' or '.join([t.__name__ for t in ok_types])
            print(
                CF.LIGHTRED_EX + Style.BRIGHT + f'NOTE: YOU RETURNED A VALUE OF TYPE "{type(val).__name__}". ARE YOU SURE YOU SHOULD RETURN A VALUE OF THAT TYPE? (AND NOT {expected_types_str})  :' + Style.NORMAL)
            return False
        for expected in expected_options:
            if type(val) != type(expected):
                return False
            if check_sorted and sorted(val) == sorted(expected): return True
            if equate(val, expected): return True
        return False

    testMethod_predicate(func_name, check_func, predicate, expected_msg, args, obj, mutableArgCheck, mutableObjCheck)


def testMethod(func_name, check_func, expected, args, obj=None, check_sorted=False, mutableArgCheck=True,
               mutableObjCheck=True):
    expected_msg = expected

    def predicate(val, actual_args, original_args, obj):
        if type(val) != type(expected):
            print(
                CF.LIGHTRED_EX + Style.BRIGHT + f'NOTE: YOU RETURNED A VALUE OF TYPE "{type(val).__name__}". ARE YOU SURE YOU SHOULD RETURN A VALUE OF THAT TYPE? (AND NOT {type(expected).__name__})  :' + Style.NORMAL)
            return False
        if check_sorted: return sorted(val) == sorted(expected)
        return equate(val, expected)

    return testMethod_predicate(func_name, check_func, predicate, expected_msg, args, obj, mutableArgCheck,
                                mutableObjCheck)


def testMethod_arg(func_name, check_func, expected, args, arg_to_check: int, obj, check_sorted=False,
                   mutableArgCheck=True, mutableObjCheck=True):
    expected_msg = expected

    def predicate(val, actual_args, original_args, obj):
        if check_sorted: return sorted(actual_args[arg_to_check]) == sorted(expected)
        return equate(actual_args[arg_to_check], expected)

    return testMethod_predicate(func_name, check_func, predicate, expected_msg, args, obj, mutableArgCheck,
                                mutableObjCheck)


def testMethod_mutableObj(func_name, check_func, expected, args, obj, mutableArgCheck=True):
    expected_msg = expected
    def predicate(val, actual_args, original_args, obj):
        return equate(expected, obj)
    exp_note = f'Note: before the method was called, the object was: {repr_obj(obj)}'
    return testMethod_predicate(func_name, check_func, predicate, expected_msg, args, obj, mutableArgCheck,
                                mutableObjCheck=False,exp_note=exp_note)


def testMethod_predicate(func_name, check_func, predicate, expected_msg, args, obj=None, mutableArgCheck=True,
                         mutableObjCheck=True, exp_note=''):
    if type(args) != tuple:
        args = (args,)
    actual_args = copy.deepcopy(args)
    actual_obj = copy.deepcopy(obj)
    try:
        val = check_func(*actual_args)
    except Exception as e:
        print_error(func_name, e, args, expected_msg, obj)
        return False
    if not predicate(val, actual_args, args, obj):
        print_fail(func_name, args, expected_msg, val, obj, exp_note=exp_note)
        return False
    if mutableArgCheck and pickle.dumps(args) != pickle.dumps(actual_args):
        print_prob(func_name, args, expected_msg, val, obj,
                   "The function changed the value of some mutable arguments, this is not allowed!")
        return False
    if obj is not None and mutableObjCheck and not pickle.dumps(obj) == pickle.dumps(actual_obj):
        print_prob(func_name, args, expected_msg, val, obj,
                   f"The function changed the value of fields of the object, this is not allowed!\nOriginal object's state:\n {repr_obj(obj)}")
        return False
    return True


####################################
def read_code_array2D(*filenames):
    code = []
    for filename in filenames:
        file = open(filename + ".py")
        lines = file.readlines()
        code.append(lines)
        file.close()
    return code


def read_code_array2D_from_zip(zipfilename, *filenames):
    code = []
    archive = zipfile.ZipFile(zipfilename + ".zip")
    for filename in filenames:
        file = archive.open(filename + ".py")
        lines = file.readlines()
        code.append(lines)
        file.close()
    return code


def import_files_dynamically(*filenames):
    import_cmds = ['from ' + fname + ' import *' for fname in filenames]
    import_cmds = '\n'.join(import_cmds)
    exec(import_cmds, globals())


class CWDLoader:
    def __init__(self):
        self.newPath = os.path.dirname(os.path.abspath(__file__))

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def main():
    try:
        colorInit()
        with CWDLoader():
            should_test_zip = input('type a number if you wish this program to read from a zip file:')
            should_test_zip = regex.match('\s*\d', should_test_zip)
            if should_test_zip:

                if not ENABLE_ZIP:
                    print("\nSorry but this week's tester doesn't support zip checks.")
                    print('Please run this tester on a python file, Thank you :) \n')
                    sys.exit(0)
                print('loading files from zip: ' + zip_filename + ".zip")
                sys.path.insert(0, zip_filename + ".zip")
                code = read_code_array2D_from_zip(zip_filename, *filenames)
            else:
                print('loading files:', *[fn + '.py' for fn in filenames])
                code = read_code_array2D(*filenames)
            if DYNAMIC_IMPORT: import_files_dynamically(*filenames)
            print(CF.CYAN + 'files loaded. now running tests...\n')
            res = test_raw_code(copy.deepcopy(code), filenames)
            if res is False:
                sys.exit(0)
            print(CF.WHITE + 'finished basic formatting test')

            print(' ')
            test_main()
            print(CF.RESET)
    except OSError as ose:
        d = os.path.dirname(os.path.abspath(__file__))
        print(CF.MAGENTA + 'could not find/load required files from folder:', d)
        raise ose
    except Exception:
        print(CF.MAGENTA + "the tester has thrown an error. please report to yair =) ")
        raise
    finally:
        time.sleep(0.1)
        input(CF.WHITE + "\nType enter when you are finished:")

if __name__ == '__main__':
    main()
