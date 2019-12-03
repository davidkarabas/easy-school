import time
from calendar import month_name

from django import forms

from .models import StudentFee


class StudentFeeAdd(forms.ModelForm):
    """ The form class for fee submission """

    def clean(self):
        """Checks if the fee for this month has been submitted"""
        try:
            StudentFee.objects.get(
                student=self.cleaned_data['student'],
                fee_group=self.cleaned_data['fee_group'],
                valid_until=self.cleaned_data['valid_until'],
            )
        except StudentFee.DoesNotExist:
            return self.cleaned_data
        raise forms.ValidationError("Fee for this month has been submitted.")

    class Meta:
        model = StudentFee
        fields = (
            'student',
            'fee_group',
            'valid_until',
        )
