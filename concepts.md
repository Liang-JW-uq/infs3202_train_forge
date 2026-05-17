# Techonology Stacks

## 0. Project Structure
- config/
    - settings.py
      - MESSAGE_TAGS = {} decorate with bootstrap classes
      - reading from info.py for all keys
      - SOCIAL LOGINS CONFIGURATIONS
      - 
    - info.py           (**encrtpted base64 for all keys/secrets)
      - We DON'T USE 'env' because when PUSHED TO GAE, it MARKS API KEYS AS INVALID
- static/
  - styles for the whole app (only app)
- staticfiles/          (**this is generated for production - app engine)
- app.yaml              (**for app engine configurations)
- requirements.txt      (**for app engine to install additional libraries - manually, dont need all of them )
- requirements_app.txt  (auto from pip freeze >)
- .gitignore/.gcloudignore

- trainer/
  - forms/
  - views/
    - templates/
      - trainer/
        - appointments/
        - clients/
        - exerccises/
        - includes/         (**all reusable html parts in templates)
        - partials/         (**maintly for part html used by htmx)
        - tags/
        - workouts/
        - 

## 1. FullCalendar6+
- https://fullcalendar.io/
### 1.1
- /trainer/templates/trainer/appointments/appointment_calendar.html
  - onload, just declare calendar object and specify the url to get data ('get_trainer_appointments')
  - set object option initialView "dayGridMonth"
  - json data
- /trainer/templates/trainer/home.html
  - onload, just declare calendar object and specify the url to get data ('get_trainer_appointments')
  - set object option initialView "listMonth"
  - json data
- /trainer/views/appointment_view.py
  - get_trainer_appoints
    - filter Appointment by trainer and populate a list with FullCalendar event data
    - add url for path name 'workout_add' on empty slots
    - return as JsonResponse

## 2. Python Social Auth (Django)
- https://python-social-auth.readthedocs.io/en/latest/configuration/django.html#
### 2.1
- settings.py
  - add 'social_django' in the apps section (this will create their own tables)
  - add all other social django settings (SOCIAL_AUTH_PIPELINES)
  - add google/github social settings
- /trainer/urls.py
  - paths for 'social-auth/' - for social third parties login
- /trainer/templates/registration/login.html
  - url buttons - 'social:begin' for 'google-oauth2' and 'github'
- /trainer/views/account_view.py
  - register_social_user
    - this is the social registration for new users via google and github
    - must set is_trainer/groups

## 3. Langchain / Pydantic
### 3.1
- ai_view.py
- define pydantic models (WOrkoutExercise/WorkoutPlan)
- get_prompt
  - specify instructions for llm
  - setup placeholders for data
- generate_workout
  - define llm, set structured_output (use defined pydantic models)
  - pass client info to prompt
  - use _with_structured_out to ensure consistent data type return
  - invoke


## 4. Google App Engine
### 4.1
- setup google account
- create a new app engine instance
  - setup as python environment
- install google cloud cli
- deply with gcloud cli

## 5. Others
### 5.1
- django authentication / authorisation
  - use login_required to wrap secured paths
  - create Groups (Free/Premium) - attach permission can_use_ai
  - permmissions is created togeher in the UserTrainer model
  - ** THERE IS NO PASSWORD RESET **
  - using default django authentication requires
    - urls.py requires path for (login and register)
    - all templates MUST be in templates/trainer/registeration (???)
- base.html controls viewing for different authenticated user levels
    - using views to pass layout down the templates via context
- note the home.html widgets
    - all the queries
- templates/trainer/includes
    - _form_errors.html
      - used in all forms
    - navbar.html
      - used in base.html
        - navigations buttons inside for authenticated users only
    - pagination
      - user in all modules list pages
    - steeper
      - used in base.html   (autheticated users only)
- permission check in templates use perms.can_use_ai
- heavy pages
  -  all list pages pagination logic
  - /templates/trainer/workouts/workout_add.html
        - HTMX
        - javascript / fetch (ajax)
  - /templates/trainer/workouts/workout_edit.html
        - 