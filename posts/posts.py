from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList
from database import Thread, Comment


class PostContent(BoxLayout):
    def __init__(self, thread, app=None, *args, **kwargs):
        super(PostContent, self).__init__(**kwargs)
        self.thread = thread
        self.app = app
        Clock.schedule_once(self.setup)

    def setup(self, *args, **kwargs):
        self.ids.dialog_author.text = self.thread.author.username
        self.ids.dialog_author.secondary_text = str(self.thread.date)
        if self.thread.description:
            self.ids.dialog_description.text = self.thread.description
        if self.thread.image:
            self.ids.dialog_img.source = f"media/thread/{self.thread.id}.png"
        self.ids.dialog_likes.text = str(self.thread.likes)
        comments = self.app.db.get_object_by_attr(Comment, 'thread_id', self.thread.id)
        self.ids.dialog_comments.text = f"Comments({len(comments) if comments else 0})"
        self.ids.dialog_like_btn.on_press = lambda: like_post(self.thread, self, "dialog_likes")


class LocationPopupMenu(MDDialog):
    def __init__(self, id):
        app = App.get_running_app()
        thread = app.db.get_object_by_attr(Thread, "id", id)[0]
        super().__init__(
            type="custom",
            content_cls=PostContent(thread, app=app),
            size_hint=(.95, 1),
            buttons = [
                MDFlatButton(text='Close', on_release=self.close_dialog)
            ]
        )
        self.title = thread.title

    def close_dialog(self, *args):
        self.dismiss()


class ThreadCard(MDCard):
    def __init__(self, thread, **kwargs):
        super(ThreadCard, self).__init__(**kwargs)
        self.thread = thread

    def on_release(self):
        menu = LocationPopupMenu(self.thread.id)
        menu.open()


class ScrollList(ScrollView):
    pass


class FeedScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super(FeedScreen, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.redraw()

    def redraw(self):
        self.clear_widgets()
        threads = self.app.db.list_threads()
        self.scroll_list = ScrollList()
        y = 0.5
        i = 1
        for x in threads:
            thread_card = ThreadCard(x)
            thread_card.ids.pos_hint = {"center_x": 0.5, "center_y": 1 - y * i}
            thread_card.ids.thread_author.text = x.author.username
            thread_card.ids.thread_author.secondary_text = str(x.date)
            thread_card.ids.thread_title.text = x.title
            if len(x.description) > 0:
                des = x.description
                while len(des) > 120:
                    des = des[:-1]
                thread_card.ids.thread_description.text = des+"..."
            if x.image:
                thread_card.ids.thread_img.source = f"media/thread/{x.id}.png"
            thread_card.ids.thread_likes.text = str(x.likes)
            comments = self.app.db.get_object_by_attr(Comment, 'thread_id', x.id)
            thread_card.ids.thread_comments.text = f"Comments({len(comments) if comments else 0})"
            self.scroll_list.ids.thread_list.add_widget(thread_card)
            thread_card.ids.thread_like_btn.on_press = lambda: like_post(x, thread_card, "thread_likes")
        self.add_widget(self.scroll_list)


def like_post(thread, slot=None, value=None):
    thread.likes += 1
    App.get_running_app().db.session.commit()
    getattr(slot.ids, value).text = str(thread.likes)
