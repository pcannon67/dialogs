#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import unittest

from dialog import Dialog

from resources_manager import ResourcePool

# raquel
from sentence import *
from parsing.parser import Parser

#sentence="take the blue cube."
#sentence="give me the small orange bottle."
#sentence="help me with this blueish thing."

#sentence="The bottle that is blue, is on the table"

#sentence="Could you take the blue cube?"
#sentence="Can you take my cube?"
#sentence="I want you to show me the black tape."
#sentence="Please take the blue cube."
#sentence="Please take the blue cube."
#sentence="put the grey tape next to the blue cube."
#sentence="put the tape on the table, next to the blue cube."
#sentence="put my tape in the trashbin."
#sentence="Where is the blue cube?"
#sentence="Where are the cubes?"
#sentence="What do you see?"
#sentence="Jido, I need the grey tape!"

#sentence="I want you to help the man that wants to bring me the blue car."

class TestBaseSentenceDialog(unittest.TestCase):
    """Tests the processing of simple sentence by the Dialog module.
    These sentences don't require discrimination.
    This must be tested with oro-server using the testsuite.oro.owl ontology.
    """

    def check_results(self, res, expected):
        def check_triplets(tr , te):
            tr_split = tr.split()
            te_split = te.split()
            
            return (tr_split[0] == te_split[0] or te_split[0] == '*') and\
                    (tr_split[1] == te_split[1]) and\
                    (tr_split[2] == te_split[2] or te_split[2] == '*')       
        while res:
            r = res.pop()
            for e in expected:
                if check_triplets(r, e):
                    expected.remove(e)
        return expected == res
    
    
    def setUp(self):
        self.dialog = Dialog()
        self.dialog.start()
        
        self.oro = ResourcePool().ontology_server
        
        try:
            self.oro.add(['shelf1 rdf:type Shelf',
                        'table1 rdf:type Table', 
                        'table2 rdf:type Table', 
                        'table2 hasColor blue', 
                        'Banana rdfs:subClassOf Plant',
                        'y_banana rdf:type Banana',
                        'y_banana hasColor yellow',
                        'y_banana isOn shelf',
                        'green_banana rdf:type Banana',
                        'green_banana hasColor green',
                        'green_banana isOn table2'
                        ])
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass

    def test_sentence1(self):

        print("\n##################### test_sentence1 ########################\n")
        
        ####
        stmt = "put the yellow banana on the shelf"
        ####

        expected_result = [ 'myself desires *',
                            '* rdf:type Place',
                            '* performedBy myself',
                            '* actsOnObject y_banana',
                            '* receivedBy shelf']
        ###
        res = self.dialog.test('myself', stmt)
        self.assertTrue(self.check_results(res, expected_result))
        

    def test_sentence2(self):
        
        print("\n##################### test_sentence2 ########################\n")

        ####
        stmt = "give me the green banana"
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Give',
                            '* performedBy myself',
                            '* actsOnObject green_banana',
                            '* receivedBy myself']
        ###
        res = self.dialog.test('myself', stmt)
        self.assertTrue(self.check_results(res, expected_result))
        

    def test_sentence3(self):
        
        print("\n##################### test_sentence3 ########################\n")              
                
        ####
        stmt = "the yellow banana is big"
        ####
        expected_result = ['y_banana hasSize big']
        ###
        res = self.dialog.test('myself', stmt)
        self.assertTrue(self.check_results(res, expected_result))
    
    
    def test_sentence4(self):
        
        print("\n##################### test_sentence4 ########################\n")
        ####
        stmt = "the green banana is good"
        ####
        res = self.dialog.test('myself', stmt)
        ###
        expected_result = ['green_banana hasFeature good']
        self.assertTrue(self.check_results(res, expected_result))

    def tearDown(self):
        self.dialog.stop()
        self.dialog.join()
        
class TestVerbalizeDialog(unittest.TestCase):
    """Tests the verbalization features of the Dialog module.
    """
    
    def setUp(self):
        self.dialog = Dialog()
        self.dialog.start()

    def test_verbalize1(self):
           
        print("\n##################### test_verbalize1: simple statements ########################\n")
        myP = Parser()                            
        stmt = "The cup is on the desk."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)
        
        print "\n####\n"
        
        stmt = "The green bottle is next to Joe."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)

    def test_verbalize2(self):
        
        print("\n##################### test_verbalize2: yes/no questions ########################\n")
        myP = Parser()

        stmt = "Are you a robot?"
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)


    def test_verbalize3(self):
        
        print("\n##################### test_verbalize3: orders ########################\n")
        myP = Parser()

        stmt = "Put the yellow banana on the shelf."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)
        
        print "\n####\n"
        
        stmt = "Give me the green banana."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)
        
        print "\n####\n"
        
        stmt = "Give the green banana to me."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)

        
    def test_verbalize4(self):
        
        print("\n##################### test_verbalize4: W questions ########################\n")
        myP = Parser()
        
        stmt = "Where is the box?"
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)
        
        print "\n####\n"
        
        stmt = "What are you doing now?"
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(stmt, res)



    def test_verbalize5(self):
        
        print("\n##################### test_verbalize5 ########################\n")
        myP = Parser()
        
        stmt = "Jido, tell me where you go."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)

    def tearDown(self):
        self.dialog.stop()
        self.dialog.join()
        
        
class TestDiscriminateDialog(unittest.TestCase):
    """Tests the differents features of the Dialog module.
    This must be tested with oro-server using the testsuite.oro.owl ontology.
    """

    def check_results(self, res, expected):
        def check_triplets(tr , te):
            tr_split = tr.split()
            te_split = te.split()
            
            return (tr_split[0] == te_split[0] or te_split[0] == '*') and\
                    (tr_split[1] == te_split[1]) and\
                    (tr_split[2] == te_split[2] or te_split[2] == '*')       
        while res:
            r = res.pop()
            for e in expected:
                if check_triplets(r, e):
                    expected.remove(e)
        return expected == res
    
    
    def setUp(self):
        self.dialog = Dialog()
        self.dialog.start()
        
        self.oro = ResourcePool().ontology_server
        
        try:
            self.oro.add(['shelf1 rdf:type Shelf',
                        'table1 rdf:type Table', 
                        'table2 rdf:type Table', 
                        'table2 hasColor blue', 
                        'Banana rdfs:subClassOf Plant',
                        'y_banana rdf:type Banana',
                        'y_banana hasColor yellow',
                        'y_banana isOn shelf',
                        'green_banana rdf:type Banana',
                        'green_banana hasColor green',
                        'green_banana isOn table2',
                        'ACCESSKIT rdf:type Gamebox', 'ACCESSKIT hasColor white', 'ACCESSKIT hasSize big', 'ACCESSKIT isOn table1',
                        'ORANGEBOX rdf:type Gamebox', 'ORANGEBOX hasColor orange', 'ORANGEBOX hasSize big', 'ORANGEBOX isOn ACCESSKIT',
                        'MYBOX rdf:type Gamebox', 'MYBOX hasColor orange', 'MYBOX hasSize small', 'MYBOX isOn table1',
                        'SPACENAVBOX rdf:type Gamebox', 'SPACENAVBOX hasColor white'
                        ])
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass

    def test_discriminate1(self):
        
        print("\n##################### test_discriminate1 ########################\n")
        ####
        stmt = "the banana is good"
        answer = "the green one"
        ####
        res = self.dialog.test('myself', stmt, answer)
        expected_result = [ 'green_banana hasFeature good']
        self.assertTrue(self.check_results(res, expected_result))
    

    def test_discriminate2(self):
        
        print("\n##################### test_discriminate2 ########################\n")
        ####
        stmt = "the banana is good"
        answer = "the yellow one"
        ####
        res = self.dialog.test('myself', stmt, answer)
        expected_result = [ 'y_banana hasFeature good']
        self.assertTrue(self.check_results(res, expected_result))
        
    def test_discriminate3(self):
        
        print("\n##################### test_discriminate3 ########################\n")
        ####
        stmt = "give me the banana"
        answer = "the green one"
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Give',
                            '* performedBy myself',
                            '* actsOnObject green_banana',
                            '* receivedBy myself']
        ###
        res = self.dialog.test('myself', stmt, answer)
        print res
        self.assertTrue(self.check_results(res, expected_result))
        
        
    def test_discriminate4(self):
        
        print("\n##################### test_discriminate4 ########################\n")
        ####
        stmt = "get the gamebox which is on the table ;"
        answer = "the orange one"
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Get',
                            '* performedBy myself',
                            '* actsOnObject MYBOX',
                            '* receivedBy myself']
        ###
        res = self.dialog.test('myself', stmt, answer)
        print res
        self.assertTrue(self.check_results(res, expected_result))
        
    def test_discriminate5(self):
        
        print("\n##################### test_discriminate5 ########################\n")
        ####
        stmt = "get the orange gamebox"
        answer = "the one that is on the ACCESSKIT ,"
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Get',
                            '* performedBy myself',
                            '* actsOnObject ORANGEBOX']
        ###
        res = self.dialog.test('myself', stmt, answer)
        print res
        self.assertTrue(self.check_results(res, expected_result))

    def test_discriminate6(self):
        
        print("\n##################### test_discriminate6 ########################\n")
        ####
        stmt = "get the big gamebox"
        answer = "the white one"
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Get',
                            '* performedBy myself',
                            '* actsOnObject ACCESSKIT']
        ###
        res = self.dialog.test('myself', stmt, answer)
        print res
        self.assertTrue(self.check_results(res, expected_result))


    """
    def test_discriminate7(self):
        
        print("\n##################### test_discriminate7 ########################\n")
        ####
        stmt = "get the gamebox which is on the ACCESSKIT ;"
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Get',
                            '* performedBy myself',
                            '* actsOnObject ORANGEBOX']
        ###
        res = self.dialog.test('myself', stmt)
        print res
        self.assertTrue(self.check_results(res, expected_result))
    """

    


    def tearDown(self):
        self.dialog.stop()
        self.dialog.join()
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format="%(message)s")
    
    # all tests
    #unittest.main()
    
    # executing only some tests

    suiteSimpleSentences = unittest.TestSuite()
    suiteSimpleSentences.addTest(TestBaseSentenceDialog('test_sentence1'))
    suiteSimpleSentences.addTest(TestBaseSentenceDialog('test_sentence2'))
    suiteSimpleSentences.addTest(TestBaseSentenceDialog('test_sentence3'))
    suiteSimpleSentences.addTest(TestBaseSentenceDialog('test_sentence4'))
    
    suiteVerbalization = unittest.TestSuite()
    suiteVerbalization.addTest(TestVerbalizeDialog('test_verbalize1'))
    suiteVerbalization.addTest(TestVerbalizeDialog('test_verbalize2'))
    suiteVerbalization.addTest(TestVerbalizeDialog('test_verbalize3'))
    suiteVerbalization.addTest(TestVerbalizeDialog('test_verbalize4'))
    suiteVerbalization.addTest(TestVerbalizeDialog('test_verbalize5'))
    
    suiteDiscriminate = unittest.TestSuite()
    suiteDiscriminate.addTest(TestDiscriminateDialog('test_discriminate1'))
    suiteDiscriminate.addTest(TestDiscriminateDialog('test_discriminate2'))
    suiteDiscriminate.addTest(TestDiscriminateDialog('test_discriminate3'))
    suiteDiscriminate.addTest(TestDiscriminateDialog('test_discriminate4'))
    suiteDiscriminate.addTest(TestDiscriminateDialog('test_discriminate5'))
    suiteDiscriminate.addTest(TestDiscriminateDialog('test_discriminate6'))
    
    
    unittest.TextTestRunner(verbosity=2).run(suiteSimpleSentences)
    #unittest.TextTestRunner(verbosity=2).run(suiteVerbalization)
    #unittest.TextTestRunner(verbosity=2).run(suiteDiscriminate)
