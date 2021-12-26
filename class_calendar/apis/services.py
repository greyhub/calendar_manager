import calendar
import datetime
from pprint import pprint


def convert_a_day_of_week_to_date(first_day, day_of_week):
    mapper = {'Thứ 2': 0, 'Thứ 3': 1, 'Thứ 4': 2, 'Thứ 5': 3, 'Thứ 6': 4, 'Thứ 7': 5, 'Chủ nhật': 6}
    return first_day + datetime.timedelta(days=mapper[day_of_week])


def convert_time_str_to_time_delta(time_str=''):
    time_str_splited = time_str.split('h')
    return datetime.timedelta(hours=int(time_str_splited[0]), minutes=int(time_str_splited[1]))


def convert_class_time_table(class_time_table):
    today = datetime.date.today()
    today = datetime.datetime.combine(today, datetime.datetime.min.time())
    today_in_week = calendar.weekday(today.year, today.month, today.day)
    first_day = today + datetime.timedelta(days=7 - today_in_week)
    subject_list = class_time_table.get('ScheduleStudentLst')
    subject_converted_list = list()
    for subject in subject_list:
        subject_converted = dict()
        study_date = convert_a_day_of_week_to_date(first_day, subject.get('DayOfWeek'))
        start_time = study_date + convert_time_str_to_time_delta(subject.get('TimeStart'))
        end_time = study_date + convert_time_str_to_time_delta(subject.get('TimeEnd'))
        subject_converted['start_time_str'] = str(start_time)
        subject_converted['end_time_str'] = str(end_time)
        summary = f"{subject.get('SubjectId')}-{subject.get('SubjectName')}"
        description = f"Loại môn học: {subject.get('TypeSubject')}. Tuần học: {subject.get('Week')}. " \
                      f"Đối tượng học: {subject.get('Description')}"
        location = f"{subject.get('Tower')}-{subject.get('Room')}"
        subject_converted['summary'] = summary
        subject_converted['description'] = description
        subject_converted['location'] = location
        subject_converted_list.append(subject_converted)
    return subject_converted_list


if __name__ == '__main__':
    convert_class_time_table({'RangeWeek': 34,
                              'RespCode': 0,
                              'RespText': 'OK',
                              'ScheduleStudentLst': [{'ClassID': '128761',
                                                      'DayOfWeek': 'Thứ 2',
                                                      'Description': 'KH máy tính-K62S',
                                                      'Room': '207',
                                                      'SubjectId': 'IT4868',
                                                      'SubjectName': 'Khai phá Web',
                                                      'TimeEnd': '10h5',
                                                      'TimeStart': '6h45',
                                                      'Tower': 'TC',
                                                      'TypeSubject': 'LT+BT',
                                                      'Week': '1-8,10-17'},
                                                     {'ClassID': '128756',
                                                      'DayOfWeek': 'Thứ 2',
                                                      'Description': 'KH máy tính-K62S',
                                                      'Room': '209',
                                                      'SubjectId': 'IT5419',
                                                      'SubjectName': 'Tích hợp Hệ thống thông tin',
                                                      'TimeEnd': '11h45',
                                                      'TimeStart': '10h15',
                                                      'Tower': 'TC',
                                                      'TypeSubject': 'LT+BT',
                                                      'Week': '1-8,10-17'},
                                                     {'ClassID': '128757',
                                                      'DayOfWeek': 'Thứ 3',
                                                      'Description': 'KH máy tính-K62S',
                                                      'Room': '210',
                                                      'SubjectId': 'IT4079',
                                                      'SubjectName': 'Ngôn ngữ và phương pháp dịch',
                                                      'TimeEnd': '9h10',
                                                      'TimeStart': '6h45',
                                                      'Tower': 'TC',
                                                      'TypeSubject': 'LT+BT',
                                                      'Week': '1-8,10-17'},
                                                     {'ClassID': '128678',
                                                      'DayOfWeek': 'Thứ 3',
                                                      'Description': 'KH máy tính 03,04-K65C',
                                                      'Room': '105',
                                                      'SubjectId': 'IT3011',
                                                      'SubjectName': 'Cấu trúc dữ liệu và thuật toán',
                                                      'TimeEnd': '17h30',
                                                      'TimeStart': '15h5',
                                                      'Tower': 'D9',
                                                      'TypeSubject': 'LT+BT',
                                                      'Week': '1-8,10-17'},
                                                     {'ClassID': '128695',
                                                      'DayOfWeek': 'Thứ 4',
                                                      'Description': 'KH máy tính-K64S',
                                                      'Room': '204',
                                                      'SubjectId': 'IT3080',
                                                      'SubjectName': 'Mạng máy tính',
                                                      'TimeEnd': '9h10',
                                                      'TimeStart': '6h45',
                                                      'Tower': 'TC',
                                                      'TypeSubject': 'LT+BT',
                                                      'Week': '1-8,10-17'},
                                                     {'ClassID': '128756',
                                                      'DayOfWeek': 'Thứ 5',
                                                      'Description': 'KH máy tính-K62S',
                                                      'Room': '209',
                                                      'SubjectId': 'IT5419',
                                                      'SubjectName': 'Tích hợp Hệ thống thông tin',
                                                      'TimeEnd': '11h45',
                                                      'TimeStart': '10h15',
                                                      'Tower': 'TC',
                                                      'TypeSubject': 'LT+BT',
                                                      'Week': '1-8,10-17'},
                                                     {'ClassID': '128694',
                                                      'DayOfWeek': 'Thứ 5',
                                                      'Description': 'KH máy tính - KT máy tính-K64C',
                                                      'Room': '302',
                                                      'SubjectId': 'IT4015',
                                                      'SubjectName': 'Nhập môn an toàn thông tin',
                                                      'TimeEnd': '17h30',
                                                      'TimeStart': '14h10',
                                                      'Tower': 'C1',
                                                      'TypeSubject': 'LT+BT',
                                                      'Week': '1-8,10-17'},
                                                     {'ClassID': '710844',
                                                      'DayOfWeek': 'Thứ 6',
                                                      'Description': 'IT3080-N06',
                                                      'Room': '204',
                                                      'SubjectId': 'IT3080',
                                                      'SubjectName': 'Mạng máy tính',
                                                      'TimeEnd': '17h30',
                                                      'TimeStart': '15h5',
                                                      'Tower': 'B1',
                                                      'TypeSubject': 'TN',
                                                      'Week': '7,10,12,14,16'}]}
                             )
    # a = convert_time_str_to_time_delta('15h5')
    # print(a)