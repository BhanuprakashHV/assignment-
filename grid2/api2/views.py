from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Student

def sdetails(request):
    page_number = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 5))
    filter_age = request.GET.get('filter_age', None)
    
    students = Student.objects.all()
    
    if filter_age is not None:
        students = students.filter(age=filter_age)
    
    paginator = Paginator(students, page_size)
    
    try:
        paginated_students = paginator.page(page_number)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
    student_list = []
    for student in paginated_students:
        student_list.append({
            'name': student.name,
            'roll_number': student.roll_number,
            'grade': student.grade
        })
    
    response = {
        'page': page_number,
        'page_size': page_size,
        'total_pages': paginator.num_pages,
        'total_students': paginator.count,
        'students': student_list
    }
    
    return JsonResponse(response)

