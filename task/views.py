from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout 
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
df = pd.read_csv('data.csv')

# Convert rain to binary: 1 = Rain, 0 = No Rain
df['rain'] = df['rain'].apply(lambda x: 1 if x > 50 else 0)

X = df[['temp', 'humidity', 'ph']]
y = df['rain']

# Split and train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)

# Accuracy for display
accuracy = round(accuracy_score(y_test, model.predict(X_test)) * 100, 2)

# Create your views here.
def loginpage(request):
    if request.method=='POST':
        username=request.POST.get('num1')
        password=request.POST.get('num2')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    return render(request,'login.html')
def registerpage(request):
    if request.method=='POST':
        username=request.POST.get('num1')
        password=request.POST.get('num2')
        conpassword=request.POST.get('num3')
        if password!=conpassword:
            return render(request,'register.html',{'result':'Invalid password'})
        user=User.objects.create_user(username=username,password=password)
        return redirect('login')
    return render(request,'register.html')
def home(request):
    return render(request,'home.html')
def ml(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {'user': request.user}

    if request.method == 'POST':
        try:
            temp = float(request.POST.get('temperature'))
            humidity = float(request.POST.get('humidity'))
            ph = float(request.POST.get('ph'))

            prediction = model.predict([[temp, humidity, ph]])[0]
            result = "🌧️ Rain Expected" if prediction == 1 else "☀️ No Rain Expected"

            context.update({
                'result': result,
                'accuracy': accuracy
            })

        except:
            context.update({'error': 'Invalid input'})

    return render(request, 'ml.html', context)
def logout(request):
    logout(request)
    return redirect('login')
