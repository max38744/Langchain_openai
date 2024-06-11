from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .init_chatmodel import qa, memory

def chat(query, chat_history, name):
    # 기존 채팅 기록을 메모리에 로드
    memory.load_memory_variables({})

    # 새로운 질문을 받고 응답을 생성
    result = qa(query)

    # 응답을 메모리에 저장
    memory.save_context({"question": query}, {"answer": result['answer']})

    return result['answer']

@csrf_exempt
def chat_view(request):
    name = request.GET.get('name', 'Default Name')
    chat_history = request.session.get('chat_history', [])
    if request.method == 'POST':
        question = request.POST.get('question', '')
        if question:
            response = chat(question, chat_history, name)
            chat_history.append({'question': question, 'response': response})
            request.session['chat_history'] = chat_history
            return JsonResponse({"question": question, "answer": response, "chat_history": chat_history})

    context = {
        'chat_history': chat_history,
        'name': name,
    }
    return render(request, 'gpt/chatgpt.html', context)

def clear_chat_view(request):
    if 'chat_history' in request.session:
        del request.session['chat_history']
    memory.clear() # 메모리 초기화
    return redirect('selfchatgpt:chat_view')
