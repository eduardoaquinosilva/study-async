from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Category, Flashcard, FlashcardChallenge, Challenge
from django.http import HttpResponse, Http404
from django.contrib.messages import constants
from django.contrib import messages

# Create your views here.
def new_flashcard(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    if request.method == "GET":
        categories = Category.objects.all()
        levels = Flashcard.LEVEL_CHOICES
        flashcards = Flashcard.objects.filter(user=request.user)

        category_filter = request.GET.get('category')
        level_filter = request.GET.get('level')

        if category_filter:
            flashcards = flashcards.filter(category__id=category_filter)
        if level_filter:
            flashcards = flashcards.filter(level=level_filter)

        return render(request, 'new_flashcard.html', {"categories": categories, "levels": levels, "flashcards": flashcards})

    if request.method == "POST":
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        category = request.POST.get('category')
        level = request.POST.get('level')

        if len(answer.strip()) == 0 or len(answer.strip()) == 0:
            messages.add_message(request, constants.ERROR, "Preencha os campos de pergunta e resposta.")            
            return redirect(reverse("new_flashcard"))

        flashcard = Flashcard(user=request.user, question=question, answer=answer, category_id=category, level=level)
        flashcard.save()

        messages.add_message(request, constants.SUCCESS, "Flashcard cadastrado com sucesso.")
        return redirect(reverse("new_flashcard"))

def delete_flashcard(request, id):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    
    flashcard_delete = Flashcard.objects.get(id=id)

    if (flashcard_delete.user_id == request.user):
        flashcard_delete.delete()
        messages.add_message(request, constants.SUCCESS, 'Flashcard deletado com sucesso!')
    
    return redirect(reverse("new_flashcard"))

def start_challenge(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    
    if request.method == "GET":
        categories = Category.objects.all()
        levels = Flashcard.LEVEL_CHOICES

        return render(request, 'start_challenge.html', {'categories': categories, 'levels': levels})

    if request.method == "POST":
        title = request.POST.get('title')
        categories = request.POST.getlist('category')
        level = request.POST.get('level')
        quant_questions = request.POST.get('quant_questions')

        challenge = Challenge(user=request.user, title=title, quant_questions=quant_questions, level=level)
        challenge.save()

        challenge.category.add(*categories) # for is executed internally

        # get random flashcards according to what user decided
        flashcards = Flashcard.objects.filter(user=request.user).filter(level=level).filter(category_id__in=categories).order_by('?')
        
        if flashcards.count() < int(quant_questions):
            return redirect(reverse('start_challenge'))
        
        flashcards = flashcards[:int(quant_questions)]

        for flashcard in flashcards:
            flashcard_challenge = FlashcardChallenge(flashcard=flashcard)
            flashcard_challenge.save()
            challenge.flashcards.add(flashcard_challenge)
        
        challenge.save()

        return redirect(reverse('list_challenge'))

def list_challenge(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    
    if request.method == "GET":
        categories = Category.objects.all()
        levels = Flashcard.LEVEL_CHOICES
        challenges = Challenge.objects.filter(user=request.user)

        category_filter = request.GET.get('category')
        level_filter = request.GET.get('level')
        status_filter = request.GET.get('status')

        if category_filter:
            challenges = challenges.filter(category__id=category_filter)
        if level_filter:
            challenges = challenges.filter(level=level_filter)
        if status_filter:
            challenges = [a for a in challenges if a.status[0] == status_filter]
        
        return render(request, 'list_challenge.html', {'categories': categories, 'levels': levels, 'status': ["A começar", "Em aberto", "Finalizado"], 'challenges': challenges})

def challenge(request, id):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    
    if request.method == "GET":
        challenge = Challenge.objects.get(id=id)

        if not challenge.user == request.user:
            raise Http404

        categories = set(flashcard.flashcard.category for flashcard in challenge.flashcards.all())

        successes = challenge.flashcards.filter(done=True).filter(got_right=True).count()
        mistakes = challenge.flashcards.filter(done=True).filter(got_right=False).count()
        missing = challenge.flashcards.filter(done=False).count()

        return render(request, 'challenge.html', {'challenge': challenge, 'successes': successes, 'mistakes': mistakes, 'missing': missing, 'categories': categories})
    
    return HttpResponse('teste')

def answer_flashcard(request, id):
    flashcard_challenge = FlashcardChallenge.objects.get(id=id)
    got_right = request.GET.get('acertou')
    challenge_id = request.GET.get('desafio_id')

    if not flashcard_challenge.flashcard.user == request.user:
        raise Http404
    
    flashcard_challenge.done = True
    flashcard_challenge.got_right = True if got_right == "1" else False
    flashcard_challenge.save()

    return redirect(f"/flashcard/challenge/{challenge_id}")

def report(request, id):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    
    if request.method == "GET":
        challenge = Challenge.objects.get(id=id)

        successes = challenge.flashcards.filter(got_right=True).count()
        mistakes = challenge.flashcards.filter(got_right=False).count()

        categories = challenge.category.all()
        categories_names = [a.name for a in categories]

        data_per_category = list()
        for category in categories:
            data_per_category.append(challenge.flashcards.filter(flashcard__category=category).filter(got_right=True).count())
        
        mistakes_per_category = list()
        for category in categories:
            mistakes_per_category.append(challenge.flashcards.filter(flashcard__category=category).filter(done=True).count())
        
        for a in range(len(mistakes_per_category)):
            mistakes_per_category[a] = mistakes_per_category[a] - data_per_category[a]
        
        # Order the lists of successes, mistakes and the names of the categories according to how good the user was on each category
        for b in range(len(categories_names) - 1):
            if data_per_category[b] < data_per_category[b + 1]:
                data_per_category[b], data_per_category[b + 1] = data_per_category[b + 1], data_per_category[b]
                mistakes_per_category[b], mistakes_per_category[b + 1] = mistakes_per_category[b + 1], mistakes_per_category[b]
                categories_names[b], categories_names[b + 1] = categories_names[b + 1], categories_names[b]
        
        return render(request, 'report.html', {'challenge': challenge, 'data': (successes, mistakes), 'categories': categories_names, 'data_per_category': data_per_category, 'mistakes_per_category': mistakes_per_category, 'n': [int(0), int(1), int(2)]})
