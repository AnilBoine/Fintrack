from django.shortcuts import render, redirect
from .models import Transaction
from .forms import TransactionForm

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm

from django.contrib.auth.decorators import login_required



def home(request):
    return render(request, 'home.html')

def emi_calculator(request):
    if request.method == "POST":
        principal = float(request.POST['principal'])
        rate_of_interest = float(request.POST['rate']) / 12 / 100
        tenure = int(request.POST['tenure'])

        emi = (principal * rate_of_interest * (1 + rate_of_interest)**tenure) / ((1 + rate_of_interest)**tenure - 1)
        context = {'emi': round(emi, 2)}
        return render(request, 'emi_calculator.html', context)

    return render(request, 'emi_calculator.html')

def sip_calculator(request):
    if request.method == "POST":
        monthly_investment = float(request.POST['monthly_investment'])
        annual_rate_of_return = float(request.POST['rate']) / 12 / 100
        tenure = int(request.POST['tenure'])

        future_value = monthly_investment * (((1 + annual_rate_of_return)**tenure - 1) / annual_rate_of_return) * (1 + annual_rate_of_return)
        context = {'future_value': round(future_value, 2)}
        return render(request, 'sip_calculator.html', context)

    return render(request, 'sip_calculator.html')

def tax_calculator(request):
    if request.method == "POST":
        income = float(request.POST['income'])
        tax = 0

        if income <= 250000:
            tax = (income * 0.00001)
        elif income <= 500000:
            tax = (income - 250000) * 0.05
        elif income <= 1000000:
            tax = (income - 500000) * 0.2 + 12500
        else:
            tax = (income - 1000000) * 0.3 + 112500

        context = {'tax': round(tax, 2)}
        return render(request, 'tax_calculator.html', context)

    return render(request, 'tax_calculator.html')

def savings_for_loan(request):
    if request.method == "POST":
        future_value = float(request.POST['future_value'])
        annual_rate_of_return = float(request.POST['rate']) / 12 / 100
        tenure = int(request.POST['tenure'])

        monthly_savings = future_value / (((1 + annual_rate_of_return)**tenure - 1) / annual_rate_of_return) / (1 + annual_rate_of_return)
        context = {'monthly_savings': round(monthly_savings, 2)}
        return render(request, 'savings_for_loan.html', context)

    return render(request, 'savings_for_loan.html')


def transaction_tracker(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_tracker')
    else:
        form = TransactionForm()
    
    transactions = Transaction.objects.all().order_by('-date')
    total_income = sum(t.amount for t in transactions if t.category == 'income')
    total_expenses = sum(t.amount for t in transactions if t.category != 'income')
    context = {
        'form': form,
        'transactions': transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': total_income - total_expenses
    }
    return render(request, 'transaction_tracker.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def transaction_tracker(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_tracker')
    else:
        form = TransactionForm()
    
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    total_income = sum(t.amount for t in transactions if t.category == 'income')
    total_expenses = sum(t.amount for t in transactions if t.category != 'income')
    context = {
        'form': form,
        'transactions': transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': total_income - total_expenses
    }
    return render(request, 'transaction_tracker.html', context)
