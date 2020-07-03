from player.models import *


def createPlayerPart1(session, pc, createPlayerPart1Form):
    pc.name = createPlayerPart1Form['character_name'].data
    pc.photo = createPlayerPart1Form['photo'].data
    abilities = Abilities()
    abilities.dexterity = createPlayerPart1Form['dex'].data
    abilities.strength = createPlayerPart1Form['str'].data
    abilities.constitution = createPlayerPart1Form['con'].data
    abilities.wisdom = createPlayerPart1Form['wis'].data
    abilities.intelligence = createPlayerPart1Form['int'].data
    abilities.charisma = createPlayerPart1Form['cha'].data
    abilities.name = pc.name
    race = createPlayerPart1Form['race'].data
    race = Race.objects.get(name=race)
    pc.abilities = abilities
    selectedRace = SelectedRace()
    selectedRace.race = race
    if "half" not in race.name:
        selectedRace.appliedAbilities = race.abilities
        session["raceAbilities"] = True
    else:
        session["raceAbilities"] = False
    pc.race = selectedRace
    session["pc"] = pc
    return


def createPlayerPart2(pc, classLevel, hp):
    pc.addLevel(classLevel, hp)
    return
