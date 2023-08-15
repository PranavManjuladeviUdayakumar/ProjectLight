import sqlite3
import sys
from datetime import datetime
import tkinter as tk


patterns = {
    'Daily':1,
    'AlternateDays':3,
    'Weekly':7,
    'AlternateWeeks':14,
    'Monthly':30
}


con = sqlite3.connect("Leitner.db")
cur = con.cursor()
cur.execute(f"CREATE TABLE IF NOT EXISTS Topics(Topic, Category)")
cur.execute(f"CREATE TABLE IF NOT EXISTS Details(Category, Pattern, Streak, LastRun)")
con.commit()
today = str(datetime.today().strftime('%Y-%m-%d'))


def insert(topics, category):
    cur.execute(f"INSERT INTO Details VALUES('{category}', 'Daily', 0, '{today}')")
    for topic in topics:
        cur.execute(f"INSERT INTO Topics VALUES('{topic.rstrip().lstrip()}', '{category}')")
    con.commit()


def update(category, pattern, streak=0):
    cur.execute(f"UPDATE Details SET Category = '{category}', Pattern='{pattern}', Streak={streak}, LastRun = '{today}'")
    con.commit()


def remove(category):
    cur.execute(f"DELETE FROM Details WHERE Category = '{category}'")
    cur.execute(f"DELETE FROM Topics WHERE Category = '{category}'")
    con.commit()


def searchcategory():
    return cur.execute("SELECT * from Details").fetchall()


def searchtopic(category):
    return cur.execute(f"SELECT Topic from Topics where Category = '{category}'")


def higher(pattern):
    lst = list(patterns.keys())
    if lst[-1] == pattern:
        return pattern
    else:
        return lst[lst.index(pattern) + 1]
    

def lower(pattern):
    lst = list(patterns.keys())
    if lst[0] == pattern or lst[1] == pattern:
        return lst[0]
    else:
        return lst[lst.index(pattern) - 2]
    

def overdue(lastrun, pattern):
    if (today - datetime.strptime(lastrun, "%Y-%m-%d")).days >= patterns[pattern]:
        return True
    else:
        return False


def is_updateable(pattern, streak):
    if patterns[pattern] <= streak:
        return True
    return False


def proceed(message= "Do you wish to proceed: "):
    ans = input(message).rstrip().lstrip()
    if ans == 'y':
        return True
    return False


def CLI():
    
    mainstr = '''
Available Actions-
                
    1 - Input New Flashcards
    2 - Remove Flashcard Category
    3 - Practice 
    4 - Exit

Input Action Number: '''
    
    while True:

        action = input(mainstr).strip()

        if action == '1':
            
            print("\nData Input Selected\n")
            print("You will be asked to enter the category under which the topics fall under, and then the topics themselves. \nEnter the topics together, separated by a comma (,)\n")
            category = input("Enter Category: ")
            topics = input("Enter all topics: ").split(',')

            print("Review topics to be added-")
            for i in topics:
                print(i.lstrip().rstrip(), category)
            if proceed():
                insert(topics, category)
            else:
                print("Action Aborted")

        elif action == '2':
            
            print("\nData Removal Selected\n")
            print("Enter the name of the category for whose data is to be deleted. NOTE: ALL records of a category will be removed.")
            category = input("Category: ")

            print("Review topics to be deleted-")
            for i in searchtopic(input("Topic: ")):
                print(i)
            if proceed():
                remove(category)
            else:
                print("Action Aborted")

        elif action == '3':

            print("\nPractice Mode\n")
            print("You will be presented topics that are due for revision. \nDepending on your comfortability enter 'y' if you are sure of the topic, or 'n' if you aren't. \nThe more often a topic appears for you, the more revision you must do on the entire category. \nThe more comfortable you are with a category, the less it will appear for you.")
            
            if proceed():

                print("Processing categories that need revision...")
                queue = set()

                for category, pattern, streak, lastrun in searchcategory():

                    if overdue(lastrun, pattern):

                        queue.add(category, pattern, streak)
                
                print("Categories processed!")
                mistakequeue = set()

                for i in queue:

                    mistake = False
                    print(f"Category to be revised: {i[0]}")

                    for i in searchtopic(i[0]):
                        print("Topic: ", i[0])
                        if not proceed(message="Are you comfortable with this topic (y/n): "):
                            mistake = True

                    if mistake:
                        mistakequeue.add(i)

                print("All Categories Revised!")
                print("Updating Frequency Charts...")

                for i in (queue - mistakequeue):

                    category, pattern, streak = i
                    streak +=1

                    if is_updateable(pattern, streak):

                        pattern = higher(pattern)
                        update(category, pattern)

                    else:

                        update(category, pattern, streak)

                for i in mistakequeue:

                    category, pattern, streak = i
                    pattern = lower(pattern)

                    update(category, pattern)


        elif action == '4':

            con.close()
            print("Exiting...")
            sys.exit()

        else:

            print("Invalid Usage. Enter Numbers from 1 - 4 only.")


def GUI():
    raise NotImplementedError

#Main
print(f'''
----------------------------------
               
        Project Light [CLI]
               
            -Pranav Udayakumar

----------------------------------
©️2022-{datetime.now().year}
''')

while True:
    print('''Availabel Modes-
    1 - CLI
    2 - GUI
    3 - Exit
''')
    action = input("Enter Mode: ").strip()

    if action == '1':

        CLI()

    elif action == '2':

        GUI()
        break

    elif action == '3':

        con.close()
        print('Exiting...')
        sys.exit()

    else:

        print("Invalid Usage. Enter Numbers from 1-3 only")

    
