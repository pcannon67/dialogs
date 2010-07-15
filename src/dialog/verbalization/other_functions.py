
"""
 Created by Chouayakh Mahdi                                                       
 07/07/2010                                                                       
 The package contains functions used by all other packages                        
 Functions:                                                                       
    list_recovery : to return the list of strings without '+'                     
    eliminate_redundancy : to eliminate redundancy in the phrase                  
    convert_string : to return concatenate token to have a string (sentence)      
"""



"""
Statement of lists
"""
cap_let_list=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']



def find_cap_lettre(word):
    """
    Function return 1 if the word starts with uppercase letter                       
    Input=word               Output=flag(0 if no uppercase or 1 if uppercase)        
    """
    for i in cap_let_list:
        if word[0]==i:
            return 1
    return 0



def list_recovery(string):
    """
    This function returns the list of strings without '+'                            
    Input=the string           Output=the list of strng corresponding                
    """

    for i in string:
        if i=='+':
            return [string[:string.index(i)]] + list_recovery(string[string.index(i)+1:])
    return [string]



def eliminate_redundancy(phrase):
    """
    This function to eliminate redundancy in the phrase                              
    Input=phrase                                             Output=phrase           
    """

    #init
    phrase_aux=[]

    if phrase!=[]:

        phrase_aux=[phrase[0]]

        #We loop in phrase
        for i in range(1,len(phrase)):
            if phrase[i]!=phrase[i-1]:
                phrase_aux=phrase_aux+[phrase[i]]

    return phrase_aux



def convert_string(token_list):
    """
     This function returns concatenate token to have a string (sentence)
     Input=list of token                                    Output=sentence           
    """

    #list is empty
    if token_list==[]:
        return ''

    if len(token_list)==1:
        return token_list[0]
    else:
        return token_list[0]+' '+convert_string(token_list[1:])
    