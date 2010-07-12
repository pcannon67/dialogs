#!/usr/bin/python
# -*- coding: utf-8 -*-

#SVN:rev202 + PythonTidy


"""
######################################################################################
## Created by Chouayakh Mahdi                                                       ##
## 21/06/2010                                                                       ##
## The package contains functions that affect verbal structure                      ##
## Functions:                                                                       ##
##    find_vrb_adv : to recover the list of adverbs bound to verb                   ##
##    find_adv : to recover the list of adverbs                                     ##
##    check_proposal : to know if there is a proposal before the object             ##
##    recover_obj_iobj : to find the direct, indirect object and the adverbial      ##
##    find_scd_vrb : to recover the second verb in a sentence                       ##
##    treat_scd_sentence : to treat the second sentence found                       ##
##    treat_subsentence : to treat the subsentence                                  ##
######################################################################################
"""
from sentence import *
import analyse_nominal_group
import analyse_nominal_structure
import other_functions
import analyse_verb
import analyse_sentence


"""
############################## Statement of lists ####################################
"""
aux_list=['have', 'has', 'had', 'is', 'are', 'am', 'was', 'were', 'will']
adv_list=['here','tonight', 'yesterday', 'tomorrow', 'today', 'now']
proposal_list=['in', 'on', 'at', 'from', 'to', 'about', 'for', 'next', 'last', 'ago', 'with', 'by']
rel_list=['which', 'who']
sub_list=['that', 'while', 'but','where', 'when']


"""
######################################################################################
## This function recovers the list of adverbs bound to verb                         ##
## Input=sentence                        Output=verb's adverb list                  ##
######################################################################################
"""
def find_vrb_adv(phrase):

    #If phrase is empty
    if phrase==[]:
        return []

    #If there is an auxiliary
    for i in aux_list:
        if i == phrase[0]:
            if phrase[1].endswith('ly'):
                return [phrase[1]]

    else:
        if phrase[0].endswith('ly'):
            return [phrase[0]]

    return []


"""
######################################################################################
## This function recovers the list of adverbs                                       ##
## Input=sentence                            Output=adverbs list                    ##
######################################################################################
"""
def find_adv(phrase):

    #If phrase is empty
    if phrase ==[]:
        return []

    #If the adverb is in the list
    for i in phrase:
        for j in adv_list:
            if j==i:
                return [i]+find_adv(phrase[phrase.index(i)+1:])

    #Using a rule of grammar
    for k in phrase:
        if k.startswith('every'):
            return [k]+find_adv(phrase[phrase.index(k)+1:])

    #Default case
    return []


"""
######################################################################################
## This function to know if there is a proposal before the object                   ##
## Input=sentence and object            Output=proposal if the object is indirect   ##
######################################################################################
"""
def check_proposal(phrase, object):

    if object==[]:
        return []

    #si on a une preposition on renvoie l'objet
    for i in proposal_list:
        if object!=phrase[0:len(object)] and i==phrase[phrase.index(object[0])-1]:
            return [i]

    #Default case
    return []


"""
######################################################################################
## This function finds the direct, indirect object and the adverbial                ##
## We, also, put these information in the class                                     ##
## Input=sentence and verbal class              Output=sentence and verbal class    ##
######################################################################################
"""
def recover_obj_iobj(phrase, vg):
    
    #init
    conjunction='AND'
    
    #We search the first nominal group in sentence
    object= analyse_nominal_group.find_sn(phrase)
   
    while object!=[]:

        #If it is not a direct object => there is a proposal
        proposal=check_proposal(phrase, object)
       
        if proposal!=[]:

            gr_nom_list=[]
            #This 'while' is for duplicate with 'and'
            while object!=[]:
                pos_object=phrase.index(object[0])
                
                #We refine the nominal group if there is an error like ending with question mark
                object=analyse_nominal_group.refine_nom_gr(object)
        
                #Recovering nominal group
                gr_nom_list=gr_nom_list+[analyse_nominal_structure.fill_nom_gr(phrase, object, pos_object,conjunction)]

                #We take off the nominal group
                phrase=analyse_nominal_group.take_off_nom_gr(phrase, object,pos_object)

                #We will take off the proposal
                phrase=phrase[:phrase.index(proposal[0])]+phrase[phrase.index(proposal[0])+1:]

                #If there is a relative
                begin_pos_rel=analyse_nominal_group.find_relative(object, phrase, pos_object,rel_list)
                end_pos_rel=other_functions.recover_end_pos_sub(phrase, rel_list)
                if begin_pos_rel!=-1:
                    #We remove the relative part of the phrase
                    phrase=phrase[:begin_pos_rel]+phrase[end_pos_rel:]

                #If there is 'and', we need to duplicate the information
                if len(phrase)!=0 and (phrase[0]=='and' or phrase[0]=='or'):
                    
                    object=analyse_nominal_group.find_sn_pos(phrase[1:], 0)
                    
                    #We treat the 'or' like the 'and' and remove it
                    if phrase[0]=='or':
                        conjunction='OR'
                    else:
                        conjunction='AND'
                    phrase=phrase[1:]
                
                else:
                    object=[]

            vg.i_cmpl=vg.i_cmpl+[Indirect_Complement(proposal,gr_nom_list)]


        else:
            #It is a direct complement
            gr_nom_list=[]
            #It reproduces the same code as above
            while object!=[]:
                pos_object=phrase.index(object[0])
                
                #We refine the nominal group if there is an error like ending with question mark
                object=analyse_nominal_group.refine_nom_gr(object)
                
                #Recovering nominal group
                gr_nom_list=gr_nom_list+[analyse_nominal_structure.fill_nom_gr(phrase, object, pos_object, conjunction)]
                
                #We take off the nominal group
                phrase=analyse_nominal_group.take_off_nom_gr(phrase, object, pos_object)
                #If there is a relative

                begin_pos_rel=analyse_nominal_group.find_relative(object, phrase, pos_object,rel_list)
                end_pos_rel=other_functions.recover_end_pos_sub(phrase, rel_list)
                
                if begin_pos_rel!=-1:
                    #We remove the relative part of the phrase
                    phrase=phrase[:begin_pos_rel]+phrase[end_pos_rel:]

                if len(phrase)!=0 and (phrase[0]=='and' or phrase[0]=='or'):
                    
                    object=analyse_nominal_group.find_sn_pos(phrase[1:], 0)
                    
                    #We treat the 'or' like the 'and' and remove it
                    if phrase[0]=='or':
                        conjunction='OR'
                    else:
                        conjunction='AND'
                    phrase=phrase[1:]
                    
                else:
                    object=[]

            #In a sentence there is just one direct complement
            if vg.d_obj==[]:
                vg.d_obj=gr_nom_list
            else:
                #Else the first nominal group found is indirect and this one is direct complement
                vg.i_cmpl=vg.i_cmpl+[Indirect_Complement([],vg.d_obj)]
                vg.d_obj=gr_nom_list

        object= analyse_nominal_group.find_sn(phrase)

    return phrase


"""
######################################################################################
## This function recovers the second verb in a sentence                             ##
## Input=sentence                        Output=second verb of the sentence         ##
######################################################################################
"""
def find_scd_vrb(phrase):
    
    for i in phrase:

        #If there is 'to'
        if i=='to':

            #It should not be followed by a noun or by an adverb
            if analyse_nominal_group.find_sn_pos(phrase, phrase.index(i)+1)==[] and find_adv([phrase[phrase.index(i)+1]])==[]:

                #If there is a proposal after 'to'
                for j in proposal_list:
                    if j == phrase[phrase.index(i)+1]:
                        return []

                return [phrase[phrase.index(i)+1]]
    
    return []


"""
######################################################################################
## This function treats the second sentence found                                   ##
## Input=sentence, verbal class and the second verb                                 ##
## Output=sentence and verbal class                                                 ##
######################################################################################
"""
def treat_scd_sentence(phrase, vg, sec_vrb):

    #We take off the part of the sentence after 'to'
    scd_sentence=phrase[phrase.index(sec_vrb[0]):]
    phrase=phrase[:phrase.index(sec_vrb[0])]
    
    #We treat the verb
    if scd_sentence[0]=='not':
        scd_verb=[other_functions.convert_to_string(analyse_verb.return_verb(scd_sentence, [scd_sentence[1]], ''))]
        vg.sv_sec=vg.sv_sec+[Verbal_Group(scd_verb, [], '', [], [], [], [], 'negative',[])]
        #We delete the verb
        scd_sentence= scd_sentence[phrase.index(scd_sentence[1])+1:]
    else:
        scd_verb=[other_functions.convert_to_string(analyse_verb.return_verb(scd_sentence, [scd_sentence[0]], ''))]
        vg.sv_sec=vg.sv_sec+[Verbal_Group(scd_verb, [], '', [], [], [], [], 'affirmative',[])]
        #We delete the verb
        scd_sentence= scd_sentence[scd_sentence.index(scd_sentence[0])+1:]

    #We treat the end of the second sentence
    vg.sv_sec[0].advrb=find_adv(scd_sentence)
    scd_sentence=recover_obj_iobj(scd_sentence, vg.sv_sec[0])

    return phrase


"""
######################################################################################
## This function treats the subsentence                                             ##
## Input=sentence and verbal class         Output=sentence and verbal class         ##
######################################################################################
"""
def treat_subsentence(phrase,vg):
    
    #init
    begin_pos=-1

    #If phrase is empty
    if len(phrase)<0:
        return phrase

    #We look down the list to see if there is a subsentence
    for w in sub_list:
        for i in phrase:
            if i == w:
                begin_pos=phrase.index(i)

                #We include the relative's proposal if there are relatives in the subsentence
                end_pos= other_functions.recover_end_pos_sub(phrase[begin_pos:], sub_list+rel_list)

                #We have to remove the proposal
                subsentence= phrase[begin_pos+1:end_pos]
                
                #We perform treatment
                vg.vrb_sub_sentence=vg.vrb_sub_sentence+[analyse_sentence.other_sentence('subsentence', w ,subsentence)]
                
                #We delete the subsentence
                phrase=phrase[:phrase.index(i)]
                phrase=phrase[end_pos:]
                
                return phrase

    return phrase
        