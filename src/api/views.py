from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


respose = """
<!DOCTYPE html>
<body>
    <h1 style="text-align: center; margin: auto;">KU Polls</h1>
    <button style="border: none; color: #2B2B2B; text-size: 16pt" id="cpb">Create poll</button>
    <ol>
        <li>Sample poll <a href="about:blank">view</a></li>
    </ol>
</body>

<script>
    document.getElementById("cpb").onclick = () => {
        alert("Not implemented.");
    }
</script>
"""
def main(request):
    return HttpResponse(respose)