# -*- coding: utf-8 -*-

#~ from __future__ import generators
import unittest
from unittest import TestCase
import re
import sys
import os
from mock import Mock
pwd = os.path.dirname(os.path.realpath(__file__))
morelia_path = os.path.join(pwd, '../morelia')
sys.path.insert(0, morelia_path)
from morelia import *
from morelia import _permute_indices

 #  TODO  add Pangolins to the sample data
 #  TODO  cron order already!


class MoreliaSuite(TestCase):

    def step_I_have_entered_a_number_into_the_calculator(self, number):
        r'I have entered (\d+) into the calculator'

        if not hasattr(self, 'stack'):  self.stack = []
        self.stack.append(int(number))

    def step_I_press_add(self):
        self.result = self.stack[0] + self.stack[1]

    def step_the_result_should_be_on_the_screen(self, number):
        "the result should be (\d+) on the screen"

        assert int(number) == self.result

    def test_feature(self):
        input = 'Feature: prevent wild animals from eating us'
        steps = Parser().parse_feature(input)
        step = steps[0]
        assert step.__class__ == Feature
        self.assertEqual(step.concept, 'Feature')
        self.assertEqual(step.predicate, 'prevent wild animals from eating us')

    def test_scenario(self):
        input = 'Scenario: range free Vegans'
        steps = Parser().parse_feature(input)
        step = steps[0]
        assert step.__class__ == Scenario
        self.assertEqual(step.concept, 'Scenario')
        self.assertEqual(step.predicate, 'range free Vegans')
        
    def test___scenario(self):
        input = '  Scenario: with spacies'
        steps = Parser().parse_feature(input)
        step = steps[0]
        assert step.__class__ == Scenario
        self.assertEqual(step.concept, 'Scenario')
        self.assertEqual(step.predicate, 'with spacies')

    def test_given_a_string_with_given_in_it(self):
        input = 'Given a string with Given in it   \nAnd another string'
        steps = Parser().parse_feature(input)  #  ^ note the spacies
        step = steps[0]
        assert step.__class__ == Given
        self.assertEqual(step.concept, 'Given')
        self.assertEqual(step.predicate, 'a string with Given in it')  # <-- note spacies are gone

    def test_given_a_broken_string_with_excess_spacies(self):
        input = 'Given a string with spacies and   \n  another string  '
        steps = Parser().parse_feature(input)
        step = steps[0]
        assert step.__class__ == Given
        self.assertEqual(step.concept, 'Given')
        self.assertEqual(step.predicate, 'a string with spacies and\nanother string')

    def test_feature_with_scenario(self):
        input = '''Feature: Civi-lie-zation
                   Scenario: starz upon tharz bucks'''
        steps = Parser().parse_feature(input)
        step = steps[0]
        assert step.__class__ == Feature
        self.assertEqual(step.concept, 'Feature')
        self.assertEqual(step.predicate, 'Civi-lie-zation')
        step = steps[1]
        assert step.__class__ == Scenario
        self.assertEqual(step.concept, 'Scenario')
        self.assertEqual(step.predicate, 'starz upon tharz bucks')

    def test_feature_with_scenario(self):
        input = '''Feature: The Sacred White Llama of the Inca
                   #  I are a comment'''
        steps = Parser().parse_feature(input)
        assert steps[0].__class__ == Feature
        
        step = steps[1]
        assert step.__class__ == Comment
        self.assertEqual(step.concept, 'Comment')
        self.assertEqual(step.predicate, 'I are a comment')

    def pet_scenario(self):
        return '''Scenario: See all vendors
                      Given I am logged in as a user in the administrator role
                        And There are 3 vendors
                       When I go to the manage vendors page
                       Then I should see the first 3 vendor names'''

    def test_parse_scenario(self):
        scenario = self.pet_scenario()
        steps = Parser().parse_feature(scenario)
        step_0, step_1, step_2, step_3, step_4 = steps
        self.assertEqual(step_0.concept, 'Scenario')
        self.assertEqual(step_0.predicate, 'See all vendors')
        self.assertEqual(step_1.concept, 'Given')
        self.assertEqual(step_1.predicate,     'I am logged in as a user in the administrator role')
        self.assertEqual(step_2.concept, 'And')
        self.assertEqual(step_2.predicate,   'There are 3 vendors')
        self.assertEqual(step_3.concept, 'When')
        self.assertEqual(step_3.predicate,    'I go to the manage vendors page')
        self.assertEqual(step_4.concept, 'Then')
        self.assertEqual(step_4.predicate,    'I should see the first 3 vendor names')

    def test_strip_predicates(self):
        step = Parser().parse_feature('  Given   gangsta girl   \t     ')[0]
        self.assertEqual(step.concept, 'Given')
        self.assertEqual(step.predicate, 'gangsta girl')

    def test_bond_predicates(self):
        step = Parser().parse_feature('  Given\n   elf quest   \t     ')[0]
        self.assertEqual(step.concept, 'Given')
        self.assertEqual(step.predicate, 'elf quest')

    def test_scenarios_link_to_their_steps(self):
        steps = Parser().parse_feature(self.pet_scenario())
        scenario, step_1, step_2, step_3, step_4 = steps
        self.assertEqual([step_1, step_2, step_3, step_4], scenario.steps)

    def test_how_to_identify_trees_from_quite_a_long_distance_away(self):
        assert Given != Step
        assert issubclass(Given, Step)
        assert issubclass(Given, Given)
        assert not issubclass(Scenario, Given)

    def test_i_look_like(self):
        self.assertEqual('Step', Step().i_look_like())
        self.assertEqual('Given', Given().i_look_like())
        self.assertEqual('\\|', Row().i_look_like())

    def test_Row_parse(self):
        sauce = 'buddha | brot |'
        row = Row()
        row._parse(sauce, [])
        assert row.predicate == sauce

    def test_parse_feature_Row(self):
        p = Parser()
        p.parse_features(''' | piggy | op |''')
        assert Row == p.steps[0].__class__
        assert p.steps[0].predicate == 'piggy | op |'

    def test_Scenes_count_Row_dimensions(self):
        self.assemble_scene_table()
        dims = self.table_scene.steps[0].steps[0].count_Row_dimensions()
        self.assertEqual([2, 3], dims)

    def test_Scenes_count_more_Row_dimensions(self):
        self.assemble_scene_table('Step whatever\n')
        dims = self.table_scene.steps[0].steps[0].count_Row_dimensions()
        self.assertEqual([2, 0, 3], dims)

    def test_permutate(self):
        expect = [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 0), (0, 1, 1), (0, 1, 2), 
                        (0, 2, 0), (0, 2, 1), (0, 2, 2), (0, 3, 0), (0, 3, 1), (0, 3, 2)]
        self.assertEqual(expect, _permute_indices([0,4,3]))
        expect = [(0, 0, 0)]
        self.assertEqual(expect, _permute_indices([1,1,1]))
        expect = [(0, 0, 0), (0, 0, 1)]
        self.assertEqual(expect, _permute_indices([1,1,2]))

    def assemble_scene_table_source(self, moar = ''):
        return '''Feature: permute tables
                       Scenario: turn one feature into many
                           Given party <zone>
                                | zone  |
                                | beach |
                                | hotel |
                           %sThen hearty <crunk>
                                | crunk | 
                                | work  | 
                                | mall  | 
                                | jail  |''' % moar
                                
    def assemble_scene_table(self, moar = ''):
        scene = self.assemble_scene_table_source(moar)
        p = Parser()
        self.table_scene = p.parse_features(scene)

    def test_permute_schedule(self):
        expect = _permute_indices([2, 0, 3])  #  NOTE:  by rights, 0 should be -1
        self.assemble_scene_table('Step you betcha\n')
        scenario = self.table_scene.steps[0].steps[0]
        schedule = scenario.permute_schedule()
        self.assertEqual(expect, schedule)

    def test_evaluate_permuted_schedule(self):
        self.assemble_scene_table('Step flesh is weak\n')
        scenario = self.table_scene.steps[0].steps[0]
        visitor = TestVisitor(self)
        global crunks, zones
        crunks = []
        zones = []
        scenario.row_indices = [1, 0, 2]
        scenario.evaluate_test_case(visitor)
        self.assertEqual('hotel', visitor.suite.got_party_zone)
        self.assertEqual('jail', visitor.suite.got_crunk)

    def test_another_two_dimensional_table(self):
        global crunks, zones
        crunks = []
        zones = []
        scene = self.assemble_scene_table_source('Step my milkshake brings all the boys to the yard\n')
        Parser().parse_features(scene).evaluate(self)
        self.assertEqual([ 'work',   'mall',  'jail',  'work',  'mall',  'jail' ], crunks)
        self.assertEqual([ 'beach', 'beach', 'beach', 'hotel', 'hotel', 'hotel' ], zones)

    def step_party_zone(self, zone):  #  TODO  prevent collision with another "step_party"
        r'party (\w+)'  #  TODO  illustrate how the patterns here form testage too

        self.got_party_zone = zone
        global zones
        zones.append(zone)

    def step_flesh_is_weak(self):  pass

    def step_hearty_crunk_(self, crunk):
        r'hearty (\w+)'
        
        global crunks
        crunks.append(crunk)
        self.got_crunk = crunk

#  TODO  note that default arguments on steps are permitted!
#  TODO  squeak if the table has no | in the middle or on the end etc, or if item not found
#  TODO  parse the || as Json/Yaml? - permit gaps & comments in tables
#  TODO  decorate exceptions failures with their source feature lines
#  TODO  respect the tests' verbosity levels

    def test_Rows_find_step_parents(self):
        self.assemble_scene_table()
        given, then, = self.table_scene.steps[0].steps[0].steps
        self.assertEqual(Row, given.steps[0].__class__)
        self.assertEqual(Row,  then.steps[0].__class__)
        self.assertEqual('zone  |', given.steps[0].predicate)
        self.assertEqual('crunk |',  then.steps[0].predicate)

    def assemble_short_scene_table(self):
        #  TODO  warn about bad but permitted style -- with | columns | out of order!
            #  TODO  reporter should beautify || markers!
        return '''Feature: the smoker you drink
                    Scenario: the programmer you get
                      Given party <element> from <faction>

                                | faction   | element  |

                                | Pangolin  | Pangea   |
                                | Glyptodon | Laurasia |'''

    def test_two_dimensional_table(self):
        global elements, factions
        elements = []
        factions = []
        Parser().parse_features(self.assemble_short_scene_table()).evaluate(self)
        self.assertEqual([['Pangolin', 'Glyptodon'], ['Pangea', 'Laurasia']], [factions, elements])

    def step_party_element_from_faction(self, element, faction):
        r'party (\w+) from (\w+)'
            #  TODO  don't default to this "party <element> in <faction>"  

        global elements, factions
        factions.append(faction)
        elements.append(element)

    def step_my_milkshake(self, youth = 'boys', article = 'the'):
        r'my milkshake brings all the (boys|girls) to (.*) yard'
        
        self.youth = youth
    
    def test_find_step_by_name(self):
        step = Given()._parse('my milkshake')
        step.find_by_name(self)
        expect = self.step_my_milkshake
        self.assertEqual(expect, step.method)

    def test_find_step_by_doc_string(self):
        step = And()._parse('my milkshake brings all the boys to the yard')
        method = step.find_by_doc_string(self)
        expect = self.step_my_milkshake
        self.assertEqual(expect, step.method)

    def test_find_step_with_match(self):
        step = When()._parse('my milkshake brings all the girls to the yard')
        step.find_by_doc_string(self)
        self.assertEqual(('girls', 'the'), step.matches)

    def test_step_not_found(self):
        step = Then()._parse('not there')
        assert None == step.find_by_name(self)
        
    def step_fail_without_enough_function_name(self):
        step = And()._parse('my milk')
        assert None == step.find_by_name(self)
        
    def step_fail_step_without_enough_doc_string(self):
        step = Given()._parse("brings all the boys to the yard it's better than yours")
        assert None == step.find_by_doc_string(self)
        
    def step_evaluate_step_by_doc_string(self):
        step = Given()._parse('my milkshake brings all the girls to a yard')
        self.youth = 'boys'
        step.evaluate(self)
        self.assertEqual('girls', self.youth)  # Uh...

    def test_evaluate_step_by_name(self):
        step = Given()._parse('my milkshake')
        self.youth = 'girls'
        step.evaluate(self)
        self.assertEqual('boys', self.youth)

    def step_multiline_predicate(self):
        feature = 'Given umma\ngumma'
        steps = Parser().parse_feature(feature)
        self.assertEqual('umma\ngumma', steps[0].predicate)

    def test_step_multiline_predicate(self):
        feature = 'When multiline predicate'
        steps = Parser().parse_feature(feature)
        steps[0].evaluate(self)

    #~ def test_evaluate_unfound(self):
        #~ Parser().parse_file(pwd + '/nada.feature').evaluate(self)
        
    def test_evaluate_file(self):
        Parser().parse_file(pwd + '/morelia.feature').evaluate(self)

    def setUp(self):
        self.culture = []

    def step_adventure_of_love_love_and_culture_(self, culture):
        r'adventure of love - love and (.+)'
        
        self.culture.append(culture)
        self.concept = self.step.concept

    def step_Moralia_evaluates_this(self):  pass

    def step_culture_contains(self, arguments):
        r'"culture" contains (.*)'
        
        self.assertEqual(1, arguments.count(self.culture[0]))
        self.assertEqual(1, len(self.culture))

    def toast_report_file(self):
        Parser().parse_file(pwd + '/morelia.feature').report(self)
        
    def step_a_feature_file_with_contents(self, file_contents):
        r'a feature file with "([^"]+)"'
        self.file_contents = file_contents
        
    #~ def step_wikked_(self):
        #~ '''wikked!
    #~ '''
#~ #  TODO get rid of linefeeds in the suggestions
        #~ assert False
        
    def step_Moralia_evaluates_the_file(self):
        self.diagnostic = None
        self.steps = []
        5
        try:
            p = Parser()
            self.file_contents.replace('\\#', '#')  # note - this is how to unescape characters - DIY
            p.parse_features(self.file_contents).evaluate(self)
            self.steps = p.steps
        except AssertionError, e: 
            #~ print str(e)
            self.diagnostic = str(e)

    def step_it_prints_a_diagnostic(self, sample):
        r'it prints a diagnostic containing "([^"]+)"'
        
        self.diagnostic.index(sample)  #  CONSIDER  clearer diagnostics!!
        #self.assertTrue(diagnostic, 'foo')
        
    def step_the_second_line_contains(self, docstring):
        r'the second line contains "([^"]+)"'
        
        self.diagnostic.split('\n')[4].index(docstring)

    def step_it_contains_1_step(self):
        r'it contains 1 step'

        self.assertEqual(1, len(self.steps))

    def step_the_step_concept_is_(self, concept):
        r'the step concept is (.+)'

        self.assertEqual(concept, self.concept)
        
    def step_a_source_file_with_a_Given_(self, predicate):
        r'a source file with a (.+)'

        self.predicate = predicate.replace('\\n', '\n')
        
    def step_we_evaluate_the_file(self):
        r'we evaluate the file'

        self.viridis = Viridis()
        self.suggestion = self.viridis.suggest_doc_string(self.predicate)

    def step_we_convert_it_into_a_(self, suggestion):
        r'we convert it into a (.+)'

        self.assertEqual(suggestion, self.suggestion)

    def step_add_extra_arguments(self, extra = ''):  #  TODO  blank columns should exist!
        r'add (.+) arguments'

        self.assertEqual(extra, self.viridis.extra_arguments)


#~ Scenario: Leading # marks comment lines.
    #~ (Warning: Only leading marks are respected for now!)
    #~ Given a feature file with "When something
                               #~ \# Given nothing"
    #~ When Moralia evaluates the file
    #~ Then it contains 1 step
    #~ And the first step contains "something"
    #~ And the first step does not contain "nothing"

#  TODO  count test cases correctly regarding entire batch
#  TODO  auto-tables
#  TODO  escape string catch

if __name__ == '__main__':
      unittest.main()  #  NOTE  this seems to return the correct shell value


