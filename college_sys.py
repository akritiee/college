import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Initialize the Firebase app
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred,{"databaseURL":"https://collegesys-default-rtdb.asia-southeast1.firebasedatabase.app/"})
db=firestore.client()

#This is all are the max marks
# Admission criteria for each course
admission_criteria = {
    ' Engineering CS': 80,
    'Electronic engineering': 85,
    'cyber engineer': 75,
    'Business & management ': 70,
    ' Diploma(Any subject)': 60
}

# Retrieve all applicants
applicants = db.collection('applicants').stream()
#This data stored in the Excel
applicant_data = []
for applicant in applicants:
    data = applicant.to_dict()
    applicant_data.append(data)
    course = data['course_choice']
    grades = data['grades']

    # Check if the applicant meets the criteria for their course
    if course in admission_criteria and grades >= admission_criteria[course]:
        status = 'Accepted'
    else:
        status = 'Rejected'
        #if grade are equal to the criteria it is accepted otherwise it got rejected

    # Update the applicant's status in the database
    db.collection('applicants').document(applicant.id).update({'status': status})

    print(f"Applicant {data['name']} ({data['email']}) status updated{status}")
# Convert Firestore documents into a list of dictionaries

# Convert data to Pandas DataFrame
df = pd.DataFrame(applicant_data)

# Save DataFrame to an Excel file
df.to_excel("College_excel.xlsx", index=False)

print("Data saved successfully in College_excel.xlsx")

# Take input from the user
name = input("Enter your name: ")
age = int(input("Enter your age: "))
email = input("Enter your email: ")
grades = float(input("Enter your grades: "))
course_choice = input("Enter your preferred course: ")
SOP=input("Enter your statement of purpose:")

# Store user data in Firestore
applicant_data = {
    'name': name,
    'age': age,
    'email': email,
    'grades': grades,
    'course_choice': course_choice,
    'status': 'Pending' , # Default status
    'sop':SOP

}

db.collection('applicants').add(applicant_data)
print("Application submitted successfully!")
