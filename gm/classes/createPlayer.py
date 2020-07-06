from player.models import *


def createPlayerPart1(session, pc, createPlayerPart1Form, photo):

    alignment = createPlayerPart1Form['alignment'].data
    alignment = Alignment.objects.get(pk=alignment)
    race = createPlayerPart1Form['race'].data
    race = Race.objects.get(name=race)
    pc.name = createPlayerPart1Form['character_name'].data
    pc.photo = createPlayerPart1Form.cleaned_data['photo']
    pc.alignment = alignment
    abilities = Abilities()
    abilities.dexterity = createPlayerPart1Form['dex'].data
    abilities.strength = createPlayerPart1Form['str'].data
    abilities.constitution = createPlayerPart1Form['con'].data
    abilities.wisdom = createPlayerPart1Form['wis'].data
    abilities.intelligence = createPlayerPart1Form['int'].data
    abilities.charisma = createPlayerPart1Form['cha'].data
    abilities.name = pc.name
    pc.abilities = abilities
    selectedRace = SelectedRace()
    selectedRace.race = race
    if "half" not in race.name:
        selectedRace.appliedAbilities = race.abilities
        session["raceAbilities"] = True
    else:
        session["raceAbilities"] = False
    pc.race = selectedRace
    pc.firstSave()
    session["pc"] = pc

    return True


def createPlayerPart2(pc, classLevel, hp):
    playerClassLevel = PlayerClassLevel()
    playerClassLevel.hp = hp
    try:
        playerClassLevel.classLevel = ClassLevel.objects.get(pk=classLevel)
    except:
        return None
    playerClassLevel.pc = pc
    return playerClassLevel


def creatPlayerPart3(pc, skills):
    playerSkills = []
    skills: list
    for skill in Skill.objects.all():
        if skill.untrained and skill.name not in skills:
            pcSkillRank = PCSkillRank()
            pcSkillRank.pc = pc
            pcSkillRank.skill = skill
            pcSkillRank.ranks = 0
            playerSkills.append(pcSkillRank)
    playerSkills += pc.addSkillRanks(skills)
    return playerSkills


def saveAll(session):
    session: dict
    try:
        classLevel: PlayerClassLevel = session['classLevel']
        pc: PC = session['pc']
        skills: list = session['skills']
    except:
        return False

    pc.race.save()
    pc.race = pc.race
    pc.save()
    classLevel.pc = pc
    classLevel.save()
    for skill in skills:
        skill.pc = pc
        skill.save()
    return True

