from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta, datetime

# für Terms-Model
from fuzzywuzzy import process, fuzz # library zum vergleich von wörtern
from .forms import TermsForm, CategoryForm
from .models import Terms
from django.core.paginator import Paginator #für seiten für wortliste

def user_filter(request):
    # holen uns erstmal alle user, die wir später dann filtern je nach kategorie
    users = get_user_model().objects.exclude(pk=request.user.pk) # alle ohne request.user, wir wollen ja nicht, dass der selbst mit angezeigt wird, ne?

    # holt die interessen rein, die in der url im GET als value zum key interests angefordert werden
    # anschließend machen wir eine liste aller interessen, die wir am "," abspalten und mit strip alle leerzeichen entfernen
    # des weiteren holen wir values für age, gender usw
    interests = request.GET.get('interests', '')
    interest_list = [interest.strip().lower() for interest in interests.split(',')] if interests else []
    
    age = request.GET.get('age')
    min_age = request.GET.get('min_age') 
    max_age = request.GET.get('max_age')
    
    gender = request.GET.get('gender')
    location = request.GET.get('location', '')
    last_online = request.GET.get('last_online')
    last_online_cut = request.GET.get('last_online_cut', '')


    # wir gehen liste der interessen durhc und wenn enthalten, wird ausgegeben
    # auf dauer kann datenmenge komplex sein.. dann evtl Q-abfrage implementieren
    if interests:
        for interest in interest_list:
                users = users.filter(profile__interests__icontains=interest) #speichern nur die leute in 'users' ab, die passende interessen haben
    
    # wenn kein user gefunden, dann ähnliches wort anzeigen
    similar_interests = [] 
    min_score_threshold = 70
    
    if interests and not users.exists():
        terms_list = Terms.objects.values_list('word', flat=True) # values_list gibt mir nur value (das wort) aus, kein objekt; flat sagt, dass es eine liste aus strings ist .. keine tuple oder sonst was
        for interest in interest_list:
            # Finde ähnliche Interessen, wenn keine User gefunden wurde
            similar_terms = process.extract(interest, terms_list, limit=10, scorer=fuzz.token_set_ratio) # default scorer wäre Wratio, der umfassender ist und genauer bei spelling fehlern, aber länger dauern kann. zum tewst scorer einfach auskommentieren oder =Wratio
            for similar_term, score in similar_terms:
                if score >= min_score_threshold:
                    similar_interests.append(similar_term)
    # wenn der suchbegriff in similar_intersts ist und aber keinen user finde, dann lösche ihn
    if interests in similar_interests and not users.exists():
        similar_interests.remove(interests)

    # weitere suchkriterien - age, gender, location...:
    if age:
        #users = users.filter(profile__age=age)
        age = int(age)
        current_year = datetime.now().year
        birth_year = current_year - age
        users = users.filter(profile__user__birthdate__year__exact=birth_year)
        
    if min_age:
        #users = users.filter(profile__age__gte=min_age)   #gte = g und gleich dem wert
        min_age = int(min_age)
        current_year = datetime.now().year
        birth_year = current_year - min_age
        users = users.filter(profile__user__birthdate__year__lte=birth_year)

    if max_age:
        #users = users.filter(profile__age__lte=max_age)  #lte = kleiner und gleich dem wert
        max_age = int(max_age)
        current_year = datetime.now().year
        birth_year = current_year - max_age
        users = users.filter(profile__user__birthdate__year__gte=birth_year)

    if gender:
        users = users.filter(profile__gender=gender)
    
    if location:
        location = location.lower()
        users = users.filter(profile__location__icontains=location)

    if last_online_cut:
        days_num = int(last_online_cut)
        last_online_delta = timezone.now() - timedelta(days=days_num) #errechne mir einen zeitpunkt: aktuell minus der tage, die der user eingegeben hat
        users = users.filter(profile__last_online__gte=last_online_delta) # alle user die ab dem zeitpunkt bis heut online waren werden aufgelistet
    
    print(f"Number of Users Found: {users.count()}")

    context = {'users': users, 
               'interests': interests, 
               'interest_list': interest_list, 
               'similar_interests': similar_interests,
               'age': age, 
               'min_age': min_age, 
               'max_age': max_age, 
               'gender': gender, 
               'location': location, 
               'last_online': last_online}
    
    return render(request, 'searchers/user_filter.html', context)



# Viewsfür Wörter-Ähnlichkeits-Implementierung und für die später zu implementierende Synonym-Verwaltung
def add_terms(request):
    # ich hol mir alle terms geordnet nach umgekehrter id:
    terms_list = Terms.objects.order_by('-id')

    # ich lasse mir mit paginator 10 terms pro seite anzeigen
    paginator = Paginator(terms_list, 10)
    page_num = request.GET.get('page')
    terms = paginator.get_page(page_num)


    if request.method == 'POST':
        form = TermsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_terms')
    else:
        form = TermsForm()
    
    # mache contextvariable, weil evtl immer mehr dicts kommen
    context = {
        'form': form,
        'terms': terms,
    }

    return render(request, 'searchers/add_terms.html', context)


def remove_terms(request, term_id):
    term = get_object_or_404(Terms, id=term_id)

    if request.method == "POST":
        term.delete()
        return redirect('add_terms')

    return render(request, 'searchers/confirm_remove_term.html', {'term': term})