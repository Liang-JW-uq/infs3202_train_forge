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
    - Omondi, A. (2020, September 21). Working with Django Templates & Static Files. Digitalocean.com; DigitalOcean. https://www.digitalocean.com/community/tutorials/working-with-django-templates-static-files

‌

* This is for "base.html line 41+", and "settings.py line 39-45"
3. Handling applicaction level messages
    - MicroPyramid. (2017, April 3). Basics of Django messages framework. Medium. https://micropyramid.medium.com/basics-of-django-messages-framework-4315a0f3a469
    - DoriDoro. (2024, September 3). Django messages framework. DEV Community. https://dev.to/doridoro/django-messages-framework-482p

‌

* This is for "searching" results in the LIST pages *
4. Adding Search / Filter to list views and templates
    - Django, L. (n.d.). Django Search Tutorial. Learndjango.com. https://learndjango.com/tutorials/django-search-tutorial


* This is for the "Page 1, 2, 3, ..." at the BOTTOM of pages
5. Adding pagination to views/templates
    - Khan, M. (2024, November 11). Django Pagination Tutorial with Example. Medium; Django Unleashed. https://medium.com/django-unleashed/django-pagination-tutorial-with-example-745cefd54eb3

‌
10. Authentication
    - Mathur Danduprolu. (2024, May 24). Getting Started with Django 2024:Authentication and Authorization [Part 8/16]. Medium. https://medium.com/@mathur.danduprolu/django-getting-started-with-django-2024-authentication-and-authorization-part-8-16-7bf55d1f7570
    - Paweł Fertyk. (2024, December 18). Get Started With Django User Management. Realpython.com; Real Python.
    - Pragnakalp Techlabs. (2024, January 22). Django Tutorial: A Comprehensive Guide to use Django’s Authentication System. Pragnakalp Techlabs.
‌

12. Handling sensitive data using env variables
    - Adeyemi, A. H. (2023, February 22). Protect Your Sensitive Data: A Guide to .env Files in Django. DEV Community. https://dev.to/defidelity/protect-your-sensitive-data-a-guide-to-env-files-in-django-499e

