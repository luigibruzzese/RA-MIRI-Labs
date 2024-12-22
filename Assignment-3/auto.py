import os

datasets = ["crusoe.txt", "dracula.txt", "iliad.txt", "mare-balena.txt", "midsummer-nights-dream.txt", "quijote.txt", "valley-fear.txt", "war-peace.txt"]

for data in datasets:
    print("------------- DATASET: " + data)
    for algorithm in ["HLL", "REC", "LL", "AS"]:
        for param in [4, 8, 16, 32, 64, 128, 256, 512]:
            os.system("python3 assignment3.py --data datasets/" + data + " --alg " + algorithm + " --param " + str(param) + " --T 300 >> datasets/output/" + data.split(".")[0] + "Output.txt")
            print("-- Configuration " + algorithm + str(param) + " done.")
