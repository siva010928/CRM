from operator import truth
from pickle import TRUE
from unicodedata import category
from urllib import request
from django.core.mail import send_mail
from django.shortcuts import render,redirect,reverse
from django.views import generic
from .models import Category, Lead
from .forms import CategoryForm, LeadCategoryUpdateForm, LeadForm,CustomUserCreationForm,AssignAgentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndLoginRequiredMixin
# Create your views here.


class sign_up_view(generic.CreateView):
    template_name='registration/signup.html'
    form_class=CustomUserCreationForm
    
    def get_success_url(self) -> str:
        return reverse('login')


class lead_list_view(LoginRequiredMixin,generic.ListView):
    template_name='leads/lead_list.html'
    
    context_object_name='leads'
    
    def get_queryset(self):
        user=self.request.user
        
        if user.is_organisor:
            queryset=Lead.objects.filter(
                organization=user.userprofile,
                agent__isnull=False
                )
        if user.is_agent:
            queryset=Lead.objects.filter(
                organization=user.agent.organization,
                agent__isnull=False
                )
            queryset=queryset.filter(agent__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_organisor:
            query_set=Lead.objects.filter(
                organization=self.request.user.userprofile,
                agent__isnull=True
                )
            context.update({
                "unassigned_leads":query_set
            })

        return context
    
            
    

class lead_detail_view(LoginRequiredMixin,generic.DetailView):
    template_name='leads/lead_detail.html'
   
    context_object_name='lead'
    
    def get_queryset(self):
        user=self.request.user
        
        if user.is_organisor:
            queryset=Lead.objects.filter(organization=user.userprofile)
        if user.is_agent:
            queryset=Lead.objects.filter(organization=user.agent.organization)
            queryset=queryset.filter(agent__user=user)
        return queryset


def list_detail(request,pk):
    lead=Lead.objects.get(id=pk)
    context={
        "lead":lead
    }
    return render(request,'leads/lead_detail.html',context)

class lead_create_view(OrganisorAndLoginRequiredMixin,generic.CreateView):
    template_name='leads/lead_create.html'
    form_class=LeadForm
    
    def get_success_url(self):
        return reverse('leads:lead-list')
    
    def get_queryset(self):
        user=self.request.user
        
        return Lead.objects.filter(organization=user.userprofile)
    
    def form_valid(self,form):
        # send_mail(
        #     subject='Regarding lead',
        #     message='Lead Created Successfully',
        #     from_email='siva010928@gmail.com',
        #     recipient_list=['test@gmail.com'],
        #     html_message='<h1>login to see....</h1>'
        # )
        lead=form.save(commit=False)
        lead.organization=self.request.user.userprofile
        lead.save()
        return super(lead_create_view,self).form_valid(form)
    
    
    

def lead_create(request):
    form=LeadForm()
    if request.method=="POST":
        form=LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context={
        'form':form
    }
    return render(request,'leads/lead_create.html',context)


class lead_update_view(OrganisorAndLoginRequiredMixin,generic.UpdateView):
    template_name='leads/lead_update.html'
    form_class=LeadForm
    
    
    def get_success_url(self):
        return reverse('leads:lead-list')
    
    def get_queryset(self):
        user=self.request.user
        
        return Lead.objects.filter(organization=user.userprofile)

def lead_update(request,pk):
    lead=Lead.objects.get(id=pk)
    form=LeadForm(instance=lead)
    if request.method=='POST':
        form=LeadForm(request.POST,instance=lead)
        if form.is_valid:
            form.save()
            return redirect('/leads')
    
    context={
        'lead':lead,
        'form':form
    }
    return render(request,'leads/lead_update.html',context)



class lead_delete_view(OrganisorAndLoginRequiredMixin,generic.DeleteView):
    template_name='leads/lead_delete.html'
    context_object_name='lead'
    
    def get_success_url(self):
        return reverse('leads:lead-list')
    
    def get_queryset(self):
        user=self.request.user
        
        return Lead.objects.filter(organization=user.userprofile)

def lead_delete(request,pk):
    lead=Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')


class assign_agent_view(OrganisorAndLoginRequiredMixin,generic.FormView):
    template_name='leads/assign_agent.html'
    form_class=AssignAgentForm
    
    def dispatch(self, request, *args, **kwargs):
        print(kwargs)
        return super().dispatch(request, *args, **kwargs)
    
    
    def get_form_kwargs(self) :
        kwargs= super().get_form_kwargs()
        kwargs.update({
            'request':self.request
        })
        return kwargs
    
    def get_success_url(self) -> str:
        return reverse("leads:lead-list")
    
    def form_valid(self, form) :
        agent=form.cleaned_data['agent']
        lead=Lead.objects.get(id=self.kwargs['pk'])
        lead.agent=agent
        lead.save()
        return super().form_valid(form)
    
class category_create_view(OrganisorAndLoginRequiredMixin,generic.CreateView):
    template_name='leads/category_create.html'
    form_class=CategoryForm
    
    def get_success_url(self) -> str:
        return reverse('leads:category-list')
    
    def form_valid(self, form) :
        user=self.request.user
        category=form.save(commit=False)
        category.organization=user.userprofile
        category.save()
        return super(category_create_view,self).form_valid(form)
    
class category_update_view(OrganisorAndLoginRequiredMixin,generic.UpdateView):
    template_name='leads/category_update.html'
    form_class=CategoryForm
    
    def get_success_url(self) -> str:
        return reverse('leads:category-list')


    def get_queryset(self):
        user=self.request.user
        
        if user.is_organisor:
            queryset=Category.objects.filter(organization=user.userprofile)
        if user.is_agent:
            queryset=Category.objects.filter(organization=user.agent.organization)
            
        return queryset
    
class category_delete_view(OrganisorAndLoginRequiredMixin,generic.DeleteView):
    template_name='leads/category_delete.html'
    
    
    def get_success_url(self) -> str:
        return reverse('leads:category-list')


    def get_queryset(self):
        user=self.request.user
        
        if user.is_organisor:
            queryset=Category.objects.filter(organization=user.userprofile)
        if user.is_agent:
            queryset=Category.objects.filter(organization=user.agent.organization)
            
        return queryset
    
    
    

class category_list_view(LoginRequiredMixin,generic.ListView):
    template_name='leads/category_list.html'
    context_object_name='category_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        
        if user.is_organisor:
            queryset=Lead.objects.filter(organization=user.userprofile)
        if user.is_agent:
            queryset=Lead.objects.filter(organization=user.agent.organization)
        context.update(
            {
                'unassigned_lead_count':queryset.filter(category__isnull=True).count(),
                # 'contacted_lead_count':queryset.filter(category__name='Contacted').count(),
                # 'converted_lead_count':queryset.filter(category__name='Converted').count(),
                # 'unconverted_lead_count':queryset.filter(category__name='Unconverted').count()
            }
        ) 
        return context
    
    
    def get_queryset(self):
        user=self.request.user
        
        if user.is_organisor:
            queryset=Category.objects.filter(organization=user.userprofile)
        if user.is_agent:
            queryset=Category.objects.filter(organization=user.agent.organization)
            
        return queryset
    

class category_detail_view(LoginRequiredMixin,generic.DetailView):
    template_name='leads/category_detail.html'
    context_object_name='category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        
        if user.is_organisor:
            queryset=Lead.objects.filter(organization=user.userprofile)
        if user.is_agent:
            queryset=Lead.objects.filter(organization=user.agent.organization)
        context.update(
            {
                'leads':queryset.filter(category=self.get_object())
            }
        ) 
        return context
    
    
    def get_queryset(self):
        user=self.request.user
        
        if user.is_organisor:
            queryset=Category.objects.filter(organization=user.userprofile)
        if user.is_agent:
            queryset=Category.objects.filter(organization=user.agent.organization)
        return queryset
    
class lead_category_update_view(LoginRequiredMixin,generic.UpdateView):
    
    template_name='leads/lead_category_update.html'
    form_class=LeadCategoryUpdateForm
    context_object_name='lead'
    
    def get_success_url(self) -> str:
        return reverse('leads:lead-detail',kwargs={'pk':self.get_object().id})
    
    def get_queryset(self):
        user=self.request.user
        
        if user.is_organisor:
            queryset=Lead.objects.filter(organization=user.userprofile)
        if user.is_agent:
            queryset=Lead.objects.filter(organization=user.agent.organization)
            queryset=queryset.filter(agent__user=user)
        return queryset
    