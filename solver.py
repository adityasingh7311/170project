from parse import read_input_file, write_output_file
import os
from Task import Task

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing
    """

    timeline = [0] * 1440
    scheduledTasks = {} #k: startTimestep v: task_id
    
    tasks.sort(reverse=True, key= lambda t: t.get_max_benefit())

    #change deadlines of tasks that always take a penalty (because duration>deadline) for schedling purposes
    for task in tasks:
        if task.get_deadline() < task.get_duration():
            task.deadline = task.get_duration() 

    for task in tasks:
        #print(task)
        endTimestep = task.get_deadline()#.effective_deadline #-1

        while endTimestep > 0:
            #print("end "+str(endTimestep))
            endTimestep -= 1
            if timeline[endTimestep] != 0:
                continue
            startTimestep = endTimestep - task.get_duration() + 1
            #print("start "+str(startTimestep))
            if startTimestep < 0:
                break

            blocked = False
            for i in range(startTimestep, endTimestep):
                if timeline[i] != 0:
                    blocked = True
                    break
            
            if blocked:
               continue
            
            for i in range(startTimestep, endTimestep + 1):
                timeline[i] = task.get_task_id()

            scheduledTasks[startTimestep] = task.get_task_id()
            break

    firstRoundTasks = list(scheduledTasks.values())


    #schedule any late tasks as soon as possible
    for task in tasks:
        if task.get_task_id() in firstRoundTasks:
            continue
        
        startTimestep = task.get_deadline() - 1

        while startTimestep < 1439:
            #print("start "+str(startTimestep))
            startTimestep += 1
            if timeline[startTimestep] != 0:
                continue
            endTimestep = startTimestep + task.get_duration() - 1
            #print("start "+str(endTimestep))
            if endTimestep >= 1440:
                break

            blocked = False
            for i in range(startTimestep, endTimestep + 1):
                if timeline[i] != 0:
                    blocked = True
                    break
            
            if blocked:
               continue
            
            for i in range(startTimestep, endTimestep + 1):
                timeline[i] = task.get_task_id()

            scheduledTasks[startTimestep] = task.get_task_id()
            break


    orderedTaskSTs = list(scheduledTasks.keys())
    orderedTaskSTs.sort()

    orderedTasks = []

    for k in orderedTaskSTs:
        orderedTasks.append(scheduledTasks[k])
 
    return orderedTasks
    #return timeline

 
#a = Task(6, 10, 5, 45)
#b = Task(7, 10, 15, 45.2)

#x=[Task(1, 237, 23, 61),
#Task(2, 757, 51, 29),
#Task(3, 132, 56, 79),
#Task(4, 185, 41, 69),
#Task(5, 330, 27, 23),
#Task(6, 622, 25, 65),
#Task(7, 1212, 12, 55),
#Task(8, 305, 14, 38),
#Task(9, 1403, 21, 40),
#Task(10, 41, 40, 77)]

#x = [b]
#print(solve(x))


# Here's an example of how to run your solver.
if __name__ == '__main__':
    for size in os.listdir('inputs/inputs/'):
         if size not in ['small', 'medium', 'large']:
             continue
         for input_file in os.listdir('inputs/inputs/{}/'.format(size)):
             if size not in input_file:
                 continue
             input_path = 'inputs/inputs/{}/{}'.format(size, input_file)
             output_path = 'outputs/{}/{}.out'.format(size, input_file[:-3])
             print(input_path, output_path)
             tasks = read_input_file(input_path)
             output = solve(tasks)
             write_output_file(output_path, output)