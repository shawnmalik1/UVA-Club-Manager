import boto3
from django.contrib.auth.decorators import login_required
from django.forms import models
from django.shortcuts import render, redirect, get_object_or_404

from . import settings
from .models import Profile
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Document, Event
from django.contrib.auth import logout, login
from .models import CheckIn, Club, Event
from a11_project.forms import ClubForm, EventForm
from .models import Suggestion
from .forms import SuggestionForm
from .forms import DocumentForm
from .models import Document
from .models import CheckIn, Club
from a11_project.forms import ClubForm
from django.shortcuts import render, redirect
from .forms import ProjectForm
from .models import Project
from .models import ChatMessage
from .models import UploadedFile
from .models import Budget
from decimal import Decimal
from .models import Expenditure
from .forms import ExpenditureForm
from django.contrib import messages
from django.http import Http404
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render






def home(request):
    if request.user.is_authenticated:
        context = {'name': request.user.username}
        return render(request, "home.html", context)

    return HttpResponseRedirect('/login')

@login_required
def add_club(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ClubForm()
    return render(request, 'add_club.html', {'form': form})


def login_view(request):
    events = Event.objects.all()
    if request.method == 'POST':
        # Handle the login form submission here
        # Assuming Django's built-in login form or custom authentication
        form = ProjectForm()
        if form.is_valid():
            return redirect('dashboard')
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')

    return render(request, "login.html", {'events': events})



@login_required
def dashboard(request):
    if request.user.groups.filter(name='PMA_administrator').exists():
        events = Event.objects.all()
        checked_in_users = CheckIn.objects.all()
        context = {'events': events, 'checked_in_users': checked_in_users}
        return render(request, 'administrator_dashboard.html', context)
    else:
        profile, created = Profile.objects.get_or_create(user=request.user)

        if request.method == 'POST':
            if 'check_in' in request.POST:
                CheckIn.objects.create(user=request.user)
                request.user.profile.points += 10
                request.user.profile.save()
                return redirect('dashboard')

            if 'join_event' in request.POST:
                event_id = request.POST.get('event_id')
                event = get_object_or_404(Event, id=event_id)
                if request.user not in event.members.all():
                    event.member_requests.add(request.user)
                    event.save()
                return redirect('dashboard')

            form = ProjectForm(request.POST, request.FILES)
            if form.is_valid():
                project = form.save(commit=False)
                project.user = request.user
                project.save()
                return redirect('dashboard')
        else:
            form = ProjectForm()

        project = Project.objects.filter(user=request.user).last()
        clubs = Club.objects.all()
        total_points = 0

        for club in clubs:
            if f"club_{club.id}" in request.POST:
                total_points += club.points

        request.user.profile.points += total_points
        request.user.profile.save()

        checked_in = CheckIn.objects.filter(user=request.user).exists()
        events = Event.objects.all().order_by('-date')
        user_join_requests = set(event.id for event in Event.objects.filter(member_requests=request.user))

        return render(request, 'member_dashboard.html', {
            'form': form,
            'project': project,
            'total_points': profile.points,
            'checked_in': checked_in,
            'events': events,
            'user_join_requests': user_join_requests,
            'user_email': request.user.email,
            'user_date_joined': request.user.date_joined
        })



def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

# @login_required
# def check_in(request):
#     if request.method == 'POST':
#         # Create a new check-in entry
#         CheckIn.objects.create(user=request.user)
#         request.user.profile.points += 10
#         request.user.profile.save()
#     return render(request, 'member_dashboard.html')

@login_required()
def delete_club(request, club_id):
    if request.method == 'POST':
        club = get_object_or_404(Club, id=club_id)
        club.delete()
    return HttpResponseRedirect('/dashboard/')

# Calendar view
def calendar(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            if request.user.groups.filter(name='PMA_administrator').exists():
                profile.is_pma_administrator = True
                profile.save()

            if profile.is_pma_administrator:
                return render(request, 'calendar_non_admin.html')
            else:
                return render(request, 'calendar.html')
        except Profile.DoesNotExist:
            pass

    return render(request, 'calendar_anonymous.html')

# View for adding an event
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        description = request.POST.get('description')
        user = request.user

        # Create and save the event
        event = Event.objects.create(title=title, date=date, description=description, user=user)
        event.members.add(user)

        return redirect('calendar')  # Redirect to calendar after adding the event

    return render(request, 'calendar.html')  # Render calendar template for GET request



def get_events(request):
    events = Event.objects.all().values('id', 'title', 'date', 'description', 'user')
    return JsonResponse(list(events), safe=False)

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Club.objects.filter(event=event).delete()
    event.delete()

    return redirect('view_events')  # Redirect back to calendar after deletion

def delete_event_PMA(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Club.objects.filter(event=event).delete()
    event.delete()

    return redirect('dashboard')  # Redirect back to calendar after deletion

@login_required
def non_admin_main_page(request):
    return render(request, 'non_admin_main.html')

def suggestion_box(request):
    suggestions = Suggestion.objects.all()
    form = SuggestionForm()
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            if request.user.groups.filter(name='PMA_administrator').exists():
                profile.is_pma_administrator = True
                profile.save()

            if profile.is_pma_administrator:
                suggestions = Suggestion.objects.all()
                return render(request, 'suggestion_list.html', {'suggestions': suggestions})

            else:
                form = SuggestionForm()
                if request.method == 'POST':
                    form = SuggestionForm(request.POST)
                    if form.is_valid():
                        suggestion = form.save(commit=False)
                        suggestion.user = request.user
                        suggestion.save()
                        return redirect('suggestion_box')

                return render(request, 'suggestion_box.html', {'form': form, 'suggestions': suggestions})

        except Profile.DoesNotExist:
            pass

    return render(request, 'suggestion_box.html', {'form': form, 'suggestions': suggestions})


def filter_files_by_keywords(files, keywords):
    # Split keywords by commas and strip extra spaces
    keywords = [kw.strip().lower() for kw in keywords.split(",") if kw.strip()]

    filtered_files = [
        file for file in files
        if any(keyword in file['keywords'].lower() for keyword in keywords)
    ]

    return filtered_files
def file_list(request):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    bucket_name = 'project-a11-storage'

    documents = Document.objects.all()

    # Fetch files from S3 bucket
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix='projects/')
    s3_files = response.get('Contents', [])

    file_data = []
    processed_doc_ids = set()  # Track processed documents

    for s3_file in s3_files:
        s3_key = s3_file['Key'].replace('projects/', '', 1)

        # Match Document object
        matching_doc = next(
            (doc for doc in documents if doc.file.name.endswith(s3_key)),
            None
        )

        # Add file data if a match is found and not already processed
        if matching_doc and matching_doc.id not in processed_doc_ids:
            file_data.append({
                'id': matching_doc.id,  # Ensure ID is included
                'name': matching_doc.file.name.split('/')[-1],
                'title': matching_doc.title,
                'description': matching_doc.description,
                'keywords': matching_doc.keywords,
                'timestamp': matching_doc.timestamp,
                'url': f"https://{bucket_name}.s3.amazonaws.com/{s3_file['Key']}"
            })
            processed_doc_ids.add(matching_doc.id)  # Mark as processed
        else:
            if not matching_doc:
                logger.warning(f"No matching document found for S3 key: {s3_key}")

    # Handle search filter
    search_keywords = request.GET.get('search')
    if search_keywords:
        file_data = filter_files_by_keywords(file_data, search_keywords)

    logger.debug(f"File data being passed to the template: {file_data}")
    return render(request, 'file_list.html', {'files': file_data})


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'project_form.html', {'form': form})

#views chat
def chat_room(request):
    #messages = ChatMessage.objects.filter(room_name=room_name).order_by('timestamp')
    return render(request, 'chat_room.html',{
        #'room_name': room_name,
        #'messages': messages,
    })


@login_required
def add_expenditure(request):
        # Query current total budget
        budget = Budget.objects.first()  # Assuming only one budget exists

        if request.method == 'POST':
            form = ExpenditureForm(request.POST)
            if form.is_valid():
                # Check if the expenditure amount is less than or equal to the available budget
                expenditure_amount = form.cleaned_data['amount']
                if budget and expenditure_amount <= budget.total_budget:
                    # Save the expenditure and associate the user
                    expenditure = form.save(commit=False)
                    expenditure.user = request.user  # Associate the logged-in user with the expenditure
                    expenditure.save()  # Save the expenditure

                    # Update the total budget after the expenditure
                    budget.total_budget -= expenditure_amount
                    budget.save()

                else:
                    # If the expenditure is more than the available budget, show an error
                    error_message = "Expenditure exceeds the available budget!"
                    return render(request, 'add_expenditure.html', {'form': form, 'budget': budget, 'error': error_message})
        else:
            form = ExpenditureForm()

        expenditures = Expenditure.objects.all().order_by('-submitted_at')
        # Pass the form and budget to the template
        return render(request, 'add_expenditure.html', {
            'form': form,
            'budget': budget,
            'expenditures': expenditures
        })


@login_required
def add_to_budget(request):
    if request.method == 'POST':
        try:
            add_amount = Decimal(request.POST.get('add_amount', '0'))
            budget = Budget.get_instance()
            budget.total_budget += add_amount
            budget.save()
            return redirect('add_expenditure')
        except Exception as e:
            return render(request, 'add_expenditure.html', {
                'error': f"An error occurred: {e}",
                'budget': Budget.get_instance(),
                'form': ExpenditureForm(),
                'expenditures': Expenditure.objects.all()
            })

@login_required
def expenditure_list(request):
    budget = Budget.objects.first()
    if budget:
        total_amount = budget.total_budget
    else:
        total_amount = 0
    expenditures = Expenditure.objects.all().order_by('-submitted_at')  # Get all expenditures ordered by date
    return render(request, 'expenditure_list.html', {'expenditures': expenditures, 'total_amount': total_amount})


@login_required
def view_tasks(request, event_id):
    clubs = Club.objects.all()  # Get all clubs
    total_points = 0  # Initialize total points

    if request.method == "POST":
        # Loop through clubs to check which tasks are completed
        for club in clubs:
            if f"club_{club.id}" in request.POST:  # If the task is checked
                total_points += club.points  # Add the points of the checked club/task

        # Add the total points to the current user's points
        request.user.profile.points += total_points  # Assuming `profile` exists
        request.user.profile.save()  # Save the updated points to the user profile

        return redirect('dashboard')  # Redirect to the dashboard after updating points

    return render(request, 'view_tasks.html', {'clubs': clubs})

@login_required
def submit_tasks(request, event_id):

    if request.method == 'POST':
        completed_task_ids = request.POST.getlist('completed_tasks')
        event = get_object_or_404(Event, id=event_id)
        profile = get_object_or_404(Profile, user=request.user)

        total_points_added = 0

        for task_id in completed_task_ids:
            try:
                # Get the task and its points
                task = Club.objects.get(id=task_id, event=event)
                total_points_added += task.points

                # Delete the task
                task.delete()
            except Club.DoesNotExist:
                continue

        # Update the user's profile points
        profile.points += total_points_added
        profile.save()

        messages.success(request, f"Successfully completed tasks! Added {total_points_added} points to your profile.")
        return redirect('dashboard')

    return redirect('dashboard')

@login_required
def leave_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user in event.members.all():
        event.members.remove(request.user)
    return redirect('view_events')

def view_events(request):
    events = Event.objects.all().order_by('-date')
    users_events = Event.objects.filter(user=request.user).order_by('-date')
    joined_events = Event.objects.filter(members=request.user).order_by('-date')

    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        form = ClubForm(request.POST)
        if form.is_valid():
            club = form.save(commit=False)
            club.event = event

            form.save()
            return redirect('view_events')
    else:
        form = ClubForm()
    return render(request, 'view_tasks.html', {'events': events, 'form': form, 'users_events': users_events, 'joined_events':joined_events})


@login_required
def upload_file(request, event_id):
    # Get the specific event based on the provided event_id
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.event = event  # Associate the uploaded file with the event
            document.save()

            # Redirect to the event page after successful upload
            return redirect('view_events')  # This will redirect back to the 'view_events' page
        else:
            # If the form is invalid, render the page with errors
            return render(request, 'view_tasks.html', {
                'form': form,
                'event': event,
                'documents': Document.objects.filter(event=event),
                'errors': form.errors,
            })
    else:
        # For GET requests, initialize an empty form
        form = DocumentForm()

    # Render the page with the form and existing documents
    return render(request, 'view_tasks.html', {
        'form': form,
        'event': event,
        'documents': Document.objects.filter(event=event),
    })


@login_required
def accept_member(request, event_id, user_id):
    event = get_object_or_404(Event, id=event_id)
    user_to_approve = get_object_or_404(User, id=user_id)

    event.member_requests.remove(user_to_approve)
    event.members.add(user_to_approve)
    messages.success(request, f"{user_to_approve.username} has been added to the event.")

    return redirect('view_events')

@login_required
def reject_member(request, event_id, user_id):
    event = get_object_or_404(Event, id=event_id)
    user_to_reject = get_object_or_404(User, id=user_id)
    event.member_requests.remove(user_to_reject)
    messages.success(request, f"{user_to_reject.username} has been removed from the join requests.")

    return redirect('view_events')


@login_required
def delete_file_task_view(request, file_id, event_id):
    event = get_object_or_404(Event, id=event_id)
    events = Event.objects.all().order_by('-date')
    users_events = Event.objects.filter(user=request.user).order_by('-date')
    joined_events = Event.objects.filter(members=request.user).order_by('-date')

    try:
        file = get_object_or_404(Document, id=file_id) 
        if request.method == "POST":
            if file.file:  
                file.file.delete()  
            file.delete() 
            messages.success(request, "File deleted successfully!")
            return render(request, 'view_tasks.html', {
                'events': events,
                'joined_events': joined_events,
                'users_events': users_events,
                'event': event,
            })
        else:
            raise Http404("Invalid request method for deleting a file.")
    except Document.DoesNotExist:
        messages.error(request, "File not found or already deleted.")
        return redirect('file_list')
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        messages.error(request, f"Error deleting file: {e}")
        return render(request, 'view_tasks.html', {
            'events': events,
            'joined_events': joined_events,
            'users_events': users_events,
            'event': event,
        })

def delete_file(request, file_id):
    try:
        file = get_object_or_404(Document, id=file_id)
        if request.method == "POST":
            if file.file:
                file.file.delete()
            file.delete()
            messages.success(request, "File deleted successfully!")
            return redirect('file_list')
        else:
            raise Http404("Invalid request method for deleting a file.")
    except Document.DoesNotExist:
        messages.error(request, "File not found or already deleted.")
        return redirect('file_list')
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        messages.error(request, f"Error deleting file: {e}")
        return redirect('file_list')

