from Tkinter import *
import numpy as np
import time

fields = 'C_transpose:', 'A:', 'B:'


def optimize(tableau, no_of_variables):
    variables = np.zeros(no_of_variables)  # array to store the values of the variables
    print '\nInitial Tableau = \n', tableau
    print 'Values of the variables = ', variables
    print 'Optimization function value = ', tableau[-1, -1]
    (a, b) = tableau.shape
    count = 1
    array = -1 * np.ones(no_of_variables)
    while 1:
        col_min = min(tableau[-1, :])
        col_index = [idx for idx, val in enumerate(tableau[-1, :]) if val == col_min]
        col_index = col_index[0]

        # check if the solution is unbounded
        if (all(tableau[i, col_index] <= 0 for i in range(0, a)) == 1):
            print 'Solution is Unbounded!'
            break

            # pivoting
        if (col_min < 0):
            print '\nIteration = ', count
            print 'Minimum column value = ', col_min
            ratio = tableau[:, -1] / tableau[:, col_index]
            print 'Ratio = ', ratio[0:-1]
            min_ratio = min([n for n in ratio[0:-1] if n >= 0])
            row_index = [idx for idx, val in enumerate(ratio[0:-1]) if val == min_ratio]
            row_index = row_index[0]
            print 'Minimum ratio = ', min_ratio
            pivot = tableau[row_index, col_index]
            print 'Pivot = ', pivot
            new_pivot_row = tableau[row_index, :] / pivot
            for i in range(0, a):
                if (i != row_index):
                    multiplier = tableau[i, col_index]
                    for j in range(0, b):
                        tableau[i, j] = tableau[i, j] - (multiplier * new_pivot_row[j])
            tableau[row_index, :] = new_pivot_row
            print 'Tableau =\n', tableau

            # storing the values of the variables
            if (col_index < no_of_variables):
                array[col_index] = row_index
            for i in range(0, no_of_variables):
                if (array[i] != (-1)):
                    variables[i] = tableau[array[i], -1]
            print 'Values of the variables = ', variables
            print 'Optimization function value = ', tableau[-1, -1]
        else:
            break
        count = count + 1
    return (tableau[-1, -1], variables)


# function to make the initial tableau
def make_tableau(C_transpose, A, B):
    (C_transpose_r, C_transpose_c) = C_transpose.shape
    (A_r, A_c) = A.shape
    I = np.identity(A_r)
    tableau = np.concatenate((A, I), axis=1)
    tableau = np.concatenate((tableau, B), axis=1)
    (tableau_r, tableau_c) = tableau.shape
    last_row = np.lib.pad(C_transpose, (0, (tableau_c - C_transpose_c)), 'constant', constant_values=0)
    last_row = last_row[0, :]
    tableau = np.vstack((tableau, last_row))
    return (tableau, A_c)


def start(C_transpose, A, B):
    start = time.time()
    (tableau, no_of_variables) = make_tableau(-1 * C_transpose, A, B)
    (value, variables) = optimize(tableau, no_of_variables)
    stop = time.time()
    print 'Execution time = ', (stop - start), 'sec'
    return (value, variables)


def fetch(entries):
    try:
        for entry in entries:
            print 'entry = ', entry
            field = entry[0]
            text = entry[1].get()
            print('%s: "%s"' % (field, text))
            mylist = text.split(',')
            print mylist
            floatlist = []
            r = int(float(mylist[0]));
            del mylist[0];
            c = int(float(mylist[0]));
            del mylist[0]
            print r, c
            for i in range(0, len(mylist)):
                floatlist.append(float(mylist[i]))
            if (field == 'C_transpose:'):
                C_r = r;
                C_c = c
                C = np.array(floatlist)
            elif (field == 'A:'):
                A_r = r;
                A_c = c
                A = np.array(floatlist)
            else:
                B_r = r;
                B_c = c
                B = np.array(floatlist)
    except:
        master = Tk()
        master.geometry('500x200')
        master.configure(background='white')
        master.title("Error Message")
        w = Message(master, text="Please enter valid numbers separated by commas",
                    bg="white", fg="black", font=(None, 20))
        w.pack()

    if ((C_r != 1) | (B_c != 1) | (C_c != A_c) | (A_r != B_r) | (C_r * C_c != len(C)) | (A_r * A_c != len(A)) | (
            B_r * B_c != len(B))):
        master = Tk()
        master.geometry('500x200')
        master.configure(background='white')
        master.title("Error Message")
        w = Message(master, text="Matrix Dimensions are inconsistent",
                    bg="white", fg="black", font=(None, 20))
        w.pack()
    else:
        C = np.reshape(C, (C_r, C_c))
        A = np.reshape(A, (A_r, A_c))
        B = np.reshape(B, (B_r, B_c))
        (value, variables) = start(C, A, B)
        root = Tk()
        root.title("Result")
        root.geometry('1200x800')
        root.configure(background='white')
        label_one = Label(root, text='The optimum variable values are:',
                          bg="white", fg="black", font=(None, 40), height=2, width=500)
        label_two = Label(root, text=variables, bg="white", fg="blue", font=(None, 50), height=3, width=500)
        label_three = Label(root, text='The maximum value possible is:',
                            bg="white", fg="black", font=(None, 40), height=2, width=500)
        label_four = Label(root, text=value, bg="white", fg="blue", font=(None, 60), height=3, width=500)
        label_one.pack()
        label_two.pack()
        label_three.pack()
        label_four.pack()


def makeform(root, fields):
    entries = []
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=15, text=field, anchor='w', bg="white", font=(None, 20), height=2, justify="center")
        ent = Entry(row, font=(None, 20), bd=5)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append((field, ent))
    return entries


if __name__ == '__main__':
    root = Tk()
    root.title("Simplex Method")
    root.geometry('1800x1200')
    root.configure(background='white')
    label_one = Label(root, text="Solution to Linear Program using SIMPLEX METHOD",
                      bg="white", fg="black", font=(None, 40), height=2, width=500)
    label_two = Label(root,
                      text="Please enter your linear program in the standard form as follows:\nmax [C_transpose][X]\nsubject to\n[A][X] <= [B]\n[X] >= 0",
                      bg="white", fg="blue", font=(None, 20), height=8, width=500)
    label_three = Label(root,
                        text="Enter the dimensions of the input matrices\n and then enter the values of the elements of the individual matrices\n for example if C_transpose = [2,1,4] then enter the values as: 1,3,2,1,4",
                        bg="white", fg="black", font=(None, 15), width=500, height=5)
    label_one.pack()
    label_two.pack()
    label_three.pack()
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))
    b1 = Button(root, text='Compute Solution', height=2, justify="center", font=(None, 20),
                command=(lambda e=ents: fetch(e)))
    b1.pack(side=TOP, padx=5, pady=5)
    b3 = Button(root, text='Quit', font=(None, 20), command=root.quit, height=2)
    b3.pack(side=TOP, padx=5, pady=5)
    root.mainloop()
