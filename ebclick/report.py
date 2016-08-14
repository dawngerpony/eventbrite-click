
def print_click_report(client, event_id):
    attendees = client.get_event_attendees(event_id)
    print "Attendees: {}".format(len(attendees['attendees']))
