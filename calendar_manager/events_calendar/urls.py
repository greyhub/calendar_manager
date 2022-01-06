from django.urls import path

from events_calendar.views.event_list import AllEventsListView, RunningEventsListView
from events_calendar.views.other_views import CalendarViewNew, CalendarView, create_event, EventEdit, event_details, load_event
from events_calendar.views.other_views import *

app_name = "events_calendar"

urlpatterns = [
    path("calendar/", CalendarViewNew.as_view(), name="calendar"),
    path("calendars/", CalendarView.as_view(), name="calendars"),
    path("event/new/", create_event, name="event_new"),
    path("event/edit/<int:pk>/", EventEdit.as_view(), name="event_edit"),
    path("event/<int:event_id>/details/", event_details, name="event-detail"),
    path(
        "add_eventmember/<int:event_id>", add_eventmember, name="add_eventmember"
    ),
    path(
        "event/<int:pk>/remove",
        EventMemberDeleteView.as_view(),
        name="remove_event",
    ),
    path("all-event-list/", AllEventsListView.as_view(), name="all_events"),
    path(
        "running-event-list/",
        RunningEventsListView.as_view(),
        name="running_events",
    ),
    path("load/calendar", load_event,name="load_ctt"),
    path("create/group", create_group, name="add_group"),
    path("view/group", view_group, name="view_group"),
    path("list_detail/groupmember/<int:pk>/", list_detail_group, name="list_detail_groupmember"),
    path("add/member/groupmember/<int:pk>/", add_member_group, name="add_group_member"),
    path("calendar/groupmember/<int:pk>/", GroupCalendarView.as_view(), name="calendar_group_member")
]