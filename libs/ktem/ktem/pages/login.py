import hashlib

import gradio as gr
from ktem.app import BasePage
from ktem.db.models import User, engine
from ktem.pages.resources.user import (
    create_user,
    validate_password,
    validate_username,
)
from sqlmodel import Session, select
from theflow.settings import settings as flowsettings

KH_FEATURE_USER_SIGNUP = getattr(flowsettings, "KH_FEATURE_USER_SIGNUP", True)

PASSWORD_HINT = (
    "At least 8 characters, with an uppercase letter, a lowercase letter, "
    "a digit and a special character (e.g. ! @ # ?)"
)

fetch_creds = """
function() {
    const username = getStorage('username', '')
    const password = getStorage('password', '')
    return [username, password, null];
}
"""

# remember the credentials only once they've been accepted, so a typo doesn't
# get replayed (with an error popup) on every page reload
persist_creds_js = """
function(creds) {
    if (creds && creds.usn) {
        setStorage('username', creds.usn);
        setStorage('password', creds.pwd);
    }
    return [];
}
"""


def _error(message: str = ""):
    return gr.update(value=message, visible=bool(message))


class LoginPage(BasePage):

    public_events = ["onSignIn"]

    def __init__(self, app):
        self._app = app
        self.on_building_ui()

    def on_building_ui(self):
        with gr.Column(elem_id="login-card"):
            gr.Markdown(
                f"# {self._app.app_name}\n"
                "Chat with your documents and get cited answers.",
                elem_id="login-heading",
            )

            # sign-in form
            with gr.Column(visible=False, elem_classes=["auth-form"]) as self.signin:
                gr.Markdown("### Sign in", elem_classes=["auth-title"])
                self.signin_error = gr.Markdown(
                    visible=False, elem_classes=["auth-error"]
                )
                self.usn = gr.Textbox(
                    label="Username",
                    placeholder="Enter your username",
                    max_lines=1,
                )
                self.pwd = gr.Textbox(
                    label="Password",
                    placeholder="Enter your password",
                    type="password",
                )
                self.btn_login = gr.Button("Sign in", variant="primary")
                self.btn_to_signup = gr.Button(
                    "Don't have an account? Create one",
                    size="sm",
                    elem_classes=["auth-switch"],
                    visible=KH_FEATURE_USER_SIGNUP,
                )

            # sign-up form
            with gr.Column(visible=False, elem_classes=["auth-form"]) as self.signup:
                gr.Markdown("### Create an account", elem_classes=["auth-title"])
                self.signup_error = gr.Markdown(
                    visible=False, elem_classes=["auth-error"]
                )
                self.signup_usn = gr.Textbox(
                    label="Username",
                    placeholder="3-32 letters, digits or underscores",
                    max_lines=1,
                )
                self.signup_pwd = gr.Textbox(
                    label="Password",
                    placeholder="Choose a password",
                    type="password",
                    info=PASSWORD_HINT,
                )
                self.signup_pwd_cnf = gr.Textbox(
                    label="Confirm password",
                    placeholder="Repeat the password",
                    type="password",
                )
                self.btn_signup = gr.Button("Create account", variant="primary")
                self.btn_to_signin = gr.Button(
                    "Already have an account? Sign in",
                    size="sm",
                    elem_classes=["auth-switch"],
                )

            # carries accepted credentials to the browser to be remembered
            self._accepted_creds = gr.JSON(value=None, visible=False)

    def on_register_events(self):
        self.btn_to_signup.click(
            lambda: (
                gr.update(visible=False),
                gr.update(visible=True),
                _error(),
                _error(),
            ),
            outputs=[self.signin, self.signup, self.signin_error, self.signup_error],
            show_progress="hidden",
        )
        self.btn_to_signin.click(
            lambda: (
                gr.update(visible=True),
                gr.update(visible=False),
                _error(),
                _error(),
            ),
            outputs=[self.signin, self.signup, self.signin_error, self.signup_error],
            show_progress="hidden",
        )

        onSignIn = gr.on(
            triggers=[self.btn_login.click, self.pwd.submit],
            fn=self.sign_in,
            inputs=[self.usn, self.pwd],
            outputs=[
                self._app.user_id,
                self.usn,
                self.pwd,
                self.signin_error,
                self._accepted_creds,
            ],
            show_progress="hidden",
        )
        self._finish_sign_in(onSignIn)

        if KH_FEATURE_USER_SIGNUP:
            onSignUp = gr.on(
                triggers=[self.btn_signup.click, self.signup_pwd_cnf.submit],
                fn=self.sign_up,
                inputs=[self.signup_usn, self.signup_pwd, self.signup_pwd_cnf],
                outputs=[
                    self._app.user_id,
                    self.signup_usn,
                    self.signup_pwd,
                    self.signup_pwd_cnf,
                    self.signup_error,
                    self._accepted_creds,
                ],
                show_progress="hidden",
            )
            self._finish_sign_in(onSignUp)

    def _finish_sign_in(self, event):
        """Remember the credentials, update the forms and notify the app"""
        # js-only steps never report completion in gradio, so nothing can be
        # chained after this one: keep it on its own branch
        event.then(fn=None, inputs=[self._accepted_creds], js=persist_creds_js)

        event = event.then(
            self.hide_forms_if_signed_in,
            inputs=[self._app.user_id],
            outputs=[self.signin, self.signup],
            show_progress="hidden",
        )
        for app_event in self._app.get_event("onSignIn"):
            event = event.success(**app_event)

    def hide_forms_if_signed_in(self, user_id):
        # after a failed attempt keep the current form (and its error) open
        if user_id is None:
            return gr.update(), gr.update()
        return gr.update(visible=False), gr.update(visible=False)

    def toggle_login_visibility(self, user_id):
        # signed out: show the sign-in form; signed in: hide both forms
        return (
            gr.update(visible=user_id is None),
            gr.update(visible=False),
        )

    def _on_app_created(self):
        onSignIn = self._app.app.load(
            self.login,
            inputs=[self.usn, self.pwd],
            outputs=[self._app.user_id, self.usn, self.pwd],
            show_progress="hidden",
            js=fetch_creds,
        ).then(
            self.toggle_login_visibility,
            inputs=[self._app.user_id],
            outputs=[self.signin, self.signup],
        )
        for event in self._app.get_event("onSignIn"):
            onSignIn = onSignIn.success(**event)

    def on_subscribe_public_events(self):
        self._app.subscribe_event(
            name="onSignOut",
            definition={
                "fn": self.toggle_login_visibility,
                "inputs": [self._app.user_id],
                "outputs": [self.signin, self.signup],
                "show_progress": "hidden",
            },
        )
        self._app.subscribe_event(
            name="onSignOut",
            definition={
                "fn": lambda: None,
                "outputs": [self._accepted_creds],
                "show_progress": "hidden",
            },
        )

    def sign_in(self, usn, pwd, request: gr.Request):
        """Handle the sign-in form"""
        if not (usn or "").strip() or not pwd:
            return None, usn, pwd, _error("Enter your username and password."), None

        user_id, usn_out, pwd_out = self.login(usn, pwd, request, warn=False)
        if user_id is None:
            return (
                None,
                usn_out,
                "",
                _error("Incorrect username or password."),
                None,
            )
        return user_id, usn_out, pwd_out, _error(), {"usn": usn.strip(), "pwd": pwd}

    def sign_up(self, usn, pwd, pwd_cnf):
        """Handle the sign-up form: create a regular user and sign them in"""
        usn = (usn or "").strip()
        pwd = pwd or ""
        pwd_cnf = pwd_cnf or ""

        error = validate_username(usn) or validate_password(pwd, pwd_cnf)
        if error:
            # show one requirement per line rather than a single long sentence
            error = "\n".join(f"- {line}" for line in error.split("; "))
            return None, usn, pwd, pwd_cnf, _error(error), None

        if not create_user(usn=usn, pwd=pwd, is_admin=False):
            return (
                None,
                usn,
                pwd,
                pwd_cnf,
                _error(f'The username "{usn}" is already taken.'),
                None,
            )

        with Session(engine) as session:
            user = session.exec(
                select(User).where(User.username_lower == usn.lower())
            ).one()
            user_id = user.id

        gr.Info(f"Welcome, {usn}! Your account has been created.")
        return user_id, "", "", "", _error(), {"usn": usn, "pwd": pwd}

    def login(self, usn, pwd, request: gr.Request, warn: bool = True):
        try:
            import gradiologin as grlogin

            user = grlogin.get_user(request)
        except (ImportError, AssertionError):
            user = None

        if user:
            user_id = user["sub"]
            with Session(engine) as session:
                stmt = select(User).where(
                    User.id == user_id,
                )
                result = session.exec(stmt).all()

            if result:
                print("Existing user:", user)
                return user_id, "", ""
            else:
                print("Creating new user:", user)
                create_user(
                    usn=user["email"],
                    pwd="",
                    user_id=user_id,
                    is_admin=False,
                )
                return user_id, "", ""
        else:
            if not usn or not pwd:
                return None, usn, pwd

            hashed_password = hashlib.sha256(pwd.encode()).hexdigest()
            with Session(engine) as session:
                stmt = select(User).where(
                    User.username_lower == usn.lower().strip(),
                    User.password == hashed_password,
                )
                result = session.exec(stmt).all()
                if result:
                    return result[0].id, "", ""

                if warn:
                    gr.Warning("Invalid username or password")
                return None, usn, pwd
