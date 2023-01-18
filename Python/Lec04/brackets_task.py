def isBalanced(n, x):
    first, second, third = ["{", "}"], ["[", "]"], ["(", ")"]
    l= len(x)- 1
    half = int(l / 2)
    counter = 0
    #Looping over the input characters
    for i in range (half+1):
        #Condition to check if the bairs of brackets meets the criteria
        if x[i] in first and x[l] in first:
            counter += 1
        elif x[i] in second and x[l] in second:
            counter += 1
        elif x[i] in third and x[l] in third:
            counter += 1
        else:
            break
        l -= 1

    # Outputing condition
    if counter == len(x)/2:
        return "YES"
    else:
        return "NO"

listt =[]
#inputing and storing the output in listt
n = int(input())
for i in range (n):
    x= input()
    listt.append(isBalanced(n,x))
#used this to output in the desired format each output in seperate line
print(*listt,sep='\n')