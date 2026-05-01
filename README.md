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


13. Handing deleting inline formset rows
    Query: Ok, I have a django inlineform set for an ADD form using client side script to add new row, i need to add a delete row option. use a delete button in each row to call a delete function (mark to row visibility only)

    Answer (ChatGPT):
    
    You’re on the right track—what you want is exactly how Django formsets are meant to handle deletion: **don’t remove the row, just mark it for deletion and hide it**.

    Here’s the clean, reliable pattern for an **inline formset (ADD + DELETE via JS)**.

    ---

    # ✅ 1. Enable deletion in your formset

    In your view:

    ```python
    formset = inlineformset_factory(
        ParentModel,
        ChildModel,
        fields=[...],
        extra=1,
        can_delete=True
    )
    ```

    ---

    # ✅ 2. Include the DELETE field in your template

    Inside each form row (including your `empty_form` template), add:

    ```html
    {{ form.DELETE }}
    ```

    You can hide it:

    ```html
    <div class="d-none">
        {{ form.DELETE }}
    </div>
    ```

    👉 This field is what Django reads to actually delete the object.

    ---

    # ✅ 3. Update your empty form template

    Make sure your template includes the DELETE field:

    ```html
    <div id="empty-form-template" class="d-none">
        <div class="formset-row ...">

            {{ formset.empty_form.DELETE }}

            ...
            <button type="button" class="remove-row btn btn-sm text-danger">
                Remove
            </button>
        </div>
    </div>
    ```

    ---

    # ✅ 4. JavaScript: mark + hide (NOT remove)

    Use **event delegation** so it works for dynamically added rows:

    ```javascript
    formsetContainerElement.addEventListener('click', function (e) {
        const btn = e.target.closest('.remove-row');
        if (!btn) return;

        const row = btn.closest('.formset-row');

        const deleteInput = row.querySelector('input[name$="-DELETE"]');

        if (deleteInput) {
            // Existing or properly structured form
            deleteInput.checked = true;
            row.style.display = 'none';
        }
    });
    ```

    ---

    # ⚠️ Important rules (this is where most bugs happen)

    ### ❌ DO NOT:

    * Remove the row from DOM
    * Decrease `TOTAL_FORMS`
    * Reindex forms

    ### ✅ DO:

    * Keep the row in DOM
    * Set `DELETE = true`
    * Hide it visually

    ---

    # 🧠 Special case: newly added rows

    For rows created from `empty_form`:

    * They also have a `DELETE` field
    * Marking DELETE = true means Django will **ignore them entirely**

    So the same logic works for both:

    * existing DB rows
    * newly added rows

    ---

    # 💡 Optional UX improvement

    Instead of fully hiding, you can “soft delete”:

    ```javascript
    row.classList.add('opacity-50');
    row.querySelectorAll('input, select').forEach(el => el.disabled = true);
    ```

    But still:

    ```javascript
    deleteInput.checked = true;
    ```

    ---

    # ✅ Final mental model

| Action     | What happens                         |
| ---------- | ------------------------------------ |
| Add row    | increase `TOTAL_FORMS`               |
| Delete row | mark `DELETE = true`, hide           |
| Submit     | Django processes deletions correctly |

---

If you want next step: I can help you add an **“undo delete” button** or integrate this cleanly with HTMX so rows can be server-rendered instead of cloned.


Social Login
=============================================================================================
REFERENCES:
    --- https://python-social-auth.readthedocs.io/en/latest/configuration/django.html
    --- https://medium.com/@kennethjiang/python-social-auth-for-django-tutorial-16bbe792659f