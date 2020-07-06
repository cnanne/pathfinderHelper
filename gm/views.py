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
    try:
        session: dict = session_data[request.session.session_key]
    except:
        session = dict()
        session_data[request.session.session_key] = session
    if request.method == "POST":
        if part == 1:
            # Create player
            pc = PC()
            form = CreatePlayerPart1Form(request.POST, request.FILES)
            # TODO needs to be if form is valid pero no funciona
            if form.is_valid():
                photo = request.FILES['photo']
                createPlayerPart1(session, pc, form, photo)
            else:
                return defaultReturnPlayerCreation(request)
            context = {"pc": pc, "levels": pc.availableClassesForNewLevel()}
            return render(request, 'gm/createPlayerStep2.html', context=context)
        elif part == 2:
            level = request.POST["level"]
            level = ClassLevel.objects.get(name=level)
            hp = level.gameClass.hp
            if level is None or session is None:
                return defaultReturnPlayerCreation()
            else:
                pc: PC = session["pc"]
                classLevel: PlayerClassLevel = createPlayerPart2(session["pc"], level, hp)
                classSkills = classLevel.classLevel.gameClass.classSkills.all()
                session_data[request.session.session_key]["classLevel"] = classLevel
                skillNames = []
                for skill in Skill.objects.all():
                    if skill in classSkills:
                        skillNames.append(skill.name + "*")
                    else:
                        skillNames.append(skill.name)
                context = {"pc": pc,
                           "skills": skillNames,
                           "maxRanks": classLevel.classLevel.gameClass.ranks}
                return render(request, 'gm/createPlayerStep3.html', context=context)
        elif part == 3:
            skills = request.POST.getlist('skills')
            if session is None or skills is None:
                return defaultReturnPlayerCreation(request)
            else:
                pc = session["pc"]
                if pc is None:
                    return defaultReturnPlayerCreation(request)
                pcSkillRanks = creatPlayerPart3(pc, skills)
                session['skills'] = pcSkillRanks
                if saveAll(session):
                    return redirect('player:pcDetail', pc_name=pc.name)
        else:
            return defaultReturnPlayerCreation(request)
    else:
        return defaultReturnPlayerCreation(request)
    return defaultReturnPlayerCreation(request)
