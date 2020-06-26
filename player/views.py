from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from player.models import *

abilities = ["STR", "DEX", "CON", "WIS", "INT", "CHA"]


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def skills(request):
    skills = Skill.objects.all()
    context = {
        'skills': skills,
    }
    return render(request, 'player/skills.html', context)


def addSkill(request):
    if request.method == 'GET':
        return render(request, 'player/addSkill.html', {'abilities': abilities})
    elif request.method == 'POST':
        name = request.POST['name']
        untrained = request.POST['untrained']
        description = request.POST['description']
        ability = request.POST['ability']
        skill = Skill.objects.create()
        skill.fillData(name, untrained, ability, description)
        skill.save()
        return HttpResponseRedirect(reverse('skills'))


def skillsAndSaves(request, pc_name):
    pc = get_object_or_404(PC, name=pc_name)
    abilities = AbilitiesMap(pc.getAbilitiesMap)
    return render(request, 'player/skillsAndSaves.html', {'pc': pc,
                                                          'skills': pc.getSkills().values(),
                                                          'saves': pc.getSaves(),
                                                          'abilities': abilities})


def pcDetails(request, pc_name):
    return render(request, 'player/playerDetails.html', {'pc': get_object_or_404(PC, name=pc_name)})


def skillDetail(request, skill_name):
    return render(request, 'player/skillDetail.html', {'skill': get_object_or_404(Skill, name=skill_name),
                                                       'untrained': True})


def inventory(request, pc_name):
    pc = get_object_or_404(PC, name=pc_name)
    equipment = pc.equipment
    inventory = equipment.carriedEquipment.all()
    return render(request, 'player/inventory.html', {'pc': pc,
                                                     'equipment': equipment,
                                                     'inventory': inventory})
