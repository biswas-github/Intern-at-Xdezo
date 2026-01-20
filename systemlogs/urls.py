from django.urls import path
from systemlogs.views import AllActivities,ExportDetails

# urls 
urlpatterns = [
    
# ------------system logs --------------#
# AllActivities
    path('AllActivities',AllActivities,name="AllActivities"),
# Export-Details
    path('Export-Details',ExportDetails,name="Export-Details"),
    


]
