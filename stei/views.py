from django.http import HttpResponse


def index(request):
    return HttpResponse("""<div
    style="
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    font-family: monospace, 'Franklin Gothic Medium', 'Arial Narrow', Arial,
    sans-serif;"><h1>API STEI'21 is running.</h1></div>""")
