import random
import logging
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import GameSession, Transaction
from .forms import DepositForm

logger = logging.getLogger(__name__)

def index(request):
    """Home page view"""
    return render(request, 'game/index.html')

@login_required
def game_simulation(request):
    """Handle the game simulation"""
    try:
        # Simulate a dice roll (1-6)
        dice_roll = random.randint(1, 6)
        
        # Determine the result
        if dice_roll > 3:
            result = f"Won! (Rolled {dice_roll})"
        else:
            result = f"Lost (Rolled {dice_roll})"
        
        # Save the game session
        GameSession.objects.create(
            user=request.user,
            result=result
        )
        
        messages.success(request, f'Game completed! You {result}')
        
    except Exception as e:
        logger.error(f"Error in game simulation: {str(e)}")
        messages.error(request, 'An error occurred during the game. Please try again.')
        result = "Error occurred"
    
    return render(request, 'game/game_detail.html', {
        'result': result,
        'recent_games': GameSession.objects.filter(user=request.user).order_by('-timestamp')[:5]
    })

@login_required
@require_http_methods(["GET", "POST"])
def deposit(request):
    """Handle deposit simulation"""
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            try:
                amount = form.cleaned_data['amount']
                
                # Create a new transaction
                transaction = Transaction.objects.create(
                    user=request.user,
                    amount=amount,
                    status='COMPLETED'  # In a real app, this would be pending until confirmed
                )
                
                messages.success(request, f'Successfully deposited ${amount}')
                return redirect('history')
                
            except Exception as e:
                logger.error(f"Error processing deposit: {str(e)}")
                messages.error(request, 'An error occurred processing your deposit. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DepositForm()
    
    return render(request, 'game/deposit.html', {
        'form': form,
        'recent_transactions': Transaction.objects.filter(
            user=request.user
        ).order_by('-transaction_date')[:5]
    })

@login_required
def history(request):
    """Display game and transaction history"""
    return render(request, 'game/history.html', {
        'game_sessions': GameSession.objects.filter(user=request.user).order_by('-timestamp')[:20],
        'transactions': Transaction.objects.filter(user=request.user).order_by('-transaction_date')[:20]
    })
