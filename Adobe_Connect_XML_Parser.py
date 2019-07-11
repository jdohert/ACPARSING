from collections import defaultdict
from bs4 import BeautifulSoup
from collections import Counter
from copy import copy
import glob


def get_student_roster(student_roster_csv_file_path):
    #read csv to get list of students in class store as list
    student_roster =
def get_student_ids(index_stream_xml_path,student_roster):
    '''make two separate dictionaries with the same keys (student names) one for pids and one for ids. Pids are used in
    chat transcripts and ids are used in camera, mic, and handsup tracking
    '''
    #get pID dict with Pid if student attended and zero if student did not attend
    student_placeholder =  dictionary with names from student roster as keys and zero value for pID and Id
    pIDS = make dict with name as key and pid as value from attendees
    student_pID = add student_placeholder and pIDS together

    #get id dict
    student_placeholder = dictionary with names from student roster as keys and zero value for pID and Id
    ids = make dict with name as key and pid as value from attendees
    student_id = add student_placeholder and pIDS together
def get_camera_contributions(index_stream_xml):
    #make dict of time on camera with student id as key
    camera_time = dict with id as key and time on camera as value
    replace id with student name from student_id dict

def get_microphone_contributions(index_stream_xml):
    #make dict of microphone events with student id as key
    on_mic_times = dict with id as key and times mic turned on as value
    replace id with student name from student_id dict

def get_handsup_contributions(index_stream_xml):
    # make dict of handsup events with student id as key
    handsup_events = dict with id as key and handsup events as value
    replace idmwith student name from student_id dict

def get_chat_contributions(ft_chat):
    # make dict of chat contributions with pID as key
    chat_contributions = dict with id as key and handsup events as value

def get_contribution_summary(student_ids,cam_contributions,mic_contributions,handsup_contributions, chat_contributions):
    # append all the dictionaries together


recording_folder_path = '/Users/JeffHalley/Adobe Connect Project/adobe connect recording files/'


def get_index_stream_xml_path(recording_folder_path):
    indexstream = "indexstream.xml"
    return recording_folder_path+indexstream

def get_student_ids_and_pIDs(index_stream_xml_path):
    with open(index_stream_xml_path) as filepath:
        index_stream = BeautifulSoup(filepath,"xml")
    #this will return a result set that can be used as an index to find 
    #the record that contains id and pID for each student
    student_names_index = index_stream.find_all('fullName')
    student_names = []
    id_numbers = []
    pID_numbers = []
    for item in range(len(student_names_index)):
        #use the name index to access the actual name and add it to the list of names
        student_name = student_names_index[item].parent.fullName.text
        '''sometimes students have connection issues and they end up with multiple
        logins with their name followed by a number, for this reason the
        following is done to remove any numbers from names'''
        student_name = ''.join([i for i in student_name if not i.isdigit()])
        student_names.append(student_name)
        #use the name index to find the student id number for the student
        id_number = student_names_index[item].find_next_sibling("id").text
        id_numbers.append(id_number)
        # use the name index to find the the pID for each student and add to list
        pID_number = student_names_index[item].find_next_sibling("pID").text
        pID_numbers.append(pID_number)
    
    '''make dict with student ID or pID and student name. Reverse list is used 
        because sometimes students change names, but the first name is always
        as listed in class roster, also note sometimes students are kicked out
        and log back in and thus given a new ID and pID, this will be dealt
        with when names are subbed in for IDs at the end of each results
        collection function'''
    
    student_ids = dict(zip(list(reversed(id_numbers)),list(reversed(student_names))))
    student_pIDs = dict(zip(list(reversed(pID_numbers)),list(reversed(student_names))))
    return student_ids, student_pIDs
    #future plans: take a second argument a student roster cvs file make a dict
    #with zeroes for all students to act as a placeholder. Then use combined
    #dict from insight project. to give students with no record a zero

    
def get_results_by_name_from_results_by_id(dict_of_results_by_id,student_ids):
    ids = list(dict_of_results_by_id.keys())
    names_subbed_for_ids = [student_ids.get(item,0) for item in ids]
    results = list(dict_of_results_by_id.values())
    results_with_names_subbed_for_ids = defaultdict(list)
    for names, results in zip(names_subbed_for_ids,results):
        results_with_names_subbed_for_ids[names].append(results) 
    return({k:sum(v) for k,v in results_with_names_subbed_for_ids.items()})
    
    return results_with_names_subbed_for_ids

def get_ftstage_file_path(recording_folder_path):
    ftstage_wildcard = "ftstage*.xml"
    ftstage_file_path = glob.glob(recording_folder_path+ftstage_wildcard)
    return ftstage_file_path[0]
    
def get_camera_contributions(index_stream_xml_path,ftstage_file_path,student_ids):
    with open(index_stream_xml_path) as filepath:
        index_stream = BeautifulSoup(filepath,"xml")
    #get time when student came on camera
    camera_starts_index = index_stream.find_all(string = 'streamAdded')
    camera_start_ids = []
    camera_start_times = []
    for item in range(len(camera_starts_index)):
        #get id number of student that started their camera
        camera_start_id = camera_starts_index[item].parent.parent.streamPublisherID.text
        camera_start_ids.append(camera_start_id)
        #get time that student started their camera
        camera_start_time = int(camera_starts_index[item].parent.parent.startTime.text)
        camera_start_times.append(camera_start_time)
    student_camera_start_times = defaultdict(list)
    for student_id, start_time in zip(camera_start_ids,camera_start_times):
        student_camera_start_times[student_id].append(start_time) 
      
    #get time when student turned off camera
    stream_removed_index = index_stream.find_all(string = 'streamRemoved')
    stream_removed_ids = []
    stream_removed_times = []
    for item in range(len(stream_removed_index)):
        #get id number of student that stopped their camera
        stream_removed_id = stream_removed_index[item].parent.parent.streamPublisherID.text
        stream_removed_ids.append(stream_removed_id)
        #get time that student stopped their camera
        stream_removed_time = int(stream_removed_index[item].parent.parent.time.text)
        stream_removed_times.append(stream_removed_time)
  
    #get time when student loses connection
    user_deleted_index = index_stream.find_all(string = 'userDeleted')
    user_deleted_ids = []
    user_deleted_times = []
    for item in range(len(user_deleted_index)):
        #get id number of student that loses connection
        user_deleted_id = user_deleted_index[item].parent.parent.parent.Number.text
        user_deleted_ids.append(user_deleted_id)
        #get time that student that loses connection
        user_deleted_time = int(user_deleted_index[item].parent.parent.parent.time.text)
        user_deleted_times.append(user_deleted_time)

    
    #merge lists of stream removed and stream ids b/c both are ways camera stops
    camera_stops_ids = stream_removed_ids + user_deleted_ids
    camera_stops_times = stream_removed_times + user_deleted_times
    #initialize a default dict that has the same keys as the student_camera_start_times dict 
    student_camera_stop_times = defaultdict(list)
    for k in student_camera_start_times.keys():
        student_camera_stop_times[k]
    for student_id, stop_time in zip(camera_stops_ids,camera_stops_times):
        student_camera_stop_times[student_id].append(stop_time)
    
    '''
    having students with ids but with no camera time interfere with later calcs
    so I will give all of the students that did not appear on camera a start
    and end time that is is the same as the end of class
    '''
     
    for k in student_camera_stop_times.keys():
        if len(student_camera_start_times[k]) == 0:
            student_camera_stop_times[k] = [0]
            student_camera_start_times[k].append(0)
              
    #determine total time on camera
    student_minutes_on_camera = defaultdict(int)
    student_fraction_of_class_on_camera = defaultdict(int)
    for k in student_camera_stop_times.keys():
        times = [a-b for a,b in zip(student_camera_stop_times[k],student_camera_start_times[k])]
        total_time = sum(times)/1000/60
        fraction_of_class_time_on_camera = (sum(times)/end_of_class_time)
        student_minutes_on_camera[k] += total_time
        student_fraction_of_class_on_camera[k] += fraction_of_class_time_on_camera
        
    #get total time student pauses camera
    with open(ftstage_file_path) as filepath:
        ftstage = BeautifulSoup(filepath,"xml")
    pause_change_index = ftstage.find_all(string ="updateVideoPauseStatus")
    pause_start_ids = []
    pause_start_times = []
    pause_stop_ids = []
    pause_stop_times = []  
    for item in range(len(pause_change_index)):
        if pause_change_index[item].parent.parent.String.find_next_sibling("String").text == 'true':
            pause_start_times.append(int(pause_change_index[item].parent.parent.Object.time.text))
            pause_start_ids.append(pause_change_index[item].parent.parent.String.find_next_sibling("Number").text)
        else:
            pause_stop_times.append(int(pause_change_index[item].parent.parent.Object.time.text))
            pause_stop_ids.append(pause_change_index[item].parent.parent.String.find_next_sibling("Number").text)
    student_pause_start_times = defaultdict(list)
    for student_id, start_time in zip(pause_start_ids,pause_start_times):
        student_pause_start_times[student_id].append(start_time)
    student_pause_stop_times = defaultdict(list)
    for student_id, stop_time in zip(pause_stop_ids,pause_stop_times):
        student_pause_stop_times[student_id].append(stop_time)
        #the first pause_stop_time is when the student turns on their camera so it will be discarded
        #trimmed_student_pause_stop_times = {k: student_pause_stop_times[k][1:] for k in student_pause_stop_times}
    
    '''sometimes a student loses connection or ends stream. when they reconnect 
    a stop pause is recorded to get rid of these false stops I will use the 
    camera_start_times to identify them (they occur within 100 ms of the camera
    start event). Since I've already trimmed the false stop from 
    the first camera start event. I will trim all of those from the camera starts
    list. Also, I can't just use the within 100 ms method to eliminate the first 
    camera start events because if a student's camera is turned on before the
    recording starts it is recorded as much as 3000 ms before the false stop
    event'''

    #give every student that didn't come on camera a zero pause stop time
    for k in student_camera_stop_times.keys():
        if len(student_pause_stop_times[k]) == 0:    
            student_pause_stop_times[k].append(0)
    
    #get rid of pause times that occur when a student loses connection and relogs   
    #trimmed_student_camera_start_times = {k: student_camera_start_times[k][1:] for k in student_camera_start_times}
    
    for k in student_camera_start_times.keys():
        for camera_start_time in reversed(range(len(student_camera_start_times[k]))):
            for pause_stop_time in reversed(range(len(student_pause_stop_times[k]))):
                    if (
                        student_pause_stop_times[k][pause_stop_time]-student_camera_start_times[k][camera_start_time] > 0 and
                        
                        student_pause_stop_times[k][pause_stop_time] < student_camera_start_times[k][camera_start_time]+100
                        ):   
                        del(student_pause_stop_times[k][pause_stop_time])
                        
                        
                        print(k,pause_stop_time,student_pause_stop_times[k][pause_stop_time])



                   #del(student_pause_stop_times[k][pause_stop_time])
     
    for k in student_camera_start_times.keys():
        #print("k:",k)
        for camera_start_time in range(len(student_camera_start_times[k])):
            #print("camera_start_time:",camera_start_time)
            for pause_stop_time in range(len(student_pause_stop_times[k])):
                print("statement1:",student_pause_stop_times[k][pause_stop_time])
                print("statement2:",student_camera_start_times[k][camera_start_time])
                print("arguemnt1:",student_pause_stop_times[k][pause_stop_time]-student_camera_start_times[k][camera_start_time]>1 )
                print("arguemnt2:",student_pause_stop_times[k][pause_stop_time]-student_camera_start_times[k][camera_start_time]<student_camera_start_times[k][camera_start_time]+100)



                print("pause_stop_time:",pause_stop_time)
        
        print(camera_start_time in range(len(student_camera_start_times[k])))
              
        :
            print(k,camera_start_time)
            
            
            for pause_stop_time in range(len(student_pause_stop_times[k])):
                
        
    
#    for k in trimmed_student_pause_stop_times.keys():
#        if len(trimmed_student_pause_stop_times[k])>len(student_pause_start_times[k]):
#            del(trimmed_student_pause_stop_times[k][len(trimmed_student_pause_stop_times[k])-1])
    
    #set end of class time for students that pause until the end of class    
    for k in trimmed_student_pause_stop_times.keys():
        if len(trimmed_student_pause_stop_times[k])<len(student_pause_start_times[k]):
            trimmed_student_pause_stop_times[k].append(end_of_class_time)
    
    #determine total time on camera
    student_minutes_with_camera_paused = defaultdict(int)
    for k in trimmed_student_pause_stop_times.keys():
        times = [a-b for a,b in zip(trimmed_student_pause_stop_times[k],student_pause_start_times[k])]
        total_time = sum(times)/1000/60
        student_minutes_with_camera_paused[k] += total_time
    
    
    #get id of instructor
    instructor_id = index_stream.find("myID").text
        
    
    #determine fraction of time student is on mic compared to instructor
    instructor_time_on_camera = student_minutes_on_camera[instructor_id]
    student_fraction_of_instructor_time_on_camera = {k:v / instructor_time_on_camera for k,v in student_minutes_on_camera.items()}
    student_fraction_of_instructor_time_on_camera = defaultdict(int, student_fraction_of_instructor_time_on_camera )
    
    
    return (
    get_results_by_name_from_results_by_id(student_minutes_on_camera,student_ids),
    get_results_by_name_from_results_by_id(student_fraction_of_class_on_camera,student_ids),
    get_results_by_name_from_results_by_id(student_fraction_of_instructor_time_on_camera,student_ids)
            )
    
    
def get_microphone_contributions(index_stream_xml_path,student_ids):
    with open(index_stream_xml_path) as filepath:
        index_stream = BeautifulSoup(filepath,"xml")
    #get times when student has a microphone change (turns it on OR off)
    mic_change_index = index_stream.find_all(string = 'userVoipStatusChanged')
    mic_start_ids = []
    mic_start_times = []
    mic_stop_ids = []
    mic_stop_times = []
    for item in range(len(mic_change_index)):
        #look in index of microphone changes to find instances where student turned mic on (started talking)
        if (
                mic_change_index[item].parent.parent.parent.String.find_next_sibling("String").text == 'true' and
                mic_change_index[item].parent.parent.parent.String.find_next_sibling("String").find_next_sibling("String").text == 'false'
            ):
            mic_start_ids.append(mic_change_index[item].parent.parent.parent.String.text)
            mic_start_times.append(int(mic_change_index[item].parent.find_next_sibling("time").text))
        elif mic_change_index[item].parent.parent.parent.String.find_next_sibling("String").find_next_sibling("String").text == 'false':
            mic_stop_ids.append(mic_change_index[item].parent.parent.parent.String.text)
            mic_stop_times.append(int(mic_change_index[item].parent.find_next_sibling("time").text))
    student_mic_start_times = defaultdict(list)
    for student_id, start_time in zip(mic_start_ids,mic_start_times):
        student_mic_start_times[student_id].append(start_time)
    student_mic_stop_times = defaultdict(list)
    for student_id, stop_time in zip(mic_stop_ids,mic_stop_times):
        student_mic_stop_times[student_id].append(stop_time)
    
    #get end of class time
    end_of_class_object = index_stream.find_all(text = '__stop__')   
    end_of_class_time = int(end_of_class_object[len(end_of_class_object)-1].parent.parent.Number.text)
    
   
    #determine total time on microphone
    student_minutes_on_microphone = defaultdict(int)
    student_fraction_of_class_on_microphone = defaultdict(int)
    
    for k in student_mic_stop_times.keys():
        times = [a-b for a,b in zip(student_mic_stop_times[k],student_mic_start_times[k])]
        total_time = sum(times)/1000/60
        fraction_of_class_time_on_microphone = (sum(times)/end_of_class_time)
        
        student_minutes_on_microphone[k] += total_time
        student_fraction_of_class_on_microphone[k] += fraction_of_class_time_on_microphone
    
    #get id of instructor
    instructor_id = index_stream.find("myID").text
        
    
    #determine fraction of time student is on mic compared to instructor
    instructor_time_on_mic = student_minutes_on_microphone[instructor_id]
    student_fraction_of_instructor_mic = {k:v / instructor_time_on_mic for k,v in student_minutes_on_microphone.items()}
    student_fraction_of_instructor_mic = defaultdict(int, student_fraction_of_instructor_mic )
    
    
    return (
    get_results_by_name_from_results_by_id(student_minutes_on_microphone,student_ids),
    get_results_by_name_from_results_by_id(student_fraction_of_class_on_microphone,student_ids),
    get_results_by_name_from_results_by_id(student_fraction_of_instructor_mic,student_ids)
            )
    
    
        
 results1,results2,results3 = get_microphone_contributions(index_stream_xml_path,student_ids)
 
 results1,results2,results3 = get_camera_contributions(index_stream_xml_path,student_ids)
 test= get_results_by_name_from_results_by_id(results1,student_ids)
 
 test,test2 = get_microphone_contributions(index_stream_xml_path)
