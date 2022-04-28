import pickle
import os
import csv
from Backend.team import Team
from Backend.team_member import TeamMember
from Backend.league import League

class LeagueDatabase:
    _sole_instance = None

    def __init__(self):
        self.leagues = []
        self._last_oid = 0

    def instance(self):
        return self._sole_instance

    def load(self, file_name):
        if os.path.exists(file_name):
            self._sole_instance = pickle.load(open(file_name, 'rb'))
        elif os.path.exists(file_name + '.backup'):
            self._sole_instance = pickle.load(open(file_name + '.backup', 'rb'))
            raise FileNotFoundError('{} Do not Exists'.format(file_name))

    def add_league(self, league):
        for one_league in self.leagues:
            if one_league.oid == league.oid:
                raise Exception('League Already Present')
        self.leagues.append(league)

    def remove_league(self, league):
        if league in self.leagues:
            self.leagues.remove(league)
        else:
            raise ValueError

    def league_named(self, name):
        for league in self.leagues:
            if league.name == name:
                return league
        return None

    def next_old(self):
        self._last_oid += 1
        return self._last_oid

    def save(self, file_name):
        if os.path.exists(file_name):
            os.rename(file_name, file_name + '.backup')

        file = open(file_name, 'wb')
        pickle.dump(self._sole_instance, file)

    def import_league_teams(self, league, file_name):
        file = open(file_name, encoding='utf-8')
        csv_read = csv.reader(file)
        header = True
        for line in csv_read:
            if header is True: #skip header
                header = False
                continue
            if line==[]:continue
            team_name = line[0]
            if team_name in [None,'',' ']:continue
            player_name = line[1]
            player_email = line[2]
            if len(league.teams)>0:
                team_oid=league.teams[-1].oid+1
            else:
                team_oid=0
            if team_oid not in [team.oid for team in league.teams]:
                team = Team(team_oid, team_name)
                league.add_team(team)
            else:
                for one_team in league.teams:
                    if one_team.oid==team_oid:
                        team=one_team
                        break

            team_member = TeamMember(team_oid,player_name , player_email)
            team.add_member(team_member)


    def export_league_teams(self, league, file_name):
        file = open(file_name, 'w', encoding='utf-8')
        csv_write = csv.writer(file)
        csv_write.writerow(['Team name', 'Member name', 'Member email'])
        for team in league.teams:
            for player in team.members:
                csv_write.writerow([team.name, player.name, player.email])
        file.close()

    def import_league(self,file_name):
        file = open(file_name, encoding='utf-8')
        csv_read = csv.reader(file)
        header = True
        for line in csv_read:
            if header is True: #skip header
                header = False
                continue
            if line==[]:continue
            league_name = line[0]
            if league_name in [None,'','None',' ']:continue
            league_oid = self.next_old()
            self.add_league(League(league_oid,league_name))

    def export_league(self,file_name):
        file = open(file_name, 'w', encoding='utf-8')
        csv_write = csv.writer(file)
        csv_write.writerow(['League name'])
        for league in self.leagues:
            csv_write.writerow([league.name])
        file.close()
