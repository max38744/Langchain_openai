from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import QueryLog, Topic
from .init_chatmodel import qa, memory, summary

from datetime import datetime


def chat(request, query, chat_history, name):
    # 기존 채팅 기록을 메모리에 로드
    memory.load_memory_variables({})
    # Define the system message
    system_message = "모든 답변에 대해서 고양이인 것 처럼 답변해주고 최대한 자세하게 답변해줘"

    combined_prompt = f"네게 바라는 것은 '{system_message}'와 같은 요구사항에 따라 \n '{query}'질문에 답변에 대답해줘"

    # 새로운 질문을 받고 응답을 생성
    result = qa(combined_prompt)

    # 응답을 메모리에 저장
    memory.save_context({"question": query}, {"answer": result['answer']})
    

    query_log = QueryLog.objects.create(username=name, datetime=datetime.now(), query=query, answer=result['answer'])
    query_log.save()
    
    # Book 생성
    session_id = request.session.session_key
    print(session_id, "where am i")
    topic = Topic.objects.create(qa_id=query_log, topic_id = session_id, title = "Null")
    topic.save()
    
    return result['answer']

@csrf_exempt
def chat_view(request):
    name = request.GET.get('name', 'Default Name')
    chat_history = request.session.get('chat_history', [])
    if request.method == 'POST':
        question = request.POST.get('question', '')
        if question:
            response = chat(request , question, chat_history, name)
            chat_history.append({'question': question, 'response': response})
            request.session['chat_history'] = chat_history
            return JsonResponse({"question": question, "answer": response, "chat_history": chat_history})

    context = {
        'chat_history': chat_history,
        'name': name,
    }
    return render(request, 'gpt/chatgpt.html', context)

def summary_topic(target) :
    chat_history = []
    query_list = [_['query'] for _ in target]
    answer_list = [_['answer'] for _ in target]
    
    for i in range(0, len(query_list)) : 
        chat_history.append({'question' : query_list[i], 'response' : answer_list[i]})
    
    return summary(chat_history)   
    

def clear_chat_view(request) :
    if 'chat_history' in request.session:
        topics = Topic.objects.filter(topic_id = request.session.get('session_key'))
        logs = QueryLog.objects.filter(id = topics)
        
        topics.update(title = summary_topic(logs))
        
        request.session.clear()
        request.session.create()
        
        
        
    memory.clear() # 메모리 초기화
    return redirect('selfchatgpt:chat_view')
