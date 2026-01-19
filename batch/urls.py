from django.urls import path,include
from batch.views import AddBatch,ViewBatches,DeleteBatch,UpdateBatch

urlpatterns = [
     # ----------Batch----------
    path('Batch',AddBatch,name="Batch"),
                  #view batch 
    path('ViewBatches',ViewBatches,name="ViewBatches"),
#                        DeleteBatch
    path('DeleteBatch/<int:id>',DeleteBatch,name="DeleteBatch"),
#                       update batch
    path('UpdateBatch/<int:id>',UpdateBatch,name="UpdateBatch"),


]