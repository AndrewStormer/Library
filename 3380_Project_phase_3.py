import mysql.connector as connector
from mysql.connector import errorcode
from datetime import datetime, date
import server_config as config


def drop_database(cursor):
    cursor.execute('DROP TABLE MY_LIBRARY.RENT_BOOK')
    cursor.execute('DROP TABLE MY_LIBRARY.TECHNICIAN')
    cursor.execute('DROP TABLE MY_LIBRARY.LIBRARIAN')
    cursor.execute('DROP TABLE MY_LIBRARY.BOOK_SECTION')
    cursor.execute('DROP TABLE MY_LIBRARY.BOOK')
    cursor.execute('DROP TABLE MY_LIBRARY.SECTION')
    cursor.execute('DROP TABLE MY_LIBRARY.STUDENT')
    cursor.execute('DROP TABLE MY_LIBRARY.EMPLOYEE')
    cursor.execute('DROP SCHEMA MY_LIBRARY')


def create_database(cursor):
    cursor.execute('CREATE SCHEMA MY_LIBRARY;')
    cursor.execute('USE	MY_LIBRARY;')
    cursor.execute('CREATE TABLE MY_LIBRARY.EMPLOYEE (Emp_id INT, Fname VARCHAR(25), Lname VARCHAR(25), Address VARCHAR(40), PRIMARY KEY(Emp_id) );')
    cursor.execute('CREATE TABLE MY_LIBRARY.STUDENT (Student_id INT, Fname VARCHAR(25) NOT NULL, Lname VARCHAR(25) NOT NULL, Address VARCHAR(40), book_count INT DEFAULT 0, Money_owed DECIMAL(6, 2) DEFAULT 0.00, PRIMARY KEY(Student_id));')
    cursor.execute('CREATE TABLE MY_LIBRARY.SECTION (Section_number INT, Section_subject VARCHAR(25), PRIMARY KEY(Section_number));')
    cursor.execute('CREATE TABLE MY_LIBRARY.BOOK (Book_id INT, Title VARCHAR(50) NOT NULL, Author VARCHAR(25) NOT NULL, Is_taken bool DEFAULT	FALSE, PRIMARY KEY(Book_id));')
    cursor.execute('CREATE TABLE MY_LIBRARY.BOOK_SECTION (Book_id INT, Section_number INT, PRIMARY KEY(Book_id), FOREIGN KEY(Section_number) REFERENCES MY_LIBRARY.SECTION(Section_number));')
    cursor.execute('CREATE TABLE MY_LIBRARY.LIBRARIAN (Emp_id INT, Section_number INT, PRIMARY KEY(Emp_id, Section_number), FOREIGN KEY(Emp_id) REFERENCES MY_LIBRARY.EMPLOYEE(Emp_id), FOREIGN KEY(Section_number) REFERENCES MY_LIBRARY.SECTION(Section_number));')
    cursor.execute('CREATE TABLE MY_LIBRARY.TECHNICIAN (Emp_id INT, PRIMARY KEY(Emp_id), FOREIGN KEY(Emp_id) REFERENCES MY_LIBRARY.EMPLOYEE(Emp_id));')
    cursor.execute('CREATE TABLE MY_LIBRARY.RENT_BOOK (Renter_id INT, Book_id INT NOT NULL, Due_date DATE NOT NULL, PRIMARY KEY(Renter_id, Book_id), FOREIGN KEY(Book_id) REFERENCES MY_LIBRARY.BOOK(Book_id));')


def populate_database(cursor):
    cursor.execute('INSERT INTO MY_LIBRARY.EMPLOYEE VALUES (123456, "Tim", "Lowe", "124 S Paradise Rd."), (239902, "Thomas", "Rost", "1530 W Dalcross Dr."), (189443, "Liz", "Rost", "1530 W Dalcross Dr.");')
    cursor.execute('INSERT INTO MY_LIBRARY.STUDENT VALUES (14387074, "Andrew", "Stormer", "219 E El Cortez Dr.", 0, 15.00), (21833904, "Evan", "Harlan", "219 E El Cortez Dr.", 0, 0.00), (39019842, "Jake", "Burns", "219 E El Cortez Dr.", 0, 0.00), (13223481, "Sam", "Froelich", "219 E El Cortez Dr.", 0, 0.00), (12345678, "Alex", "Harang", "1284 W Royal St.", 0, 0.00);')
    cursor.execute('INSERT INTO MY_LIBRARY.SECTION VALUES (1, "Non-fiction"), (2, "Biographies"), (3, "Science fiction"), (4, "Historical fiction"), (5, "Dystopia"), (6, "Novel"), (7, "Textbooks");')
    cursor.execute('INSERT INTO MY_LIBRARY.BOOK VALUES (12345, "Moby Dick", "Herman Mellville", False), (11394, "1984", "George Orwell", False), (974, "The Great Gatsby", "F. Scott Fitzgerald", False), (1873, "To Kill a Mockingbird", "Harper Lee", False), (6547, "The Catcher in the Rye", "J. D. Salinger", False), (4431, "Steve Jobs", "Walter Isaacson", False);')
    cursor.execute('INSERT INTO MY_LIBRARY.BOOK_SECTION VALUES (12345, 4), (11394, 5), (974, 6), (1874, 4), (6547, 6), (4431, 2);')
    cursor.execute('INSERT INTO MY_LIBRARY.LIBRARIAN VALUES (123456, 1), (123456, 2), (123456, 3), (189443, 4), (189443, 5), (189443, 6), (189443, 7);')
    cursor.execute('INSERT INTO MY_LIBRARY.TECHNICIAN VALUES (239902);')
    cursor.execute('INSERT INTO MY_LIBRARY.RENT_BOOK VALUES (14387074, 12345, "2023-12-07"), (14387074, 6547, "2023-11-12"), (21833904, 974, "2023-12-4");')


def get_student_id(cursor) -> int:
    while True:
        try:
            while True:
                student_id = input("Input your student id number: ")
                try:
                    stu_id = int(student_id)
                    break
                except ValueError:
                    print("Please enter a valid student id")
            student_query = 'SELECT * FROM MY_LIBRARY.STUDENT WHERE Student_id = {};'.format(student_id)
            cursor.execute(student_query)
            results = list(cursor.fetchall())
            if len(results) == 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid student id.")
    return student_id


def check_out_book(cursor):
    student_id = get_student_id(cursor)
        
    while True:
        try:
            book_name = input("Input the name of the book you would like to check out: ")
            break
        except ValueError:
            print("Please enter a valid book title.")
            
    query = 'SELECT * FROM MY_LIBRARY.BOOK WHERE Title LIKE "%{}%";'.format(book_name)
    cursor.execute(query)

    results = list(cursor.fetchall())
    for (book_id, title, author, is_taken) in results:
        if is_taken == False:
            while True:
                try:
                    rent = input("Book titled {} by {} is avaliable, would you like to check this book out (y/n): ".format(title, author))
                    if "y" not in rent and "n" not in rent:
                        raise ValueError
                    elif rent == 'y':
                        due_date = date.today().strftime("%Y-%m-%d")
                        cursor.execute('INSERT INTO MY_LIBRARY.RENT_BOOK VALUES ({}, {}, "{}");'.format(student_id, book_id, due_date))
                        cursor.execute('UPDATE MY_LIBRARY.STUDENT SET book_count=book_count+1 WHERE Student_id = {};'.format(student_id))
                        cursor.execute('UPDATE MY_LIBRARY.BOOK SET is_taken=True WHERE Book_id = {};'.format(book_id))
                        print("Book checked out!\n\n")
                        return
                    break
                except ValueError:
                    print("Please enter a valid input (y/n).")
    


def return_book(cursor):
    student_id = get_student_id(cursor)

    cursor.execute('SELECT Title FROM MY_LIBRARY.BOOK WHERE Book_id IN (SELECT Book_id FROM MY_LIBRARY.RENT_BOOK WHERE Renter_id = {});'.format(student_id))
    results = list(cursor.fetchall())
    if len(results) == 0:
        print("You can't return books if you don't have any books!\n\n")
        return

    print("Books checked out:\n")
    for title in results:
        print(" - {}".format(title))
    print("\n")
        
    while True:
        try:
            book_name = input("Input the name of the book you would like to return: ")
            break
        except ValueError:
            print("Please enter a valid book title.")
            
    query = 'SELECT * FROM MY_LIBRARY.BOOK WHERE Title LIKE "%{}%";'.format(book_name)
    cursor.execute(query)

    results = list(cursor.fetchall())
    for (book_id, title, author, is_taken) in results:
        while True:
            try:
                cursor.execute('SELECT Due_date FROM MY_LIBRARY.RENT_BOOK WHERE Renter_id = {} AND Book_id = {};'.format(student_id, book_id))
                result = list(cursor.fetchall())
                if len(result) == 0:
                    raise ValueError
                delta = date.today() - result[0][0]
                if delta.days > 14:
                    print("Book being returned is overdue, charging $10 to your account!")
                    cursor.execute('UPDATE MY_LIBRARY.STUDENT SET money_owed=money_owed+10 WHERE Student_id = {};'.format(student_id))
                    
                cursor.execute('DELETE FROM MY_LIBRARY.RENT_BOOK WHERE Renter_id = {} AND Book_id = {};'.format(student_id, book_id))
                cursor.execute('UPDATE MY_LIBRARY.BOOK SET is_taken=False WHERE Book_id = {};'.format(book_id))

                print("Thank you for returning your book, have a nice day!\n\n")
                break
            except ValueError:
                print("You can't return a book that you haven't checked out!\n\n")


def pay_fees(cursor):
    student_id = get_student_id(cursor)

    cursor.execute('SELECT money_owed FROM MY_LIBRARY.STUDENT WHERE Student_id = {}'.format(student_id))
    amount_owed = (list(cursor.fetchall()))[0][0]

    while True:
        try:
            amount_payed = int(input("Please input how much you would like to pay today; "))
            if amount_payed <= 0 or amount_payed > amount_owed:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid amount to pay. It must be greater than $0 and less than or equal to the amount owed!")

    cursor.execute('UPDATE MY_LIBRARY.STUDENT SET money_owed=money_owed-{} WHERE Student_id = {}'.format(amount_payed, student_id))
    cursor.execute('SELECT money_owed FROM MY_LIBRARY.STUDENT WHERE Student_id = {}'.format(student_id))
    print("Money still owed: {}\n\n".format(list(cursor.fetchall())[0][0]))


    
def main():
    try:
        cnx = connector.connect(**config.config)
        cursor = cnx.cursor()
        drop_database(cursor)
        create_database(cursor)
        populate_database(cursor)

        while True:
            while True:
                try:
                    options = int(input("Would you like to:\n(1) Check out a book.\n(2) Return a book.\n(3) Pay overdue fees.\n(4) Exit.\n\nEnter a number 1-4: "))
                    if options < 1 or options > 4:
                        raise ValueError
                    break
                except ValueError:
                    print("Please enter a valid input 1-4.")
            if options == 1:
                check_out_book(cursor)
            elif options == 2:
                return_book(cursor)
            elif options == 3:
                pay_fees(cursor)
            else:
                drop_database(cursor)
                cursor.close()
                cnx.close()
                break    
    except connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)    


if __name__ == '__main__':
    main()
