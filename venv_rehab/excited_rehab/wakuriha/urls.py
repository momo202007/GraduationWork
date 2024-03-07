from django.urls import path
from . import views


app_name = 'wakuriha'
urlpatterns = [
    path('',views.top,name="top"),
    path('supporter',views.supporter_top,name="sp_top"),

    path('allauth/login/',views.login,name="login"),
    path('allauth/signup/',views.signup,name="signup"),
    path('allauth/password_reset/',views.password_reset,name="password_reset"),
    path('allauth/first_password_set/',views.first_password_set,name="first_password_set"),
    path('allauth/withdrawal',views.withdrawal,name="withdrawal"),
    path('allauth/info_confirmation',views.info_confirmation,name="info_confirmation"),
    path('allauth/info_change',views.info_change,name="info_change"),
    path('allauth/rehab_complete',views.rehab_complete,name="rehab_complete"),
    path('id_conf',views.id_conf,name="id_conf"),
    path('pass_conf',views.pass_conf,name="pass_conf"),

    path('diary/menu/',views.diary_menu,name="diary_menu"),
    path('diary/post/',views.diary_post,name="diary_post"),
    path('diary/list/',views.diary_list,name="diary_list"),
    path('diary/editing/',views.diary_editing,name="diary_editing"),
    path('diary/reference/',views.diary_reference,name="diary_reference"),

    path('sns/menu/',views.sns_menu,name="sns_menu"),
    path('sns/timeline/',views.timeline,name="timeline"),
    path('sns/reference/',views.sns_reference,name="sns_reference"),
    path('sns/post/',views.sns_post,name="sns_post"),

    path('calendar/',views.calendar,name="calendar"),
    path('calendar/happy_editing',views.happy_editing,name="happy_editing"),
    path('calendar/happy_rederence',views.happy_rederence,name="happy_rederence"),
    path('calendar/happy_register',views.happy_register,name="happy_register"),

    path('ToDO/menu/',views.ToDO_menu,name="ToDO_menu"),
    path('ToDO/list/',views.ToDO_list,name="ToDO_list"),
    path('ToDO/add/',views.ToDO_add,name="ToDO_add"),
    path('ToDO/delete/',views.ToDO_delete,name="ToDO_delete"),
    path('ToDO/reference/',views.ToDO_reference,name="ToDO_reference"),
    path('supporter/ToDO/',views.supporter_ToDO,name="sp_ToDO"),
    path('collection_list',views.collection_list,name="collection_list"),
    path('rehab_complete_top',views.rehab_complete_top,name="rehab_complete_top"),

    path('experience/register',views.experience_register,name="experience_register"),
    path('experience/editing',views.experience_editing,name="experience_editing"),
]
