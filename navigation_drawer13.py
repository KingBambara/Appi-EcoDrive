navigation_helper = """
MDScreen:

    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: 'EcoDrive'
            right_action_items: [["molecule-co2", lambda x: app.CO2()]]
            left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
            md_bg_color: 'green'
            elevation: 5

        MDBottomNavigation:
            selected_color_background: "green"
            text_color_active: "gray"

            MDBottomNavigationItem:
                name: 'screen 1'
                text: 'account'
                icon: 'account'
                FloatLayout:
                    Image:
                        source: 'mm.png'  # Remplacer par le chemin de votre image de fond
                        allow_stretch: True
                        keep_ratio: False
                        size_hint: (1, 1)
                        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                BoxLayout:
                    orientation: 'vertical'
                    padding: dp(10)
                    spacing: dp(10)

                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(200)

                        MDTextField:
                            id: username
                            hint_text: "Username"
                            mode: "rectangle"
                            icon_right: "account"
                            line_color_normal: 0, 0.5, 0, 1  # Dark green line
                            line_color_focus: 0, 0.5, 0, 1  # Dark green line when focused
                            text_color: 0, 0, 0, 1  # Black text
                            color_mode: 'custom'
                            fill_color: 0, 0, 0, 0.1
                            size_hint_x: None
                            width: dp(200)
                            pos_hint: {'center_x': 0.5}

                        MDTextField:
                            id: password
                            hint_text: "Password"
                            password: True
                            mode: "rectangle"
                            icon_right: "lock"
                            line_color_normal: 0, 0.5, 0, 1  # Dark green line
                            line_color_focus: 0, 0.5, 0, 1  # Dark green line when focused
                            text_color: 0, 0, 0, 1  # Black text
                            color_mode: 'custom'
                            fill_color: 0, 0, 0, 0.1
                            size_hint_x: None
                            width: dp(200)
                            pos_hint: {'center_x': 0.5}

                    MDRaisedButton:
                        text: "Login"
                        md_bg_color: 0, 0.5, 0, 1  # Dark green background
                        text_color: 1, 1, 1, 1  # White text
                        size_hint_x: None
                        width: dp(200)
                        pos_hint: {'center_x': 0.5}
                        on_release: app.login(username.text, password.text)

                    MDRaisedButton:
                        text: "Create Profile"
                        md_bg_color: 0, 0.5, 0, 1  # Dark green background
                        text_color: 1, 1, 1, 1  # White text
                        size_hint_x: None
                        width: dp(200)
                        pos_hint: {'center_x': 0.5}
                        on_release: app.show_create_profile_dialog()

                    MDLabel:
                        id: login_message
                        text: ""
                        halign: "center"
                        font_style: "H6"
                        theme_text_color: "Custom"
                        text_color: 0, 0.5, 0, 1  # Dark green text

            MDBottomNavigationItem:
                name: 'screen 2'
                text: 'Calculator'
                icon: 'foot-print'

                PredictionScreen:

            MDBottomNavigationItem:
                name: 'screen 3'
                text: 'Map'
                icon: 'map'

                MDRelativeLayout:
                    MapView:
                        lat: 50.6
                        lon: 3.05
                        zoom: 13

                    MDBoxLayout:
                        spacing: 20
                        padding: 10
                        orientation: 'horizontal'
                        pos_hint: {'y': 0.87}
                        MDBoxLayout:
                            radius: 30
                            size_hint_x: 0.1
                            size_hint_y: 0.2

    MDNavigationLayout:
        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                orientation: 'vertical'
                padding: "8dp"
                spacing: "8dp"

                Image:
                    id: avatar
                    size_hint: (1, 1)
                    source: "MINE.jpg"

                MDLabel:
                    text: "Welcome to our carbon footprint calculator"
                    font_style: "Subtitle1"
                    theme_text_color: "Custom"
                    text_color: 0, 0, 0, 1
                    size_hint_y: None
                    height: self.texture_size[1]

                ScrollView:
                    DrawerList:
                        id: md_list
                        MDList:
                            OneLineIconListItem:
                                text: "About us"
                                theme_text_color: "Custom"
                                text_color: 0, 0.32, 0, 1
                                on_release: app.about_us()
                                IconLeftWidget:
                                    icon: "information-outline"
                                    theme_text_color: "Custom"
                                    text_color: 0, 0.32, 0, 1
                                    on_release: app.about_us()

                            OneLineIconListItem:
                                text: "Help"
                                theme_text_color: "Custom"
                                text_color: 0, 0.32, 0, 1
                                on_release: app.Help()
                                IconLeftWidget:
                                    icon: "help-circle-outline"
                                    theme_text_color: "Custom"
                                    text_color: 0, 0.32, 0, 1
                                    on_release: app.Help()

                            OneLineIconListItem:
                                text: "Contact Us"
                                theme_text_color: "Custom"
                                text_color: 0, 0.32, 0, 1
                                on_release: app.contact_us()
                                IconLeftWidget:
                                    icon: "phone"
                                    on_release: app.contact_us()
                                    theme_text_color: "Custom"
                                    text_color: 0, 0.32, 0, 1

                            OneLineIconListItem:
                                text: "Logout"
                                theme_text_color: "Custom"
                                text_color: 0, 0.32, 0, 1
                                on_release: app.logout()
                                IconLeftWidget:
                                    icon: "logout"
                                    theme_text_color: "Custom"
                                    text_color: 0, 0.32, 0, 1
                                    on_release: app.logout()

<PredictionScreen>:
    orientation: "vertical"
    padding: "10dp"
    spacing: "10dp"

    ScrollView:
        do_scroll_x: False
        do_scroll_y: True
        size_hint_y: None
        height: root.height if root.height <= 600 else 600

        BoxLayout:
            orientation: "vertical"
            padding: "10dp"
            spacing: "10dp"
            size_hint_y: None
            height: self.minimum_height

            MDTextField:
                id: engine_size_input
                hint_text: "Engine Size"
                mode: "rectangle"
                size_hint_y: None
                size_hint_x: 1
                height: "40dp"
                text_color: "black"
                line_color_focus: 0, 0.5, 0, 1  # Dark green line
                line_color_normal: 0, 0.5, 0, 1  # Dark green line
                current_hint_text_color: "black"
                cursor_color: "black"
                font_size: "14sp"
                foreground_color: 0, 0, 0, 1
                write_tab: False
                on_focus: if self.focus: self.foreground_color = [0, 0, 0, 1]

            MDTextField:
                id: cylinders_input
                hint_text: "Cylinders"
                mode: "rectangle"
                size_hint_y: None
                size_hint_x: 1
                height: "40dp"
                text_color: "black"
                line_color_focus: 0, 0.5, 0, 1  # Dark green line
                line_color_normal: 0, 0.5, 0, 1  # Dark green line
                current_hint_text_color: "black"
                cursor_color: "black"
                font_size: "14sp"
                foreground_color: 0, 1, 0, 1  # Dark green
                write_tab: False
                on_focus: if self.focus: self.foreground_color = [0, 1, 0, 1]

            MDTextField:
                id: fuel_consumption_input
                hint_text: "Fuel Consumption"
                mode: "rectangle"
                size_hint_y: None
                size_hint_x: 1
                height: "40dp"
                text_color: "black"
                line_color_focus: 0, 0.5, 0, 1  # Dark green line
                line_color_normal: 0, 0.5, 0, 1  # Dark green line
                current_hint_text_color: "black"
                cursor_color: "black"
                font_size: "14sp"
                foreground_color: 0, 0, 0, 1
                write_tab: False
                on_focus: if self.focus: self.foreground_color = [0, 0, 0, 1]

            MDTextField:
                id: kilometers_input
                hint_text: "Kilometers"
                mode: "rectangle"
                size_hint_y: None
                size_hint_x: 1
                height: "40dp"
                text_color: "black"
                line_color_focus: 0, 0.5, 0, 1  # Dark green line
                line_color_normal: 0, 0.5, 0, 1  # Dark green line
                current_hint_text_color: "black"
                cursor_color: "black"
                font_size: "14sp"
                foreground_color: 0, 0, 0, 1
                write_tab: False
                on_focus: if self.focus: self.foreground_color = [0, 0, 0, 1]

            MDRaisedButton:
                id: fuel_type_button
                text: "Fuel Type"
                size_hint_y: None
                size_hint_x: 1
                height: "40dp"
                md_bg_color: "darkgreen"
                text_color: "white"
                on_release: root.open_fuel_menu()

            MDRaisedButton:
                text: "Predict"
                size_hint_y: None
                size_hint_x: 1
                height: "40dp"
                md_bg_color: "darkgreen"
                text_color: "white"
                on_release: root.make_prediction()
"""
