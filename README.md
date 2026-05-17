Cloud Deployment URL (Google App Engine): https://uq-train-forge.as.r.appspot.com
Database Hosting Service: Aiven - DAAS : https://aiven.io/
Admin Login Details:    - (Username): admin
                        - (Password): 12345678!
User Login Details:     - (Username): aaa@gmail.com
                        - (Password): 123123123

Directory Structure:
uq-train-forge/
-- config/
-- orm/
-- static/
-- trainer/
---- forms/
---- templates/
---- views/
---- urls.py

[ AI Usage Statements ]
1.  { Query }:

    Ok, I have a django inlineform set for an ADD form using client side script to add new row, i need to add a delete row option. use a delete button in each row to call a delete function (mark to row visibility only)

    { Answer (ChatGPT) }:
    
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

--------------------------------

2. { Query }:

    any_done = WorkoutExercise.objects.filter(
        workout=OuterRef('pk'),
        is_done=True
    )

    workouts = workouts.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True)),
        not_started=Count(
            'id', 
            filter=Q(is_completed=False) & ~Exists(any_done)
        ),
        in_progress= Count('id',
            filter=Q(is_completed=False) & ~Exists(any_done)
        )
    )

    Now, if I instead want in_progress to be the count of any workout that has is_completed set to False, but with >=1 or even all of its Workout_Exercise entities' is_done property set to True, what is the syntax to find that?

    To capture workouts that have actually been started but aren't finished yet, you can leverage the same `Exists` logic but remove the negation (`~`).

    If a workout is not completed, but **at least one** exercise is done, it is semantically "In Progress."

    ### The Updated Query

    ```python
    from django.db.models import Count, Q, Exists, OuterRef

    # Subquery: Checks if there is AT LEAST ONE exercise marked as done
    any_done = WorkoutExercise.objects.filter(
        workout=OuterRef('pk'),
        is_done=True
    )

    stats = workouts.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True)),
        # Case 1: Not finished AND not a single exercise done
        not_started=Count(
            'id', 
            filter=Q(is_completed=False) & ~Exists(any_done)
        ),
        # Case 2: Not finished AND at least one exercise is done
        in_progress=Count(
            'id', 
            filter=Q(is_completed=False) & Exists(any_done)
        )
    )
    ```

    ### Breakdown of the Logic

    *   **`Exists(any_done)`**: This translates to a SQL `EXISTS` clause. It returns `True` the moment the database finds the very first `WorkoutExercise` related to that workout where `is_done=True`.
    *   **The "At Least One" Rule**: By using `Exists` without the tilde (`~`), you are specifically targeting workouts that have initiated progress.
    *   **The "All Exercises Done" Scenario**: If a workout has **all** exercises done but `is_completed` is still `False`, it will still fall into `in_progress` with the logic above. 

    ---

    ### Refined Logic: "In Progress" vs "Needs Review"
    If you want to be extremely specific and differentiate between "Started" and "Everything finished but not officially closed," you can use `annotate` before the aggregate to count the discrepancies:

    ```python
    from django.db.models import F

    stats = workouts.annotate(
        done_count=Count('exercises', filter=Q(exercises__is_done=True)),
        total_exercises=Count('exercises')
    ).aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True)),
        # In progress: Started, but at least one exercise is still pending
        in_progress=Count(
            'id',
            filter=Q(is_completed=False, done_count__gt=0, done_count__lt=F('total_exercises'))
        ),
        # Fully finished exercises, but the Workout toggle is still False
        needs_closure=Count(
            'id',
            filter=Q(is_completed=False, done_count=F('total_exercises'), total_exercises__gt=0)
        )
    )
    ```

    ### Performance Tip
    Using `Exists` (as shown in the first example) is generally significantly faster than comparing `Count` values. Databases are very efficient at checking if "at least one" row exists, whereas a `Count` forces the database to scan every single related exercise record to get an exact sum before it can finish the calculation.


--------------------------------

3. { Query }:

class Workout(models.Model):
    trainer = models.ForeignKey(
        Trainer,
        on_delete = models.PROTECT,     # cannot delete trainer if workouts still exists
        related_name = 'workouts'
    )

    client = models.ForeignKey(
        Client,
        on_delete = models.PROTECT,     # cannot delete client if workouts still exists
        related_name = "workouts"
    )
    is_completed = models.BooleanField(default=False)

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name="exercises"
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete = models.RESTRICT,
        related_name = 'workout_exercises'
    )

    workouts = Workout.objects.filter(trainer=userTrainer)

    workouts = workouts.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True)),
        pending=Count('id', filter=Q(is_completed=False) and Q(workout_exercises__is_done=0))
    )

In a Django project using ORM models, in the second half of the "pending" aggregate property, if I want to find the number of workout_exercise entities that have is_done = 0, then compare that with the total number of workout_exercise entities for the same workout, what is the proper syntax to find that?

    { Answer (Gemini) }:

    To achieve this, you need to compare two different counts within the same row's context. In Django, this is typically handled by using `ExpressionWrapper` or `Case/When` logic to determine if a condition is met across the relationship, and then counting those results.

    Since you want to find workouts where **all** associated exercises are not done (or where the count of "not done" equals the "total" count), you can use the following approach.

    ### The Refined Query
    You can use `Count` with a filter that checks if the number of incomplete exercises matches the total number of exercises for that workout.

    ```python
    from django.db.models import Count, Q, F

    workouts = Workout.objects.filter(trainer=userTrainer).annotate(
        # 1. Count total exercises in this workout
        total_ex=Count('exercises'),
        # 2. Count only those that are NOT done
        incomplete_ex=Count('exercises', filter=Q(exercises__is_done=False))
    ).aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True)),
        # 3. Pending is where is_completed is False AND all exercises are incomplete
        pending=Count(
            'id', 
            filter=Q(is_completed=False, total_ex=F('incomplete_ex'), total_ex__gt=0)
        )
    )
    ```

    ---

    ### Why this works
    *   **`.annotate()`:** We first calculate the exercise stats for every individual workout. This allows us to compare `total_ex` against `incomplete_ex` on a per-row basis.
    *   **`F('incomplete_ex')`:** This allows us to compare the value of one column/annotation to another. If they are equal, it means no exercises have been finished yet.
    *   **`total_ex__gt=0`:** This is a safety check. A workout with zero exercises would technically have "all" of its exercises incomplete (0 == 0), which might give you a false positive for a "pending" workout.

    ---

    ### Alternative: Using `Subqueries` or `Exists`
    If you specifically want to find workouts where **not a single exercise** has been started, using `~Exists` is often more performant than counting every related row:

    ```python
    from django.db.models import Exists, OuterRef

    # Subquery to find if ANY exercise in a workout is done
    any_done = WorkoutExercise.objects.filter(
        workout=OuterRef('pk'),
        is_done=True
    )

    workouts = Workout.objects.filter(trainer=userTrainer).aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True)),
        pending=Count(
            'id', 
            filter=Q(is_completed=False) & ~Exists(any_done)
        )
    )
    ```

    ### Key Logic Difference
    *   **The Count Method:** Best if you need to know *how many* exercises are left.
    *   **The Exists Method:** Best for a boolean "has anything started?" check. It is generally faster on large datasets because the database stops looking as soon as it finds one finished exercise.

    > **Note:** Ensure your `WorkoutExercise` model actually has the `is_done` field defined as a `BooleanField` or `IntegerField`, as it wasn't explicitly in your snippet but was referenced in your query logic.

--------------------------------

4. { Query }:

workouts = workouts.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True)),
        not_started=Count(
            'id', 
            filter=Q(is_completed=False) & ~Exists(any_done)
        ),
        in_progress= ...,
    )

If I want to add another "in_progress" aggregate, and for testing purposes just want it to be the difference between the total number of workouts and the number of completed and pending workouts, what is the syntax to do so?

    { Answer (Gemini) }:

    In Django's `aggregate()` method, you cannot reference the names of other keys you just defined (like `completed` or `not_started`) within the same dictionary. The database calculates these values simultaneously, so "total" isn't available to subtract from until the query is finished.

    To perform math on these results, you have two main options:

    ### Option 1: Use `ExpressionWrapper` with `F` expressions
    You can use `F()` to reference the calculated values and wrap them in an `ExpressionWrapper` to define the output type. However, for a single `aggregate()` call, this can get a bit verbose because you have to define the logic explicitly.

    ```python
    from django.db.models import Count, Q, Exists, OuterRef, F, IntegerField

    any_done = WorkoutExercise.objects.filter(workout=OuterRef('pk'), is_done=True)

    stats = Workout.objects.filter(trainer=userTrainer).aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True)),
        not_started=Count('id', filter=Q(is_completed=False) & ~Exists(any_done)),
        # Use F expressions to subtract the other counts from the total count
        in_progress=Count('id') - (
            Count('id', filter=Q(is_completed=True)) + 
            Count('id', filter=Q(is_completed=False) & ~Exists(any_done))
        )
    )
    ```

    ### Option 2: Post-Processing in Python (Recommended)
    Since `aggregate()` returns a standard Python dictionary, the cleanest and most performant way to handle "testing" logic or simple arithmetic is to calculate it in Python immediately after the query. This avoids making the SQL query unnecessarily complex.

    ```python
    stats = Workout.objects.filter(trainer=userTrainer).aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True)),
        not_started=Count('id', filter=Q(is_completed=False) & ~Exists(any_done)),
    )

    # Calculate the difference in Python
    stats['in_progress'] = stats['total'] - (stats['completed'] + stats['not_started'])
    ```

    ### Option 3: The Semantic SQL approach
    If you eventually want `in_progress` to be based on actual exercise logic (e.g., "at least one exercise is done, but the workout isn't finished"), the syntax looks like this:

    ```python
    in_progress=Count(
        'id', 
        filter=Q(is_completed=False) & Exists(any_done)
    )
    ```

    **Note on syntax:** I used `stats` as the variable name instead of `workouts` because `aggregate()` returns a **dictionary** (e.g., `{'total': 10, ...}`), not a QuerySet. If you try to call more ORM methods on it later, it will throw an error!

--------------------------------

5. { Query }:

    any_done = WorkoutExercise.objects.filter(
        workout=OuterRef('pk'),
        is_done=True
    )

    workouts = workouts.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True)),
        not_started=Count(
            'id', 
            filter=Q(is_completed=False) & ~Exists(any_done)
        ),
        in_progress= Count('id',
            filter=Q(is_completed=False) & ~Exists(any_done)
        )
    )

Now, if I instead want in_progress to be the count of any workout that has is_completed set to False, but with >=1 or even all of its Workout_Exercise entities' is_done property set to True, what is the syntax to find that?

    { Answer (Gemini) }:

    To capture workouts that have actually been started but aren't finished yet, you can leverage the same `Exists` logic but remove the negation (`~`).

    If a workout is not completed, but **at least one** exercise is done, it is semantically "In Progress."

    ### The Updated Query

    ```python
    from django.db.models import Count, Q, Exists, OuterRef

    # Subquery: Checks if there is AT LEAST ONE exercise marked as done
    any_done = WorkoutExercise.objects.filter(
        workout=OuterRef('pk'),
        is_done=True
    )

    stats = workouts.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True)),
        # Case 1: Not finished AND not a single exercise done
        not_started=Count(
            'id', 
            filter=Q(is_completed=False) & ~Exists(any_done)
        ),
        # Case 2: Not finished AND at least one exercise is done
        in_progress=Count(
            'id', 
            filter=Q(is_completed=False) & Exists(any_done)
        )
    )
    ```

    ### Breakdown of the Logic

    *   **`Exists(any_done)`**: This translates to a SQL `EXISTS` clause. It returns `True` the moment the database finds the very first `WorkoutExercise` related to that workout where `is_done=True`.
    *   **The "At Least One" Rule**: By using `Exists` without the tilde (`~`), you are specifically targeting workouts that have initiated progress.
    *   **The "All Exercises Done" Scenario**: If a workout has **all** exercises done but `is_completed` is still `False`, it will still fall into `in_progress` with the logic above. 

    ---

    ### Refined Logic: "In Progress" vs "Needs Review"
    If you want to be extremely specific and differentiate between "Started" and "Everything finished but not officially closed," you can use `annotate` before the aggregate to count the discrepancies:

    ```python
    from django.db.models import F

    stats = workouts.annotate(
        done_count=Count('exercises', filter=Q(exercises__is_done=True)),
        total_exercises=Count('exercises')
    ).aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True)),
        # In progress: Started, but at least one exercise is still pending
        in_progress=Count(
            'id',
            filter=Q(is_completed=False, done_count__gt=0, done_count__lt=F('total_exercises'))
        ),
        # Fully finished exercises, but the Workout toggle is still False
        needs_closure=Count(
            'id',
            filter=Q(is_completed=False, done_count=F('total_exercises'), total_exercises__gt=0)
        )
    )
    ```

    ### Performance Tip
    Using `Exists` (as shown in the first example) is generally significantly faster than comparing `Count` values. Databases are very efficient at checking if "at least one" row exists, whereas a `Count` forces the database to scan every single related exercise record to get an exact sum before it can finish the calculation.

--------------------------------

6. { Query }: 

    <div class="progress" id="progress-bar" style="display: none;">
        <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div>
    </div>

    <div id="pending-workouts-display" hx-indicator="#progress-bar" hx-get="{% url 'get_pending_workouts' %}" hx-trigger="load" hx-target="this">
    </div>

The progress bar isn't showing when the HTMX hasn't finished loading in. Is it possible to fix this?

    { Answer (Gemini) }:

    Yes. The issue is that your progress bar starts with:

    ```html
    style="display: none;"
    ```

    HTMX indicators work by automatically toggling the `htmx-request` class on the indicator element during the request, but HTMX does **not** automatically override an inline `display: none`.

    So the element stays hidden even while the request is active.

    A common fix is to hide the indicator using CSS instead of inline styles.

    ```html
    <style>
        .htmx-indicator {
            display: none;
        }

        .htmx-request.htmx-indicator {
            display: block;
        }
    </style>

    <div class="progress htmx-indicator" id="progress-bar">
        <div class="progress-bar progress-bar-striped progress-bar-animated"
            role="progressbar"
            aria-valuenow="100"
            aria-valuemin="0"
            aria-valuemax="100"
            style="width: 100%">
        </div>
    </div>

    <div id="pending-workouts-display"
        hx-indicator="#progress-bar"
        hx-get="{% url 'get_pending_workouts' %}"
        hx-trigger="load"
        hx-target="this">
    </div>
    ```

    How this works:

    * `.htmx-indicator` → hidden normally
    * During the request, HTMX adds `htmx-request`
    * The selector `.htmx-request.htmx-indicator` becomes active
    * The progress bar becomes visible automatically

    This is the pattern recommended by [HTMX indicator documentation](https://htmx.org/attributes/hx-indicator/?utm_source=chatgpt.com).


--------------------------------

7. { Query }: 

    <div class="progress htmx-indicator" id="progress-bar">
        <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div>
    </div>

    <div id="pending-workouts-display" hx-indicator="#progress-bar" hx-get="{% url 'get_pending_workouts' %}" hx-trigger="load" hx-target="this">
    </div>

    Now the loading bar appears when loading, but the Bootstrap 5 styles don't work and it has no colour.

    { Answer (ChatGPT) }:

    The Bootstrap 5 .progress and .progress-bar classes are failing because htmx's default .htmx-indicator CSS uses opacity: 0. In many browsers, an element with zero opacity loses certain rendering properties, or the Bootstrap styles are being overridden by how htmx toggles visibility.
    ## The Fix: Use Display Instead of Opacity
    Bootstrap 5 components often rely on display: flex. Instead of using the built-in htmx opacity toggle, use custom CSS to switch between none and flex.
    1. Update your CSS
    Add this to your stylesheet to ensure the bar maintains its Bootstrap layout:

    /* Hide by default */
    #progress-bar {
        display: none;
    }
    /* Show as flex when htmx is requesting */
    .htmx-request#progress-bar,
    .htmx-request #progress-bar {
        display: flex;
    }

    2. Update your HTML
    Remove the .htmx-indicator class from the div, as we are now handling the visibility manually via the ID and the .htmx-request class htmx provides.

    <div class="progress" id="progress-bar">
        <div class="progress-bar progress-bar-striped progress-bar-animated" 
            role="progressbar" 
            style="width: 100%">
        </div>
    </div>

    <div id="pending-workouts-display" 
        hx-indicator="#progress-bar" 
        hx-get="{% url 'get_pending_workouts' %}" 
        hx-trigger="load" 
        hx-target="this">
    </div>

    ------------------------------
    ## Why this happens

    * Opacity vs. Display: The standard .htmx-indicator class only changes opacity.
    * Bootstrap Conflict: Bootstrap's .progress class requires display: flex to render the inner bar and background color correctly.
    * The "Invisible" State: When htmx adds the .htmx-request class to your indicator, it sets opacity: 1, but if the base .htmx-indicator class was interfering with Bootstrap's flexbox logic, the bar appears "broken" or colorless.

    ## Pro Tip: Smooth Transitions
    If you want the bar to fade in rather than pop in, use visibility and opacity together in your CSS:

    #progress-bar {
        opacity: 0;
        transition: opacity 200ms ease-in;
    }

    .htmx-request#progress-bar {
        opacity: 1;
    }

    To help me debug further, tell me:

    * Is the bar completely invisible or just grey/white?
    * Are you using a custom Bootstrap theme?
    * Is the bar inside another container that has overflow: hidden?


--------------------------------

8. { Query }: 

    What is the proper syntax to create Django display inline formset field errors?

    { Answer (Gemini) }:

    In Django, handling errors for **Inline Formsets** can be a bit tricky because you have to manage errors at three different levels: the **Management Form**, the **individual forms** within the set, and the **non-form errors** (errors that apply to the collection as a whole).

    To display these errors properly in your template, you should follow this structural pattern:

    ### 1. Non-Form Errors

    These are errors that aren't specific to a single field or even a single row (e.g., "You must have at least two related items").

    ```html
    {{ formset.non_form_errors }}

    ```

    ### 2. Form-Specific Errors

    Since an inline formset is a collection of forms, you need to loop through them. Each form has its own `non_field_errors` and individual field errors.

    ```html
    <form method="post">
        {% csrf_token %}
        {{ formset.management_form }}

        {% for form in formset %}
            <div class="form-row">
                {% if form.instance.pk %}{{ form.DELETE }}{% endif %}
                {{ form.id }}
                
                {# 1. Display non-field errors for this specific row #}
                {{ form.non_field_errors }}

                {% for field in form.visible_fields %}
                    <div class="field-container">
                        {{ field.label_tag }} 
                        {{ field }}
                        
                        {# 2. Display specific field errors #}
                        {% if field.errors %}
                            <ul class="errorlist">
                                {% for error in field.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                {% endfor %}
            </div>
            <hr>
        {% endfor %}
        
        <button type="submit">Save</button>
    </form>

    ```

    ---

    ### Key Components to Remember

    * **`{{ formset.management_form }}`**: **CRITICAL.** If you omit this, Django will throw a `ValidationError` because it won't know how many forms were sent back to the server.
    * **`{{ form.id }}`**: Always include the hidden ID field for inline forms so Django knows which existing records are being updated versus which are new.
    * **CSS Classes**: Django's default error list uses the class `.errorlist`. You can style this in your CSS to make the errors stand out (usually `color: red;`).

    ### Handling Errors in the View

    In your `views.py`, ensure you are actually checking the validity of the formset before attempting to save.

    ```python
    if request.method == 'POST':
        formset = MyInlineFormSet(request.POST, instance=parent_instance)
        if formset.is_valid():
            formset.save()
            return redirect('success_url')
        # If not valid, the formset (with errors) is passed back to the template context
    else:
        formset = MyInlineFormSet(instance=parent_instance)

    ```

    > **Tip:** If you are using a front-end framework like Bootstrap, you might want to manually check `{% if field.errors %}` to add a class like `is-invalid` directly to the widget attributes.

--------------------------------

9. { Query }: 



    { Answer (Gemini) }:

--------------------------------

10. { Query }: 



    { Answer (Gemini) }:

--------------------------------