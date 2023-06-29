# CSE303-Autumn'22-Section-04-Group-03

# Application - Student Performace Monitoring System
A web based application written for CSE303 (Database Management) using Python (Django), Javascript, CSS and HTML. For Database we used MySQL. The objective of this application is to monitor the performance of the students at university. This can be done by the faculty members, higher authorities (Department Head, Vice Chancallor and Dean) or the student themselves. This application will monitor the performance by tracking their evaluations, assessments, marks and grades and map all these to specific Course Learning Outcomes (CLO), which itself will be mapped to different Program Learning Outcomes (PLO).

Additional features that were implemented is the Question Bank (for storing all past questions and assesments) and Course Outline Generator.

![Screenshot (002)](images/output1.png)

## Contributors

1.	Faiza Omar Arpita @Arpitaaa2001
2.	Injamam Ul Haque @injamam00155
3.	Istiaq Ahmed  @isti2415
4.	Jaima Jahan Khan @schatten7393
5.	Showrov Mallick @Showrov007
6.	Syed Niaz Mohtasim @syedniaz

<!-- ## Dependencies
* Python
* Django
* Pandas
* Numpy
* Plotly
* Wheel
* MySQL -->

## How to Run
1.  Open the Terminal
2.	Clone the repository. 
    You may run the following command in the terminal:
        
        git clone https://github.com/injamam00155/CSE303-sec-04-Group-03.git

3.	Change directory to the cloned directory.
    You may run the following command in the terminal:

        cd .\CSE303-sec-04-Group-03\ 

4.	Create a virtual environment.
    You may run the following command in the terminal:

        python -m venv env

5.  Use the sql script and create a database with the required data.
6.  Activate the virtual environment:

        .\env\Scripts\activate

7.  These commands are to Install all the prerequisites.
    You may run the following commands in the terminal:

        pip install -r req.txt
        pip install -r requirements.txt

    
8.	Run the command(either one of them should work. If the first one does not work, try the second one): 
    
        python manage.py runserver 
        python3 manage.py runserver

9.	Open a browser and go to the url: http://127.0.0.1:8000/

## Login Credentials
* Student:
    - Username: 1616161
    - Password: student
* Faculty:
    - Username: 4101
    - Password: faculty
* Higher Management:
    - Username: 1020
    - Password: admin

## Screenshots
![Screenshot (001)](images/login.png)
![Screenshot (003)](images/output2.png)
![Screenshot (004)](images/output3.png)
![Screenshot (005)](images/output4.png)
![Screenshot (006)](images/output5.png)
