from django.shortcuts import render
from player.models import *
from gm.forms import *
from gm.classes.createPlayer import *


# Create your views here.
def index(request):
    return render(request, 'gm/index.html')


def createPlayer(request, part=None):
    if request.method == "POST":
        pc = request.session.get('pcCreation')
        if part == 1:
            # Create player
            pc = PC()
            form = CreatePlayerPart1Form(request.POST)
            if form.is_valid():
                createPlayerPart1(request, pc, form)
            else:
                form = CreatePlayerPart1Form()
                context = {'form': form}
                return render(request, 'gm/createPlayerStep1.html', context=context)
            return
        else:
            # Player creation initiated
            return
    else:
        form = CreatePlayerPart1Form()
        context = {'form': form}
        return render(request, 'gm/createPlayerStep1.html', context=context)