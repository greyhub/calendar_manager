from re import template
import re
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, date, datetime
import datetime
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
import json
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from events_calendar.models import *
from events_calendar.utils import Calendar
from events_calendar.forms import EventForm, AddMemberForm, AddGroupForm, AddGroupMemberForm, AddGroupEvent, Recommendform
import pandas as pd
from events_calendar.views.pipeline import pipeline
import os

path_to_integration = 'events_calendar/fixtures/event_data.json'
path_to_integration_google = '/home/datdinh/Documents/20211/Tich_ho_he_thong/calendar_manager/google_calendar/data.json'
path_to_demoData = 'events_calendar/views/data/Demo_data_1.json'
path_to_Data = 'events_calendar/views/data/'
path_to_recommendData = 'events_calendar/views/data/output/suggestion.json'

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = "accounts:signin"
    model = Event
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


@login_required(login_url="signup")
def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,  
            end_time=end_time,
        )
        return HttpResponseRedirect(reverse("events_calendar:calendar"))
    return render(request, "event.html", {"form": form})

@login_required(login_url="signup")
def load_event(request):

    with open(path_to_integration,encoding='utf-8') as event_data:
        data_subjects = json.load(event_data)
        for subject in data_subjects:
            Event.objects.get_or_create(
                user=request.user,
                title=subject['title'],
                description=subject['description'],
                start_time=subject['start_time_str'],
                end_time=subject['end_time_str'],
            ) 
    events = Event.objects.get_all_events(user=request.user)
    event_list = []
    # start: '2021-09-16T16:00:00'
    for event in events:
        event_list.append(
            {
                "title": event.title,
                "description": event.description,
                "start_time_str": event.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time_str": event.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
    with open(path_to_integration_google,'w',encoding='utf-8') as f:
        json.dump(event_list, f, ensure_ascii=False, indent=4)

    return HttpResponseRedirect(reverse("events_calendar:calendar"))



class EventEdit(generic.UpdateView):
    model = Event
    fields = ["title", "description", "start_time", "end_time"]
    template_name = "event.html"


@login_required(login_url="signup")
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "event_details.html", context)


def add_eventmember(request, event_id):
    forms = AddMemberForm()
    if request.method == "POST":
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            if member.count() <= 9:
                user = forms.cleaned_data["user"]
                EventMember.objects.create(event=event, user=user)
                return redirect("events_calendar:event-detail", event_id)
            else:
                print("--------------User limit exceed!-----------------")
    context = {"form": forms}
    return render(request, "add_member.html", context)


class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = "event_delete.html"
    success_url = reverse_lazy("events_calendar:calendar")


class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "accounts:signin"
    template_name = "events_calendar/calendar.html"
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        events = Event.objects.get_all_events(user=request.user)
        events_month = Event.objects.get_running_events(user=request.user)
        event_list = []
        # start: '2021-09-16T16:00:00'
        for event in events:
            event_list.append(
                {
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'display': 'list-item',
                    "url": reverse('events_calendar:event-detail', args=[event.id])
                }
            )

        context = {"form": forms, "events": event_list, "events_month": events_month}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST or None)
        if forms.is_valid() and forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("events_calendar:calendar")
        context = {"form": forms}
        return render(request, "event.html", context)


def create_group(request):
    forms = AddGroupForm()
    if request.method == "POST":
        forms = AddGroupForm(request.POST)
        if forms.is_valid():
            instance = forms.save(commit=False)
            instance.save()
            GroupMember.objects.create(group_id=instance.id, user_id=request.user.id, is_leader=True)
            return redirect('events_calendar:view_group')
    context = {"form": forms}
    return render(request, "add_group.html", context)

def view_group(request):
    groups = Group.objects.all()

    paginator = Paginator(groups, 10)

    page = request.GET.get('page')
    groups = paginator.get_page(page)

    return render(request, "view_group.html", {"groups": groups})

def list_detail_group(request, pk):
    group = Group.objects.get(id=pk)
    groupmember = GroupMember.objects.filter(group_id=pk)
    list_event_of_group = GroupEvent.objects.filter(group_id=pk)
    context = {"group": group, "groupmember": groupmember, "list_event":list_event_of_group}
    return render(request, "list_detail_group.html", context)

def add_member_group(request, pk):
    check_create_user_in_group = True
    forms = AddGroupMemberForm()
    if request.method == "POST":
        forms = AddGroupMemberForm(request.POST)
        if forms.is_valid():
            members = GroupMember.objects.filter(group_id=pk)
            if members.count() <= 9:
                user = forms.cleaned_data["user"]
                for member in members.all():
                    if member.id == user.id:
                        check_create_user_in_group  = False
                        break

                if check_create_user_in_group:
                    GroupMember.objects.create(group_id=pk,user=user)

                return redirect("events_calendar:list_detail_groupmember", pk)
            else:
                print("--------------User limit exceed!-----------------")
    context = {"form": forms}
    return render(request, "add_member_group.html", context)

def remove_member_group(request, pk):
    obj = get_object_or_404(GroupMember, id=pk)
    temp = obj.group.id
    obj.delete()
    return redirect("events_calendar:list_detail_groupmember",temp)

class GroupCalendarView(generic.View):
    login_url = "accounts:sigin"
    template_name = "group_calendar/calendar.html"
    form_class = AddGroupEvent

    def get(self, request, pk, *args, **kwargs):
        check_recommend = 0
        forms = self.form_class()
        members = list(GroupMember.objects.filter(group_id=pk).all())
        name_group = Group.objects.get(id=pk)
        event_list = []
        color = ["#099688","#17a2b8","#556b2f","yellow","black","purple","brown","grey"]
        blue = "blue"
        for index, member in enumerate(members):
            setattr(member, 'color', color[index])
            events = Event.objects.get_all_events(user=member.user)
            # events_month = Event.objects.get_running_events(user=member.user)
            for event in events:
                event_list.append(
                    {
                        "title": event.title,
                        "start": event.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "end": event.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                        'display': 'list-item',
                        "backgroundColor": color[index],
                        "background": color[index],
                        "url": reverse('events_calendar:event-detail', args=[event.id])
                    }
                )

        list_event = GroupEvent.objects.filter(group_id = pk)
        for event in list_event:
            event_list.append(
                {
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "backgroundColor": "rgb(82, 20, 76)",
                    "background": "rgb(47, 224, 255)",
                    "url": reverse('events_calendar:list_detail_groupmember', args=[pk])
                }
            )

        try: 
            with open(path_to_recommendData,encoding='utf-8') as event_data:
                data_subjects = json.load(event_data)
                for subject in data_subjects:
                    event_list.append(
                        {
                            "title":subject['title'],
                            "start": subject['start'],
                            "end":subject['end'],
                            "backgroundColor": "rgba(218, 167, 15, 0.692)"
                        }
                    )
                    check_recommend = 1
                os.remove(path_to_recommendData)
                
        except:
            print("None")

        context = {"form":forms, "events": event_list, "members": members, "name_group":name_group, "blue":blue, "pk":pk, "check_recommend":check_recommend}
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        forms = self.form_class(request.POST or None)
        if forms.is_valid() and forms.is_valid():
            form = forms.save(commit=False)
            form.group_id = pk
            form.save()
            return redirect("events_calendar:calendar_group_member", pk)
        context = {"form": forms}
        return render(request, "group_event.html", context)

def remove_event_group(request,pk):
    obj = get_object_or_404(GroupEvent, id=pk)
    temp = obj.group.id
    obj.delete()
    return redirect("events_calendar:list_detail_groupmember",temp)

def list_event_of_group(request, pk):
    list_event = GroupEvent.objects.get(group_id = pk)
    context = {"list_event":list_event}
    return render(request, "list_event_of_group",context)

def export_data_of_group(request, pk):
    form = Recommendform(request.POST or None)
    try:
        start_time = datetime.strptime(form["start_time"].value(), "%Y-%m-%dT%H:%M")
        end_time = datetime.strptime(form["end_time"].value(), "%Y-%m-%dT%H:%M")
        print(start_time, end_time)
        print(start_time.isocalendar(), end_time.isocalendar())
        print(start_time.isocalendar()[1], end_time.isocalendar()[1])
    except:
        print("None")
    print("Hello: ",form.is_valid())

    if request.POST and start_time.isocalendar()[1] == end_time.isocalendar()[1]:
        members = list(GroupMember.objects.filter(group_id=pk).all())
        event_list = []
        for index, member in enumerate(members):
            events = Event.objects.get_all_events(user=member.user)
            for event in events:
                event_start_time = datetime.strptime(event.start_time.strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
                event_end_time = datetime.strptime(event.end_time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                if event_start_time > start_time and  event_end_time < end_time:
                    event_list.append(
                        {
                            "user_id": member.user.id,
                            "leader": member.is_leader,
                            "title": event.title,
                            "start": event.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                            "end": event.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                        }
                    )
                
        df = pd.DataFrame(event_list)
        with open(path_to_demoData ,'w', encoding='utf-8') as f:
            json.dump(event_list, f, ensure_ascii=False, indent=4)
        
        pipeline(input=path_to_demoData ,data_dir=path_to_Data,year=start_time.isocalendar()[0], week=start_time.isocalendar()[1])
        return redirect("events_calendar:calendar_group_member", pk)

    return render(request, "group_calendar/recommend_calendar.html", {"form": form})

