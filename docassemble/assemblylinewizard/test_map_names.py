import unittest

from .interview_generator import map_names, trigger_gather_string
from docassemble.base.util import log

__all__ = ['TestMapNames']

# Some basic test input pdf label strings (left) with desired results (right)
attachment_scenarios = {
  # Reserved whole words
  "signature_date": "signature_date",
  # Not yet implemented
  #"attorney_of_record_address_on_one_line": "attorney_of_record_address_on_one_line",

  # Reserved endings
  "user1": "users[0]",
  "user2": "users[1]",
  "user__2": "users[0]",
  "user____2": "users[0]",
  "user_name": "users[0]",
  "user_name_full": "users[0]",
  "user_name_first": "users[0].name.first",
  "user_name_middle": "users[0].name.middle",
  "user_name_last": "users[0].name.last",
  "user_name_suffix": "users[0].name.suffix",
  "user_gender": "users[0].gender",
  "user_birthdate": "users[0].birthdate.format()",
  "user_age": "users[0].age_in_years()",
  "user_email": "users[0].email",
  "user_phone": "users[0].phone_number",
  "user_phone_number": "users[0].phone_number",
  "user_mobile": "users[0].mobile_number",
  "user_mobile_number": "users[0].mobile_number",
  "user_address_block": "users[0].address.block()",
  "user_address_street": "users[0].address.address",
  "user_address_street2": "users[0].address.unit",
  "user_address_city": "users[0].address.city",
  "user_address_state": "users[0].address.state",
  "user_address_zip": "users[0].address.zip",
  "user_address_on_one_line": "users[0].address.on_one_line()",
  "user_address_line_one": "users[0].address.line_one()",
  "user_address_city_state_zip": "users[0].address.line_two()",
  "user_signature": "users[0].signature",
  "user_mail_address": "users[0].mail_address",
  'user_mail_address_block': "users[0].mail_address.block()",
  'user_mail_address_address': "users[0].mail_address.address",
  'user_mail_address_zip': "users[0].mail_address.zip",

  # Combo all
  "user3_birthdate__4": "users[2].birthdate.format()",
  "user3_birthdate____4": "users[2].birthdate.format()",

  # County
  # "county_name_short": not implemented,
  # "county_division": not implemented,
  "court_address_county": "courts[0].address.county",
  "court_county": "courts[0].address.county",

  # # Reserved starts (with names)
  "user": "users[0]",
  "plaintiff": "plaintiffs[0]",
  "defendant": "defendants[0]",
  "petitioner": "petitioners[0]",
  "respondent": "respondents[0]",
  "spouse": "spouses[0]",
  "parent": "parents[0]",
  "guardian": "guardians[0]",
  "caregiver": "caregivers[0]",
  "attorney": "attorneys[0]",
  "translator": "translators[0]",
  "debt_collector": "debt_collectors[0]",
  "creditor": "creditors[0]",
  "court": "courts[0]",
  "other_party": "other_parties[0]",
  "child": "children[0]",
  "guardian_ad_litem": "guardians_ad_litem[0]",
  "witness": "witnesses[0]",
  "users": "users",
  "plaintiffs": "plaintiffs",
  "defendants": "defendants",
  "petitioners": "petitioners",
  "respondents": "respondents",
  "spouses": "spouses",
  "parents": "parents",
  "guardians": "guardians",
  "caregivers": "caregivers",
  "attorneys": "attorneys",
  "translators": "translators",
  "debt_collectors": "debt_collectors",
  "creditors": "creditors",
  "courts": "courts",
  "other_parties": "other_parties",
  "children": "children",
  "guardians_ad_litem": "guardians_ad_litem",
  "witnesses": "witnesses",

  # Starts with no names
  "docket_number": "docket_numbers[0]",
  "docket_numbers": "docket_numbers",
  "signature_date": "signature_date",

  # Reserved start with unreserved end
  "user_address_street2_zip": "user_address_street2_zip",  

  # Not reserved
  "my_user_name_last": "my_user_name_last",
  "foo": "foo",
}

interview_order_scenarios = {
  # Reserved whole words
  "signature_date": "signature_date",
  # Not yet implemented
  #"attorney_of_record_address_on_one_line": "attorney_of_record_address_on_one_line",

  # Reserved endings
  "user1": "users.gather()",
  "user2": "users.gather()",
  "user__2": "users.gather()",
  "user_name": "users.gather()",
  "user_name_full": "users.gather()",
  "user_name_first": "users.gather()",
  "user_name_middle": "users.gather()",
  "user_name_last": "users.gather()",
  "user_name_suffix": "users.gather()",
  "user_gender": "users[0].gender",
  "user_birthdate": "users[0].birthdate",
  "user_age": "users[0].birthdate",
  "user_address_unit": "users[0].address",
  "user_address_address": "users[0].address",
  "user_address_city": "users[0].address",
  "user_email": "users[0].email",
  "user2_phone": "users[1].phone_number",
  "user_signature": "users[0].signature",
  "user_mail_address": "users[0].mail_address",
  'user_mail_address_block': "users[0].mail_address",
  'user_mail_address_address': "users[0].mail_address",
  'user_mail_address_zip': "users[0].mail_address",

  # County
  # "county_name_short": not implemented,
  # "county_division": not implemented,
  "court_address_county": "courts[0].address",
  "court_county": "courts[0].address",

  # # Reserved starts (with names)
  "user": "users.gather()",
  "users": "users.gather()",
  "plaintiff": "plaintiffs.gather()",
  "defendant": "defendants.gather()",
  "courts": "courts.gather()",
  "other_parties": "other_parties.gather()",
  "children": "children.gather()",
  "guardians_ad_litem": "guardians_ad_litem.gather()",
  "witnesses": "witnesses.gather()",

  "defendant1_name": "defendants.gather()",
  "defendant1_email": "defendants[0].email",

  # Starts with no names
  "docket_number": "docket_numbers.gather()",
  "docket_numbers": "docket_numbers.gather()",
  "signature_date": "signature_date",

  # Reserved start with unreserved end
  "user_address_street2_zip": "user_address_street2_zip",

  # Not reserved
  "my_user_name_last": "my_user_name_last",
  "foo": "foo",
}


class TestMapNames(unittest.TestCase):
    def setUp(self):
        pass

    def test_mapped_scenarios(self, run_from_yaml=False):
        test_scenarios = [
          (attachment_scenarios, map_names),
          (interview_order_scenarios, lambda x: trigger_gather_string(map_names(x)))
        ]
        # Look in the console for a prettier version of the messages
        passed = []
        errored = []
        for scenarios, function in test_scenarios:
          # TODO(brycew): log / print which test scenario is running here
          temp_passed, temp_errored = self.run_scenarios(scenarios, function)
          passed += temp_passed
          errored += temp_errored
        results = {"errored": errored, "passed": passed}
        log(results, "console")
        # This is True if this test is run from generator-test.yml
        if run_from_yaml:
            return results
        self.assertEqual(len(passed), sum([len(sc[1]) for sc in self.scenarios]))
        self.assertEqual(len(errored), 0)

    def run_scenarios(self, scenarios, function):
        errored = []
        passed = []
        log("------ New Scenario Batch ------\n", "console")
        for scenario_input in scenarios:
            try:
                desired_output = scenarios[scenario_input]
                self.assertEqual(desired_output, function(scenario_input))
                # Add our result to the collection
                passed.append(scenario_input)
            except AssertionError as error:
                # The error should show us what specifically didn't match up
                log(str(error) + "\n", "console")
                log("~~~~~~~~~~\n", "console")
                errored.append({"test": scenario_input, "result": error})
        return passed, errored


if __name__ == "__main__":
    unittest.main()
