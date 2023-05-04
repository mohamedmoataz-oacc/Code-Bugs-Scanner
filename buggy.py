# Program to test the scanner we built
# def calculate_grade(grades):
#     output = list()
#     for grade in grades:
#         if grade >= 0 and grade <= 100:
#             if grade <= 59: output.append('F')
#             elif grade <= 69: output.append('D')
#             elif grade <= 79: output.append('C')
#             elif grade <= 89: output.append('B')
#             else: output.append('A')
#     return output
    # print('a bug')

slots = 5
memory = []
frequency = [0] * slots
full = False
hits, faults = 0, 0

def addProcess(process):
    if process in memory:
        hits += 1
        frequency[memory.index(process)] += 1
        return 'Hit'

    faults += 1
    if full:
        # min(frequency) gets the least frequently used process.
        # lfp is the first index of it in the frequency list, so it is similar to using FIFO when 
        # two processes have same frequency. Then we remove the process from the memory.
        lfp = frequency.index(min(frequency))
        memory.pop(lfp)
        frequency.pop(lfp)
        memory.append(process)
        frequency.append(0)
    else:
        memory.append(process)
        if len(memory) == slots: full = True
    frequency[memory.index(process)] += 1
    return 'Fault'


lis = [1,5,3,4,1,2,6,4,1,3,1,3,4,2,6,5,1,5,2,6,3,2]
for i in lis:
    print(addProcess(i), memory, frequency)
print('Faults:', faults)
print('Hits:', hits)