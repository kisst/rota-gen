#!/usr/bin/env python3
import sys
import random
import yaml


with open("settings.yaml", "r", encoding="utf-8") as settings_file:
    settings_dict = yaml.safe_load(settings_file)
with open("team.yaml", "r", encoding="utf-8") as team_file:
    TEAM_DICT = yaml.safe_load(team_file)

TEAM_SIZE = len(TEAM_DICT["team"])
SHIFTS = settings_dict["shifts"]
WEEKS = settings_dict["weeks"]


def shift_counts(rota, team_id):
    """
    Count how many time the given user, exist already in the rota
    """
    counter = 0
    for week in rota:
        for shift in range(1, SHIFTS + 1):
            if week[shift] == team_id:
                counter = counter + 1
    return counter


def has_time_off(member, week):
    """
    return true if the team member have scheduled holiday
    """
    try:
        if week in TEAM_DICT["team"][member]["TimeOff"]:
            return True
    except KeyError:
        pass
    return False


def generate_weight(rota, week):
    """
    Provide a weight list for the given week
    """
    member_list = []
    weight = []
    for member in range(TEAM_SIZE):
        in_rota = shift_counts(rota, member)
        if has_time_off(member, week):
            weight.append(0)
        else:
            weight.append(WEEKS - in_rota)
        member_list.append(member)
    return member_list, weight


def name_lookup(team_id):
    """
    Give the name of the user
    """
    return TEAM_DICT["team"][team_id]["Name"]


def print_rota(rota):
    """
    Helper function to print out the rota
    """
    print("Week", end="")
    for shift_counter in range(SHIFTS):
        print(",", shift_counter + 1, end="")
    print(",")
    for rota_entry in rota:
        print(str(rota_entry["week"]).zfill(2), end="")
        for shift_cv in range(1, SHIFTS + 1):
            print(",", name_lookup(rota_entry[shift_cv]), end="")
        print(",")


rota = []

for week_cv in range(1, WEEKS + 1):
    entry = {"week": week_cv}
    members, weight = generate_weight(rota, week_cv)
    for shift in range(SHIFTS):
        try:
            selection = random.choices(members, weights=weight, k=1)
        except ValueError:
            print("No one is avaible for week: ", week_cv, " Maybe try to run again")
            sys.exit(0)
        entry[shift + 1] = selection[0]
        weight[selection[0]] = 0  # don't draw it again
    rota.append(entry)

print_rota(rota)
