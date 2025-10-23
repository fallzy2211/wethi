from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OfferForm, CustomUserCreationForm
from .models import Offer
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Offer, Message
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

from django.contrib.auth.views import LoginView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, CustomTokenObtainPairSerializer

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts/login')  # à adapter selon ton flux
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige après inscription
    else:
        form = UserCreationForm()

    return render(request, 'users/signup.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('/')  # Redirige vers la page d'accueil après la déconnexion

@login_required
def create_offer(request):

    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            offer.save()

            if request.user.type == "cambiste":
                return redirect('offer_list')  # Rediriger vers la liste des offres
            else:
                return redirect('/')
    else:
        form = OfferForm()
    return render(request, 'users/create_offer.html', {'form': form})



def offer_list(request):
    user = request.user
    offers = Offer.objects.filter(status='disponible').order_by('-date_creation')
    return render(request, 'users/offer_list.html', {'offers': offers, 'user':user})


@login_required
def reserve_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id, status='disponible')

    if request.user.type != 'cambiste':
        messages.error(request, "Seuls les Cambistes peuvent réserver une offre.")
        return redirect('offer_list')

    if request.user.credits < 1:
        messages.error(request, "Vous n'avez pas assez de crédits.")
        return redirect('offer_list')

    # Débiter un crédit et réserver l’offre
    request.user.credits -= 1
    request.user.save()

    offer.status = 'reservee'
    offer.reserved_by = request.user
    offer.save()

    messages.success(request, "L'offre a été réservée avec succès !")
    return redirect('offer_list')


@login_required
def chat(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id, status='reservee')

    if request.user != offer.user and request.user != offer.reserved_by:
        messages.error(request, "Vous n'avez pas accès à cette conversation.")
        return redirect('offer_list')

    messages_list = offer.messages.all().order_by('timestamp')

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=offer.user if request.user == offer.reserved_by else offer.reserved_by,
                offer=offer,
                content=content
            )
            return JsonResponse({"message": "Message envoyé"}, status=200)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'users/chat.html', {'offer': offer, 'messages': messages_list})

    return render(request, 'users/chat.html', {'offer': offer, 'messages': messages_list})

@login_required
def available_offers(request):
    # Récupère toutes les offres où le statut est 'disponible'
    offers = Offer.objects.filter(status='disponible')
    return render(request, 'users/available_offers.html', {'offers': offers})

@login_required
def dashboard(request):
    if request.user.type == 'cambiste':
        offers = Offer.objects.filter(status='reservee').order_by("-date_creation")
        return render(request, 'users/dashboard_cambiste.html', {'offers': offers, 'credits': request.user.credits})
    else:
        user_offers = Offer.objects.filter(user=request.user).order_by("-date_creation")
        return render(request, 'users/dashboard_particulier.html', {'offers': user_offers})

@login_required
def filtered_offers(request):
    if request.user.type != 'cambiste':
        return redirect('dashboard')

    query = request.GET.get('q', '')
    offers = Offer.objects.filter(status='disponible')

    if query:
        offers = offers.filter(ma_devise__icontains=query) | offers.filter(devise_souhaitee__icontains=query)

    return render(request, 'users/filtered_offers.html', {'offers': offers})

@login_required
def recharge_credits(request):
    return render(request, 'users/recharge_credits.html')

@login_required
def process_payment(request):
    if request.method == "POST":
        credits = int(request.POST.get("credits"))
        payment_method = request.POST.get("payment_method")

        if credits <= 0:
            messages.error(request, "Le nombre de crédits doit être supérieur à 0.")
            return redirect('recharge_credits')

        # Simuler l'intégration des API de paiement
        payment_successful = False

        if payment_method == "wave":
            payment_successful = process_wave_payment(request.user, credits)
        elif payment_method == "orange_money":
            payment_successful = process_orange_money_payment(request.user, credits)

        if payment_successful:
            request.user.credits += credits
            request.user.save()
            messages.success(request, f"Recharge réussie ! Vous avez {request.user.credits} crédits.")
            return redirect('dashboard_cambiste')
        else:
            messages.error(request, "Le paiement a échoué. Veuillez réessayer.")

    return redirect('recharge_credits')

def process_wave_payment(user, credits):
    """ Simule un paiement avec l'API Wave """
    url = "https://api.wave.com/payments"
    data = {
        "phone_number": user.phone,  # Assurez-vous que l'utilisateur a un numéro de téléphone
        "amount": credits * 500,  # Exemple : 1 crédit = 100 XOF
        "currency": "XOF"
    }
    response = requests.post(url, json=data)
    return response.status_code == 200  # Vérifier si le paiement a réussi

def process_orange_money_payment(user, credits):
    """ Simule un paiement avec l'API Orange Money """
    url = "https://api.orange.com/payment"
    data = {
        "phone_number": user.phone,
        "amount": credits * 100,
        "currency": "XOF"
    }
    response = requests.post(url, json=data)
    return response.status_code == 200  # Vérifier si le paiement a réussi
