def profile_changed(sender, instance, **kwargs):
    # import 写在函数里面避免循环依赖
    from accounts.services import UserService
    # note: it's user_id instead of id
    UserService.invalidate_profile(instance.user_id)