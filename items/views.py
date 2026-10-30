from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ItemReportForm
from .models import ItemReport


class FindItLoginView(LoginView):
    template_name = 'items/login.html'
    redirect_authenticated_user = True


@login_required
def dashboard(request):
    reports = ItemReport.objects.select_related('owner').all()
    return render(request, 'items/dashboard.html', {'reports': reports})


@login_required
def report_item(request):
    if request.method == 'POST':
        form = ItemReportForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, 'Report saved.')
            return redirect('dashboard')
    else:
        form = ItemReportForm()

    return render(request, 'items/report.html', {'form': form})


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(ItemReport, id=item_id, owner=request.user)
    if request.method == 'POST':
        form = ItemReportForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report updated.')
            return redirect('dashboard')
    else:
        form = ItemReportForm(instance=item)

    return render(request, 'items/edit.html', {'form': form, 'item': item})


@login_required
@require_POST
def delete_item(request, item_id):
    item = get_object_or_404(ItemReport, id=item_id, owner=request.user)
    item.delete()
    messages.success(request, 'Report deleted.')
    return redirect('dashboard')


@require_POST
def logout_user(request):
    logout(request)
    return redirect('login')
