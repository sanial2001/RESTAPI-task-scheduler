import spacy
import datetime
from deep_translator import GoogleTranslator
import time
from .schedule_mail import send_mail
from .config import settings

username = f"{settings.mail_username}"
password = f"{settings.mail_password}"



class NlpEnglish:
    def __init__(self, english_text):
        self.input = english_text
        self.result_dict = {}
        self.result_pos = {}
        self.input = self.input.split()

        # code to convert all month types to January,february format as only these types are included as DATE type
        for i, word in enumerate(self.input):
            if word == 'Jan' or word == 'january' or word == 'jan':
                self.input[i] = 'January'
            if word == 'Feb' or word == 'february' or word == 'feb':
                self.input[i] = 'February'
            if word == 'Mar' or word == 'march' or word == 'mar':
                self.input[i] = 'March'
            if word == 'Apr' or word == 'april' or word == 'apr':
                self.input[i] = 'April'
            if word == 'may':
                self.input[i] = 'May'
            if word == 'Jun' or word == 'june' or word == 'jun':
                self.input[i] = 'June'
            if word == 'Jul' or word == 'july' or word == 'july':
                self.input[i] = 'July'
            if word == 'Aug' or word == 'august' or word == 'aug':
                self.input[i] = 'August'
            if word == 'Sep' or word == 'september' or word == 'sep':
                self.input[i] = 'September'
            if word == 'Oct' or word == 'october' or word == 'oct':
                self.input[i] = 'October'
            if word == 'Nov' or word == 'november' or word == 'nov':
                self.input[i] = 'November'
            if word == 'Dec' or word == 'december' or word == 'dec':
                self.input[i] = 'December'
        self.input = ' '.join(self.input)
        # print(self.input)
        self.nlp = spacy.load('en_core_web_sm')
        self.doc = self.nlp(self.input)

    def time(self):
        for ent in self.doc.ents:
            # print(ent.text, ent.label_)
            if ent.label_ == 'DATE' and ent.text[0].isdigit() or ent.label_ == 'TIME':
                time_on_hand = str(ent.text)
                self.result_dict['task_time'] = time_on_hand

    def date(self):
        match = ['day', 'month', 'week', 'year']
        match_month = 'January February March April May June July August September October November December'
        match_month = match_month.split()
        cal = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
               'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
               }

        for ent in self.doc.ents:
            if ent.label_ == 'DATE':
                if ent.text.startswith('tod'):
                    date_req = datetime.date.today()
                    self.result_dict['task_date'] = date_req.strftime('%A-%d-%b-%Y')

                elif ent.text == 'tomorrow':
                    date_req = datetime.date.today() + datetime.timedelta(days=1)
                    self.result_dict['task_date'] = date_req.strftime('%A-%d-%b-%Y')

                elif any(word in ent.text for word in match):
                    x = ent.text.split()
                    if 'month' in x[1]:
                        req_days = int(x[0]) * 30
                    elif 'week' in x[1]:
                        req_days = int(x[0]) * 7
                    elif 'year' in x[1]:
                        req_days = int(x[0]) * 365
                    else:
                        if x[0].isalpha():
                            break
                        else:
                            req_days = int(x[0])
                    date_req = datetime.date.today() + datetime.timedelta(days=req_days)
                    self.result_dict['task_date'] = date_req.strftime('%A-%d-%b-%Y')

                elif any(word in ent.text for word in match_month):
                    value_month = ''
                    value_day = ''
                    month_format = ent.text.split()
                    if month_format[1].isdigit():
                        value_month = cal[month_format[0]]
                        value_day = month_format[1]
                    elif month_format[0].isdigit():
                        value_month = cal[month_format[1]]
                        value_day = month_format[0]
                    if len(month_format) == 3:
                        d1 = datetime.date(int(month_format[2]), int(value_month), int(value_day))
                    else:
                        d1 = datetime.date(datetime.date.today().year, int(value_month), int(value_day))
                    d0 = datetime.date(datetime.date.today().year, datetime.date.today().month,
                                       datetime.date.today().day)
                    req_days = d1 - d0
                    date_req = datetime.date.today() + datetime.timedelta(days=req_days.days)
                    self.result_dict['task_date'] = date_req.strftime('%A-%d-%b-%Y')

    def display_data(self):
        if ('task_time' in self.result_dict) and (len(self.result_dict) == 1):
            date_req = datetime.date.today()
            self.result_dict['task_date'] = date_req.strftime('%A-%d-%b-%Y')
        elif ('task_date' in self.result_dict) and (len(self.result_dict) == 1):
            self.result_dict['task_time'] = '00:00'
        #print(self.result_dict)
        return self.result_dict

    def check_date(self):
        in_date = self.result_dict['task_date']
        date_obj = datetime.datetime.strptime(in_date, '%A-%d-%b-%Y')
        date_str = datetime.datetime.strftime(date_obj, '%Y-%m-%d')
        out_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return out_date

    def check_time(self):
        time_segment = self.result_dict['task_time']
        if '.' in time_segment:
            time_segment = time_segment.replace('.', ':')
        if 'a.m' in time_segment:
            time_segment = time_segment.replace('a.m', 'am')
        elif 'A.M' in time_segment:
            time_segment = time_segment.replace('A.M', 'am')
        elif 'p.m' in time_segment:
            time_segment = time_segment.replace('p.m', 'pm')
        elif 'P.M' in time_segment:
            time_segment = time_segment.replace('P.M', 'pm')

        key = ['am', 'pm']
        if any(word in time_segment for word in key):
            in_time = datetime.datetime.strptime(time_segment, "%H:%M %p")
            out_time = datetime.datetime.strftime(in_time, "%H:%M")
            out_time = datetime.datetime.strptime(out_time, "%H:%M")
        else:
            out_time = datetime.datetime.strptime(time_segment, "%H:%M")

        return out_time


def trans_to_eng(text):
    translated = GoogleTranslator(source='auto', target='en').translate(text)
    return translated


def processing(input_text: str, to_emails):
    translated_input_text = trans_to_eng(input_text)
    task = NlpEnglish(translated_input_text)
    task.time()
    task.date()
    result = task.display_data()
    req_date = task.check_date()
    req_time = task.check_time()
    # print(req_date, req_time)
    updated_req_time = req_time - datetime.timedelta(minutes=30)
    send_time = datetime.datetime(req_date.year, req_date.month, req_date.day,
                                  updated_req_time.hour, updated_req_time.minute, updated_req_time.second)
    print(send_time)
    send_mail(text="REMINDER", subject=input_text, from_email=username, to_emails=to_emails, html=None)
    #time.sleep(send_time.timestamp() - time.time())
    # send_email()
