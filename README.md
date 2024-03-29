# Library  service project
The current project is created to help the local library to manage book borrowings. 
It helps to track a borrowing status of every book, which is registered in the library database.

# Features
* JWT authentication
* Creating/updating and deleting books
* Email authorization
* Detailed book and borrowing info
* Book inventory validation
* Updating book inventory depending on creating/returning the borrowing
* Filtering borrowings by book status(not returned)
* Filtering borrowings by user_id (available only for admin)
* Documentation in swagger and redoc

![Borrowing list](api_photos/borrowing_list.png)  
![Borrowing detail](api_photos/detailled_borrowing_info.png)  
![Borrowing filtering](api_photos/filtering_book_by_return_status.png)  
![Token obtain](api_photos/obtain_token.png)  

# Installing using git
* `git clone https://github.com/Script1988/Library-service-project.git`
* `python -m venv venv`
* `venv\Scripts\activate (on Windows)`
* `source venv/bin/activate (on macOS)`
* `pip install -r requirements.txt`
* create .env file
* set all environment variables in .env file using examples from .env.sample
* `python manage.py migrate`
* `python manage.py runserver`

# Getting access
* use email=`test_admin@admin.com `and password = `test_admin` for testing
* download ModHeader extension for your browser
* get access token from /api/user/token/
* create request header in ModHeader extension
* write Authorization in the first line
* write Bearer and access token from /api/user/token/ in the second line
 