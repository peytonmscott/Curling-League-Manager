import os
import sys

import numpy as np
import pandas as pd
import scipy.stats
from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QTableWidgetItem
from openpyxl import load_workbook
from Backend.league_database import LeagueDatabase
from Backend.league import League
from Backend.team import Team
from Backend.team_member import TeamMember
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('untitled.ui', self)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.main_window_button.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(0))
        self.league_editor_button.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(1))
        self.team_editor_button.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(2))

        #LEAGUES

        self.load_league_file.clicked.connect(self.load_leagues_file)
        self.save_league_file.clicked.connect(self.save_leagues_file)

        self.League_Database=LeagueDatabase()
        # self.League_Database.leagues.append(League(1,'ABC'))
        # self.League_Database.leagues.append(League(2,'CDF'))
        # self.League_Database.leagues.append(League(3,'FGH'))
        # if len(self.League_Database.leagues)>0:
        #     self.selected_league=self.League_Database.leagues[0]
        self.update_leagues_table()
        self.add_league.clicked.connect(lambda: self.add_item(self.leagues_list,self.league_input,'league'))
        self.remove_league.clicked.connect(lambda: self.remove_item(self.leagues_list,self.league_input,'league'))
        self.edit_league.clicked.connect(lambda: self.edit_leagues())
        self.leagues_list.doubleClicked.connect(self.load_teams_view)



        #TEAMS

        
        self.load_team_file.clicked.connect(self.load_teams_file)
        self.save_team_file.clicked.connect(self.save_teams_file)
        self.add_team.clicked.connect(lambda: self.add_item(self.teams_list,self.team_input,'team'))
        self.remove_team.clicked.connect(lambda: self.remove_item(self.teams_list,self.team_input,'team'))
        self.edit_team.clicked.connect(lambda: self.edit_teams(self.edit_team_old_name))
        self.teams_list.doubleClicked.connect(self.load_members_view)



        # MEMBERS
        # self.edit_team.clicked.connect(lambda :self.edit_team)
        self.remove_member.clicked.connect(lambda : self.remove_item(self.members_list,self.member_input,'member',self.member_input_email))
        self.add_member.clicked.connect(lambda : self.add_item(self.members_list,self.member_input,'member',self.member_input_email))
        self.edit_name.clicked.connect(lambda : self.edit_item(self.members_list,self.edit_member_old_name,self.edit_member_name))
        self.edit_email_address.clicked.connect(lambda : self.edit_item(self.members_list,self.edit_member_old_email,self.edit_member_email,row2=True))



        self.show()

    def edit_leagues(self):
        League=self.League_Database.league_named(str(self.edit_league_old_name.text()).strip())
        if League is None:return
        self.League=League
        self.load_teams_view()
    
    def edit_teams(self,item):
        Team=None
        for team in self.League.teams:
            if str(team.name).strip() == str(item.text()).strip():
                Team = team
                break
        if Team is None:return
        self.Team=Team
        self.load_members_view()
    

    def load_teams_view(self,coord=False):
        self.league_editor_button.setStyleSheet("""border-radius:0px;
background-color: rgb(255, 255, 255);
color: rgb(63, 122, 138);""")
        self.main_window_button.setStyleSheet("""border-radius:0px;
color: rgb(255, 255, 255);
background-color: rgb(63, 122, 138);""")
        if coord:
            league_name=str(self.leagues_list.item(coord.row(), 0).text()).strip()
            self.League=self.League_Database.league_named(league_name)
        # self.League.add_team(Team(0,'test_Team1'))
        # self.League.add_team(Team(1,'test_Team2'))
        # self.League.add_team(Team(2,'test_Team3'))
        self.update_teams_table()

        self.stackedWidget.setCurrentIndex(1)

    def load_members_view(self, coord=False):
            self.team_editor_button.setStyleSheet("""border-radius:0px;
    background-color: rgb(255, 255, 255);
    color: rgb(63, 122, 138);""")
            self.league_editor_button.setStyleSheet("""border-radius:0px;
    color: rgb(255, 255, 255);
    background-color: rgb(63, 122, 138);""")
            if coord:
                for team in self.League.teams:
                    if team.name==str(self.leagues_list.item(coord.row(), 0).text()).strip():
                        self.Team=team

            # self.Team.add_member(TeamMember(0, 'test_member1','email1'))
            # self.Team.add_member(TeamMember(1, 'test_member2','email2'))
            # self.Team.add_member(TeamMember(2, 'test_member3','email3'))
            self.update_members_table()

            self.stackedWidget.setCurrentIndex(2)

    def add_item(self,tablewidget,item,type,email=False):
        if type=='league':
            oid=self.League_Database.leagues[-1].oid+1
            _league=League(oid,item.text())
            self.League_Database.add_league(_league)
        elif type=='team':
            oid = self.League.teams[-1].oid+1
            _team=Team(oid,item.text())
            self.League.add_team(_team)
        elif type=='member':
            oid = self.Team.members[-1].oid+1
            _team_member=TeamMember(oid,item.text(),email.text())
            self.Team.add_member(_team_member)

        item = QTableWidgetItem(item.text())
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        if email:
            email = QTableWidgetItem(email.text())
            email.setFlags(QtCore.Qt.ItemIsEnabled)
        for row in range(0, tablewidget.rowCount()):
            if tablewidget.item(row, 0) is None:
                tablewidget.setItem(row, 0, item)
                if email:
                    tablewidget.setItem(row, 1, email)
                return
            else:
                if str(tablewidget.item(row, 0).text()).strip() in [None, '', ' ', 'None']:
                    tablewidget.setItem(row, 0, item)
                    if email:
                        tablewidget.setItem(row, 1, email)
                    return

    def remove_item(self,tablewidget,item,type,email=False):
        if type == 'league':
            _league = self.League_Database.league_named(item.text())
            if _league is None:return
            self.League_Database.remove_league(_league)
        elif type == 'team':
            for team in self.League.teams:
                if str(team.name).strip()==str(item.text()).strip():
                    self.League.remove_team(team)
                    break
        elif type == 'member':
            oid = self.Team.members[-1].oid+1
            _team_member = TeamMember(oid, item.text(), email.text())
            if _team_member is None:return
            self.Team.remove_member(_team_member)

        for row in range(0, tablewidget.rowCount()):
            if tablewidget.item(row, 0) is None:
                continue
            else:
                if str(tablewidget.item(row, 0).text()).strip()==str(item.text()).strip():
                    if email:
                        if str(tablewidget.item(row, 1).text()).strip()!=str(email.text()).strip():continue
                    tablewidget.removeRow(row)
                    rowPosition = tablewidget.rowCount()
                    tablewidget.insertRow(rowPosition)
                    return

    def edit_item(self,tablewidget,cur_item,prop_item,row2=False):
        if type == 'league':
            _league = self.League_Database.league_named(cur_item.text())
            _league.name=prop_item.text()
        elif type == 'team':
            for team in self.League.teams:
                if str(team.name).strip()==str(cur_item.text()).strip():
                    team.name=prop_item.text()
        elif type == 'member':
            for member in self.Team.members:
                if row2:
                    if str(member.email).strip() != str(cur_item.text()).strip():continue

                if str(member.name).strip()==str(cur_item.text()).strip():
                    member.name=prop_item.text()

        for row in range(0, tablewidget.rowCount()):
            if row2:
                column=1
            else:
                column=0
            if tablewidget.item(row, column) is None:
                continue
            else:
                if str(tablewidget.item(row, column).text()).strip() == str(cur_item.text()).strip():
                    item = QTableWidgetItem(prop_item.text())
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    tablewidget.setItem(row, column, item)
                    return

    def load_leagues_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Load File", "",
                                                  "All Files (*.*)", options=options)
        if fileName is None: return
        #need clearance
        self.League_Database.import_league(fileName)
        self.update_leagues_table()


    def save_leagues_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                  "All Files (*.*)", options=options)
        if fileName in [None,'']: return
        self.League_Database.export_league(fileName)
        # need clearance

    def load_teams_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Load File", "",
                                                  "All Files (*.*)", options=options)
        if fileName in [None,'']: return
        #need clearance
        self.League_Database.import_league_teams(self.League,fileName)
        self.update_teams_table()
        print('here')

    def save_teams_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                  "All Files (*.*)", options=options)
        if fileName in [None,'']: return
        self.League_Database.export_league_teams(self.League,fileName)
        # need clearance
    def update_members_table(self):
        for member_item in self.Team.members:
            item=QTableWidgetItem(member_item.name)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            for row in range(0,self.members_list.rowCount()):
                if self.members_list.item(row, 0) is None:
                    self.members_list.setItem(row, 0, item)
                else:
                    if str(self.members_list.item(row, 0).text()).strip() in [None,'',' ','None']:
                        self.members_list.setItem(row, 0, item)
                        break

    
    
    def update_teams_table(self):
        for team_item in self.League.teams:
            item=QTableWidgetItem(team_item.name)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            for row in range(0,self.teams_list.rowCount()):
                if self.teams_list.item(row, 0) is None:
                    self.teams_list.setItem(row, 0, item)
                else:
                    if str(self.teams_list.item(row, 0).text()).strip() in [None,'',' ','None']:
                        self.teams_list.setItem(row, 0, item)
                        break

    
    def update_leagues_table(self):
        for league_item in self.League_Database.leagues:
            item=QTableWidgetItem(league_item.name)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            for row in range(0,self.leagues_list.rowCount()):
                print(row)
                if self.leagues_list.item(row, 0) is None:
                    self.leagues_list.setItem(row, 0, item)
                else:
                    if str(self.leagues_list.item(row, 0).text()).strip() in [None,'',' ','None']:
                        self.leagues_list.setItem(row, 0, item)
                        break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())