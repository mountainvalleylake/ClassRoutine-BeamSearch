import random
from queue import PriorityQueue
import copy
t, s, r, c, req = 0, 0, 0, 0, 0
routine = None
room_weight,teacher_weight,class_weight = 0,0,0
file_name1,file_name2 = '',''
class Element:
    def __init__(self, r, c, t):
        #print("Creating an element")
        self.room = r
        self.cls = c
        self.teacher = t

    def get_teacher(self):
        return self.teacher

    def get_class(self):
        return self.teacher

    def get_room(self):
        return self.room

class Routine:
    def __init__(self, day, periods, req):
        self.day = day
        self.periods = periods
        self.req = req
        self.schedule = []
        self.cost = 0
        for i in range(0,self.day):
            self.schedule.append([])
            for j in range(0,self.periods):
                self.schedule[i].append([])

    def get_day(self):
        return self.day

    def get_period(self):
        return self.periods

    def get_schedule(self):
        return self.schedule

    def is_teacher_conflict(self, element1, element2):
        if element1.get_teacher() == element2.get_teacher():
            return 1
        return 0

    def is_class_conflict(self,element1,element2):
        if element1.get_class() == element2.get_class():
            return 1
        return 0

    def is_room_conflict(self,element1,element2):
        if element1.get_room() == element2.get_room():
            return 1
        return 0

    def add_element(self, day, period, element):
        #print("Adding one element")
        self.schedule[day][period].append(element)

    def remove_element(self, day, period, index):
        self.schedule[day][period].__delitem__(index)
        #print("removed it")

    def print_routine(self):
        for i in range(0,self.day):
            print('Day no: ',i)
            for j in range(0,self.periods):
                print('Period No : ',j)
                slot = self.schedule[i][j]
                print('[')
                for k in range(0,len(slot)):
                    item = slot[k]
                    print('t,c,r=',item.get_teacher(),',',item.get_class(),',',item.get_room())
                print(']')
            print('\n')


    def teacher_conflict(self):
        tflict = 0
        for i in range(0,self.day):
            for j in range(0,self.periods):
                slot = self.schedule[i][j]
                for k in range(0,len(slot)):
                    ek = slot[k]
                    for m in range(0,len(slot)):
                        em = slot[m]
                        if k!=m:
                            if ek.get_teacher() == em.get_teacher():
                                tflict += 1

        return tflict

    def class_conflict(self):
        cflict = 0
        for i in range(0, self.day):
            for j in range(0, self.periods):
                slot = self.schedule[i][j]
                for k in range(0, len(slot)):
                    ek = slot[k]
                    for m in range(0, len(slot)):
                        em = slot[m]
                        if k != m:
                            if ek.get_class() == em.get_class():
                                cflict += 1

        return cflict

    def room_conflict(self):
        rflict = 0
        for i in range(0, self.day):
            for j in range(0, self.periods):
                slot = self.schedule[i][j]
                for k in range(0, len(slot)):
                    ek = slot[k]
                    for m in range(0, len(slot)):
                        em = slot[m]
                        if k != m:
                            if ek.get_room() == em.get_room():
                                rflict += 1

        return rflict

    def get_cost(self):
        global teacher_weight,class_weight,room_weight
        self.cost = self.teacher_conflict()*teacher_weight + self.class_conflict()*class_weight\
                    + self.room_conflict()*room_weight
        return self.cost

def Initialize_State(day, period):
    global file_name1,file_name2
    speclist = [] #[teacher,subject,class,room,req]
    File1 = open(file_name1,'r')
    File2 = open(file_name2,'r')
    spstr = ""
    for character in File1.read():
        if character.isdigit():
            spstr += character
        if character == '\n':
            speclist.append(int(spstr))
            #print(spstr)
            spstr = ""
    #print(speclist)
    global t, s, c, r, req
    t = speclist[0]
    s = speclist[1]
    c = speclist[2]
    r = speclist[3]
    req = speclist[4]
    global routine
    routine = Routine(day, period, req)
    sstr = ""
    el = [] #[room-->class-->teacher-->occurance]
    for char in File2.read():
        if char.isdigit():
            sstr += char
        if char == " " or char == '\n':
            #print(sstr)
            el.append(int(sstr))
            sstr = ""
    #print(el)
    i = 0
    for ro in range(r):
        for co in range(c):
            for to in range(t):
                credit = el[i]
                i += 1
                e = Element(ro,co,to)
                for c in range(credit):
                    #the combination is <r0,c0,t0>
                    rday = random.randint(0, day-1)
                    rperiod = random.randint(0, period-1)
                    #print(rday, ' is the day and ', rperiod, ' is the period.')
                    routine.add_element(rday, rperiod, e)
    routine.print_routine()
    print('The initial cost is : ',routine.get_cost())
    return routine
def Get_Children(routine):
    q = PriorityQueue()
    counter = 0
    sch = routine.get_schedule()
    for i in range(0,routine.get_day()):
        for j in range(0,routine.get_period()):
            cell = sch[i][j]
            for k in range(0,len(cell)):
                ek = cell[k]
                for m in range(0,len(cell)):
                    em = cell[m]
                    if (k != m) &(routine.is_teacher_conflict(ek,em)or routine.is_class_conflict(ek,em)
                                  or routine.is_room_conflict(ek,em)):
                        rday = random.randint(0, routine.get_day()-1)
                        rperiod = random.randint(0, routine.get_period()-1)
                        child_routine = copy.deepcopy(routine)
                        #print('i,j,randday,randperiod = ', i, j, rday, rperiod)
                        child_routine.remove_element(i, j, m)
                        child_routine.add_element(rday, rperiod, em)
                        cost = child_routine.get_cost()
                        #print('Child cost is: ', cost)
                        q.put((cost,counter,child_routine))
                        counter += 1
    #print(counter, ' is the count')
    return q


def Beam_search(routine,beam_width):
    ancestor = []
    counter = 0
    ancestor.append(routine)
    best = routine
    while (1):
        q = PriorityQueue()
        for i in range(0, len(ancestor)):
            p = Get_Children(ancestor[i])
            while not p.empty():
                tuplet = p.get()
                obj = tuplet[2]
                ocost = tuplet[0]
                q.put((ocost, counter, obj))
                counter += 1
        tuplett = q.get()
        best_child = tuplett[2]
        if best.get_cost() <= best_child.get_cost():
            return best
        best = best_child
        counter = 0
        ancestor = []
        ancestor.append(best_child)
        for k in range(1,beam_width):
            otuple = q.get()
            o = otuple[2]
            ancestor.append(o)

def main():
    day = 5
    period = 6
    global room_weight,teacher_weight,class_weight
    room_weight = 1
    teacher_weight = 1
    class_weight = 1
    beam_width = 5
    per_cost = 0
    global file_name1,file_name2
    file_name1 = input("Enter the hdttnote file : ")
    file_name2 = input("Enter the hdttreq file : ")
    itnum = int(input('Number of iterations '))
    for i in range(0,itnum):
        routine = Initialize_State(day, period)
        final_routine = Beam_search(routine,beam_width)
        final_routine.print_routine()
        print('Final Routine cost is: ', final_routine.get_cost())
        per_cost += final_routine.get_cost()
    ult_cost = per_cost/itnum
    print('Average cost is : ',ult_cost)
if __name__ == '__main__':
    main()
