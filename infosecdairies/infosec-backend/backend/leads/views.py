from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Lead
from .serializers import LeadSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def create_lead(request):
    """Create a new lead/enquiry from live course page. Links to user if authenticated."""
    serializer = LeadSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user if request.user.is_authenticated else None
        serializer.save(user=user)
        return Response(
            {"detail": "Thank you! Your enquiry has been submitted. We will contact you soon."},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_leads(request):
    """List all leads - admin only"""
    if not request.user.is_staff:
        return Response({"detail": "Admin access required"}, status=status.HTTP_403_FORBIDDEN)

    leads = Lead.objects.select_related('user').all()
    serializer = LeadSerializer(leads, many=True)
    return Response(serializer.data)
