import mysql.connector as connector
from mysql.connector import errorcode
from datetime import datetime, date
import server_config as config


def get_student_id(cursor) -> int:
    while True:
        try:
            while True:
                student_id = input("Input your student id number: ")
                try:
                    s = int(student_id)
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
    
    query = 'SELECT Title FROM MY_LIBRARY.BOOK WHERE Is_taken = {}'.format(False)
    cursor.execute(query)
    results = list(cursor.fetchall())
    
    print('\n')
    print("Here are the books available to rent:")
    for result in results:
        print(result)
    print('\n')
    
        
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
                #drop_database(cursor)
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



