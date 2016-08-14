import unittest
import pickle
from ebclick.eventbrite import AttendeeData


class AttendeeDataTest(unittest.TestCase):

    responses = None

    def setUp(self):
        self.responses = load_response_data('data_1471178138.72.requests.models.Response.p')

    def test_num_responses(self):
        """ Test that an AttendeeData object initializes correctly.
        """
        attendee_data = AttendeeData(self.responses)
        num_expected_responses = 60
        self.assertEqual(len(attendee_data.responses), num_expected_responses)


def load_response_data(filename):
    with open(filename) as f:
        data = pickle.load(f)
    return data
