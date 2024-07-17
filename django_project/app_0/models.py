from django.db import models

class model_Person(models.Model):
    name=models.TextField(default='') #이름
    phone=models.TextField(default='') #전화번호
    know_hanja=models.IntegerField(default=-1) # 한자에 대한 기초지식
    know_component=models.IntegerField(default=-1)  # 부수에 대한 기초지식
    hanjas=models.JSONField(default=list)
    sampling_type=models.IntegerField(default=-1)
    result=models.JSONField(default=list)
    time=models.FloatField(default=0)
    
    
class model_Hanja(models.Model):
    #공통
    word=models.CharField(default='一', db_collation='utf8mb4_unicode_ci',max_length=1) #한자
    one_stroke=models.IntegerField(default=0) #획수
    total_stroke=models.IntegerField(default=1) #총획
    meaning=models.TextField(default='하나') #훈
    sound=models.CharField(default='일',max_length=30) #음
    meaning_sound=models.CharField(default='하나 일', max_length=50) #훈음
    lev_read=models.CharField(default='',max_length=10) #읽기급수
    lev_write=models.CharField(default='',max_length=10) #쓰기급수
    form=models.CharField(default='',max_length=10) #제자원리
    explanation=models.TextField(default='') #설명
    component_meaning=models.CharField(default='一',max_length=1) #부수

    #형성자
    component_sound=models.CharField(default='一', db_collation='utf8mb4_unicode_ci',max_length=10) #성부
    trace=models.CharField(default='', db_collation='utf8mb4_unicode_ci',max_length=10) #음 #index [-1]은 회의자(원시 성부). 원시 성부로부터의 거리는 len(trace). 
    origin=models.CharField(default='一',db_collation='utf8mb4_unicode_ci',max_length=1) #원시 성부

    # #회의자(합자)
    # component_combined=models.JSONField(default=list) #구성요소로 보는 경우 해당 없음. 합자의 경우에만 존재.

    @classmethod
    def distacne(cls, model_Hanja_1, model_Hanja_2):
        trace1=model_Hanja_1.trace
        trace2=model_Hanja_2.trace
        
        #convert list to trace
        set1=set(trace1)
        set2=set(trace2)
        #check if there is a overlapping component.

        set_common=set1.intersection(set2)

        if set_common:
            common_list=list(set_common)
            sound_core=common_list[0] #closest common component
            dis1=trace1.index(sound_core)+1
            dis2=trace2.index(sound_core)+1
            dis=dis1+dis2
            return dis 
        else: return "no common component"


