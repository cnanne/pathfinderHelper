from django.shortcuts import render
from player.models import *
from gm.forms import *


# Create your views here.
def index(request):
    return render(request, 'gm/index.html')


def createPlayer(request):
    if request.method == "GET":
        form = CreatePlayerPart1()
        context = {'form': form}
        return render(request, 'gm/createPlayerStep1.html', context=context)
    elif request.method == "POST":
        pc = request.session.get('pcCreation')
        if pc is None:
            # Create player
            pc = PC()

            return
        else:
            # Player creation initiated
            return
