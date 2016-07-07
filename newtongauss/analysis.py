import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import copy

#np.set_printoptions(precision=16)

# base = pd.read_excel("Cantera Evaluation.xlsx",sheetname='ROLETA' ,header=None)
# base = base.fillna(0) #fill NaN data with 0
# base = base.replace(to_replace='NO RPT', value=0) #replace no RPT with 0
#
# wholedata = np.matrix(base)
#
# #wholedata = np.delete(wholedata,(0), axis=0) #delete first row
# wholedata = np.delete(wholedata,(0), axis=1) #delete first column
# #wholedata = np.delete(wholedata,(0), axis=1) #delete another first column
#
# # sort out the name of the file

prod_input =[3000,1500,1000,700,500,400]

def run_analysis(prod_input):

    input =np.matrix(prod_input)

    time = np.arange(len(np.transpose(input)))
    
    time = np.add(time,1)
    
    time =time.reshape((1,len(np.transpose(input))))
   
    top = np.zeros((1,2),dtype=np.int)
    


    input = np.transpose(np.concatenate((time,input),axis =0))

    input = np.concatenate((top,input),axis =0)

    time =np.transpose(time)

    lam = 4.0
    limit_runs =300


    no_converge =0




    #size = size1 in matlab
    ##inside for loop
    # for loop from 0 to , therefore running 3 times
    for column in range(1, 2):
    #for column in range(1, size):

        prod_range = len(input[:,column])
        prod = input[1:prod_range ,column]
        print(prod)
         #initial geuss a and b factor
        di = .5
        b = .5




        error_ratio=1
        error_array =0#initial start of error ratio array
        run = 0
        tot_regs=np.array([500]) #might need to be fixed
        

        ####levenBerg - Marquardt Algorith##################################
        lam = lam
        ####################################################################

        while error_ratio > .1:
            run = run+1
            if run>1:
                di =di_new
                b = b_new

            #find maximum point position and decline from that point and onward
            max_pos = np.argmax(prod)
            print(max_pos)
            qi = prod[max_pos]
            qt = qi/np.power((1+b*di*time),(1/b))
            qt = qt[0:len(prod)-1-max_pos]
            time1= time[0:len(time)-max_pos]

            #d_di = np.divide(

            d_di = np.divide(-np.multiply(qi,time1),(np.power((time1*di*b+1),(1/b+1))))

            #break big equation into sections
            #d_b =  math.log(50)
            a1 = np.log(np.float64(time1*di*b+1))
            a2 = (b**2)*np.power((time1*di*b+1),(1/b))
            a3 = np.divide((time1*di),b*np.power((time1*di*b+1),(1/b+1)))
            d_b= np.multiply(qi,np.subtract(np.divide(a1,a2), a3))



            #calculating Derivative fit
            original = prod[max_pos:len(prod)]
            qt = np.concatenate((qi,qt),axis=0)
            D = original-qt
            regress = np.power(D,2)
            total_regress = np.sum(regress,axis=0)
            tot_regs=np.c_[tot_regs,total_regress]

            #graph in matplotlib
            # plt.semilogy(time,prod)
            # plt.semilogy(time[max_pos:len(time)],qt)
            # plt.xlabel('Time in months')
            # plt.ylabel('BOPM')
            # plt.title('Prod Per Month vs Month')
            # plt.show(column)

            #calculate, form z0 (di first)
            z0 = np.concatenate((d_di,d_b),axis=1)
            zTz = np.transpose(z0)*z0
            #######################################
            diag1 = copy.copy(zTz)

            diag1[0,1] =0
            diag1[1,0] =0

            zTz = zTz+lam*diag1
            #######################################
            right = np.transpose(z0)*D
            ans,resid,rank,s=np.linalg.lstsq(zTz,right)

            #break loop when there is complex numbers involved
            if di+ ans[0,0]<0 or b+ans[1,0] < 0:
                break

            di_new= di+ans[0,0]
            b_new = b+ans[1,0]
            # print(run)
            # print(tot_regs)
            # print(tot_regs[0,1])
            error_ratio = np.abs((tot_regs[0,run]-tot_regs[0,run-1]))/100;

            if run>limit_runs:
                no_converge= no_converge+1
                break

            error_array = np.c_[error_array,error_ratio]

        #there is an end here in matlab
        # b_array[column] = b_new;

        if column == 1:

            run_matrix = np.empty([1,0])
            run_matrix=np.c_[run_matrix,run]

            error_Matrix = np.empty([1,0])
            error_Matrix=np.c_[error_Matrix,error_ratio]

            qi_array = np.empty([1,0])
            qi_array = np.c_[qi_array,qi]

            di_array = np.empty([1,0])
            di_array = np.c_[di_array,di_new]

            b_array = np.empty([1,0])
            b_array = np.c_[b_array,b_new]

        else:
            run_matrix=np.c_[run_matrix,run]
            error_Matrix=np.c_[error_Matrix,error_ratio]
            qi_array = np.c_[qi_array,qi]
            di_array = np.c_[di_array,di_new]
            b_array = np.c_[b_array,b_new]
        #
        # print(run_matrix, 'run Matrix')
        # print(error_Matrix, 'error_Matrix')
        # print(qi_array, 'qi array')
        # print(di_array, 'di_array')
        # print(b_array, 'b array')
        # print (no_converge)

        # qt_array = np.empty([range1,0])
        # qt_array = np.c_[qt_array,qt]
        # print(qt_array, 'qt array')


    # print(time.size)
    # print(b_array.shape)
    # print(di_array.shape)
    # print(qt,'qt')
    # print("****************")
    qt =np.transpose(np.intc(qt))

    return qt

bob = run_analysis(prod_input)
print(bob)
#print(b)
#print(d_b)
# print (total_regress)
# print (tot_regs)
#print (run_matrix)
# print(range1)
# print(np.empty([range1,0]).shape)
# print(qt.shape)