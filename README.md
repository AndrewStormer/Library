# Library_database
Library database in MySQL created for my database applications and information systems course at the University of Missouri.

## Startup
This application needs a server_config.py file to run, the file should be in the form:

```
config = {
  'user': 'username',
  'password': 'user_password',
  'host': '127.0.0.1'
}
```

where 'username' and 'password' should correspond to the login user and password of your MySQL server


## Database

```
EMPLOYEE (
    Emp_id		INT,
    Fname 		VARCHAR(25),
    Lname		VARCHAR(25),
    Address		VARCHAR(40),
    PRIMARY KEY(Emp_id) 
);

STUDENT (
    Student_id	INT,
    Fname		VARCHAR(25)		NOT NULL,
    Lname		VARCHAR(25)		NOT NULL,
    Address		VARCHAR(40),
    book_count	INT				DEFAULT 0,
    Money_owed	DECIMAL(6, 2)	DEFAULT 0.00,
    PRIMARY KEY(Student_id)
);

SECTION (
    Section_number INT,
    Section_subject	VARCHAR(25),
    PRIMARY KEY(Section_number)
);

BOOK (
    Book_id		INT,
    Title		VARCHAR(50)		NOT NULL,
    Author		VARCHAR(25)		NOT NULL,
    Is_taken	bool			DEFAULT	FALSE,
    PRIMARY KEY(Book_id)
);

BOOK_SECTION (
    Book_id		INT,
    Section_number INT,
    PRIMARY KEY(Book_id),
    FOREIGN KEY(Section_number) REFERENCES SECTION(Section_number)
);

LIBRARIAN (
    Emp_id		INT,
    Section_number INT,
    PRIMARY KEY(Emp_id, Section_number),
    FOREIGN KEY(Emp_id) REFERENCES EMPLOYEE(Emp_id),
    FOREIGN KEY(Section_number) REFERENCES SECTION(Section_number)
);

TECHNICIAN (
    Emp_id		INT,
    PRIMARY KEY(Emp_id),
    FOREIGN KEY(Emp_id) REFERENCES EMPLOYEE(Emp_id)
);

RENT_DATE (
    Renter_id	INT,
    Rent_date	date
);

RENT_BOOK (
    Renter_id	INT,
    Book_id 	INT			NOT NULL,
    Due_date  	DATE,
    PRIMARY KEY(Renter_id, Book_id),
    FOREIGN KEY(Book_id) REFERENCES BOOK(Book_id)
);
```