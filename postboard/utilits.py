from postboard.models import Feedback


def send_feedback(request, post):
    text = request.POST['feedback']
    user = request.user
    feedback = Feedback(text=text, post=post, author=user, is_active=False)
    feedback.save()
