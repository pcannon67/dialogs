
"""
 Created by Chouayakh Mahdi                                                       
 07/07/2010                                                                       
 The package contains functions needed to perform verbalisation of sentences      
 Functions:                                                                       
    statement : to verbalise a statment                                           
    imperative : to verbalise an imperative                             
    relative : to verbalise a relative              
    y_o_question : to verbalise an yes or no question                             
    w_question : to verbalise a w_question                   
    description_ques : to verbalise a question about description                      
    quantity_ques : to verbalise a question about quantity                        
    choice_ques : to verbalise a question about choice                            
    possession_ques : to verbalise a question about possession                    
    sub_process : to verbalises a subsentence                                      
"""
import element_rebuilding
import other_functions


"""
Statement of lists
"""
how_list=['often','soon']



def statement(analysis):
    """
    This function verbalises a statment                                              
    Input=class sentence                              Output=sentence                
    """
    
    #Recovering the subject
    phrase=element_rebuilding.nom_struc_rebuilding(analysis.sn)
    
    if analysis.sv!=[]:
        #Recovering the end of the sentence
        phrase=element_rebuilding.end_statement_rebuilding(phrase, analysis.sv, analysis.sn, analysis.data_type,analysis.aim)
        
        #Recovering subsentences
        for s in analysis.sv[0].vrb_sub_sentence:
            phrase=phrase+sub_process(s)

    #Eliminate redundancies if there are
    phrase=other_functions.eliminate_redundancy(phrase)
    
    #If it is a relative form
    if analysis.data_type=='relative' or analysis.data_type=='subsentence':
        if phrase[len(phrase)-1][len(phrase[len(phrase)-1])-1]!=',':
            phrase[len(phrase)-1]=phrase[len(phrase)-1]+','
        return phrase
    if analysis.data_type=='w_question':
        return phrase+['?']
    
    #To take of all not useless comma
    while phrase[len(phrase)-1][len(phrase[len(phrase)-1])-1]==',':
        phrase[len(phrase)-1]=phrase[len(phrase)-1][:len(phrase[len(phrase)-1])-1]
    return phrase+['.']
    
    
        
def imperative(analysis):
    """
    This function verbalises an imperative                                           
    Input=class sentence                              Output=sentence                
    """

    #init
    phrase=[]
    
    if analysis.sv!=[]:
        #Recovering the basic part of the sentence
        phrase=element_rebuilding.end_statement_rebuilding(phrase, analysis.sv, analysis.sn, analysis.data_type,analysis.aim)
    
        #Recovering subsentences
        for s in analysis.sv[0].vrb_sub_sentence:
            phrase=phrase+sub_process(s)
            
    #Eliminate redundancies if there are
    phrase=other_functions.eliminate_redundancy(phrase)
    
    if analysis.data_type=='relative':
        if phrase[len(phrase)-1][len(phrase[len(phrase)-1])-1]!=',':
            phrase[len(phrase)-1]=phrase[len(phrase)-1]+','
        return phrase
    
    return phrase+['.']



def relative(relative, ns):
    """
    This function verbalises a relative                                  
    Input=class sentence                              Output=sentence                
    """
    
    if ns==[]:
        phrase=statement(relative)
    else:
        relative.sn=ns
        phrase=imperative(relative)
    return phrase



def y_o_question(analysis):
    """
    This function verbalises an yes or no question                                   
    Input=class sentence                              Output=sentence                
    """
    
    #init
    phrase=[]
    
    #Recovering the subject
    subject=element_rebuilding.nom_struc_rebuilding(analysis.sn)
    
    if analysis.sv!=[]:
        #Recovering the end of the sentence
        phrase=element_rebuilding.end_question_rebuilding(phrase, analysis.sv, analysis.sn,analysis.aim)
    
        #We need special processing to find the position of the subject
        if analysis.sv[0].state=='negative':
            phrase=phrase[0:2]+subject+phrase[2:]
        else:
            phrase=[phrase[0]]+subject+phrase[1:]
    
        #Recovering subsentences
        for s in analysis.sv[0].vrb_sub_sentence:
            phrase=phrase+sub_process(s)
    else:
        phrase=subject
        
    #Eliminate redundancies if there are
    phrase=other_functions.eliminate_redundancy(phrase)
    
    #If it is a question about the origin
    if analysis.aim=='origin':
        return phrase+['from']+['?']
    
    return phrase+['?']



def w_question(analysis):
    """
    This function verbalises a w_question                                            
    Input=class sentence                              Output=sentence                
    """
    if analysis.sv!=[]:
        #Opinion is a what question so we have to make some changes
        if analysis.sv[0].vrb_main[0].endswith('like'):
            verb=analysis.sv[0].vrb_main[0]
            analysis.sv[0].vrb_main[0]=verb[:len(verb)-4]+'think+of'

    #processing as yes or no question
    phrase=y_o_question(analysis)
    
    #Specific processing for invitation
    if analysis.aim=='invitation':
        return ['how', 'about']+phrase[1:]
    
    #Specific processing for classification
    if analysis.aim.startswith('classification'):
        aim_question=other_functions.list_rebuilding(analysis.aim)
        return ['what','kind','of']+aim_question[1:]+phrase
    
    for i in how_list:
        if i==analysis.aim:
            return ['how']+[analysis.aim]+phrase
    
    #It is an how question
    if other_functions.is_an_adj(analysis.aim)==1:
        return ['how']+[analysis.aim]+phrase
    elif analysis.aim=='manner':
        return ['how']+phrase 
        
    if analysis.aim=='thing' or analysis.aim=='situation' or analysis.aim=='explication' or analysis.aim=='opinion':
        return ['what']+phrase
    return ['what']+[analysis.aim]+phrase



def description_ques(analysis):
    """
    This function verbalises a question about description                               
    Input=class sentence                              Output=sentence
    """
    if analysis.sv[0].vrb_tense.startswith('present'):
        analysis.sv[0].vrb_tense='present progressive'
    if analysis.sv[0].vrb_tense.startswith('past'):
        analysis.sv[0].vrb_tense='present progressive'
    sentence=y_o_question(analysis)
    for i in sentence:
        if i=='likeing':
            sentence[sentence.index(i)]='like'
    return ['what']+sentence
            
    

def quantity_ques(analysis):
    """
    This function verbalises a question about quantity                               
    Input=class sentence                              Output=sentence
    """
    
    #init
    phrase=[]
    
    #We have to memorise the verb
    verb=other_functions.list_rebuilding(analysis.sv[0].vrb_main[0])
    
    if analysis.sv!=[]:
    #First case : aim is the subject with verb be
        if analysis.sv[0].d_obj==[] and (verb[0]=='be' or (len(verb)>1 and  verb[1]=='be')):
            phrase=statement(analysis)
            return ['how','much']+phrase[1:len(phrase)-1]+['?']
    
        #Second case : aim is the subject without verb be
        elif  analysis.sv[0].d_obj==[]:
            return ['how','much']+y_o_question(analysis)
    
        #Third case : as yes no question without the direct complement
        else:
            subject=element_rebuilding.nom_struc_rebuilding(analysis.sn)
            
            #Same processing with yes no question
            phrase=element_rebuilding.vrb_ques_rebuilding(analysis.sv[0].vrb_tense, analysis.sv[0].vrb_main, analysis.sv[0].vrb_adv, analysis.sn, analysis.sv[0].state, analysis.aim)
            
            for x in analysis.sv[0].i_cmpl:
                phrase=phrase+element_rebuilding.indirect_compl_rebuilding(x)
            
            phrase=phrase+analysis.sv[0].advrb
            for k in analysis.sv[0].sv_sec:
                phrase=phrase+['to']+k.vrb_adv+other_functions.list_rebuilding(k.vrb_main[0])
                
                #We add the direct and indirect complement
                if k.i_cmpl!=[] and k.i_cmpl[0].prep!=[]:
                    phrase=phrase+element_rebuilding.nom_struc_rebuilding(k.d_obj)
                    for x in k.i_cmpl:
                        phrase=phrase+element_rebuilding.indirect_compl_rebuilding(x)
                else:
                    if k.i_cmpl!=[]:
                        phrase=phrase+element_rebuilding.indirect_compl_rebuilding(k.i_cmpl[0])
                    phrase=phrase+element_rebuilding.nom_struc_rebuilding(k.d_obj)
                    #init
                    x=1
                    while x < len(k.i_cmpl):
                        phrase=phrase+element_rebuilding.indirect_compl_rebuilding(k.i_cmpl[x])
                        x=x+1
                
                phrase=phrase+k.advrb
    
            for s in analysis.sv[0].vrb_sub_sentence:
                phrase=phrase+sub_process(s)
            
            #processing of the state
            if analysis.sv[0].state=='negative':
                phrase=phrase[0:2]+subject+phrase[2:]
            else:
                phrase=[phrase[0]]+subject+phrase[1:]
    
            return ['how', 'much']+analysis.sv[0].d_obj[0].noun+phrase+['?']



def possession_ques(analysis):
    """
    This function verbalises a question about possession                             
    Input=class sentence                              Output=sentence                
    """

    #processing as statement
    phrase=statement(analysis)

    #We have to know if it is plural or singular
    if other_functions.plural_noun(analysis.sn)==1:
        return ['whose']+phrase[:len(phrase)-1]+['these']+['?']
    else:
        return ['whose']+phrase[1:len(phrase)-1]+['this']+['?']



def sub_process(analysis):
    """
    This function verbalises a subsentence                                           
    Input=class sentence                              Output=sentence                
    """
    
    #processing as statement
    subsentence=statement(analysis)
    if analysis.aim=='if':
        return [',']+[analysis.aim]+subsentence
    return [analysis.aim]+subsentence
