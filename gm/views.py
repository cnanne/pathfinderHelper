from django.shortcuts import render, redirect
from player.models import *
from gm.forms import *
from gm.classes.createPlayer import *

session_data = dict()


# Create your views here.
def index(request):
    return render(request, 'gm/index.html')


def defaultReturnPlayerCreation(request):
    form = CreatePlayerPart1Form()
    context = {'form': form}
    return render(request, 'gm/createPlayerStep1.html', context=context)


# TODO: document
def createPlayer(request, part=None):
    if request.method == "POST":
        if part == 1:
            # Create player
            pc = PC()
            form = CreatePlayerPart1Form(request.POST)
            # TODO needs to be if form is valid pero no funciona
            if True:
                session: dict = session_data.get(request.session.session_key)
                if session is None:
                    session = dict()
                    session_data[request.session.session_key] = session
                createPlayerPart1(session, pc, form)
            else:
                return defaultReturnPlayerCreation(request)
            context = {"pc": pc, "levels": pc.availableClassesForNewLevel()}
            return render(request, 'gm/createPlayerStep2.html', context=context)
        elif part == 2:
            level = request.POST["level"]
            hp = request.POST["hp"]
            level = ClassLevel.objects.get(name=level)
            session = session_data[request.session.session_key]
            if level is None or session is None:
                return defaultReturnPlayerCreation()
            else:
                createPlayerPart2(session["pc"], level, hp)
                pc:PC = session_data[request.session.session_key]["pc"]
                context = {"pc": pc,
                           "skills": Skill.objects.all(),
                           "classLevels": pc.classLevels.all()}
                return render(request, 'gm/createPlayerStep3.html', context=context)
        else:
            return defaultReturnPlayerCreation(request)
    else:
        return defaultReturnPlayerCreation(request)
    return defaultReturnPlayerCreation(request)
