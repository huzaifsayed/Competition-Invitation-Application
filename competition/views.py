from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, View
from .forms import CompetitionForm
from .models import CompetitionUser, CompetitionInvite
from django.db.models import Count
from django.contrib import messages
from django.core.mail import send_mail

class CompetitionView(TemplateView):
    form = CompetitionForm
    template_name = 'competition.html'

    def post(self, request, *args, **kwargs):
        form = CompetitionForm(request.POST)
        if form.is_valid():
            obj = form.save()
            if 'invite_user_slug' in request.session:
                from_invite = CompetitionUser.objects.get(slug=request.session.get('invite_user_slug'))
                CompetitionInvite.objects.create(from_invite=from_invite, to_invite=obj)
                del self.request.session['invite_user_slug']
            
            # Email
            send_mail(
                'Subject - HoneyMint Drink Competition', 
                'Hello ' + obj.first_name + ',\n' + 'Your Competition Invite Link is - '+ ',\n' + 'localhost:8000/invite/' + obj.slug, 
                'sender@example.com', # Admin
                [
                    'receiver@example.com',
                ]
            ) 

            return HttpResponseRedirect(reverse_lazy('competition-enter', kwargs={'pk': obj.id}))
        context = self.get_context_data(form=form)
        return self.render_to_response(context)     

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CompetitionUserDisplayView(DetailView):
    model = CompetitionUser
    template_name = 'competition-interface.html'
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_users'] = CompetitionUser.objects.all()
        all_users_top_5 = CompetitionInvite.objects.values('from_invite_id').annotate(from_invite_count=Count('from_invite')).order_by('-from_invite_count')[:11]
        all_user_list = [f['from_invite_id'] for f in all_users_top_5]
        context['all_users_top_5'] = CompetitionUser.objects.filter(pk__in=all_user_list)
        return context

class CompetitionInviteView(View):
    
    def get(self, request, *args, **kwargs):
        request.session['invite_user_slug'] = self.kwargs['slug']
        return HttpResponseRedirect(reverse_lazy('competition'))

class CompetitionWinnerView(TemplateView):
    template_name = 'competition-winner.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_users'] = CompetitionUser.objects.all()
        all_users_top_5 = CompetitionInvite.objects.values('from_invite_id').annotate(from_invite_count=Count('from_invite')).order_by('-from_invite_count')[:11]
        all_user_list = [f['from_invite_id'] for f in all_users_top_5]
        context['all_users_top_5'] = CompetitionUser.objects.filter(pk__in=all_user_list)
        return context