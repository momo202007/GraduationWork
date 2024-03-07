from django import forms
from .models import Diary
# from .models import #
class LoginForm(forms.Form):
    user_id_textbox = forms.CharField(error_messages={"required": ""},label='アカウントID',max_length=10)
    user_pw_textbox = forms.CharField(label='パスワードを入力',max_length= 10,min_length=4,widget=forms.PasswordInput())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_id_textbox'].widget.attrs['class'] = 'form-control_login'
        self.fields['user_id_textbox'].widget.attrs['name'] = 'user_id_textbox'
        self.fields['user_pw_textbox'].widget.attrs['pattern'] = '^[a-zA-Z0-9]+$'
        self.fields['user_pw_textbox'].widget.attrs['class'] = 'form-control_pw'
        self.fields['user_pw_textbox'].widget.attrs['name'] = 'user_pw_textbox'

class Pw_resetForm(forms.Form):
    Pw_reset_textbox = forms.CharField(label='パスワード再設定',max_length=10,widget=forms.PasswordInput())
    Pw_reset_check_textbox = forms.CharField(label='パスワード再設定確認',max_length= 10,widget=forms.PasswordInput())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Pw_reset_textbox'].widget.attrs['class'] = 'Pw_reset_form-control'
        self.fields['Pw_reset_textbox'].widget.attrs['name'] = 'Pw_reset_textbox'

        self.fields['Pw_reset_check_textbox'].widget.attrs['class'] = 'Pw_reset_check_form-control'
        self.fields['Pw_reset_check_textbox'].widget.attrs['name'] = 'Pw_reset_check_textbox'

class First_pw_settingForm(forms.Form):
    first_pw_id_textbox = forms.CharField(label='パスワード設定_アカウントID',max_length=10)
    first_pw_textbox = forms.CharField(label='パスワード設定',max_length= 10,widget=forms.PasswordInput())
    first_pw_check_textbox = forms.CharField(label='パスワード設定確認',max_length= 10,widget=forms.PasswordInput())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_pw_id_textbox'].widget.attrs['class'] = 'form-control_pwset_id'
        self.fields['first_pw_id_textbox'].widget.attrs['name'] = 'first_pw_id_textbox'

        self.fields['first_pw_textbox'].widget.attrs['class'] = 'form-control_pwset'
        self.fields['first_pw_textbox'].widget.attrs['name'] = 'first_pw_textbox'

        self.fields['first_pw_check_textbox'].widget.attrs['class'] = 'form-control_pwset_cofimetion'
        self.fields['first_pw_check_textbox'].widget.attrs['name'] = 'first_pw_check_textbox'

class Sns_postForm(forms.Form):
    sns_inputbox = forms.CharField(error_messages={"required": ""} ,label='',max_length=300 ,widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['sns_inputbox'].widget.attrs['class'] = 'sns_form-control'
        self.fields['sns_inputbox'].widget.attrs['name'] = 'sns_inputbox'

class Diary_newpostForm(forms.Form):
    # class Meta:
    #     model = Diary
    #     fields = ('diary_images')
    #     widgets = {
    #         'diary_text': forms.Textarea(attrs={'rows':30, 'cols':80}),
    #     }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.widget.attrs['class'] = 'form-control'
    
    diary_inputbox = forms.CharField(label='',max_length=1000, widget=forms.Textarea())
    diary_image = forms.ImageField(required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['diary_inputbox'].widget.attrs['class'] = 'diary_form-control'
        self.fields['diary_inputbox'].widget.attrs['name'] = 'diary_inputbox'
        self.fields['diary_image'].widget.attrs['class'] = 'diary_image_form-control'
        self.fields['diary_image'].widget.attrs['name'] = 'diary_image'

# class Diary_editingForm(forms.Form):
#     diary_editingbox = forms.CharField(label='',max_length=30)
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['diary_editingbox'].widget.attrs['class'] = 'form-control'
#         self.fields['diary_editingbox'].widget.attrs['name'] = 'diary_editingbox'

class Happy_registrationForm(forms.Form):
    calendar_inputbox = forms.CharField(label='',max_length=30,widget=forms.Textarea())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['calendar_inputbox'].widget.attrs['class'] = 'calendar_exprience_form_control'
        self.fields['calendar_inputbox'].widget.attrs['name'] = 'calendar_inputbox'

class Happy_editingForm(forms.Form):
    calendar_editingbox = forms.CharField(label='',max_length=30,widget=forms.Textarea())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['calendar_editingbox'].widget.attrs['class'] = 'calendar_exprience_form_control'
        self.fields['calendar_editingbox'].widget.attrs['name'] = 'calendar_editingbox'

class Experience_registrationForm(forms.Form):
    experience_inputbox = forms.CharField(label='',max_length=2000,widget=forms.Textarea())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['experience_inputbox'].widget.attrs['class'] = 'calendar_exprience_form_control'
        self.fields['experience_inputbox'].widget.attrs['name'] = 'experience_inputbox'

class Experience_editingForm(forms.Form):
    experience_editingbox = forms.CharField(label='',max_length=2000,widget=forms.Textarea())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['experience_editingbox'].widget.attrs['class'] = 'calendar_exprience_form_control'
        self.fields['experience_editingbox'].widget.attrs['name'] = 'experience_editingbox'

class Rehab_todo_addForm(forms.Form):
    todo_inputbox = forms.CharField(label='',max_length=30)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['todo_inputbox'].widget.attrs['class'] = 'tod_form-control'
        self.fields['todo_inputbox'].widget.attrs['name'] = 'todo_inputbox'

class Sign_upForm(forms.Form):
    email_box = forms.CharField(label='メールアドレス',max_length=30)
    pw_textbox = forms.CharField(label='パスワードを入力',max_length= 10,widget=forms.PasswordInput())
    pw_check_textbox = forms.CharField(label='パスワードを再度入力',max_length= 10,widget=forms.PasswordInput())
    birth_date = forms.DateField(label='患者様生年月日', input_formats=['%d'], widget=forms.DateInput(attrs={'class':'form-control'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email_box'].widget.attrs['class'] = 'Sign_up_mail_form-control'
        self.fields['email_box'].widget.attrs['name'] = 'email_box'

        self.fields['pw_textbox'].widget.attrs['class'] = 'Sign_up_pw_form-control'
        self.fields['pw_textbox'].widget.attrs['name'] = 'pw_textbox'
        self.fields['pw_textbox'].widget.attrs['pattern'] = '^[a-zA-Z0-9]+$'

        self.fields['pw_check_textbox'].widget.attrs['pattern'] = '^[a-zA-Z0-9]+$'
        self.fields['pw_check_textbox'].widget.attrs['class'] = 'Sign_up_pw_confimation_form-control'
        self.fields['pw_check_textbox'].widget.attrs['name'] = 'pw_check_textbox'

        self.fields['birth_date'].widget.attrs['class'] = 'Sign_up_birth_date_form-control'
        self.fields['birth_date'].widget.attrs['name'] = 'birth_date'
        
class Supporter_rehab_todo_addForm(forms.Form):
    supporter_todo_inputbox = forms.CharField(label='',max_length=30)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['todo_inputbox'].widget.attrs['class'] = 'form-control'
        self.fields['todo_inputbox'].widget.attrs['name'] = 'todo_inputbox'

class information_changeForm(forms.Form):
    information_birth_date = forms.CharField(label='',max_length=30)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget.attrs['class'] = 'form-control'
        self.fields['birth_date'].widget.attrs['name'] = 'birth_date'

class Pass_confForm(forms.Form):
    user_id_textbox = forms.CharField(error_messages={"required": ""},label='アカウントID',max_length=10)
    user_email_box = forms.CharField(label='メールアドレス',max_length=30)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_id_textbox'].widget.attrs['class'] = 'form-control_login'
        self.fields['user_id_textbox'].widget.attrs['name'] = 'user_id_textbox'

        self.fields['user_email_box'].widget.attrs['class'] = 'Sign_up_mail_form-control'
        self.fields['user_email_box'].widget.attrs['name'] = 'user_email_box'