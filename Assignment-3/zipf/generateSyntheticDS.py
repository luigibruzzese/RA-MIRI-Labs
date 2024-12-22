import random
import argparse

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

def check_positive_float(value):
    ivalue = float(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive float value" % value)
    return ivalue

parser = argparse.ArgumentParser()
parser.add_argument("--n", help="Number of terms (distinct elements).", type=check_positive, default=10200)
parser.add_argument("--alpha", help="alpha.", type=check_positive_float, default=1)
parser.add_argument("--N", help="Number of tokens N.", type=check_positive, default=135247)

args = parser.parse_args()
N = args.N 
n = args.n 
alpha = args.alpha 

def generateRandomWord():
    length = random.randint(2, 7)
    word = []
    for _ in range(length):
        word.append(chr(random.randint(97,122)))
    return ''.join(word)

if N < n:
    print("Invalid choice: N should be greater or equal than n.")
    exit()


c = 1/sum(i**(-alpha) for i in range(1, n+1))
dictionary = {}
stream = []
# generate n distinct words
for i in range(1, n+1):
    word = generateRandomWord()
    while word in dictionary:
        word = generateRandomWord()
    prob = c/(i**alpha)
    freq = max(1, int(prob*N))
    dictionary[word] = freq
    for _ in range(freq):
        stream.append(word)
random.shuffle(stream)
file = open("zipf_"+str(alpha)+"_"+str(n)+"_"+str(N)+".txt", "w")
for word in stream:
    file.write(word + "\n")
file.close()
file = open("zipf_"+str(alpha)+"_"+str(n)+"_"+str(N)+".dat", "w")
for word, freq in dictionary.items():
    file.write(word + ": " + str(freq) + "\n")
file.close()


