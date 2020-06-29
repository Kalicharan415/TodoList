''' Todolist to schedule your task with date '''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date)

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def task_printer(container):
    if len(container) == 0:
        print('Nothing to do!\n')
    else:
        count = 1
        for i in container:
            print('{}. {}'.format(count, i.task))
            count += 1
        print('\n')


def task_adder():
    add_task = input('Enter task\n')
    year,month,day = input('Enter Deadline\n').split('-')
    new_row = Table(task=add_task,
                    deadline=datetime(int(year), int(month), int(day)))
    session.add(new_row)
    session.commit()
    print('The task has been added!\n')


def week_tasks():
    day_delta = timedelta(days=1)

    start_date = datetime.today()
    end_date = start_date + 7 * day_delta

    for i in range((end_date - start_date).days):
        date = start_date + i * day_delta
        print(date.strftime('%A %e %b')+':')
        total = session.query(Table).filter(Table.deadline == date.strftime('%Y-%m-%d')).all()
        task_printer(total)

def missed_task():
    today = datetime.today()
    lines = session.query(Table).filter(Table.deadline < today.strftime('%Y-%m-%d')).all()
    if len(lines) == 0:
        print('Nothing missed!\n')
    else:
        iterate = 0
        for line in lines:
            iterate += 1
            print(str(iterate)+'.',line.task,line.deadline.strftime('%e %b'))
        print('\n')

def delete_task():
    delte_rows = session.query(Table).order_by(Table.deadline).all()
    print('Chose the number of the task you want to delete:')
    i = 0
    for row in delte_rows:
        i += 1
        print(str(i)+'.',row.task,row.deadline.strftime('%e %b'))
    i = 0
    task_delete = int(input())
    if len(delte_rows) == 0:
        print('Nothing to delete')
    else:
        while task_delete != 0:
            session.delete(delte_rows[i])
            i += 1
            task_delete -= 1
            session.commit()
        print('The task has been deleted!\n')
while True:
    print('''1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit''')
    rows = session.query(Table).all()
    value = int(input())
    print('\n')
    if value == 1:
        today = datetime.today()
        print('Today',today.strftime('%e %b')+':')
        rows = session.query(Table).filter(Table.deadline == today.strftime('%Y-%m-%d')).all()
        task_printer(rows)
    elif value == 2:
        week_tasks()
    elif value == 3:
        rows = session.query(Table).all()
        print('All tasks:')
        count = 0
        for i in rows:
            count += 1
            print(str(count)+'.',i.task,i.deadline.strftime('%e %b'))
        count = 0
        print('\n')
    elif value == 4:
        print('Missed tasks:')
        missed_task()
    elif value == 5:
        task_adder()
    elif value == 6:
        delete_task()
    elif value == 0:
        print('\nBye!')
        exit()
