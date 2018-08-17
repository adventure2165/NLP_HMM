import random
from sklearn.model_selection import train_test_split
import math
import pickle

def main():
    print("Please input your file")
    file_name = input()
    file = open("./"+file_name,encoding="utf-8")
    total_text = file.read()
    each_line_text = total_text.split("\n")
    train_text_raw = list()
    test_text = list()
    for i in each_line_text:
        if "<emotion>" in i or "</emotion>" in i:
            train_text_raw.append(i)
        else:
            test_text.append(i)
    random.shuffle(train_text_raw)
    random.shuffle(test_text)
    train_text_raw = list_divider(train_text_raw,10)
    best_accuracy = 0
    best_model = [0,0,0]
    for i in range(10):
        train_text_set=[]
        number = [x for x in range(10)]
        for j in number:
            if j == i:
                pass
            else:
                train_text_set = train_text_set + train_text_raw[j]
        validation_text_set = train_text_raw[i]
        train_text_preprocessed = opinion_tagger(train_text_set)
        validation_text_preprocessed = opinion_tagger(validation_text_set)
        validation_text_tag_removed = tag_remover(validation_text_set)
        initial_probability, propagation_probability, emission_probability  = train(train_text_preprocessed)
        accuracy = score(validation_text_preprocessed,validation_text_tag_removed,initial_probability,propagation_probability,emission_probability)
        print(i,"train accuracy : ",accuracy)
        if accuracy>=best_accuracy:
            best_accuracy = accuracy
            best_model = [initial_probability,propagation_probability,emission_probability]
    print(best_accuracy)
    predicted_text = predict(test_text,best_model[0],best_model[1],best_model[2])
    extracted_opinion = opinion_extractor(predicted_text)
    with open('model.m', 'wb') as file:
        pickle.dump(best_model, file)
    print(extracted_opinion)

def load_best_model():
    try:
        with open('model.m', 'rb') as file:
            best_model = pickle.load(file)
            return best_model
    except:
        print("You must make the model first. please run the extractor.py and make sure model.m file created in same folder")
        
def list_divider(lst, n):
    division = len(lst) /n
    return [lst[round(division * i):round(division * (i + 1))] for i in range(n)]


def train(text):
    i = get_initial_prob(text)
    p = get_propagation_prob(text)
    e = get_emission(text)
    return i, p, e

def score(predicted, origin,initial_probability,propagation_probability,emission_probability):
    origin_get_tag = predict(origin,initial_probability,propagation_probability,emission_probability)
    predict_vector = []
    origin_vector = []
    correct = 0
    total = 0
    for i in range(len(predicted)):
        temp_list=[]
        for j in range(len(predicted[i])):
            temp_list.append(predicted[i][j][1])
        predict_vector.append(temp_list)
        
    for k in range(len(origin_get_tag)):
        temp_list=[]
        for l in range(len(origin_get_tag[k])):
            temp_list.append(origin_get_tag[k][l][1])
        origin_vector.append(temp_list)
    for m in range(len(predict_vector)):
        for n in range(len(predict_vector[m])):
            if predict_vector[m][n] == origin_vector[m][n]:
                correct +=1
                total +=1
            else:
                total +=1
    print("score : ", correct/total*100,"%")
    return correct/total*100
                
    

def opinion_extractor(predict):
    extracted_text = []
    for i in range(len(predict)):
        extract = list()
        for j in range(len(predict[i])):
            if predict[i][j][1] == 1:
                extract.append(predict[i][j][0])
            else:
                pass
        extracted_text.append(extract)
    return extracted_text

def tag_remover(text):
    tag_removed_text = list()
    for i in text:
        if i.find("<emotion>") != -1:
            current_text = i.replace("<emotion>","")
            current_text = current_text.replace("</emotion>","")
            tag_removed_text.append(current_text)
        else:
            tag_removed_text.append(i)
    return tag_removed_text  
    
def opinion_tagger(train_text_X):
    train_text_preprocessed = list()
    for i in train_text_X:
        temp_list = list()
        splited_text = i.split(" ")
        for j in splited_text:
            if j.find("<emotion>") != -1:
                current_text = j.replace("<emotion>","")
                current_text = current_text.replace("</emotion>","")
                temp_list.append((current_text,1))
            elif j == "[" or j == "]" or j == "(" or j == ")" or j == "," or j == ".":
                temp_list.append((j,0))
            else:
                temp_list.append((j,0))
        train_text_preprocessed.append(temp_list)
    return train_text_preprocessed

def get_initial_prob(train_text_preprocessed):
    initial_prob = {'opinion' : 0,'not_opinion' : 0}
    for i in range(len(train_text_preprocessed)):
        #시작확률 구하기 위해 셈세는거
            if train_text_preprocessed[i][0][1] == 0:
                initial_prob["opinion"] +=1
            else:
                initial_prob["not_opinion"] +=1
    initial_prob_sum = initial_prob["opinion"]+initial_prob["not_opinion"]
    initial_prob["opinion"]= initial_prob["opinion"] / initial_prob_sum
    initial_prob["not_opinion"] =  initial_prob["not_opinion"] / initial_prob_sum
    return initial_prob

def get_propagation_prob(train_text_preprocessed):
    propagation_pos = 0
    propagation_neg = 0
    propagation_prob = {"0,0" : 0,"0,1" : 0,"1,0" : 0,"1,1" : 0}
    for i in range(len(train_text_preprocessed)):
        for j in range(len(train_text_preprocessed[i])-1):
            if train_text_preprocessed[i][j][1] == 1:
                propagation_pos = propagation_pos + 1 
            else:
                propagation_neg = propagation_neg + 1
            propagation_prob[str(train_text_preprocessed[i][j][1])+","+str(train_text_preprocessed[i][j+1][1])] +=1
    propagation_prob["0,0"] /= propagation_neg
    propagation_prob["0,1"] /= propagation_neg
    propagation_prob["1,0"] /= propagation_pos
    propagation_prob["1,1"] /= propagation_pos
    return propagation_prob

def get_emission(train_text_preprocessed):
    emission_pos = 2      #Add 1 기법 사용으로 인해 4개의 요소가 더해지므로 각각 2씩 증가
    emission_neg = 2
    emission_prob = {}
    for i in train_text_preprocessed:
        for j in i:
            emission_prob[j] = 0
    for i in range(len(train_text_preprocessed)):
        for j in range(len(train_text_preprocessed[i])-1): 
            if train_text_preprocessed[i][j][1] == 1:
                emission_pos = emission_pos + 1 
                emission_prob[(train_text_preprocessed[i][j][0],(train_text_preprocessed[i][j][1]))] +=1
            else:
                emission_neg = emission_neg + 1
                emission_prob[(train_text_preprocessed[i][j][0],(train_text_preprocessed[i][j][1]))] +=1
    keys = list(emission_prob.keys())
    for i in range(len(keys)):
        if keys[i][1] == 0:
            emission_prob[keys[i]] /= emission_neg
        else :
            emission_prob[keys[i]] /= emission_pos
    return emission_prob

def predict(test_text,initial_prob, propagation_prob, emission_prob):
    result = []
    for text in test_text:
        state_list = [[],[]]
        result_text = []
        input_text = text.split(" ")
        temp_list2 = list()
        for j in input_text:
            if j.find("<emotion>") != -1:
                current_text = j.replace("<emotion>","")
                current_text = current_text.replace("</emotion>","")
                temp_list2.append(current_text)
            elif j == "[" or j == "]" or j == "(" or j == ")" or j == "," or j == ".":
                temp_list2.append(j)
            else:
                temp_list2.append(j)
        input_text_processed = temp_list2
        try:
            state_list[0].append(initial_prob[("opinion")]*emission_prob[(input_text_processed[0],0)])
        except KeyError as e:
            state_list[0].append(initial_prob[("not_opinion")]*0)
        try:
            state_list[1].append(initial_prob[("not_opinion")]*emission_prob[(input_text_processed[0],1)])
        except KeyError as e:
            state_list[1].append(initial_prob[("not_opinion")]*0)
        
        if state_list[0]> state_list[1]:
            result_text.append((input_text[0],0))
        else:
            result_text.append((input_text[0],1))
        for idx in range(1,len(input_text)):
            try:
                state_00 = (state_list[0][idx-1]) *(propagation_prob["0,0"]) *(emission_prob[(input_text_processed[idx],0)])
            except KeyError as e:
                state_00 = (state_list[0][idx-1]) *(propagation_prob["0,0"]) *0
            try:
                state_01 = (state_list[0][idx-1]) *(propagation_prob["0,1"]) *(emission_prob[(input_text_processed[idx],1)])
            except KeyError as e:
                state_01 = (state_list[0][idx-1]) *(propagation_prob["0,1"]) *0
            try:
                state_10 = (state_list[1][idx-1]) *(propagation_prob["1,0"]) *(emission_prob[(input_text_processed[idx],0)])
            except KeyError as e:
                state_10 = (state_list[1][idx-1]) *(propagation_prob["1,0"]) *0
            try:
                state_11 = (state_list[1][idx-1]) *(propagation_prob["1,1"]) *(emission_prob[(input_text_processed[idx],1)])
            except KeyError as e:
                state_11 = (state_list[1][idx-1]) *(propagation_prob["1,1"]) *0
    
            if result_text[idx-1][1] == 0:
                if state_00 > state_01 :
                    state_list[0].append(state_00)
                    result_text.append((input_text[idx],0))
                else:
                    state_list[0].append(state_01)
                    result_text.append((input_text[idx],1))     
                if state_10 > state_11:
                    state_list[1].append(state_10)
                else:
                    state_list[1].append(state_11)
            else:
                if state_10 > state_11:
                    state_list[1].append(state_10)
                    result_text.append((input_text[idx],0))
                else:
                    state_list[1].append(state_11)
                    result_text.append((input_text[idx],1))
                if state_00 > state_01:
                    state_list[0].append(state_10)
                else:
                    state_list[0].append(state_11)
        result.append(result_text)
    return(result)
    
if __name__ == "__main__":
    main()
