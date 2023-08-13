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


def insert(titles, category):
    cur.execute(f"INSERT INTO Details VALUES('{category}', 'Daily', 0, '{today}')")
    for title in titles:
        cur.execute(f"INSERT INTO Topics VALUES('{title}', '{category}')")
    con.commit()


def update(pattern, category, streak=0):
    cur.execute(f"UPDATE Details SET Category = '{category}', Pattern='{pattern}', Streak={streak}, LastRun = '{today}'")
    con.commit()


def searchcategory():
    return cur.execute("SELECT Category from Details").fetchall()


def searchtopic(category):
    return cur.execute(f"SELECT Topic from Topics where Category = '{category}'")


def higher(pattern):
    if list(patterns.keys())[-1] == pattern:
        return pattern
    else:
        return list(patterns.keys())[list(patterns.keys()).index(pattern) + 1]
    

def lower(pattern):
    if list(patterns.keys())[0] == pattern:
        return pattern
    else:
        return list(patterns.keys())[list(patterns.keys()).index(pattern) - 1]
    

def overdue(lastrun, pattern):
    if (today - datetime.strptime(lastrun, "%Y-%m-%d")).days >= patterns[pattern]:
        return True
    else:
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
            print("Input")
        elif action == '2':
            print("Remove")
        elif action == '3':
            print("Remove")
        elif action == '4':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid Usage. Enter Numbers from 1 - 4 only.")


def GUI():
    print("GUI")


print('''
----------------------------------
               
        Project Light [CLI]
               
            -Pranav Udayakumar

----------------------------------
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
        print('Exiting...')
        sys.exit()
    else:
        print("Invalid Usage. Enter Numbers from 1-3 only")

    
