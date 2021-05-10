from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from database import Database
from login.login import LoginWindow, CreateAccountWindow
from feed.feed import FeedScreen


class TextScreen(Screen):
    pass


class FormScreen(Screen):
    pass


class TableScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class BottomNav(Screen):
    pass


class MyManager(ScreenManager):
    pass


ssm = ScreenManager()


class RetterApp(MDApp):
    global ssm
    sm = ssm
    def build(self):
        screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), BottomNav(name="bottom")]
        for screen in screens:
            ssm.add_widget(screen)

        ssm.current = "login"
        return ssm

app = RetterApp()
app.db = Database(dbtype='sqlite', dbname='retter.db')
app.run()