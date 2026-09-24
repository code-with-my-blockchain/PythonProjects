
# fruits = ["apple", "banana", "cherry"]
# for x in fruits:
#   if x == "banana":
#     continue
#   print(x)


#   fruits = ["apple", "banana", "cherry"]
# for x in fruits:
#   if x == "banana":
#     break
#   print(x)



#   fruits = ["apple", "banana", "cherry"]
# for x in fruits:
#   print(x)
#   if x == "banana":
#     break


# for i in range(1, 100):
#   print(i)  
#   if i == 63:
#      break
#print(63+i)



# for i in range ( 1 , 100):
#   print (i)
#   if i == 63:
#       break

#   def myfunc():
#    print (" python language ")
# myfunc()




# x = dict(name="Ephlal", age=28)
# print(x)


# num = int(input("any number:"))
# for i in range ( 1 , 10 ):
#  print(num , "X" , i , "=", num * i )



# num = int(input( "place any number:"))
# for i in range (1 , 10):
#  print(num , "x" , i , "=" ,num *i)

# while i < 11:
#   print(i)
#   i += 1


# def myfunc():
#  num =int(input("place any number:"))
#  for i in range (1 , 11):
#    myfunc()
#    print (num)

# def my_func1():
#  num = int(input("place any number:"))
#  for i in range (1 , 11):
#   print(num , "x" , i , "="  , num * i )
#  i += 1
# my_func1()



# def myfunc():
# #  num =int(input ("place any number:"))
# #  for i in range (1 , 11):
#     myfunc()
# num = int(input("place any number:"))
# for i in range (1 , 11):
#  print(num , "x" , i , "="  , num * i )
#  i += 1



# num = int(input(" any number")) 
# while i < 10:
#  print(num , "x" , i , "="  , num * i )
#  i = i +1


# num = int(input("Enter any number: ")) 
# i = 1  
# while i <= 10: 
#     print(num, "x", i, "=", num * i)
#     i = i + 1  # while loop mein bohat important hai. Iska main kaam hai i ki current value ko 1 se increase karna,
#     #taake loop next number par ja sake.





# import pandas as pd

# # Create the initial student dataset dictionary
# students = {
#     "name": ["Ali", "Sara", "Ahmed", "Usman", "Ayesha", "Hamza"],
#     "age": [21, 22, 20, 23, 21, 22],
#     "math": [85, 92, 76, 88, 95, 69],
#     "python": [90, 89, 80, 85, 94, 72],
#     "ai": [88, 95, 78, 91, 96, 70]
# }

# # Load data into a Pandas DataFrame
# df = pd.DataFrame(students)

# # 1 & 2. Calculate each student's average across subjects and add an 'average' column
# df['average'] = df[['math', 'python', 'ai']].mean(axis=1)

# # 3. Find the highest-performing student
# highest_student = df.loc[df['average'].idxmax(), 'name']

# # 4. Find the lowest-performing student
# lowest_student = df.loc[df['average'].idxmin(), 'name']

# # 5. Calculate the class average for each subject
# subject_averages = df[['math', 'python', 'ai']].mean()

# # 6. Find students whose average is above 85
# above_85_students = df[df['average'] > 85]['name'].tolist()

# # 7. Sort students by average (highest to lowest)
# df_sorted = df.sort_values(by='average', ascending=False)

# # 8. Find the average score of students older than 21 (Ages 22 and 23)
# older_than_21_avg = df[df['age'] > 21]['average'].mean()


# # --- Displaying the Results ---
# print("--- Final Processed DataFrame ---")
# print(df.round(2))
# print("\n--- Analysis Reports ---")
# print(f" Highest-Performing Student: {highest_student}")
# print(f" Lowest-Performing Student: {lowest_student}")
# print(f" Students with Average > 85: {', '.join(above_85_students)}")
# print(f"⏱ Average Score of Students Older than 21: {older_than_21_avg:.2f}")
# print("\n Class Average per Subject:")
# print(subject_averages.round(2).to_string())
# print("\n Students Sorted by Average:")
# print(df_sorted[['name', 'average']].round(2).to_string(index=False))



# def myfunc():
#   num =int(input ("place any number:"))
#   for i in range (1 , 11):
#     myfunc()
# num = int(input("place any number:"))
# for i in range (1 , 11):
#  print(num , "x" , i , "="  , num * i )
#  i += 1


# def myfunc():
#   num =int(input("place any number:"))
#   return num 

# def my_func1():
#   num = myfunc()
#   for i in range (1 , 11):
#    print(num , "x" , i , "="  , num * i )
 
# my_func1()



# def myfunc():
#   num = int(input ("place any number:"))
#   return num 


# def my_func1():
#   num = myfunc()
#   for i in range (1 , 11 ):
#     print (num , "x" , i , "=" , num * i)
# my_func1()



# def myfunc():
#     x = (9+11)
#     return (x)
# y = myfunc()
# print(y)


#     name = "ALI"
#     age = 27
#     return ("name" , age)
# my_self()
# print("ALI" , 27)


# def my_func1():
#   y = myfunc()
#   for i in range (1 , 11 ):
#     print (y , "x" , i , "=" , y * i)
# my_func1()


# def my_self():
#     name = "Ali haider"
#     age = 27
#     return name, age
# name, age = my_self()

# print("Name:", name)
# print("Age:", age)

# if age > 20:
#     print(name, "age is greater than 20")
# else:
#     print(name, "age is less than 20 ")



# def my_self():
#     name = input(" your name:")
#     age = int(input(" your age:"))
#     return name, age

# name, age = my_self()
# print("Name:", name)
# print("Age:", age)

# if age >= 20:
#     print(name, "age is higher than 18")
# else:
#     print(name, "age is lower than 18")

#largest_number = max(x)





# # #Check whether a number is positive, negative, or zero..
# num = int(input ("place any number:"))
# if num > 0:
#        print (num , "positive" )
#elif num < 0:
#       print(num , "negative")
# else:
#        print("0")



#Check whether a number is even or odd.
# num = int(input ("any number:"))
# if num % 2 == 0:
#     print (num, "even")
# else:
#     print(num , "odd")






# # #  #Check whether someone is eligible to vote based on age.
# num = int (input ( "number of age"))
# if num > 18:
#  print(num , "ready to vote")
# elif num < 18:
#  print(num , "age not valid")




# #  #Check whether a year is a leap year.
# num = int(input("ask a year"))
# if (num % 4 == 0 ):
#         print(num, "is a leap year")
# else:
#     (num % 4 != 0)
#     print(num, "is not a leap year")






# # # #Print all even numbers from 1 to 100.
# for i in range (1,100):
#  if i % 2 == 0:
#   print(i , "even")
# i += 1

 



# # #Print all odd numbers from 1 to 100.
# for i in range (1,100):
#  if i % 2 != 0:
#   print(i , "odd")
# i += 1



# #Calculate the sum of numbers from 1 to N.
# def myfunc():
#  for i in range( 1,10):
#   n = 1+2+3+4+5+6+7+8+9+10 
#  sum = (n)
#  print (sum)
#  i = i + 1
# myfunc()




# for i in range (1,10):
# largest_num =(x)
# if largest_num == x:
#  largest_num =(x)
# print(largest_num)
# result = largest_num
# print(result)
# # result = ("710" , "555")
# print(largest_num)
# i +=1




# #Find the largest of three numbers
# num = [51 , 11 , 32 , 47 , 555 , 63 , 911, 88 , 99 , 100 ]
# largest_num = max(num)
# y = (largest_num)
# print(y)



# # # #Find the larger of two numbers.
# num = (51 , 11 , 32 , 47 , 555 , 63 , 733, 88 , 99 , 100 )
# largest_num = max(num)
# y = (largest_num)
# print(y)


# # #Find the larger of two numbers.
# for i in range (1 ,10):
#     list = (51 , 11 , 32 , 47 , 555 , 63 , 733, 88 , 99 , 100 )
# num1 = 51
# num2 = 11

# if num1 > num2:
#     larger = num1
# else:
#     larger = num2

# print("larger one" , num1 or num2 )



# num = (51, 11, 32, 47, 999, 63, 733, 88, 99, 100)
# largest = num[0]
# for i in range(len(num)):
#     if num[i] > largest:
#         largest = num[i]
# print("Largest one :", largest)




# num = (51, 11, 32, 47, 999, 63, 733, 88, 99, 100)
# largest1 = num[0]
# largest2 = num[1]
# for i in num:
#     if i > largest1:
#         largest1 = i
# for i in num:
#     if i > largest2 and i != largest1:
#         largest2 =i
# print("First Largest :", largest1)
# print("Second Largest:", largest2)



# num = (51, 911, 32, 47, 999, 63, 733, 88, 99, 100)
# largest1 = num[0]
# largest2 = num[1]
# largest3 = num[2]
# for i in num:
#     if i > largest1:
#         largest1 = i
# for i in num:
#     if i > largest2 and i != largest1:
#         largest2 = i
# for i in num:
#     if i > largest3 and i != largest1 and i != largest2:
#         largest3 = i      
# print("First Largest :", largest1)
# print("Second Largest:", largest2)
# print("Third Largest :" , largest3)



# # num = [2,7,11,15]
# y = 9
# # def myfunc():
# #  for i in num:
# #    i +=1
# num1 =[2]
# num2=[7]
# # num3=[11]
# # num4 =[15]
# # if [2 + 7 ]== y:
# #    print(num1 , num2)
# # else: [11 + 15] == y
# # myfunc()
# print(num1 , num2)

# for i in range(len(num)):
#     for j in range(i + 1, len(num)):
#         if num[i] + num[j] == target:
#             print(f"Values: {num[i]} aur {num[j]}")
#             print(f"Indices: {i} aur {j}")


#  num1 + num2 
# # if num == y:
#  for i in num:
#   if sum(num) == y:
#    num = []
#    myfunc()
# print(num)

#  x = num[0]
#  x = num[1]



# num = (51, 11, 32, 47, 999, 63, 733, 88, 99, 100)
# largest1 = num[0]
# largest2 = num[1]
# for i in num:
#     if i > largest1:
#         largest1 = i
# for i in num:
#     if i > largest2 and i != largest1:
#         largest2 =i
# print("First Largest :", largest1)
# print("Second Largest:", largest2)




# num = (51, 911, 32, 47, 999, 63, 733, 88, 99, 100)
# largest1 = num[0]
# largest2 = num[1]
# largest3 = num[2]
# for i in num:
#     if i > largest1:
#         largest1 = i
# for i in num:
#     if i > largest2 and i != largest1:
#         largest2 = i
# for i in num:
#     if i > largest3 and i != largest1 and i != largest2:
#         largest3 = i      
# print("First Largest :", largest1)
# print("Second Largest:", largest2)
# print("Third Largest :" , largest3)




# x = [1,11,0,15]
# val = 8
# i = (0)
# for a in range(len(x)):
#     for b in range(i +1 , len(x)):
#       if x[a] + x[b] == val:
#         print(f"num = {x[a]} , {x[b]}")
#         print(f"index = {a} , {b}")
# else:
#      print("no values found")



# def my_self():
#     name = "Ali haider"
#     age = 27
#     return name, age
# name, age = my_self()

# print("Name:", name)
# print("Age:", age)

# if age > 20:
#     print(name, "age is greater than 20")
# else:
#     print(name, "age is less than 20")


# import pandas as pd
# students = {
#     "name": ["Ali", "Sara", "Ahmed", "Usman", "Ayesha", "Hamza"],
#     "age": [21, 22, 20, 23, 21, 22],
#     "math": [85, 92, 76, 88, 95, 69],
#     "python": [90, 89, 80, 85, 94, 72],
#     "ai": [88, 95, 78, 91, 96, 70]
# }
# df = pd.DataFrame(students) 
# def my_func():
#  df['average'] = df[['math', 'python', 'ai']] , students('/')
#  my_func()
# print (df)

# subjects= "math" , "python" , "ai"
# num = subjects
# i =(0)
# print(f"students , '%'", "i"  "=" ,f"num / subjects")
# print(students , '%', i , "=" , "num / subjects")
# name = (input(" Student Name : "))





















# Task 1: Student Dataset Analysis

# Create a Pandas DataFrame from:

# students = {
#     "name": ["Ali", "Sara", "Ahmed", "Usman", "Ayesha", "Hamza"],
#     "age": [21, 22, 20, 23, 21, 22],
#     "math": [85, 92, 76, 88, 95, 69],
#     "python": [90, 89, 80, 85, 94, 72],
#     "ai": [88, 95, 78, 91, 96, 70]
# }

# Perform the following:

# Calculate each student's average.
# Add an average column.
# Find the highest-performing student.
# Find the lowest-performing student.
# Calculate the class average for each subject.
# Find students whose average is above 85.
# Sort students by average.
# Find the average score of students older than 21.



# pd.DataFrame()       → DataFrame banao
# .mean()              → Average
# .idxmax()            → Maximum ka index
# .idxmin()            → Minimum ka index
# .loc[]               → Row/index select
# df[condition]        → Condition ke mutabiq rows
# .sort_values()       → Sort
# axis=1               → Row-wise
# axis=0               → Column-wise



# import pandas as pd

# students = {
#     "name": ["Ali", "Sara", "Ahmed", "Usman", "Ayesha", "Hamza"],
#     "age": [21, 22, 20, 23, 21, 22],
#     "math": [85, 92, 76, 88, 95, 69],
#     "python": [90, 89, 80, 85, 94, 72],
#     "ai": [88, 95, 78, 91, 96, 70]
# }


# df = pd.DataFrame(students)  # dictionary ko data frame ya table mey convert karta hai


# df["average"] = df[["math", "python", "ai"]].mean(axis=1) # DataFrame mein average naam ka column banao. Math, Python aur AI columns ko select karo,
#                                                           #har student ki row ka average nikalo, aur us result ko average column mein store kar do.



# highest = df.loc[df["average"].idxmax()] # Average column mein sabse badi value ka index deta hai.   df - avg - idx max                                  
# print("Highest-performing student:")     #Us index ki poori row nikal deta hai.     df.loc
# print(highest)


# lowest = df.loc[df["average"].idxmin()] # avg colomn main subsey chothi value ka index deta hai.       df - avg -idx min
# print("\nLowest-performing student:")   ##Us index ki poori row nikal deta hai.     df.loc
# print(lowest)


# class_average = df[["math", "python", "ai"]].mean() #Yahan axis nahi diya, isliye Pandas normally har column ka average calculate karta hai.
# print("\nClass average:")
# print(class_average)


# above_85 = df[df["average"] > 85]  #Pandas har student's average check karega: or 85% above valon ko select karey ga 
# print("\nStudents with average above 85:")    # df[condition]        → Condition ke mutabiq rows
# print(above_85)


# sorted_students = df.sort_values("average")  #Average coloumn ke according sorting values / Default mein ascending hota hai:
# print("\nStudents sorted by average:")   # if we place (ascending=flase) then descending mey values barri sy chothi place kary ga
# print(sorted_students)


# older_than_21 = df[df["age"] > 21] # Pehla .mean() → har subject ka average. Doosra .mean() → un teen subject averages ka overall average.
# average_older_than_21 = older_than_21[["math", "python", "ai"]].mean().mean()
# print("\nAverage score of students older than 21:")
# print(average_older_than_21)    # data types like name = object & int whole no = int64 , decimal no = float64 



####################################################################################################################################

# max_salary_idx = salaries.index(max_salary)
# print(max_salary_idx)


# min_salary_idx = salaries.index(min_salary)
# print(min_salary_idx)


# max_salary_employee = names[max_salary_idx]
# print(max_salary_employee)


# min_salary_employee = names[min_salary_idx]
# print(min_salary_employee)


# high_earners = []
# for i in range(len(salaries)):
#     if salaries[i] > 80000:
#         high_earners.append(names[i])
#         print(high_earners)


# print(df.head(5))   uper vali pahli 5 rows

# print(df.tail(3))    # neechey vali 3 rows (tail)

# print(len(df))        # for counting total numbers

# print(df.columns.tolist()) #coloums ki list ya names ya categories

# print(df.dtypes)      # pandas mey dataframe ki data types like oject , int64 , float64



# customer_spending = df.groupby("customer")["revenue"].sum()
# print("\n1. Total amount spent by each customer:")
# print(customer_spending)

# top_spender_name = customer_spending.idxmax()
# top_spender_amount = customer_spending.max()
# print("\n2. Customer who spent the most:")
# print(f"{top_spender_name} ({top_spender_amount:,})")

# customer_quantity = df.groupby("customer")["quantity"].sum()
# top_quantity_name = customer_quantity.idxmax()
# top_quantity_value = customer_quantity.max()
# print("\n3. Customer who purchased the highest quantity:")
# print(f"{top_quantity_name} ({top_quantity_value} items)")


# high_spenders = customer_spending[customer_spending > 100000]
# print("\n4. Customers who spent more than 100,000:")
# print(high_spenders)


# high_rating_customers = df[df["rating"] > 4.5][["customer", "rating"]]
# print("\n5. Customers whose rating is above 4.5:")
# print(high_rating_customers.to_string(index=False))





# category_analysis = (
#     df.groupby("category")
#     .agg(
#         total_sales=("revenue", "sum"),
#         total_quantity=("quantity", "sum"),
#         average_price=("price", "mean"),
#         average_rating=("rating", "mean"),
#         num_transactions=("category", "count"),
#     )
#     .reset_index()
# )
# print(category_analysis)











#################################################################################################################################




# Task 2: Employee Performance Analysis

# You are given information about employees in a company.

# employees = {
#     "name": ["Ali", "Sara", "Ahmed", "Usman", "Ayesha", "Hamza", "Zain", "Fatima"],
#      age": [25, 29, 24, 31, 27, 26, 30, 28],
#     "department": ["IT", "HR", "IT", "Finance", "HR", "IT", "Finance", "IT"],
#     "experience": [2, 5, 1, 7, 4, 3, 6, 5],
#     "projects": [4, 8, 2, 10, 7, 5, 9, 8],
#     "performance": [82, 91, 75, 95, 88, 84, 93, 90],
#     "salary": [70000, 85000, 65000, 120000, 80000, 75000, 110000, 95000]
# }
# Requirements

# Create a Pandas DataFrame from the dictionary and perform the following:

# 1. Basic Analysis
# Display the first 5 employees.
# Display the last 3 employees.
# Display the number of employees.
# Display all column names.
# Display the data types of each column.


# 2. Salary Analysis

# Find:

# Average salary
# Highest salary
# Lowest salary
# Employee with the highest salary
# Employee with the lowest salary
# Employees earning more than 80,000
# 3. Performance Analysis

# Find:

# Average performance score
# Highest performance score
# Lowest performance score
# Best-performing employee
# Employees with performance above 85
# Employees with performance below 80
# 4. Experience Analysis

# Find:

# Average years of experience
# Employee with the most experience
# Employee with the least experience
# Employees with more than 5 years of experience


# import pandas as pd
# employees = {
#     "name": ["Ali", "Sara", "Ahmed", "Usman", "Ayesha", "Hamza", "Zain", "Fatima"],
#     "age": [27, 29, 24, 31, 27, 26, 30, 28],
#     "department": ["IT", "HR", "IT", "Finance", "HR", "IT", "Finance", "IT"],
#     "experience": [2, 5, 1, 7, 4, 3, 6, 5],
#     "projects": [4, 8, 2, 10, 7, 5, 9, 8],
#     "performance": [82, 91, 75, 95, 88, 84, 93, 90],
#     "salary": [70000, 85000, 65000, 120000, 80000, 75000, 110000, 95000]
# }

# df = pd.DataFrame(employees)

#                  # 1. Basic Analysis

# print(df.head(5))   

# print(df.tail(3))    

# print(len(df))        

# print(df.columns.tolist()) 

# print(df.dtypes)     


#               # 2. Salary Analysis


# salaries = employees["salary"]
# names = employees["name"]


# avg_salary = sum(salaries) / len(salaries)
# print(avg_salary)


# max_salary = max(salaries)
# print(max_salary)

# min_salary = min(salaries)
# print(min_salary)


# highest_salary = df.loc[df["salary"].idxmax()]
# print(highest_salary)



# lowest_salary = df.loc[df["salary"].idxmin()]
# print(lowest_salary)


# highest_earner = df[df["salary"] > 80000]
# print("\nEmployees with salary above 80000:") 
# print(highest_earner)



#                # Performance Analysis

# avg_score = df['performance'].mean()
# print(avg_score)


# high_score = df['performance'].max()
# print(high_score)


# low_score = df['performance'].min()
# print(low_score)

# highest_score = df.loc[df["performance"].idxmax()]
# print(highest_score)


# above_85 = df[df["performance"] > 85]
# print("\nEmployees with performance above 85:") 
# print(above_85)


# below_85 = df[df["performance"] < 85]
# print("\nEmployees with performance below 85:") 
# print(below_85)


#              #Experience Analysis

# avg_year = df['experience'].mean()
# print(avg_year)



# experience = employees["experience"]



# avg_year = sum(experience) / len(experience)
# print(avg_year)



# most_experience = df.loc[df["experience"].idxmax()]
# print(most_experience)


# least_experience = df.loc[df["experience"].idxmin()]
# print(least_experience)



# less_then_5 = df[df["experience"] < 5]
# print("\nEmployees with less then 5 years of experience:") 
# print(less_then_5)


# more_then_5 = df[df["experience"] > 5]
# print("\nEmployees with more then 5 years of experience:")
# print(more_then_5)


# age_less_then = df[df["age"] < 25]
# print("\nEmployee whose age is less then 25:")
# print(age_less_then)



####################################################################################################################################
                                              #NUMPY FUNCTIONS

# Mean	np.mean(a)	Average of array elements       

# Median	np.median(a)	Middle value of sorted elements      

# Standard Deviation	np.std(a)	Spread of data relative to the mean

# Variancenp.var(a)Average squared deviation from mean ($\sigma^2$)

# Minimum	np.min(a)	Smallest element

# Maximum	np.max(a)	Largest element

# 25th Percentile	np.percentile(a, 25)	Value below which 25% of data falls (Q1)

# 75th Percentile	np.percentile(a, 75)	Value below which 75% of data falls (Q3)





# print("Mean:", np.mean(revenue)) # yh statical method average kai liye use hota hai jesy pandas mey mean use hota hai


# print("Median:", np.median(revenue)) # sari values ko tarteeb mey dey kai chothi sey bari center ka number nikal kai deta hai 
# agar even yani 4 numbers hongy to beech kai 2 num, ko jama karky 2 py devide karey ga / agar 3 numbers hongy to center one num lai ga



# print("Variance:", np.var(revenue))  # mean sey distance yani center value sey bari bari sub values ko - karky unka square lai ga
# phir un sub squares ko add karky un squares ki length py divide kardey ga


# print("Std Deviation:", np.std(revenue)) # Variance ka square root tak kai asli value samny a saky


# print("Minimum:", np.min(revenue)) # data mey subsey chothi value 


# print("Maximum:", np.max(revenue))  # data mey subssey barra number



# print("25th Percentile (Q1):", np.percentile(revenue, 25)) # yh data kai last 25% hisy yani values ko mark karta hai 
#percentile():"Data mein is percentage wali position par value kya hai?" 
# Q1         → 25% point
# Q2         → 50% point
# Q3         → 75% point
#25th Percentile = Q1 = First Quartile
# 50th Percentile = Q2 = Median
# 75th Percentile = Q3 = Third Quartile
# 100th percentile = Q4 = fourth quartile

# print("75th Percentile (Q3):", np.percentile(revenue, 75)) #  # yh data kai last 75%% hisy ya 25% start yani values ko mark karta hai


# top_3_indices = sorted_indices[-3:][::-1]
# bottom_3_indices = sorted_indices[:3]
# sorted_indices[-3:][::-1] (Top 3):

# [-3:] array ke aakhri 3 sab se bade values uthata hai.

# [::-1] unhe reverse karta hai taake sab se bada score pehle (1st place) aaye.

# sorted_indices[:3] (Bottom 3): Array ke shuruati 3 sab se chote values uthata hai.




#########################################################################################################################################



# Task: Sales & Customer Analysis

# Build a Sales Analysis program using Python, NumPy, and Pandas. The goal is to practice data manipulation, filtering, aggregation, and basic numerical analysis.

# Dataset
# sales = {
#     "customer": ["Ali", "Sara", "Ahmed", "Usman", "Ayesha", "Hamza", "Zain", "Fatima", "Bilal", "Hina"],
#     "product": ["Laptop", "Phone", "Laptop", "Tablet", "Phone", "Laptop", "Headphones", "Phone", "Tablet", "Headphones"],
#     "category": ["Electronics", "Electronics", "Electronics", "Electronics", "Electronics",
#                  "Electronics", "Accessories", "Electronics", "Electronics", "Accessories"],
#     "quantity": [1, 2, 1, 3, 2, 1, 4, 1, 2, 3],
#     "price": [120000, 80000, 120000, 55000, 80000, 120000, 15000, 80000, 55000, 15000],
#     "rating": [4.5, 4.2, 4.8, 3.9, 4.1, 4.7, 4.0, 4.6, 3.8, 4.3]
# }
# 1. Create the DataFrame

# Using Pandas:

# Create a DataFrame from the dictionary.
# Display the first 5 rows.
# Display the number of rows and columns.
# Display column names and data types.
# Generate basic statistics for numerical columns.



# 2. Calculate Revenue

# Create a new column:

# revenue

# Calculate:

# revenue = quantity × price

# Then find:

# Total revenue
# Average revenue
# Highest revenue
# Lowest revenue



# 3. Product Analysis

# Find:

# Total quantity sold for each product.
# Total revenue generated by each product.
# Average rating for each product.
# The product with the highest total revenue.
# The product with the highest average rating.



# 4. Customer Analysis

# Find:

# How much each customer spent.
# The customer who spent the most.
# The customer who purchased the highest quantity.
# Customers who spent more than 100,000.
# Customers whose rating is above 4.5.



# 5. Category Analysis

# Use groupby() to calculate for each category:

# Total sales
# Total quantity
# Average price
# Average rating
# Number of transactions



# 6. Filtering Challenge

# Create separate DataFrames for:

# Products costing more than 50,000
# Products with rating >= 4.5
# Transactions where quantity >= 3
# Electronics with revenue > 100,000





# 7. NumPy Analysis
# Do not use Pandas for these calculations.

# Convert the revenue column into a NumPy array.

# Use NumPy to calculate:

# Mean
# Median
# Standard deviation
# Variance
# Minimum
# Maximum
# 25th percentile
# 75th percentile



# 8. Revenue Normalization
# Do not use Pandas for these calculations.
# Using NumPy, normalize the revenue values between 0 and 1:

# normalized = (x - min) / (max - min)

# Add the result to the DataFrame as:

# normalized_revenue



# 9. Performance Score

# Create a new column:

# performance_score

# Use:

# performance_score = revenue * 0.7 + rating * 10000 * 0.3

# Then:

# Sort customers by performance score.
# Display the top 3.
# Display the bottom 3.

# 10. Final Challenge

# Create a summary DataFrame containing:

# product
# total_quantity
# total_revenue
# average_rating

# Sort it by total_revenue from highest to lowest.



####################################################################################################################################

# import pandas as pd

# sales = {
#     "customer": ["Ali", "Sara", "Ahmed", "Usman", "Ayesha", "Hamza", "Zain", "Fatima", "Bilal", "Hina"],
#     "product": ["Laptop", "Phone", "Laptop", "Tablet", "Phone", "Laptop", "Headphones", "Phone", "Tablet", "Headphones"],
#     "category": ["Electronics", "Electronics", "Electronics", "Electronics", "Electronics",
#                  "Electronics", "Accessories", "Electronics", "Electronics", "Accessories"],
#     "quantity": [1, 2, 1, 3, 2, 1, 4, 1, 2, 3],
#     "price": [120000, 80000, 120000, 55000, 80000, 120000, 15000, 80000, 55000, 15000],
#     "rating": [4.5, 4.2, 4.8, 3.9, 4.1, 4.7, 4.0, 4.6, 3.8, 4.3]
# }

#                                        #PART1

# df = pd.DataFrame(sales)


# print(df.head(5))


# print("\nDataFrame(Rows, Columns)")
# print(df.shape)


# print(df.columns.tolist()) 


# print(df.dtypes) 


# print("\narray Statistics")
# print(df.describe())


#                                                       #PART2
# df["revenue"] = df["quantity"] * df["price"]

# total_revenue = df["revenue"].sum()
# print(total_revenue)


# average_revenue = df["revenue"].mean()
# print(average_revenue)

# highest_revenue = df["revenue"].max()
# print(highest_revenue)

# lowest_revenue = df["revenue"].min()
# print(lowest_revenue)


#                                                       #PART3

# total_quantity_each_product = df.groupby("product")["quantity"].sum()
# print("\n1. Total quantity sold for each product:")
# print(total_quantity_each_product)



# total_revenue_each_product = df.groupby("product")["revenue"].sum()
# print("\n2. Total revenue generated by each product:")
# print(total_revenue_each_product)



# average_rating_each_product = df.groupby("product")["rating"].mean()
# print("\n3. Average rating for each product:")
# print(average_rating_each_product)


# highest_revenue_product = total_revenue_each_product.idxmax()
# highest_revenue_value = total_revenue_each_product.max()
# print("\n4. Product with the highest total revenue:")
# print(f"{highest_revenue_product} ({highest_revenue_value})")



# highest_rating_product = average_rating_each_product.idxmax()
# highest_rating_value = average_rating_each_product.max()
# print("\n5. Product with the highest average rating:")
# print(f"{highest_rating_product} ({highest_rating_value:.2f})")



#                                                         #PART4



# customer_spending = df . groupby("customer")["revenue"].sum()
# print("\n1. Total amount spent by each customer:")
# print(customer_spending)


# top_spender_name = customer_spending.idxmax()
# top_spender_amount = customer_spending.max()
# print("\n2. Customer who spent the most:")
# print(f"{top_spender_name} ({top_spender_amount:,})")



# highest_quantity = df.groupby ("customer") ["quantity"] . sum()
# top_quantity_name = highest_quantity.idxmax()
# top_quantity_value = highest_quantity.max()
# print("\n3. Customer who purchase the highest quantity:")
# print(f"{top_quantity_name})  ({top_quantity_value} items)")



# high_spenders = customer_spending [customer_spending > 100000]
# print("\n4. Customers who spent more than 100,000:")
# print(high_spenders)


# high_rated_customers = df[df["rating"] > 4.5] [["customer", "rating"]]
# print("\n5. Csutomers whose rating is above 4.5:")
# print(high_rated_customers.to_string(index = False))


#                                    #Part5

# category_analysis = (
#     df.groupby("category")
#     .aggregate(
#         total_sales=("revenue", "sum"),
#         total_quantity=("quantity", "sum"),
#         avg_price=("price", "mean"),
#         avg_rating=("rating", "mean"),
#         no_transactions=("category", "count"),
#     )
#     .reset_index()
     
# )
# print(category_analysis)

# average_revenue = df["revenue"].mean()
# print(average_revenue)



#                                              #Part6

# import pandas as pd

# product = {
#   "product" : ["Laptop", "Phone", "Laptop", "Tablet", "Phone", "Laptop", "Headphones", "Phone", "Tablet", "Headphones"],
#   "price"   : [120000, 80000, 120000, 55000, 80000, 120000, 15000, 80000, 55000, 15000],
#   "rating": [4.5, 4.2, 4.8, 3.9, 4.1, 4.7, 4.0, 4.6, 3.8, 4.3],
#   "quantity": [1, 2, 1, 3, 2, 1, 4, 1, 2, 3],
#   "category": ["Electronics", "Electronics", "Electronics", "Electronics", "Electronics",
#                    "Electronics", "Accessories", "Electronics", "Electronics", "Accessories"],
# }
# df = pd.DataFrame(product)    
# product_costing = df[df["price"] > 50000][["product", "price"]]
# print("\n6. product costing is above 50,000:")
# print(product_costing.to_string(index=False))



# high_rated_products = df[df["rating"] >= 4.5] [["product", "rating"]]
# print("\n5. product whose rating is greater than equal to 4.5:")
# print(high_rated_products.to_string(index = False))


# more_quantity_products = df[df["quantity"] >= 3] [["product", "quantity"]]
# print("\n5.Transaction where product quantity greater than equal to 3:")
# print(more_quantity_products.to_string(index = False))



# df["revenue"] = df["quantity"] * df["price"]
# total_revenue = df["revenue"].sum()
# revenue = total_revenue
# print(f"Total Revenue: {total_revenue}")

# revenue_more_than = df[(df["category"] == "Electronics") & (df["revenue"] > 100000)]
# revenue_more_than = revenue_more_than[["quantity", "price"]]
# print("\n5. Electronic products revenue more than 100,000:")
# print(revenue_more_than.to_string(index=False))


#                                                 #PART7 NUMPY


# import numpy as np
# df["revenue"] = df["quantity"] * df["price"]
# array = {
#            "revenue" : df["revenue"],
#      "total_revenue" : df["revenue"].sum(),
#            "revenue" : total_revenue,
#                print :(total_revenue),
# }

# revenue = df["revenue"].to_numpy()



# print("Mean:", np.mean(revenue)) 


# print("Median:", np.median(revenue)) 


# print("Std Deviation:", np.std(revenue)) 


# print("Variance:", np.var(revenue)) 


# print("Minimum:", np.min(revenue)) 


# print("Maximum:", np.max(revenue))  


# print("25th Percentile (Q1):", np.percentile(revenue, 25)) 


# print("75th Percentile (Q3):", np.percentile(revenue, 75)) 





#                                                     #PART 8


# rev_min = np.min(revenue)
# rev_max = np.max(revenue)

# normalized_revenue = (revenue - rev_min) / (rev_max - rev_min)


# sales["revenue"] = revenue
# sales["normalized_revenue"] = normalized_revenue


# print(f"{'Customer':<10} {'Revenue':<10} {'Normalized Revenue'}")
# print("-" * 40)
# for i in range(len(sales["customer"])):
#     print(f"{sales['customer'][i]:<10} {sales['revenue'][i]:<10} {sales['normalized_revenue'][i]:.6f}")


#                                                      #Part 9



# customer = np.array(sales["customer"])
# quantity = np.array(sales["quantity"])
# price = np.array(sales["price"])
# rating = np.array(sales["rating"])


# revenue = quantity * price
# performance_score = revenue * 0.7 + rating * 10000 * 0.3


# sales["revenue"] = revenue
# sales["performance_score"] = performance_score
# sorted_indices = np.argsort(performance_score)


# top_3_indices = sorted_indices[-3:][::-1]


# bottom_3_indices = sorted_indices[:3]


# print("--- TOP 3 CUSTOMERS ---")
# print(f"{'Customer':<10} {'Performance Score':<20}")
# print("-" * 32)
# for idx in top_3_indices:
#   print(f"{customer[idx]:<10} {performance_score[idx]:<20.2f}")


# print("\n--- BOTTOM 3 CUSTOMERS ---")
# print(f"{'Customer':<10} {'Performance Score':<20}")
# print("-" * 32)
# for idx in bottom_3_indices:
#   print(f"{customer[idx]:<10} {performance_score[idx]:<20.2f}")


#                                                  #PART10


# products = np.array(sales["product"])
# quantities = np.array(sales["quantity"])
# prices = np.array(sales["price"])
# ratings = np.array(sales["rating"])

# revenues = quantities * prices

# unique_products = np.unique(products)


# total_quantity = np.zeros(len(unique_products), dtype=int)
# total_revenue = np.zeros(len(unique_products), dtype=int)
# average_rating = np.zeros(len(unique_products), dtype=float)

# for i, prod in enumerate(unique_products):
#     mask = (products == prod)
#     total_quantity[i] = np.sum(quantities[mask])
#     total_revenue[i] = np.sum(revenues[mask])
#     average_rating[i] = np.mean(ratings[mask])
                                               
# sorted_indices = np.argsort(total_revenue)[::-1]


# print(f"{'product':<10} {'total_quantity':<16} {'total_revenue':<15} {'average_rating':<15}")
# print("-" * 60)
# for idx in sorted_indices:
#     print(f"{unique_products[idx]:<12} {total_quantity[idx]:<16} {total_revenue[idx]:<15} {average_rating[idx]:<15.2f}")


    
######################################################################################################################################





