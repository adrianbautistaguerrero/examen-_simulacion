from django.shortcuts import render
from django.views import View
from .forms import EmailAnalysisForm
from .utils.ml_handler import predict_spam


class SpamDetectorView(View):
    """
    Vista principal para el detector de spam.
    """
    template_name = 'spam_detector/index.html'
    
    def get(self, request):
        form = EmailAnalysisForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = EmailAnalysisForm(request.POST)
        
        if form.is_valid():
            email_text = form.cleaned_data['email_text']
            
            # Realizar predicción
            result = predict_spam(email_text)
            
            return render(request, self.template_name, {
                'form': form,
                'result': result,
                'email_preview': email_text[:300] + '...' if len(email_text) > 300 else email_text
            })
        
        return render(request, self.template_name, {'form': form})
