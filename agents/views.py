import imp


import random
from django.core.mail import send_mail
from django.shortcuts import render,reverse
from django.views import generic
from leads.models import Agent 
from .forms import AgentForm
from .mixins import OrganisorAndLoginRequiredMixin

class agent_list_view(OrganisorAndLoginRequiredMixin,generic.ListView):
    template_name='agents/agent_list.html'
    context_object_name='agents'
    
    def get_queryset(self):
        current_user=self.request.user
        userOrganization=current_user.userprofile
        return Agent.objects.filter(organization=userOrganization)
    

class agent_detail_view(OrganisorAndLoginRequiredMixin,generic.DetailView):
    template_name='agents/agent_detail.html'
    context_object_name='agent'
    
    def get_queryset(self):
        current_user=self.request.user
        userOrganization=current_user.userprofile
        return Agent.objects.filter(organization=userOrganization)
    
    
class agent_create_view(OrganisorAndLoginRequiredMixin,generic.CreateView):
    template_name='agents/agent_create.html'
    form_class=AgentForm
    
    def get_success_url(self) -> str:
        return reverse('agents:agent-list')
    
    def form_valid(self, form) :
        user=form.save(commit=False)
        user.is_organisor=False
        user.is_agent=True
        user.set_password(f"{random.randint(0,1000000)}")
        user.save()
        Agent.objects.create(user=user,organization=self.request.user.userprofile)

        # send_mail(
        #     subject='Agent Invitation',
        #     message=f"your email: {user.email} and the link: ",
        #     from_email='siva010928@gmail.com',
        #     recipient_list=[user.email,],
        # )
        
        return super(agent_create_view,self).form_valid(form)
    
    def get_queryset(self):
        current_user=self.request.user
        userOrganization=current_user.userprofile
        return Agent.objects.filter(organization=userOrganization)
    
    
    
class agent_update_view(OrganisorAndLoginRequiredMixin,generic.UpdateView):
    template_name='agents/agent_update.html'
    form_class=AgentForm
    
    def get_success_url(self) -> str:
        return reverse('agents:agent-list')
    
    def get_queryset(self):
        current_user=self.request.user
        userOrganization=current_user.userprofile
        return Agent.objects.filter(organization=userOrganization)
    
    
class agent_delete_view(OrganisorAndLoginRequiredMixin,generic.DeleteView):
    template_name='agents/agent_delete.html'
    context_object_name='agent'
    
    def get_success_url(self) -> str:
        return reverse('agents:agent-list')
    
    def get_queryset(self):
        current_user=self.request.user
        userOrganization=current_user.userprofile
        return Agent.objects.filter(organization=userOrganization)
    
    
    
