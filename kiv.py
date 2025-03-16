from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog

KV = '''
Screen:
    canvas.before:
        Color:
            rgba: 0.05, 0.05, 0.2, 1  # Darker blue professional background
        Rectangle:
            pos: self.pos
            size: self.size
    
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        
        MDLabel:
            text: "Enter Your Scores"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: "H5"

        MDCard:
            orientation: 'vertical'
            padding: dp(20)
            size_hint: None, None
            size: dp(320), dp(220)
            elevation: 12
            radius: [15, 15, 15, 15]
            shadow_softness: 15
            shadow_offset: 3, 3
            pos_hint: {'center_x': 0.5}
            md_bg_color: 1, 1, 1, 1
            
            MDTextField:
                id: math_score
                hint_text: "Math Score"
                mode: "fill"
                size_hint_x: 1
                helper_text_mode: "on_focus"
                pos_hint: {'center_x': 0.5}
                icon_right: "calculator"
                icon_right_color: 0, 0.6, 0, 1
                
            MDTextField:
                id: science_score
                hint_text: "Science Score"
                mode: "fill"
                size_hint_x: 1
                helper_text_mode: "on_focus"
                icon_right: "atom"
                icon_right_color: 0, 0.6, 0, 1
                
            MDTextField:
                id: english_score
                hint_text: "English Score"
                mode: "fill"
                size_hint_x: 1
                helper_text_mode: "on_focus"
                icon_right: "book"
                icon_right_color: 0, 0.6, 0, 1
    
        MDRaisedButton:
            id: recommend_button
            text: "Get Recommended Topic"
            md_bg_color: 0, 0.8, 0.2, 1
            pos_hint: {'center_x': 0.5}
            on_release: app.get_recommendation()
            elevation: 5
            size_hint_x: None
            width: dp(220)
        
        MDRaisedButton:
            id: try_again_button
            text: "Try Another"
            md_bg_color: 0, 0.8, 0.2, 1  # Green button
            pos_hint: {'right': 1, 'top': 1}  # Aligned to top-right corner
            on_release: app.reset_fields()
            elevation: 5
            size_hint_x: None
            width: dp(120)
            opacity: 0  # Initially hidden

        MDLabel:
            id: result_label
            text: ""
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: "H6"

        MDCard:
            id: error_card
            md_bg_color: 1, 0, 0, 1
            size_hint: None, None
            size: dp(320), dp(50)
            elevation: 8
            pos_hint: {'center_x': 0.5}
            radius: [12, 12, 12, 12]
            opacity: 0
            
            MDLabel:
                id: error_label
                text: "⚠ Error! Check API or input values."
                halign: "center"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
'''

class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def get_recommendation(self):
        math = self.root.ids.math_score.text.strip()
        science = self.root.ids.science_score.text.strip()
        english = self.root.ids.english_score.text.strip()
        
        if not math.isdigit() or not science.isdigit() or not english.isdigit():
            self.root.ids.error_card.opacity = 1
            return
        
        self.root.ids.error_card.opacity = 0
        scores = {'Math': int(math), 'Science': int(science), 'English': int(english)}
        weak_subject = min(scores, key=scores.get)
        recommended_topics = {'Math': 'Geometry', 'Science': 'Physics', 'English': 'Grammar'}
        
        self.root.ids.result_label.text = f"Weak Subject: {weak_subject}\nRecommended Topic: {recommended_topics[weak_subject]}"
        self.root.ids.recommend_button.opacity = 0  # Hide the button after getting a recommendation
        self.root.ids.try_again_button.opacity = 1  # Show Try Another button

    def reset_fields(self):
        self.root.ids.math_score.text = ""
        self.root.ids.science_score.text = ""
        self.root.ids.english_score.text = ""
        self.root.ids.result_label.text = ""
        self.root.ids.error_card.opacity = 0
        self.root.ids.recommend_button.opacity = 1  # Show the recommend button again
        self.root.ids.try_again_button.opacity = 0  # Hide Try Another button

if __name__ == "__main__":
    MainApp().run()
