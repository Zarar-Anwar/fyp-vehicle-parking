from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth import logout
from src.web.accounts.forms import UserProfileForm, IncompleteAgencyForm
from src.web.accounts.models import User


@method_decorator(login_required, name='dispatch')
class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('account_login')


@method_decorator(login_required, name='dispatch')
class CrossAuthView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_superuser:
                return redirect("/admin/")

            if request.user.is_staff:
                return redirect('/admins/')

            if request.user.is_completed:

                if request.user.is_agency or request.user.is_driver:
                    return redirect("agency:dashboard")

                elif request.user.is_traveller:
                    return redirect("website:home")

            else:

                if request.user.is_agency:
                    return redirect('accounts:agency-profile-complete')

                else:
                    return redirect('accounts:identification-check')

        else:
            return redirect("account_login")


@method_decorator(login_required, name='dispatch')
class UserUpdateView(View):

    def get(self, request):
        form = UserProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, template_name='accounts/user_update_form.html', context=context)

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            messages.success(request, "Your profile updated successfully")
            form.save(commit=True)
        context = {'form': form}
        return render(request, template_name='accounts/user_update_form.html', context=context)


class IdentificationCheck(View):

    def get(self, request):
        return render(request, template_name='accounts/identification_check.html')

    def post(self, request):
        user_type = self.request.POST.get('user_type', None)

        if user_type:
            user = get_object_or_404(User, id=self.request.user.id)

            if user_type == '1':

                user.is_agency = True
                user.save()
                messages.success(request, 'Fill the information to Complete your Vendor Profile')
                return redirect('accounts:agency-profile-complete')

            elif user_type == '2':
                user.is_traveller = True
                user.is_completed = True
                user.save()
                messages.success(request, 'Your Buyer Account has Been Created Successfully')

                return redirect('website:home')

        messages.error(request, 'Some issues inside user selection make sure you are selecting the right one.')
        return redirect('accounts:identification_check')


class ProfileCompleteView(View):

    def get(self, request):
        form = IncompleteAgencyForm(instance=request.user)
        context = {'form': form}
        return render(request, template_name='accounts/complete_agency_form.html', context=context)

    def post(self, request):
        form = IncompleteAgencyForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()

            user = User.objects.get(id=self.request.user.id)
            user.is_completed = True
            user.save()

            messages.success(self.request, 'Verification Has Been Completed Successfully')
            # notify_vendor_account_completed(user)
            # error, account = stripe_connect_account_create(user)

            return redirect('accounts:cross-auth')

        return render(request, template_name='accounts/complete_profile_company.html', context={'form': form})
