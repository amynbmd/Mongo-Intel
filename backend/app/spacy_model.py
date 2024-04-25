# Author: Han Thai

import spacy
import re
from datetime import datetime, date, time
from datetime import timedelta

# This function takes in a question and returns a MongoDB query
def convert_question_to_query(question):
    nlp = spacy.load("en_core_web_sm")
    #if question include the word in a list, remove the word from the question
    remove_words = ["location", "the"]
    for word in remove_words:
        question = re.sub(r'\b' + word + r'\b', '', question, flags=re.IGNORECASE)

    doc = nlp(question)
    
    #initialize time string and date string
    timeString = None
    dateString = None
    
    # Initialize query components
    _id = None 
    index = None
    entity_id = None
    name = None
    description = None
    location = None
    elevation = None
    timestamp = None
    bearing = None
    speed = None

    #print the all tokens of the question
    for token in doc:
        print("text: " + token.text, ", dep: " + token.dep_,", pos: "+ token.pos_, ", type: "+ token.ent_type_)

    # Extract the MAIN subject from the question (simple question)
    sub_toks = next((tok for tok in doc if tok.dep_ == "nsubj" or tok.pos == "PERSON" or tok.ent_type_ == "PERSON"),None)
    #if no subject is found, extract tok with format "name-id"
    if not sub_toks:
        sub_toks = next((tok for tok in doc if re.match(r'\b^[a-zA-Z]+-\d+\b$', tok.text)), None)
    print("SUBJECT TOKENS: "+ str(sub_toks))
    #if no subject is found, extract the root that is not an auxiliary verb or preposition or verb
    if not sub_toks:
        sub_toks = next((tok for tok in doc if tok.dep_ == "ROOT" and tok.pos_ != "AUX" and tok.pos_ != "ADP" and tok.pos_ != "VERB"), None)
    #if no subject is found, extract the first noun or proper noun
    if not sub_toks:
        sub_toks = next((tok for tok in doc if tok.pos_ == "PROPN" or tok.pos_ == "NOUN" and not "AM" or not "PM"), None)
    name = str(sub_toks) if sub_toks else "None Found"
    name = name.replace("]", "") if name else "None Found"
    name = name.replace("[", "") if name else "None Found"
    #print("SUBTOK: "+ str(sub_toks)) if sub_toks else print("SUBTOK: None Found") 
    print("SUBJECT: "+ name) 
    
    #This part is for description extracted
    for tok in doc:
        if tok.pos_ == "ADJ" and tok.ent_type_ != "DATE":
            if description:
                description += " " + tok.text
            else:
                description = tok.text

    # Extract information from the question
    for ent in doc.ents:
        print(ent.text, ent.label_)
        if ent.label_ == "PERSON" and name == "None Found":
            name = ent.text
        if ent.label_ == "TIME":
            if timeString:
                timeString += " " + ent.text
            else:
                timeString = ent.text
        elif ent.label_ == "DATE":
            if dateString:
                dateString += " " + ent.text
            else:
                dateString = ent.text
        #if the entity is a cardinal number but in pattern format, add to date string
        elif ent.label_ == "CARDINAL" and re.match(r'^(\d{1,2})/(\d{1,2})(/(\d{2,4}))?$', ent.text):
            if dateString:
                dateString += " " + ent.text
            else:
                dateString = ent.text
        #if the entity is a cardinal number but in pattern format, add to time string
        elif ent.label_ == "CARDINAL" and re.match(r'^(\d{1,2}):(\d{1,2})?\s?(am|pm)?$', ent.text):
            if timeString:
                timeString += " " + ent.text
            else:
                timeString = ent.text        
        elif ent.label_ == "GPE": #if the entity is a geopolitical entity, concat to description
            if description:
                description += " " + ent.text
            else:
                description = ent.text
        elif ent.label_ == "LOC":           
            if description:
                description += " " + ent.text
            else:
                description = ent.text
        elif ent.label_ == "ORG":
            if description:
                description += " " + ent.text
            else:
                description = ent.text
               
    print("TIME_STRING: " + str(timeString)) 
    print("DATE_STRING: " + str(dateString))   
    # Convert time and date strings to datetime objects
    timestamp = convert_time_to_mongo_format(timeString, dateString)
    print("TIMESTAMP: " + str(timestamp))
    newDate = timestamp.date()
    print("DATE: " + str(newDate)+ "\n")

    # Create the MongoDB query
    query = "db.PositionSnapshot.findOne({\n"
    if name:
        query += f'  "name": "{name}",\n'
    if timestamp:
        # Convert to MongoDB Date format and set the range
        start_time = str(timestamp.date()) + "T" + str(timestamp.time()) # Start of the hour
        end_hour = timestamp + timedelta(hours=24)
        end_time = str(end_hour.date()) + "T" + str(end_hour.time()) # End of the hour
        query += f'  "timestamp": {{\n    "$gte": "{start_time}",\n    "$lt": "{end_time}"\n  }},\n'
    if description:
        query += f'  "description": "{description}",\n'
    query = query[:-2]  # Remove trailing comma and space
    query += ", {_id: 0, location: 1}\n})"
    return query


def convert_time_to_mongo_format(time_string, date_string):
    #initialize timestamp as time right now without microsecond
    timestamp = datetime.now().replace(microsecond=0)
    if(date_string != None):
        date_string = date_string.lower()
        month_names = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
                        "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
                        "jan" : 1, "feb": 2, "mar": 3, "apr": 4, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}
        # Check if any day of the week is in the string
        days = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6}
        day_found = any(day in date_string for day in days) #use later#check if the date already contains time
        
        time_pattern = r'\b(\d{1,2})(?::(\d{2}))?\s?(am|pm)?\b'
        invalid_time_pattern = r'^(\d{1,2})\s*[/-]\s*(\d{1,2})\s*[/-]\s*(\d{4})$'
        match = re.search(time_pattern, str(date_string), re.IGNORECASE)
        match_invalid = re.search(invalid_time_pattern, str(date_string), re.IGNORECASE)
        if match and time_string == None and not match_invalid:
            hour = match.group(1) # Extract the hour
            print("HOUR: " + hour)
            minute = match.group(2) # Extract the minute
            print("MINUTE: " + str(minute))
            am_pm = match.group(3) # Extract the AM/PM 
            # Construct the time string based on the matched groups
            time_string = hour
            if minute:
                time_string += f":{minute}"
            if am_pm:
                time_string += f" {am_pm.lower()}"
            print("TIME SELF-BUILT: " + time_string)
            
        #if a day of a week is found (e.g. "next Monday", "last Monday", "this Monday" or "Monday")
        res = date.today()
        
        if day_found:
            today = date.today()
            today_weekday = today.weekday()

            for day, day_index in days.items():
                if day in date_string:
                    day_diff = day_index - today_weekday  # Days until 'day'

                    if "next" in date_string:
                        day_diff += 7 if day_diff <= 0 else 0
                    elif "last" in date_string:
                        day_diff -= 7 if day_diff >= 0 else 0
                    # 'this' week or no week specifier does not change day_diff
                    res = today + timedelta(days=day_diff)
                    break  # Found the day, no need to continue the loop
        date_val = res  # Store the resul
        pass        

        #if the date contain "today"
        if "today" in date_string:
            date_val = date.today()
        #if the date contain "tomorrow"
        elif "tomorrow" in date_string:
            date_val = date.today() + timedelta(days=1)
        #if the date contain "yesterday"
        elif "yesterday" in date_string:
            date_val = date.today() - timedelta(days=1)
        #if the date is in all other formats
        else: 
            date_patterns = [
            (r'^(\d{4})$', lambda y: date(int(y), 1, 1)),  # yyyy
            (r'^(\d{2})\s*[/-]\s*(\d{4})$', lambda m, y: date(int(y), int(m), 1)),  # mm/yyyy
            (r'^(\d{1,2})\s*[/-]\s*(\d{1,2})\s*[/-]\s*(\d{4})$', lambda m, d, y: date(int(y), int(m), int(d))),  # mm/dd/yyyy or mm-dd-yyyy
            (r'^(\d{1,2})\s*[/-]\s*(\d{1,2})$', lambda m, d: date(date.today().year, int(m), int(d))),  # mm/dd
            (r'^(\d{2})$', lambda d: date(date.today().year, date.today().month, int(d))),  # dd
            (r'^(january|february|march|april|may|june|july|august|september|october|november|december) (\d{1,2})\s*(?:th|st|nd|rd)?\s*,?\s*(\d{4})$', 
                lambda month, day, year: date(int(year), month_names[month], int(day))), # month dd, yyyy
            (r'^(jan|feb|mar|apr|may|june|jul|aug|sep|oct|nov|dec) (\d{1,2})\s*(?:th|st|nd|rd)?\s*,?\s*(\d{4})$', 
                lambda month, day, year: date(int(year), month_names[month], int(day))), # month dd, yyyy
            (r'^(january|february|march|april|may|june|july|august|september|october|november|december) (\d{1,2})\s*(?:th|st|nd|rd)?$',
                lambda month, day: date(date.today().year, month_names[month], int(day))), #month dd
            (r'^(jan|feb|mar|apr|may|june|jul|aug|sep|oct|nov|dec) (\d{1,2})\s*(?:th|st|nd|rd)?$',
                lambda month, day: date(date.today().year, month_names[month], int(day))), #month dd                
            (r'^(january|february|march|april|may|june|july|august|september|october|november|december) (\d{1,2})\s*(?:th|st|nd|rd)?\s*next?\s*year$', 
                lambda month, day: date(date.today().year+1, month_names[month], int(day))), # month dd next year  
            (r'^(jan|feb|mar|apr|may|june|jul|aug|sep|oct|nov|dec) (\d{1,2})\s*(?:th|st|nd|rd)?\s*next?\s*year$', 
                lambda month, day: date(date.today().year+1, month_names[month], int(day))) # month dd next year         
            ]
            # Check each pattern and apply the corresponding logic
            for pattern, func in date_patterns:
                match = re.match(pattern, date_string)
                if match:
                    date_val = func(*match.groups())
                    break

    else:
        date_val = date.today()

    if(time_string != None):
        time_string = time_string.lower()

        #if the time is in the format of "hh:mm" or "h:mm" or "hh:mm am/pm" or "h:mm am/pm" using patterns
        if re.match(r'^(\d{1,2}):(\d{1,2})\s?(am|pm)?$', time_string):
            if "pm" in time_string:
                hour = int(time_string.split(":")[0])
                hour += 12
                time_string = time_string.replace("pm", "")
                minute = int(time_string.split(":")[1])
            elif "am" in time_string:
                hour = int(time_string.split(":")[0])
                time_string = time_string.replace("am", "")
                minute = int(time_string.split(":")[1])
            else:
                hour = int(time_string.split(":")[0])
                minute = int(time_string.split(":")[1]) 
            time_val = time(hour, minute)
        
        #if the time is in the format of "hh" or "h"
        elif len(time_string) == 5 and time_string.split(":")[0].isdigit() and time_string.split(":")[1].isdigit():
            time_val = time(int(time_string.split(":")[0]), int(time_string.split(":")[1]))
        #if the time contain hh and am/pm
        elif len(time_string) > 2 and ("am" in time_string or "pm" in time_string):
            if "am" in time_string:
                time_string = time_string.split("am")[0]
                time_val = time(int(time_string), 0)
            elif "pm" in time_string:                
                time_string = time_string.split("pm")[0]
                time_val = time(int(time_string) + 12, 0)
            elif len(time_string) == 2 and time_string.isdigit():
                time_val = time(int(time_string), 0)
            elif (len(time_string) == 5 and time_string.split(":")[0].isdigit() and time_string.split(":")[1].isdigit() ):
                time_val = time(int(time_string.split(":")[0]), int(time_string.split(":")[1]))                             
        #if the time is in the format of "hh" or "h"
        elif time_string.isdigit() and int(time_string) < 24: 
            time_val = time(int(time_string), 0)
        #if the time contain "now"    
        elif "now" in time_string or "now" in str(date_string):
            timestamp = datetime.now()
        else:
            if "morning" in str(time_string):
                time_val = time(6, 0)
            if "noon" in str(time_string):
                time_val = time(12, 0)
            if "afternoon" in str(time_string):
                time_val = time(13, 0)
            if "evening" in str(time_string):
                time_val = time(18, 0)
            if "night" in str(time_string):
                time_val = time(20, 0)
            if "midnight" in str(time_string):
                time_val = time(0, 0)
    else:
        time_val = time(1,0)  # If the time is not specified, default to 1:00  
    
    if(timestamp != datetime.now()):
        timestamp = datetime.combine(date_val, time_val) # Combine the date and time into a single datetime object
    return timestamp 


# Example usage
if __name__ == "__main__":
    again = True
    while (again == True) : 
        question = input("Enter a query for Mongo Intel 🌎 : ")
        print("QUESTION: " + question)
        query = convert_question_to_query(question)
        print(query)  # This will print the MongoDB query
        again = input("\nAgain? (Y/N): ")
        again = True if again.lower() == "y" else False