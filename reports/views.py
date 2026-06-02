# reports/views.py

from django.shortcuts import render
from members.models import Member, Department
from attendance.models import Attendance, Service
from giving.models import Contribution
from django.db.models import Sum
from django.http import HttpResponse
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
import csv
from activity.models import ActivityLog
from events.models import Event


from reportlab.lib.styles import getSampleStyleSheet

from members.models import Member

def membership_report(request):

    departments = Department.objects.all()

    context = {
        'member_count': Member.objects.count(),
        'active_members':
            Member.objects.filter(
                status='ACTIVE'
            ).count(),

        'inactive_members':
            Member.objects.filter(
                status='INACTIVE'
            ).count(),

        'visitor_count':
            Member.objects.filter(
                status='VISITOR'
            ).count(),

        'departments': departments,
    }

    return render(
        request,
        'reports/membership_report.html',
        context
    )


def membership_pdf(request):

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; '
        'filename="membership_report.pdf"'
    )

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Mityana Pentecostal Church",
            styles['Title']
        )
    )

    content.append(
        Paragraph(
            "Membership Report",
            styles['Heading2']
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            f"Total Members: {Member.objects.count()}",
            styles['Normal']
        )
    )

    content.append(
        Spacer(1, 12)
    )

    members = Member.objects.all()

    for member in members:

        content.append(
            Paragraph(
                f"{member.first_name} "
                f"{member.last_name} "
                f"({member.status})",
                styles['Normal']
            )
        )

    doc.build(content)

    return response

def membership_csv(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; '
        'filename="membership_report.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'First Name',
        'Last Name',
        'Gender',
        'Status',
        'Phone Number',
        'Email',
        'Department'
    ])

    for member in Member.objects.all():

        writer.writerow([
            member.first_name,
            member.last_name,
            member.gender,
            member.status,
            member.phone_number,
            member.email,
            member.department
        ])

    return response

def attendance_report(request):

    context = {
        'attendance_count':
            Attendance.objects.count(),

        'service_count':
            Service.objects.count(),

        'present_count':
            Attendance.objects.filter(
                status='PRESENT'
            ).count(),

        'absent_count':
            Attendance.objects.filter(
                status='ABSENT'
            ).count(),

        'excused_count':
            Attendance.objects.filter(
                status='EXCUSED'
            ).count(),
    }

    return render(
        request,
        'reports/attendance_report.html',
        context
    )


def attendance_pdf(request):

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; filename="attendance_report.pdf"'
    )

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Attendance Report",
            styles['Title']
        )
    )

    content.append(
        Spacer(1, 12)
    )

    for record in Attendance.objects.all():

        content.append(
            Paragraph(
                f"{record.member} - "
                f"{record.service} - "
                f"{record.status}",
                styles['Normal']
            )
        )

    doc.build(content)

    return response

def attendance_csv(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; filename="attendance_report.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Member',
        'Service',
        'Status',
        'Recorded At'
    ])

    for record in Attendance.objects.all():

        writer.writerow([
            record.member,
            record.service,
            record.status,
            record.recorded_at
        ])

    return response

def finance_report(request):

    total_amount = Contribution.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    cash_total = Contribution.objects.filter(
        payment_method='CASH'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    mobile_money_total = Contribution.objects.filter(
        payment_method='MOBILE_MONEY'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    bank_total = Contribution.objects.filter(
        payment_method='BANK'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    context = {
        'total_amount': total_amount,
        'cash_total': cash_total,
        'mobile_money_total': mobile_money_total,
        'bank_total': bank_total,
    }

    return render(
        request,
        'reports/finance_report.html',
        context
    )

def finance_pdf(request):

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; '
        'filename="finance_report.pdf"'
    )

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    content = []

    total = Contribution.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    content.append(
        Paragraph(
            "Financial Report",
            styles['Title']
        )
    )

    content.append(
        Paragraph(
            f"Total Giving: UGX {total}",
            styles['Normal']
        )
    )

    doc.build(content)

    return response


def finance_csv(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; filename="finance_report.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Member',
        'Category',
        'Amount',
        'Payment Method',
        'Reference Number',
        'Contribution Date',
        'Remarks'
    ])

    for contribution in Contribution.objects.all():

        writer.writerow([
            contribution.member,
            contribution.category,
            contribution.amount,
            contribution.payment_method,
            contribution.reference_number,
            contribution.contribution_date,
            contribution.remarks,
        ])

    return response

def contributions_csv(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; filename="contributions_report.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Member',
        'Category',
        'Amount',
        'Method',
        'Date'
    ])

    for item in Contribution.objects.all():

        writer.writerow([
            item.member,
            item.category,
            item.amount,
            item.payment_method,
            item.contribution_date
        ])

    return response

def contributions_pdf(request):

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; filename="contributions_report.pdf"'
    )

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Contributions Report",
            styles['Title']
        )
    )

    content.append(
        Spacer(1, 12)
    )

    for item in Contribution.objects.all():

        content.append(
            Paragraph(
                f"{item.member} - "
                f"{item.category} - "
                f"UGX {item.amount}",
                styles['Normal']
            )
        )

    doc.build(content)

    return response



def activity_csv(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; filename="activity_report.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'User',
        'Action',
        'Date'
    ])

    for activity in ActivityLog.objects.all():

        writer.writerow([
            activity.user,
            activity.action,
            activity.created_at
        ])

    return response

def activity_pdf(request):

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; filename="activity_report.pdf"'
    )

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Activity Report",
            styles['Title']
        )
    )

    for activity in ActivityLog.objects.all():

        content.append(
            Paragraph(
                f"{activity.user} - "
                f"{activity.action}",
                styles['Normal']
            )
        )

    doc.build(content)

    return response



def events_csv(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; filename="events_report.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Title',
        'Date',
        'Venue'
    ])

    for event in Event.objects.all():

        writer.writerow([
            event.title,
            event.event_date,
            event.venue
        ])

    return response

def events_pdf(request):

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; filename="events_report.pdf"'
    )

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Events Report",
            styles['Title']
        )
    )

    for event in Event.objects.all():

        content.append(
            Paragraph(
                f"{event.title} - "
                f"{event.event_date}",
                styles['Normal']
            )
        )

    doc.build(content)

    return response