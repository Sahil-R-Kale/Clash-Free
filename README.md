# ClashFree

ClashFree is an automatic timetable builder and validation tool that provides a user friendly workspace to design schedules in a robust way.  

## Key functionalities and features

* Drag and drop UI which allows speedy modifications in the schedule, without requiring manual input of long names!
* Clashes between resources can be validated with a single button click, allowing the human scheduler to focus on more important aspects of timetable design.
* Input data (Teacher names, Subject names and Room number labels) need not be manually fed; instead user can simply upload a relevant PDF document containing this data from which the labels are automatically extracted. (an example input file has been provided in the repo, called 'TECOMP AllClass TT-1.pdf')
* The workspace opens up with a pre-filled schedule containing subject names, which can be later modified as required by the human scheduler. This initial state of the timetable is not random, rather it is genrated using the Genetic Algorithm with common constraints which can be modified as per your needs!
* Once a complete and consistent schedule has been developed, a user has the choice of exporting time-tables for each class as a PDF for further actions. 


## How to run ClashFree
1. Clone the repo
2. Create a virtual environment and copy the project folder into it (optional)
3. Install the required dependencies using the command:
```
pip install -r requirements.txt
```
4. Create a .env file and add the following environment variables
```
DB_CONNECTION_STRING = <MongoDB Connection String>
COLLECTION_NAME = <Any valid MongoDB collection name>
```
5. Run the main_build file to start ClashFree
```
python3 main_build.py
```
6. Design your own schedule, validate on the go, save each day, and hit export for the class needed. The PDF will be generated in the outputs folder on your local machine. 

## ClashFree Project Tour


![Screenshot (61)](https://user-images.githubusercontent.com/107458263/234787596-f43120f2-abf2-4c47-a5f0-92843984df60.png)

![Screenshot (62)](https://user-images.githubusercontent.com/107458263/234788443-f272bde8-754b-48db-9c69-f1ca6047bf15.png)

![Screenshot (63)](https://user-images.githubusercontent.com/107458263/234788483-8d3d1c48-dc12-4d6a-b78d-c93897d616d9.png)

![Screenshot (64)](https://user-images.githubusercontent.com/107458263/234788513-ae5ab6fc-8196-43e2-bced-2b615b2a69ea.png)

![Screenshot (65)](https://user-images.githubusercontent.com/107458263/234788552-f47ea988-7d45-4e32-9a74-291dc4ac9476.png)

![Screenshot (66)](https://user-images.githubusercontent.com/107458263/234789262-1ff411aa-12cc-46d5-a192-5c9931b0042d.png)

![Screenshot (67)](https://user-images.githubusercontent.com/107458263/234789325-5a0f54a1-4bc1-4b40-ae6b-1a060a89607d.png)

## UI Demo:
![Screenshot (73)](https://user-images.githubusercontent.com/107458263/234789384-57fdf40f-b241-489d-bd8d-40aa591c5b33.png)

![Screenshot (69)](https://user-images.githubusercontent.com/107458263/234789460-c6072549-f9f7-4aba-9e92-c8fa37e2efd1.png)

![Screenshot (70)](https://user-images.githubusercontent.com/107458263/234789530-3d7062c8-7a88-422e-ba6f-cc7ccddcf6f7.png)

## Future Scope:
![Screenshot (72)](https://user-images.githubusercontent.com/107458263/234789611-f3bb26b1-cbbb-40bf-a351-614b4f4c2a60.png)

We hope you enjoy using ClashFree to make your scheduling as easy and as hassle-free as posssible! Kindly star the repo if you find it useful and relevant!
