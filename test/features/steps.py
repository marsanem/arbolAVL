# -*- coding: utf-8 -*-
from lettuce import *
import avl as m

@step(u'The list: "([^"]*)"')
def given_the_list_group1(step, group1):
    world.avl = m.Avl(group1.split(', '))
    

@step(u'What do you like "([^"]*)" or "([^"]*)"')
def when_what_do_you_like_group1_or_group2(step, group1, group2):
    assert "Que prefieres 'al pesto' o 'bbq'?" == world.avl.question(), 'obtuve: {}'.format(world.avl.question())

@step(u'I anwser: "([^"]*)"')
def and_i_anwser_group1(step, group1):
    world.avl.answer(group1)

@step(u'sorted list should look: "([^"]*)"')
def then_sorted_list_should_look_group1(step, group1):
    assert group1 == world.avl.sorted(), 'la lista se ve {}'.format(world.avl.sorted())
