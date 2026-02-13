from datetime import timedelta
from .models import Visit

#this function takes in a participant and the visit details of the participant, then it schedules it on those days.
#the participant is nothing but a row from the participant table and visit_defs (visit definitions) is a list of dictionaries. The structure of visit_defs is same as VISIT_SCHEDULE in "protocol.py"
def schedule_visits_for_participant(participant, visit_defs):
    #the baseline date of the participant which is when they enroll
    baseline_date = participant.enrolled_at
    #is participant is already scheduled then dont continue
    if participant.visits.exists():
        return

    visits = []

    for v in visit_defs:
        #we calculate the due_date by adding the target_day to the baseline. The target_day can be either 0, 90 or 365. We add it to participant's baseline_date to get due_date
        #target_day is a int so we convert it to a date object and add it to baseline_date (another date object) to create due_date (date object)
        due_date = baseline_date + timedelta(days=v["target_day"])
        #create a new visit model object using the new due_date
        visits.append(
            Visit(
                #the participant foreign key is the current participant
                participant=participant,
                visit_code=v["visit_code"],
                due_date=due_date,
                #window_start is a date not days so we need to subtract window_before from due_date to get window_start
                window_start=due_date - timedelta(days=v["window_before"]),
                window_end=due_date + timedelta(days=v["window_after"]),
                status="scheduled",
                #actual_date will be none as it'll be scheduled when the participant comes for the test
                actual_date=None
            )
        )
    
    #save all the visit objects to db
    Visit.objects.bulk_create(visits)