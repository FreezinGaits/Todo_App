from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Task

# Create your views here.
def addTask(request):
  # print(request.POST) # <QueryDict: {'csrfmiddlewaretoken': ['ohqmCT47B3kSLr7E9UdWmZLJ7m4wGl7LCMjiCzJsHXMUWVrWqzhN7naZh2bOn9sT'], 'task': ['Hey boi!']}>, task is input field name attribute
  # print(request.POST['task']) # Hey boi!
  task = request.POST['task']
  Task.objects.create(task = task)
  return redirect('home')
  # return HttpResponse('The form is submitted')

def mark_as_done(request, pk):
  task = get_object_or_404(Task, pk = pk) # pk: field name of task model, pk is passed from url dynamically
  task.is_completed = True
  task.save()
  return redirect('home')
  # return HttpResponse(task) # or pk

def mark_as_undone(request, pk):
  task = get_object_or_404(Task, pk = pk) # pk: field name of task model, pk is passed from url dynamically
  task.is_completed = False
  task.save()
  return redirect('home')

def editTask(request, pk):
  get_task = get_object_or_404(Task, pk = pk)
  if request.method == 'POST':
    new_task = request.POST['task']
    get_task.task = new_task
    get_task.save()
    return redirect('home')
  else:
    context = {
      'get_task': get_task,
    }
    return render(request, 'edit_task.html', context)
  
def deleteTask(request, pk):
  task = get_object_or_404(Task, pk = pk)
  task.delete()
  return redirect('home')


#   The primary thing the `redirect('home')` line is doing is implementing the **Post/Redirect/Get (PRG)** pattern. It ensures that after the task is successfully added via a `POST` request, the user's browser is sent a command to navigate to a new, different page via a `GET` request.

# Here's a detailed explanation of what `redirect('home')` does in your `addTask` function:

# -----

# ## What `redirect('home')` Does

# 1.  **Stops `POST` processing:** After the line `Task.objects.create(task = task)` successfully saves the data to the database, the view immediately executes the redirect.
# 2.  **Sends a 302 Response:** Django sends an **HTTP 302 Found** response back to the user's browser. This response includes a `Location` header that contains the URL resolved from the view name `'home'`.
# 3.  **Browser Navigates:** The browser receives the 302 response and, instead of displaying the result of the `addTask` function, it immediately makes a new **HTTP `GET` request** to the URL specified in the `Location` header (which is the URL associated with the `'home'` view).
# 4.  **Final Page Load:** The browser loads the content returned by the `home` view.

# -----

# ## Why It's Necessary (The PRG Pattern)

# Yes, in a way, it makes sure you "stay" on the home page (or, more accurately, return to a non-form page) after a successful form submission, but the key reason is to **prevent duplicate form submissions**.

# If you had used the commented-out line:

# ```python
# # return HttpResponse('The form is submitted')
# ```

# ...and the user hit the **Refresh** button on that page, the browser would re-submit the original `POST` data, resulting in a duplicate task being created in your database (e.g., two "Hey boi\!" tasks).

# By using `return redirect('home')`:

#   * The initial `POST` request is handled, and the task is saved.
#   * The redirect forces the browser to make a subsequent, harmless **`GET` request** to the home page.
#   * Now, if the user hits **Refresh**, the browser simply repeats the last (safe) **`GET` request**, and no duplicate task is created. This is the core benefit of the **Post/Redirect/Get** pattern.