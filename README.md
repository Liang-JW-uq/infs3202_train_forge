Project Structure
    pt_trainer/
        --- config/
        --- backend/
        --- orm/
        --- trainer/


# [Authentication] Trainer to User_Trainer

* Main function is to have the Trainer INHERIT from the "default" of user, so it can be used w/ Django Authentication
* User_Trainer will have a new column "is_trainer" boolean to identify if they are a Trainer or *Admin User*
* After INHERITING Abstract User Class for own ORM Model, NEED TO UPDATE SETTINGS.PY, *AUTH_USER_MODEL="orm.UserTrainer"*
* Then, need to go to Django Admin page, and *SET GROUPS* so that "Premium" has special "AI Features"

2. Handling static files (css,js,images)
    ---- https://www.digitalocean.com/community/tutorials/working-with-django-templates-static-files

* This is for "base.html line 41+", and "settings.py line 39-45"
3. Handling applicaction level messages
    ---- https://micropyramid.medium.com/basics-of-django-messages-framework-4315a0f3a469
    ---- https://dev.to/doridoro/django-messages-framework-482p

10. Authentication
    --- https://medium.com/@mathur.danduprolu/django-getting-started-with-django-2024-authentication-and-authorization-part-8-16-7bf55d1f7570
    --- https://realpython.com/django-user-management/
    --- https://www.pragnakalp.com/django-tutorial-a-comprehensive-guide-to-use-djangos-authentication-system/

12. Handling sensitive data using env variables
        --- https://dev.to/defidelity/protect-your-sensitive-data-a-guide-to-env-files-in-django-499e


