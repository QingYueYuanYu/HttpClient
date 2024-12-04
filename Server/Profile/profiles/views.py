from django.shortcuts import render, redirect
from .models import Profile
from .forms import ProfileForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages  # 导入消息模块

@csrf_exempt
def profile_view(request):
    profile = Profile.objects.first()  # 假设只处理一个个人信息
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            print("Valid Form")
            messages.success(request, "Update Success")  # 成功消息
            form.save()
            return redirect('profile_view')
        else:
            print("Invalid Form")
            messages.error(request, f"Update Failure")  # 错误消息
            return redirect('profile_view')

    else:
        form = ProfileForm(instance=profile)
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'profiles/profile.html', context)
