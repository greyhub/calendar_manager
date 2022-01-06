from re import template
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
import json
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from events_calendar.models import *
from events_calendar.utils import Calendar
from events_calendar.forms import EventForm, AddMemberForm, AddGroupForm, AddGroupMemberForm, AddGroupEvent

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
    with open('F:/Desktop/THHT_13/calendar_manager/calendar_manager/events_calendar/fixtures/event_data.json',encoding='utf-8') as event_data:
        data_subjects = json.load(event_data)
        for subject in data_subjects:
            Event.objects.get_or_create(
                user=request.user,
                title=subject['title'],
                description=subject['description'],
                start_time=subject['start_time_str'],
                end_time=subject['end_time_str'],
            )
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
                    "start": event.start_time.date().strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.date().strftime("%Y-%m-%dT%H:%M:%S"),
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
    context = {"group": group, "groupmember": groupmember}
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

class GroupCalendarView(generic.View):
    login_url = "accounts:sigin"
    template_name = "group_calendar/calendar.html"
    form_class = GroupEvent

    def get(self, request, pk, *args, **kwargs):
        forms = self.form_class()
        members = list(GroupMember.objects.filter(group_id=pk).all())
        name_group = Group.objects.get(id=pk)
        event_list = []
        color = ["black","green","red","blue","yellow"]
        blue = "blue"
        for index, member in enumerate(members):
            setattr(member, 'color', color[index])
            events = Event.objects.get_all_events(user=member.user)
            events_month = Event.objects.get_running_events(user=member.user)
            for event in events:
                event_list.append(
                    {
                        "title": event.title,
                        "start": event.start_time.date().strftime("%Y-%m-%dT%H:%M:%S"),
                        "end": event.end_time.date().strftime("%Y-%m-%dT%H:%M:%S"),
                        "color": color[index],
                        "background": color[index],
                    }
                )

        context = {"form":forms, "events": event_list, "members": members, "name_group":name_group, "blue":blue}
        return render(request, self.template_name, context)



    



    