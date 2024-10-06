
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
from django.http import JsonResponse
import random
from itertools import islice

#retrieves the variable name as a string
def variable_name(input):
    output = [name for name, value in globals().items() if value is input][0]
    return output
def CountReturnOne(input):
    if isinstance(input,str): return str(input)
    elif isinstance(input,list):return str(input[0])

from .models import model_Person
@method_decorator(csrf_exempt, name='dispatch')
class view_Person(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            new_name = data.get('name', '')
            if not isinstance(new_name, str):
                return JsonResponse({'error': 'name must be a string'}, status=400)
            
            # Extract and validate survey_answer0
            survey_answer0 = data.get('survey_answer0', '')
            if not isinstance(survey_answer0, str):
                return JsonResponse({'error': 'survey_answer0 must be a string'}, status=400)
            
            # Extract and validate survey_answer1
            survey_answer1 = data.get('survey_answer1')
            if survey_answer1 is None:
                return JsonResponse({'error': 'survey_answer1 is missing'}, status=400)
            try:
                survey_answer1 = int(survey_answer1)
            except ValueError:
                return JsonResponse({'error': 'survey_answer1 must be an integer'}, status=400)
            
            # Extract and validate survey_answer2
            survey_answer2 = data.get('survey_answer2')
            if survey_answer2 is None:
                return JsonResponse({'error': 'survey_answer2 is missing'}, status=400)
            try:
                survey_answer2 = int(survey_answer2)
            except ValueError:
                return JsonResponse({'error': 'survey_answer2 must be an integer'}, status=400)
            
            elapsedTime = data.get('elapsedTime')
            if elapsedTime is None:
                return JsonResponse({'error': 'elapsedTime is missing'}, status=400)
            try:
                elapsedTime = float(elapsedTime)
            except ValueError:
                return JsonResponse({'error': 'elapsedTime must be an float'}, status=400)
            
            # Extract and validate sampling_type
            sampling_type_str = data.get('sampling_type')
            if sampling_type_str is None:
                return JsonResponse({'error': 'sampling_type is missing'}, status=400)
            try:
                sampling_type_int = int(sampling_type_str)
            except ValueError:
                return JsonResponse({'error': 'sampling_type must be an integer'}, status=400)
            
            # Extract and validate sampled_Hanja
            sampled_Hanja_json = data.get('sampled_Hanja', '[]')
            try:
                sampled_Hanja_list = json.loads(sampled_Hanja_json)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON for sampled_Hanja'}, status=400)
            
            # Extract and validate result
            result_json = data.get('result', '[]')
            try:
                result_list = json.loads(result_json)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON for result'}, status=400)
            
            # Create a new model_Person
            new_Person = model_Person.objects.create(
                name=new_name,
                phone=survey_answer0,
                know_hanja=survey_answer1,
                know_component=survey_answer2,
                sampling_type=sampling_type_int,
                hanjas=sampled_Hanja_list,
                result=result_list,
                time=elapsedTime
            )
            return JsonResponse({'message': 'User Created Successfully'}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        #retrieve all model_Person in the database
        QuerySet_Person=model_Person.objects.all()
        dict_Person=list(QuerySet_Person.values()) 
        return JsonResponse(dict_Person,safe=False)
    
    def delete(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            person_id = data.get('id', None)
            person_name = data.get('name', None)
            message_recent = ""
            message_id = ""
            if person_id is not None:
                message_id = str(person_id)
                try:
                    person_to_delete = model_Person.objects.get(id=person_id)
                except model_Person.DoesNotExist:
                    return JsonResponse({'error': 'Person with this ID not found'}, status=404)
            elif person_name is not None:
                try:
                    person_to_delete = model_Person.objects.get(name=person_name)
                    message_id = f'with name {person_name}'
                except model_Person.DoesNotExist:
                    return JsonResponse({'error': 'Person with this name not found'}, status=404)
            else:
                person_to_delete = model_Person.objects.latest('id')
                message_recent = "most recently added"
                message_id = f'with ID {person_to_delete.id}'

            person_to_delete.delete()
            return JsonResponse({'message': f'{message_recent} Person {message_id} deleted successfully'}, status=200) 
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except model_Person.DoesNotExist:
            return JsonResponse({'error': 'No persons found to delete'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

from django.db.models import Q  # Import Q object for complex queries
from .models import model_Hanja
@method_decorator(csrf_exempt, name='dispatch')
class view_Hanja(View):
    def get(self, request, *args, **kwargs):
        # #retrieve all model_Person in the database
        QuerySet_Hanja=model_Hanja.objects.all()

        target_id=request.GET.get('id')
        target_word=request.GET.get('word')
        target_meaning=request.GET.get('meaning')
        target_sound=request.GET.get('sound')
        target_origin=request.GET.get('origin')
        
        if target_id: 
            QuerySet_Hanja=QuerySet_Hanja.filter(id=target_id)
        if target_word: 
            QuerySet_Hanja=QuerySet_Hanja.filter(word=target_word)
        if target_meaning: 
            QuerySet_Hanja=QuerySet_Hanja.filter(meaning=target_meaning)
        if target_sound:
            QuerySet_Hanja=QuerySet_Hanja.filter(sound=target_sound)
        # Filter the queryset 
        if target_origin:   
            QuerySet_Hanja=QuerySet_Hanja.filter(origin=target_origin) 
        #     #QuerySet_Hanja = QuerySet_Hanja.filter(Q(word=target_origin)|Q(trace__contains=target_origin) | Q(component_combined=target_origin))
                                                               
        # #use .values method to return a Django QuerySet
        # #QuerySet is a collection of database queries to retrieve objects from your database
        #convert QuerySet into a dictionary by using list()
        dict_Hanja=list(QuerySet_Hanja.values()) 
        return JsonResponse(dict_Hanja, safe=False)
        # value=random.choice([0,1,2])
        # list_output=model_Hanja.objects.none()
        # if value==0: #chooce any random hanja
        #     list_output = model_Hanja.objects.all()
        # else: 
        #     if value==1: #choose from the same meaning_component
        #         components = model_Hanja.objects.values_list('component_meaning', flat=True)
        #     else: #choose form the same origin  
        #         components = model_Hanja.objects.values_list('origin', flat=True)
        #     unique_components = list(set(components)) # remove duplicates
        #     QuerySet_Hanja=model_Hanja.objects.all()
        #     if value==1:
        #         while len(list_output)<5:
        #             random_component=random.choice(unique_components)
        #             QuerySet_Hanja=QuerySet_Hanja.filter(component_meaning=random_component)
        #             list_output=list_output|QuerySet_Hanja
        #     else:
        #         while len(list_output)<5:
        #             random_component=random.choice(unique_components)
        #             QuerySet_Hanja=QuerySet_Hanja.filter(origin=random_component)
        #             list_output=list_output|QuerySet_Hanja
        # output=list(list_output.values())
        # random.shuffle(output)
        # output=output[:5] 
        # output.append(value)
 
        # print(output)
        # return JsonResponse(output, safe=False)
@method_decorator(csrf_exempt, name='dispatch')
class view_Question(View):
    def get(self, request, *args, **kwargs):
        words=[]
        try:
            for i in range(5):  # Adjust the range as needed
                word = request.GET.get(f'word{i}')
                if word:
                    words.append(word)
        except: return JsonResponse({'error'}, status=500)
    #retrieve all model_Person in the database
        QuerySet_Hanja=model_Hanja.objects.all()
    #etrieve origin and component_sound for all words
        origins=[] #근원 성부
        component_meanings=[] #부수
        actual_m=[] #실제 훈
        actual_s=[] #실제 음
        #단, random의 경우 성부가 존재하지 않는 경우(회의자)가 존재한다. 이 경우 스킵한다.
        for element in words:
            filtered_QuerySet=QuerySet_Hanja.filter(word=element)
            try:
                origins.append(CountReturnOne(filtered_QuerySet.values('origin').first()['origin']))
            except: origins.append('')
            actual_m.append(CountReturnOne(filtered_QuerySet.values('meaning').first()['meaning'])) 
            actual_s.append(CountReturnOne(filtered_QuerySet.values('sound').first()['sound']))
            component_meanings.append(CountReturnOne(filtered_QuerySet.values('component_meaning').first()['component_meaning']))

    #generate options for meaning
        mean_dicts=[]
        sound_dicts=[]
        for i in range(0,len(words)):
            mean_options=[]
            actual_meaning=(actual_m[i])
            actual_sound=(actual_s[i])
            #성부 기원이 같은 한자들 중에서 의미를 가져온다. 단, 회의자 처리가 곤한해짐.
            _origin=origins[i]
            if _origin=='':
                mean_options=[]
            else:
                filtered_QuerySet1=QuerySet_Hanja.filter(origin=_origin).order_by('?').values('meaning')
                if isinstance(filtered_QuerySet1,str):
                    mean_options=[filtered_QuerySet1[0]]
                else: 
                    filtered_QuerySet1=filtered_QuerySet1[:4]
                    means_list_of_dicts = list(filtered_QuerySet1)
                    mean_options = [item['meaning'] for item in means_list_of_dicts]
            while actual_meaning in mean_options or len(mean_options)<4:
                while actual_meaning in mean_options:
                    mean_options.remove(actual_meaning)
                while len(mean_options)<4:
                    temp=CountReturnOne(QuerySet_Hanja.order_by('?').values('meaning').first()['meaning']) 
                    mean_options.append(temp)

            mean_options.append(actual_meaning)
            random.shuffle(mean_options)
            answer=mean_options.index(actual_meaning)
            mean_dict={
                'question': words[i],
                'choices': mean_options,
                'answer': answer
            }
            mean_dicts.append(mean_dict)

            #부수가 같은 한자들 중에서 소리를 가져온다.
            _mean=component_meanings[i]
            filtered_QuerySet=QuerySet_Hanja.filter(component_meaning=_mean).order_by('?').values('sound')
            if isinstance(filtered_QuerySet,str):
                sound_options=[filtered_QuerySet[0]]
            else:
                filtered_QuerySet=filtered_QuerySet[:4]
                sound_list_of_dicts = list(filtered_QuerySet)
                sound_options = [item['sound'] for item in sound_list_of_dicts]

            while actual_sound in sound_options or len(sound_options)<4:
                while actual_sound in sound_options:
                    sound_options.remove(actual_sound)
                while len(sound_options)<4:
                    temp=CountReturnOne(QuerySet_Hanja.order_by('?').values('meaning').first()['meaning']) 
                    sound_options.append(temp)
            
            sound_options.append(actual_sound)
            random.shuffle(sound_options)
            answer=sound_options.index(actual_sound)
            
            sound_dict={
                'question': words[i],
                'choices': sound_options,
                'answer': answer
            }
            sound_dicts.append(sound_dict)
        dicts=mean_dicts+sound_dicts
        return JsonResponse(dicts,safe=False)

